<script setup lang="ts">
import { ref, onMounted } from "vue";
import {
	gradeAndPolishStream,
	healthCheck,
	downloadTelemetryLog,
	type StreamEvent,
} from "./api/service";
import { useAuth } from "./composables/useAuth";
import AuthModal from "./components/AuthModal.vue";
import HistoryPanel from "./components/HistoryPanel.vue";
import Sidebar from "./components/Sidebar.vue";
import GradingView from "./components/GradingView.vue";
import TOEFLWritingView from "./components/TOEFLWritingView.vue";
import WelcomeView from "./components/WelcomeView.vue";

const { isAuthenticated, currentUser, logout, ensureAuthenticated } = useAuth();

const showAuthModal = ref(false);
const showHistoryPanel = ref(false);
const historyPanelRef = ref<{
	loadHistories: (page?: number) => Promise<void>;
} | null>(null);

const loading = ref(false);
const error = ref<string | null>(null);
const isBackendHealthy = ref<boolean | null>(null);
const statusMessage = ref<string | null>(null);
const downloadingLog = ref(false);
const currentView = ref<"welcome" | "grading" | "writing">("welcome");
const welcomeViewRef = ref<{ refreshHistory: () => Promise<void> } | null>(
	null
);
const writingViewRef = ref<{
	setQuestionFile: (file: string) => void;
} | null>(null);
const currentHistoryId = ref<number | undefined>(undefined); // 当前评分的历史记录ID

const checkBackend = async () => {
	try {
		await healthCheck();
		isBackendHealthy.value = true;
	} catch (err) {
		isBackendHealthy.value = false;
		console.error("Backend health check failed:", err);
	}
};

const handleClear = () => {
	currentHistoryId.value = undefined;
	error.value = null;
	statusMessage.value = null;
};

const handleDownloadLog = async () => {
	downloadingLog.value = true;
	try {
		const blob = await downloadTelemetryLog();
		const url = URL.createObjectURL(blob);
		const a = document.createElement("a");
		a.href = url;
		a.download = "telemetry.log";
		a.click();
		URL.revokeObjectURL(url);
	} catch (err) {
		error.value =
			err instanceof Error ? err.message : "下载日志失败，请检查后端日志接口";
		console.error("Download log error:", err);
	} finally {
		downloadingLog.value = false;
	}
};

const handleLogout = () => {
	logout();
	showHistoryPanel.value = false;
};

const handleWritingSubmit = async (data: {
	text: string;
	wordCount: number;
	timeSpent: number;
	questionFile: string;
}) => {
	loading.value = true;
	error.value = null;
	currentHistoryId.value = undefined;

	try {
		// 发送评分请求，获取历史记录ID
		const historyId = await gradeAndPolishStream(
			data.text,
			data.questionFile,
			(event: StreamEvent) => {
				// 收到 history_id 后，切换到 GradingView
				if (event.type === "history_id" && event.history_id) {
					currentHistoryId.value = event.history_id;
					currentView.value = "grading";
					loading.value = false;
				}
			}
		);

		// 如果直接返回了ID（非流式情况）
		if (historyId !== null && historyId !== undefined) {
			currentHistoryId.value = historyId;
			currentView.value = "grading";
		}
	} catch (err) {
		error.value =
			err instanceof Error ? err.message : "提交失败，请检查后端服务是否运行";
		console.error("Error:", err);
	} finally {
		loading.value = false;
	}
};

const handleWelcomeLogin = () => {
	showAuthModal.value = true;
};

const handleWelcomeSelectQuestion = (file: string) => {
	currentView.value = "writing";
	// 通过ref设置TOEFLWritingView的题目文件
	setTimeout(() => {
		if (writingViewRef.value) {
			writingViewRef.value.setQuestionFile(file);
		}
	}, 0);
};

const handleWelcomeViewHistory = (history: any) => {
	if (history.id) {
		currentHistoryId.value = history.id;
		currentView.value = "grading";
		showHistoryPanel.value = true;
		if (historyPanelRef.value) {
			historyPanelRef.value.loadHistories();
		}
	}
};

const handleWelcomeViewAllHistory = () => {
	currentView.value = "grading";
	showHistoryPanel.value = true;
	if (historyPanelRef.value) {
		historyPanelRef.value.loadHistories();
	}
};

const handleViewChange = (view: "welcome" | "grading" | "writing") => {
	currentView.value = view;
};

onMounted(async () => {
	checkBackend();
	await ensureAuthenticated();
});
</script>

<template>
	<div class="app-container">
		<WelcomeView
			v-if="currentView === 'welcome'"
			ref="welcomeViewRef"
			@login="handleWelcomeLogin"
			@select-question="handleWelcomeSelectQuestion"
			@view-history="handleWelcomeViewHistory"
			@view-all-history="handleWelcomeViewAllHistory"
		/>

		<template v-else>
			<Sidebar
				:is-authenticated="isAuthenticated"
				:current-user="currentUser"
				:show-history="showHistoryPanel"
				:backend-healthy="isBackendHealthy"
				:loading="loading"
				:status-message="statusMessage"
				:current-view="currentView"
				:downloading-log="downloadingLog"
				@login="showAuthModal = true"
				@logout="handleLogout"
				@toggle-history="showHistoryPanel = !showHistoryPanel"
				@check-backend="checkBackend"
				@view-change="handleViewChange"
				@download-log="handleDownloadLog"
			/>

			<HistoryPanel
				v-if="showHistoryPanel && isAuthenticated"
				ref="historyPanelRef"
			/>

			<GradingView
				v-if="currentView === 'grading'"
				:history-id="currentHistoryId"
				@clear="handleClear"
			/>

			<TOEFLWritingView
				v-if="currentView === 'writing'"
				ref="writingViewRef"
				@submit="handleWritingSubmit"
			/>
		</template>

		<AuthModal :show="showAuthModal" @close="showAuthModal = false" />
	</div>
</template>

<style scoped>
.app-container {
	display: flex;
	min-height: 100vh;
	background: #f5f5f5;
	font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
		"Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
}
</style>

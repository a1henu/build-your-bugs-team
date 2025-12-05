<template>
	<main class="grading-view">
		<GradingResults
			:answer="answer"
			:comment="comment"
			:polished-answer="polishedAnswer"
			:current-stage="currentStage"
			:loading="loading"
			:error="error"
			@clear="handleClear"
		/>
	</main>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import GradingResults from "./grading/GradingResults.vue";
import {
	gradeAndPolishStreamById,
	getHistoryById,
	type StreamEvent,
} from "../api/service";
import type { History } from "../api/history";

const props = defineProps<{
	historyId?: number; // 历史记录ID，用于加载已有数据或流式接收新数据
}>();

// 响应式数据
const answer = ref("");
const comment = ref("");
const polishedAnswer = ref("");
const loading = ref(false);
const error = ref<string | null>(null);
const currentStage = ref<"idle" | "evaluating" | "polishing" | "done">("idle");
const statusMessage = ref<string | null>(null);

const emit = defineEmits<{
	(e: "clear"): void;
}>();

// 加载历史记录数据
const loadHistoryData = async (historyId: number) => {
	loading.value = true;
	error.value = null;
	try {
		const history: History = await getHistoryById(historyId);
		answer.value = history.answer || "";
		comment.value = history.comment || "";
		polishedAnswer.value = history.polished_answer || "";
		currentStage.value = "done";
	} catch (err) {
		error.value = err instanceof Error ? err.message : "加载历史记录失败";
		console.error("Load history error:", err);
	} finally {
		loading.value = false;
	}
};

// 流式接收评分结果
const streamGradingResult = async (historyId: number) => {
	loading.value = true;
	error.value = null;
	comment.value = "";
	polishedAnswer.value = "";
	currentStage.value = "idle";
	statusMessage.value = null;

	try {
		await gradeAndPolishStreamById(historyId, (event: StreamEvent) => {
			switch (event.type) {
				case "status":
					statusMessage.value = event.message || "";
					if (event.stage === "evaluating") {
						currentStage.value = "evaluating";
					} else if (event.stage === "polishing") {
						currentStage.value = "polishing";
					}
					break;

				case "comment_chunk":
					if (event.content) {
						comment.value += event.content;
					}
					break;

				case "comment_complete":
					if (event.comment) {
						comment.value = event.comment;
					}
					currentStage.value = "polishing";
					break;

				case "polished_chunk":
					if (event.content) {
						polishedAnswer.value += event.content;
					}
					break;

				case "polished_complete":
					if (event.polished_answer) {
						polishedAnswer.value = event.polished_answer;
					}
					break;

				case "history_saved":
					// 历史记录已保存
					break;

				case "done":
					currentStage.value = "done";
					statusMessage.value = "处理完成";
					loading.value = false;
					break;

				case "error":
					error.value = event.message || "处理过程中发生错误";
					loading.value = false;
					currentStage.value = "idle";
					break;
			}
		});
	} catch (err) {
		error.value =
			err instanceof Error ? err.message : "请求失败，请检查后端服务是否运行";
		console.error("Error:", err);
		loading.value = false;
		currentStage.value = "idle";
	}
};

const handleClear = () => {
	emit("clear");
};

// 监听 historyId 变化
watch(
	() => props.historyId,
	async (newId) => {
		if (newId) {
			// 先尝试加载历史记录数据
			try {
				const history: History = await getHistoryById(newId);
				answer.value = history.answer || "";
				// 如果已有完整数据，直接显示
				if (history.comment && history.polished_answer) {
					comment.value = history.comment;
					polishedAnswer.value = history.polished_answer;
					currentStage.value = "done";
					loading.value = false;
				} else {
					// 如果没有完整数据，开始流式接收
					await streamGradingResult(newId);
				}
			} catch (err) {
				// 如果加载失败，尝试流式接收
				await streamGradingResult(newId);
			}
		}
	},
	{ immediate: true }
);

onMounted(() => {
	if (props.historyId) {
		// 组件挂载时如果有 historyId，加载数据
		loadHistoryData(props.historyId);
	}
});
</script>

<style scoped>
.grading-view {
	flex: 1;
	display: flex;
	flex-direction: column;
	overflow: hidden;
}
</style>

<template>
	<div class="action-section">
		<button @click="$emit('view-change', 'welcome')" class="btn">
			返回欢迎界面
		</button>
		<button
			@click="
				$emit(
					'view-change',
					props.currentView === 'grading' ? 'writing' : 'grading'
				)
			"
			class="btn"
			:class="{ active: props.currentView === 'writing' }"
		>
			{{
				props.currentView === "grading" ? "切换到写作界面" : "切换到评分界面"
			}}
		</button>
		<button @click="$emit('check-backend')" class="btn">检查连接</button>
		<button
			@click="$emit('download-log')"
			class="btn"
			:disabled="downloadingLog"
		>
			{{ downloadingLog ? "下载中..." : "下载遥测日志" }}
		</button>
	</div>
</template>

<script setup lang="ts">
const props = defineProps<{
	currentView: "welcome" | "grading" | "writing";
	downloadingLog: boolean;
}>();

defineEmits<{
	(e: "view-change", view: "welcome" | "grading" | "writing"): void;
	(e: "check-backend"): void;
	(e: "download-log"): void;
}>();
</script>

<style scoped>
.action-section {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
	margin-top: 1rem;
}

.btn {
	padding: 0.5rem;
	border: 1px solid #ddd;
	background: #fff;
	cursor: pointer;
	border-radius: 4px;
}

.btn:hover:not(:disabled) {
	background: #f5f5f5;
}

.btn:disabled {
	opacity: 0.5;
	cursor: not-allowed;
}

.btn.active {
	background: #e3f2fd;
	border-color: #667eea;
}
</style>

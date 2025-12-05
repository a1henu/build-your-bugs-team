<template>
	<div class="grading-results">
		<div class="comparison-section">
			<div class="comparison-panel">
				<div class="panel-header">
					<h3>原文</h3>
				</div>
				<div class="panel-content">
					<div class="text-content">{{ answer }}</div>
				</div>
			</div>

			<div class="comparison-panel">
				<div class="panel-header">
					<h3>润色后</h3>
					<span
						v-if="currentStage === 'polishing' && !polishedAnswer"
						class="loading-indicator"
					>
						生成中...
					</span>
				</div>
				<div class="panel-content">
					<div class="text-content">
						{{ polishedAnswer || "正在生成..." }}
					</div>
				</div>
			</div>
		</div>

		<div class="comment-section">
			<div class="comment-header">
				<h3>评分评语</h3>
				<span
					v-if="currentStage === 'evaluating' && !comment"
					class="loading-indicator"
				>
					生成中...
				</span>
			</div>
			<div class="comment-content">
				<div class="text-content">{{ comment || "正在生成评语..." }}</div>
			</div>
		</div>

		<div class="results-actions">
			<button @click="$emit('clear')" class="btn">重新开始</button>
		</div>
	</div>
</template>

<script setup lang="ts">
defineProps<{
	answer: string;
	comment: string;
	polishedAnswer: string;
	currentStage: "idle" | "evaluating" | "polishing" | "done";
	loading?: boolean;
	error?: string | null;
}>();

defineEmits<{
	(e: "clear"): void;
}>();
</script>

<style scoped>
.grading-results {
	flex: 1;
	display: flex;
	flex-direction: column;
	padding: 2rem;
	overflow-y: auto;
}

.comparison-section {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 1rem;
	margin-bottom: 1rem;
}

.comparison-panel {
	border: 1px solid #ddd;
	border-radius: 4px;
	display: flex;
	flex-direction: column;
}

.panel-header {
	padding: 1rem;
	border-bottom: 1px solid #ddd;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.panel-header h3 {
	margin: 0;
	font-size: 1rem;
}

.panel-content {
	flex: 1;
	padding: 1rem;
	overflow-y: auto;
}

.text-content {
	white-space: pre-wrap;
	word-wrap: break-word;
	line-height: 1.6;
}

.loading-indicator {
	color: #666;
	font-size: 0.9rem;
}

.comment-section {
	border: 1px solid #ddd;
	border-radius: 4px;
	margin-bottom: 1rem;
}

.comment-header {
	padding: 1rem;
	border-bottom: 1px solid #ddd;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.comment-header h3 {
	margin: 0;
	font-size: 1rem;
}

.comment-content {
	padding: 1rem;
}

.results-actions {
	display: flex;
	justify-content: center;
}

.btn {
	padding: 0.75rem 1.5rem;
	border: 1px solid #ddd;
	background: #fff;
	cursor: pointer;
	border-radius: 4px;
}

.btn:hover {
	background: #f5f5f5;
}

.error-message {
	margin: 1rem 0;
	padding: 0.75rem;
	background: #ffebee;
	color: #c62828;
	border-radius: 4px;
	border: 1px solid #ef5350;
}

@media (max-width: 768px) {
	.comparison-section {
		grid-template-columns: 1fr;
	}
}
</style>

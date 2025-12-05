<template>
	<div class="status-section">
		<div class="status-item">
			<span class="status-label">后端状态</span>
			<span class="status-value" :class="getStatusClass()">
				{{ getStatusText() }}
			</span>
		</div>

		<div v-if="loading" class="status-item">
			<span class="status-label">处理状态</span>
			<span class="status-value">{{ statusMessage || "处理中..." }}</span>
		</div>
	</div>
</template>

<script setup lang="ts">
const props = defineProps<{
	backendHealthy: boolean | null;
	loading: boolean;
	statusMessage: string | null;
}>();

const emit = defineEmits<{
	(e: "check-backend"): void;
}>();

const getStatusClass = () => {
	if (props.backendHealthy === null) return "";
	return props.backendHealthy ? "healthy" : "unhealthy";
};

const getStatusText = () => {
	if (props.backendHealthy === null) return "检查中";
	return props.backendHealthy ? "正常" : "未连接";
};
</script>

<style scoped>
.status-section {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.status-item {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
}

.status-label {
	font-size: 0.75rem;
	color: #666;
	font-weight: 600;
}

.status-value {
	padding: 0.5rem;
	background: #f5f5f5;
	border-radius: 4px;
	font-size: 0.9rem;
}

.status-value.healthy {
	background: #e8f5e9;
	color: #2e7d32;
}

.status-value.unhealthy {
	background: #ffebee;
	color: #c62828;
}
</style>

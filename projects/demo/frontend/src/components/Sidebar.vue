<template>
	<aside class="sidebar">
		<div class="sidebar-header">
			<h2>TOEFL 写作评分</h2>
		</div>
		<div class="sidebar-content">
			<UserSection
				:is-authenticated="isAuthenticated"
				:current-user="currentUser"
				@login="$emit('login')"
				@logout="$emit('logout')"
				@toggle-history="$emit('toggle-history')"
				:show-history="showHistory"
			/>

			<div class="divider"></div>

			<StatusSection
				:backend-healthy="backendHealthy"
				:loading="loading"
				:status-message="statusMessage"
				@check-backend="$emit('check-backend')"
			/>

			<ActionSection
				:current-view="currentView"
				@view-change="$emit('view-change', $event)"
				@check-backend="$emit('check-backend')"
				@download-log="$emit('download-log')"
				:downloading-log="downloadingLog"
			/>
		</div>
	</aside>
</template>

<script setup lang="ts">
import UserSection from "./sidebar/UserSection.vue";
import StatusSection from "./sidebar/StatusSection.vue";
import ActionSection from "./sidebar/ActionSection.vue";

defineProps<{
	isAuthenticated: boolean;
	currentUser: any;
	showHistory: boolean;
	backendHealthy: boolean | null;
	loading: boolean;
	statusMessage: string | null;
	currentView: "welcome" | "grading" | "writing";
	downloadingLog: boolean;
}>();

const emit = defineEmits<{
	(e: "login"): void;
	(e: "logout"): void;
	(e: "toggle-history"): void;
	(e: "check-backend"): void;
	(e: "view-change", view: "welcome" | "grading" | "writing"): void;
	(e: "download-log"): void;
}>();
</script>

<style scoped>
.sidebar {
	background: #fff;
	border-right: 1px solid #ddd;
	display: flex;
	flex-direction: column;
}

.sidebar-header {
	padding: 1rem;
	border-bottom: 1px solid #ddd;
}

.sidebar-header h2 {
	margin: 0;
	font-size: 1rem;
}

.sidebar-content {
	flex: 1;
	padding: 1rem;
	overflow-y: auto;
}

.divider {
	border-top: 1px solid #ddd;
	margin: 1rem 0;
}
</style>

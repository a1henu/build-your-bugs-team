<script setup lang="ts">
import { ref, computed } from "vue";
import { useAuth } from "../composables/useAuth";

defineProps<{
	show: boolean;
}>();

const emit = defineEmits<{
	close: [];
}>();

const { login, register, loading, error } = useAuth();

const isLoginMode = ref(true);
const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");

const formError = ref<string | null>(null);

const canSubmit = computed(() => {
	if (isLoginMode.value) {
		return username.value.trim() && password.value.trim();
	} else {
		return (
			username.value.trim() &&
			email.value.trim() &&
			password.value.trim() &&
			password.value === confirmPassword.value &&
			password.value.length >= 6
		);
	}
});

const handleSubmit = async () => {
	formError.value = null;

	if (!canSubmit.value) {
		return;
	}

	if (!isLoginMode.value) {
		if (password.value !== confirmPassword.value) {
			formError.value = "两次输入的密码不一致";
			return;
		}
		if (password.value.length < 6) {
			formError.value = "密码长度至少为6位";
			return;
		}
	}

	try {
		if (isLoginMode.value) {
			await login(username.value, password.value);
		} else {
			await register(username.value, email.value, password.value);
		}
		// 成功后关闭模态框
		emit("close");
		// 清空表单
		username.value = "";
		email.value = "";
		password.value = "";
		confirmPassword.value = "";
	} catch (err) {
		// 错误已在useAuth中设置
	}
};

const switchMode = () => {
	isLoginMode.value = !isLoginMode.value;
	formError.value = null;
	username.value = "";
	email.value = "";
	password.value = "";
	confirmPassword.value = "";
};

const handleClose = () => {
	formError.value = null;
	emit("close");
};
</script>

<template>
	<div v-if="show" class="modal-overlay" @click="handleClose">
		<div class="modal-content" @click.stop>
			<div class="modal-header">
				<h2>{{ isLoginMode ? "登录" : "注册" }}</h2>
				<button class="close-btn" @click="handleClose">×</button>
			</div>

			<div class="modal-body">
				<div v-if="error || formError" class="error-message">
					{{ error || formError }}
				</div>

				<form @submit.prevent="handleSubmit">
					<div class="form-group">
						<label for="username">用户名</label>
						<input
							id="username"
							v-model="username"
							type="text"
							placeholder="请输入用户名"
							required
							:disabled="loading"
						/>
					</div>

					<div v-if="!isLoginMode" class="form-group">
						<label for="email">邮箱</label>
						<input
							id="email"
							v-model="email"
							type="email"
							placeholder="请输入邮箱"
							required
							:disabled="loading"
						/>
					</div>

					<div class="form-group">
						<label for="password">密码</label>
						<input
							id="password"
							v-model="password"
							type="password"
							:placeholder="
								isLoginMode ? '请输入密码' : '请输入密码（至少6位）'
							"
							required
							:disabled="loading"
						/>
					</div>

					<div v-if="!isLoginMode" class="form-group">
						<label for="confirmPassword">确认密码</label>
						<input
							id="confirmPassword"
							v-model="confirmPassword"
							type="password"
							placeholder="请再次输入密码"
							required
							:disabled="loading"
						/>
					</div>

					<button
						type="submit"
						class="btn-submit"
						:disabled="!canSubmit || loading"
					>
						<span v-if="loading">处理中...</span>
						<span v-else>{{ isLoginMode ? "登录" : "注册" }}</span>
					</button>
				</form>

				<div class="switch-mode">
					<span>{{ isLoginMode ? "还没有账号？" : "已有账号？" }}</span>
					<button class="link-btn" @click="switchMode" :disabled="loading">
						{{ isLoginMode ? "立即注册" : "立即登录" }}
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
.modal-overlay {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: rgba(0, 0, 0, 0.5);
	backdrop-filter: blur(4px);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 1000;
	animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
	from {
		opacity: 0;
	}
	to {
		opacity: 1;
	}
}

.modal-content {
	background: white;
	border-radius: 12px;
	width: 90%;
	max-width: 450px;
	max-height: 90vh;
	overflow-y: auto;
	box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
	animation: slideUp 0.3s ease;
}

@keyframes slideUp {
	from {
		transform: translateY(20px);
		opacity: 0;
	}
	to {
		transform: translateY(0);
		opacity: 1;
	}
}

.modal-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 1.5rem;
	border-bottom: 1px solid #e0e0e0;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	border-radius: 12px 12px 0 0;
}

.modal-header h2 {
	margin: 0;
	font-size: 1.5rem;
	font-weight: 700;
}

.close-btn {
	background: none;
	border: none;
	color: white;
	font-size: 2rem;
	cursor: pointer;
	width: 32px;
	height: 32px;
	display: flex;
	align-items: center;
	justify-content: center;
	border-radius: 50%;
	transition: background 0.2s;
}

.close-btn:hover {
	background: rgba(255, 255, 255, 0.2);
}

.modal-body {
	padding: 2rem;
}

.error-message {
	padding: 0.875rem 1rem;
	background: #ffebee;
	color: #c62828;
	border-radius: 6px;
	margin-bottom: 1.5rem;
	border-left: 4px solid #c62828;
	font-size: 0.9rem;
}

.form-group {
	margin-bottom: 1.5rem;
}

.form-group label {
	display: block;
	margin-bottom: 0.5rem;
	font-weight: 600;
	color: #333;
	font-size: 0.9rem;
}

.form-group input {
	width: 100%;
	padding: 0.75rem 1rem;
	border: 2px solid #e0e0e0;
	border-radius: 6px;
	font-size: 1rem;
	transition: all 0.3s;
	font-family: inherit;
}

.form-group input:focus {
	outline: none;
	border-color: #667eea;
	box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input:disabled {
	background: #f5f5f5;
	cursor: not-allowed;
}

.btn-submit {
	width: 100%;
	padding: 0.875rem;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	border: none;
	border-radius: 6px;
	font-size: 1rem;
	font-weight: 600;
	cursor: pointer;
	transition: all 0.3s;
	margin-top: 1rem;
}

.btn-submit:hover:not(:disabled) {
	transform: translateY(-2px);
	box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
	opacity: 0.6;
	cursor: not-allowed;
	transform: none;
}

.switch-mode {
	text-align: center;
	margin-top: 1.5rem;
	color: #666;
	font-size: 0.9rem;
}

.link-btn {
	background: none;
	border: none;
	color: #667eea;
	cursor: pointer;
	font-weight: 600;
	text-decoration: underline;
	margin-left: 0.5rem;
	transition: color 0.2s;
}

.link-btn:hover:not(:disabled) {
	color: #764ba2;
}

.link-btn:disabled {
	opacity: 0.6;
	cursor: not-allowed;
}
</style>

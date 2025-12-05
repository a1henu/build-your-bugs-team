// 用户认证状态管理

import { ref, computed } from "vue";
import type { User } from "../api/auth";
import {
	login as apiLogin,
	register as apiRegister,
	getCurrentUser as apiGetCurrentUser,
	refreshToken as apiRefreshToken,
	getStoredUser,
	setStoredUser,
	setStoredToken,
	setStoredRefreshToken,
	clearStoredTokens,
	getStoredToken,
} from "../api/auth";

// 全局状态
const user = ref<User | null>(getStoredUser());
const loading = ref(false);
const error = ref<string | null>(null);

export function useAuth() {
	// 计算属性
	const isAuthenticated = computed(() => user.value !== null);
	const currentUser = computed(() => user.value);

	/**
	 * 登录
	 */
	async function login(username: string, password: string): Promise<void> {
		loading.value = true;
		error.value = null;
		try {
			const response = await apiLogin({ username, password });
			user.value = response.user;
			setStoredUser(response.user);
			setStoredToken(response.access_token);
			setStoredRefreshToken(response.refresh_token);
		} catch (err) {
			error.value = err instanceof Error ? err.message : "登录失败";
			throw err;
		} finally {
			loading.value = false;
		}
	}

	/**
	 * 注册
	 */
	async function register(
		username: string,
		email: string,
		password: string
	): Promise<void> {
		loading.value = true;
		error.value = null;
		try {
			const response = await apiRegister({ username, email, password });
			user.value = response.user;
			setStoredUser(response.user);
			setStoredToken(response.access_token);
			setStoredRefreshToken(response.refresh_token);
		} catch (err) {
			error.value = err instanceof Error ? err.message : "注册失败";
			throw err;
		} finally {
			loading.value = false;
		}
	}

	/**
	 * 登出
	 */
	function logout(): void {
		user.value = null;
		clearStoredTokens();
		error.value = null;
	}

	/**
	 * 刷新用户信息
	 */
	async function refreshUserInfo(): Promise<void> {
		if (!isAuthenticated.value) return;

		try {
			const currentUserData = await apiGetCurrentUser();
			user.value = currentUserData;
			setStoredUser(currentUserData);
		} catch (err) {
			// 如果获取失败，尝试刷新token
			try {
				const tokenData = await apiRefreshToken();
				setStoredToken(tokenData.access_token);
				// 再次尝试获取用户信息
				const currentUserData = await apiGetCurrentUser();
				user.value = currentUserData;
				setStoredUser(currentUserData);
			} catch (refreshErr) {
				// 刷新也失败，清除登录状态
				logout();
				throw refreshErr;
			}
		}
	}

	/**
	 * 检查并刷新token（如果需要）
	 */
	async function ensureAuthenticated(): Promise<boolean> {
		if (!getStoredToken()) {
			return false;
		}

		if (!user.value) {
			try {
				await refreshUserInfo();
			} catch {
				return false;
			}
		}

		return isAuthenticated.value;
	}

	return {
		// 状态
		user,
		loading,
		error,
		isAuthenticated,
		currentUser,
		// 方法
		login,
		register,
		logout,
		refreshUserInfo,
		ensureAuthenticated,
	};
}

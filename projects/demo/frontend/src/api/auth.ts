// 用户认证API服务

export interface RegisterRequest {
	username: string;
	email: string;
	password: string;
}

export interface LoginRequest {
	username: string;
	password: string;
}

export interface AuthResponse {
	message: string;
	user: User;
	access_token: string;
	refresh_token: string;
	token_type: string;
}

export interface User {
	id: number;
	username: string;
	email?: string;
	created_at: string;
	updated_at: string;
	is_active: boolean;
}

export interface ApiError {
	error: string;
}

// API 基础地址配置
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

/**
 * 获取存储的token
 */
export function getStoredToken(): string | null {
	return localStorage.getItem("access_token");
}

/**
 * 存储token
 */
export function setStoredToken(token: string): void {
	localStorage.setItem("access_token", token);
}

/**
 * 获取存储的refresh token
 */
export function getStoredRefreshToken(): string | null {
	return localStorage.getItem("refresh_token");
}

/**
 * 存储refresh token
 */
export function setStoredRefreshToken(token: string): void {
	localStorage.setItem("refresh_token", token);
}

/**
 * 清除所有存储的token
 */
export function clearStoredTokens(): void {
	localStorage.removeItem("access_token");
	localStorage.removeItem("refresh_token");
	localStorage.removeItem("user");
}

/**
 * 存储用户信息
 */
export function setStoredUser(user: User): void {
	localStorage.setItem("user", JSON.stringify(user));
}

/**
 * 获取存储的用户信息
 */
export function getStoredUser(): User | null {
	const userStr = localStorage.getItem("user");
	if (!userStr) return null;
	try {
		return JSON.parse(userStr);
	} catch {
		return null;
	}
}

/**
 * 注册新用户
 */
export async function register(data: RegisterRequest): Promise<AuthResponse> {
	const response = await fetch(`${API_BASE_URL}/auth/register`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(data),
	});

	const result = await response.json();

	if (!response.ok) {
		throw new Error((result as ApiError).error || "注册失败");
	}

	return result as AuthResponse;
}

/**
 * 用户登录
 */
export async function login(data: LoginRequest): Promise<AuthResponse> {
	const response = await fetch(`${API_BASE_URL}/auth/login`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(data),
	});

	const result = await response.json();

	if (!response.ok) {
		throw new Error((result as ApiError).error || "登录失败");
	}

	return result as AuthResponse;
}

/**
 * 刷新访问令牌
 */
export async function refreshToken(): Promise<{
	access_token: string;
	token_type: string;
}> {
	const refreshTokenValue = getStoredRefreshToken();
	if (!refreshTokenValue) {
		throw new Error("没有刷新令牌");
	}

	const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${refreshTokenValue}`,
		},
	});

	const result = await response.json();

	if (!response.ok) {
		clearStoredTokens();
		throw new Error((result as ApiError).error || "刷新令牌失败");
	}

	return result;
}

/**
 * 获取当前用户信息
 */
export async function getCurrentUser(): Promise<User> {
	const token = getStoredToken();
	if (!token) {
		throw new Error("未登录");
	}

	const response = await fetch(`${API_BASE_URL}/auth/me`, {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${token}`,
		},
	});

	const result = await response.json();

	if (!response.ok) {
		if (response.status === 401) {
			clearStoredTokens();
		}
		throw new Error((result as ApiError).error || "获取用户信息失败");
	}

	return (result as { user: User }).user;
}

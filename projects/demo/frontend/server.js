// 简单的 Node.js 服务器，支持代理和 SPA 路由
import express from "express";
import { createProxyMiddleware } from "http-proxy-middleware";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import { readFileSync } from "fs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;
const API_TARGET = process.env.API_TARGET || "http://127.0.0.1:8000";

// API 代理
app.use(
	"/api",
	createProxyMiddleware({
		target: API_TARGET,
		changeOrigin: true,
		pathRewrite: {
			"^/api": "", // 移除 /api 前缀
		},
		onProxyReq: (proxyReq, req, res) => {
			console.log(
				`[Proxy] ${req.method} ${req.url} -> ${API_TARGET}${req.url.replace(
					"/api",
					""
				)}`
			);
		},
		onError: (err, req, res) => {
			console.error("[Proxy Error]", err.message);
			res.status(500).json({ error: "Proxy error" });
		},
	})
);

// 静态文件服务
app.use(express.static(join(__dirname, "dist")));

// SPA 路由支持：所有路由都返回 index.html
app.get("*", (req, res) => {
	try {
		const indexHtml = readFileSync(
			join(__dirname, "dist", "index.html"),
			"utf-8"
		);
		res.send(indexHtml);
	} catch (err) {
		res.status(404).send("Not found");
	}
});

app.listen(PORT, () => {
	console.log(`\n🚀 服务器启动成功！`);
	console.log(`📱 前端地址: http://localhost:${PORT}`);
	console.log(`🔗 API 代理: http://localhost:${PORT}/api -> ${API_TARGET}`);
	console.log(`\n按 Ctrl+C 停止服务器\n`);
});

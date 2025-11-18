import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
	plugins: [vue()],
	// 生产环境基础路径（如果部署在子目录，需要设置）
	// base: '/your-subdirectory/',
	build: {
		// 构建输出目录
		outDir: "dist",
		// 生成 source map（生产环境可以关闭以减小体积）
		sourcemap: false,
		// 压缩配置
		minify: "esbuild", // 使用 esbuild 更快，或使用 "terser" 需要额外配置
		// 分块策略
		rollupOptions: {
			output: {
				manualChunks: {
					vendor: ["vue"],
				},
			},
		},
		// 构建大小警告阈值（KB）
		chunkSizeWarningLimit: 1000,
	},
	server: {
		port: 5173,
		proxy: {
			"/api": {
				target: "http://127.0.0.1:8000",
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api/, ""),
				configure: (proxy) => {
					proxy.on("error", (err) => {
						console.log("proxy error", err);
					});
					proxy.on("proxyReq", (_proxyReq, req) => {
						console.log("Sending Request to the Target:", req.method, req.url);
					});
					proxy.on("proxyRes", (proxyRes, req) => {
						console.log(
							"Received Response from the Target:",
							proxyRes.statusCode,
							req.url
						);
					});
				},
			},
		},
	},
});

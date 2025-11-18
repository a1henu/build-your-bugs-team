# TOEFL 写作评分与润色系统 - 前端

基于 Vite + Vue 3 + TypeScript 构建的前端界面。

## 启动前端

```bash
npm install
npm run dev

```

## 功能特性

- 📝 输入学生作文内容
- 📊 自动评分并生成详细评语
- ✨ 自动润色作文，提升到 5 分标准
- 🔄 实时后端健康状态检查
- 🎨 现代化、响应式 UI 设计

## 开发环境要求

- Node.js 20.19.0+ 或 22.12.0+
- npm 或 yarn

## 安装依赖

```bash
cd frontend
npm install
```

## 开发运行

```bash
npm run dev
```

前端服务将在 `http://localhost:5173` 启动（Vite 默认端口）。

**注意**：确保后端服务（Flask）在 `http://localhost:8000` 运行。

## 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist/` 目录。

## 预览生产构建

```bash
npm run preview
```

## 项目结构

```
frontend/
├── src/
│   ├── api/
│   │   └── service.ts      # API 服务封装
│   ├── components/         # Vue 组件
│   ├── App.vue            # 主应用组件
│   ├── main.ts            # 应用入口
│   └── style.css          # 全局样式
├── public/                # 静态资源
├── index.html            # HTML 模板
├── vite.config.ts        # Vite 配置（包含代理设置）
└── package.json          # 项目依赖
```

## API 代理配置

在 `vite.config.ts` 中配置了代理，将 `/api/*` 请求转发到后端：

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

这意味着前端调用 `/api/grade_and_polish` 会被转发到后端的 `http://localhost:8000/grade_and_polish`。

## 使用说明

1. **启动后端服务**（在项目根目录）：

   ```bash
   python app.py
   ```

2. **启动前端服务**（在 frontend 目录）：

   ```bash
   npm run dev
   ```

3. **打开浏览器**访问 `http://localhost:5173`

4. **使用界面**：
   - 输入或选择题目文件（默认：test.yaml）
   - 在文本框中输入学生作文
   - 点击"提交评分与润色"按钮
   - 查看评分评语和润色后的作文

## 故障排除

### 后端连接失败

- 确保后端服务在 `http://localhost:8000` 运行
- 检查后端健康状态指示器（页面顶部）
- 查看浏览器控制台的错误信息

### 端口冲突

如果 5173 端口被占用，Vite 会自动使用下一个可用端口。或者可以在 `vite.config.ts` 中指定端口：

```typescript
server: {
  port: 3000,  // 自定义端口
  // ...
}
```

# Build Your Bugs Team - 团队和项目管理仓库

## 仓库简介

这是一个用于记录团队足迹和项目简单信息的管理仓库。具体的项目开发细节请参考对应的项目仓库。

## 仓库结构

```text
build-your-bugs-team/
├── README.md                           # 仓库说明文档
├── team/                              # 团队信息目录
│   ├── members/                       # 团队成员信息
│   │   └── team-overview.md          # 团队概览
│   ├── meetings/                      # 会议记录
│   │   ├── meeting-template.md       # 会议记录模板
│   │   └── 2024-09-29-first-meeting.md # 具体会议记录
│   └── resources/                     # 团队资源
├── projects/                          # 项目信息目录
│   ├── current-project/              # 当前项目
│   │   ├── docs/                     # 项目文档
│   │   │   └── project-goals.md      # 项目目标
│   │   ├── requirements/             # 需求文档
│   │   │   └── 需求.md              # 项目需求
│   │   ├── milestones/               # 里程碑跟踪
│   │   │   └── milestone-tracking.md # 里程碑跟踪表
│   │   └── project-overview.md       # 项目概览
│   └── archive/                      # 已归档项目
└── .gitignore                        # Git忽略文件
```

## 使用指南

### 团队信息管理

- **团队成员信息**: 在 `team/members/` 目录下维护团队成员的基本信息和角色分工
- **会议记录**: 在 `team/meetings/` 目录下按时间顺序记录所有会议
- **团队资源**: 在 `team/resources/` 目录下存放团队共享资源

### 项目管理

- **当前项目**: 在 `projects/current-project/` 目录下管理当前进行中的项目
- **项目文档**: 按功能模块分类存放项目相关文档
- **里程碑跟踪**: 使用 `milestones/` 目录跟踪项目进度
- **项目归档**: 完成的项目移至 `projects/archive/` 目录

### 文档规范

- 使用Markdown格式编写文档
- 文件名使用有意义的描述性名称
- 会议记录使用 `YYYY-MM-DD-会议主题.md` 格式
- 重要决策和变更需要团队讨论确认

## 当前项目

### 托福/雅思作文智能备考辅助系统

- **项目状态**: 需求分析阶段
- **核心功能**: 考法解析、自动问答、模拟机器评分
- **技术栈**: 大模型、RAG检索增强、Agent交互
- **项目目标**: 为托福/雅思作文备考学生提供免费、高质量的智能辅助工具

## 团队协作

### 会议安排

- **正式会议**: 每周一晚上8:40
- **日常沟通**: 微信群聊
- **文档协作**: 使用GitHub PR进行文档协作

### 工作流程

1. 创建功能分支进行文档编写
2. 提交PR进行代码审查
3. 团队讨论和评审
4. 合并到主分支
5. 更新项目状态和里程碑

## 贡献指南

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 联系方式

如有问题或建议，请通过以下方式联系：

- 微信群聊
- GitHub Issues
- 邮件联系团队成员

---

**最后更新**: 2024-10-05  
**维护团队**: Build Your Bugs Team

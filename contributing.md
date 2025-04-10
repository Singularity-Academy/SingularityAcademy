# 🛠️Singularity Academy Github 协作指南

## 🧩 项目概述

本项目是一个基于 **Go/Gin + React + TypeScript + Python + Langchain + APIs** 的大型 Web 应用。目标是构建一个智能、稳定、可拓展的系统，适用于 AI 驱动型服务场景。

---

## 🧑‍💻 技术栈分工

### 🖥️ 前端（React + TypeScript）

- 页面架构与路由管理（React Router）
- 与后端 API 对接 Websocket
- UI 组件库（Tailwind CSS + shadcn/ui）

### 🔧 后端（Go + Gin）

- Mysql

### 🤖 AI 服务（Python + Langchain）

- 构建智能任务链（LangChains / Agents）

- 调用 OpenAI 等大模型 API

  

---

## 🗂️ Git 协作流程

1. **Fork & Clone 项目**

   ```bash
   https://github.com/chrisdsasa/AI-online-School.git
   cd AI-online-School
   ```

2.	**新建分支（功能 / 修复 / 实验）**

          git checkout -b feat/your-feature-name



​3.	**提交规范（建议使用 Emoji）**

​	•	 feat: 新功能

​	•	 fix: 修复 Bug

​	•	 refactor: 重构代码

​	•	 chore: 配置、脚手架等

​	•	 docs: 文档更新

e.g.

​	git commit -m "✨ feat: 添加用户注册接口"

​4.	**推送分支**

git push origin feat/your-feature-name



​5.	**创建 Pull Request（PR）**

​	•	标题建议格式：[Feature] 用户登录模块

​	•	包含变更说明、影响范围、测试方法等

​	6.	**代码审查 & 合并**

​	•	所有 PR 需至少一人 Review 后才能合并

​	•	合并策略推荐：**Squash and Merge**

​	•	严禁强推 main / dev

**🔍 开发注意事项**

​	•	所有配置项统一放入 .env 文件

​	•	所有接口应保持统一的请求体和响应体结构

​	•	不确定的设计请 **单独建分支开发**，避免直接修改主分支

​	•	遇到冲突时使用：



git pull --rebase origin dev



**📌 TODO**

​	•	添加 PR 模板 .github/pull_request_template.md

​	•	添加代码检查工具（如 ESLint, GolangCI）

​	•	自动化测试（CI/CD）

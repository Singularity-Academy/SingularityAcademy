# 🎓 Singularity Academy (知澜 AI 在线学校)

<div align="center">

<img src="frontend/src/assets/illus/illus_hero_16.png" alt="ClarifAI Logo" width="200" height="200" style="margin-bottom: 20px;">

![Python Version](https://img.shields.io/badge/Python-3.11%2B-blue)
![Go Version](https://img.shields.io/badge/Go-1.23%2B-blue)
![TypeScript Version](https://img.shields.io/badge/TypeScript-5%2B-blue)
![React](https://img.shields.io/badge/React-18%2B-blue)
![Chakra UI](https://img.shields.io/badge/Chakra%20UI-2.10%2B-blue)
![Gin](https://img.shields.io/badge/Gin-1.10%2B-blue)
![GORM](https://img.shields.io/badge/GORM-1.26%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.3%2B-blue)
![Sanic](https://img.shields.io/badge/Sanic-25.3%2B-blue)

**一个基于 AI 驱动的现代化在线教育平台，融合先进的 Web 技术与人工智能能力，提供个性化学习体验。**

[English](#english) | [中文](#chinese)

</div>

---

## 📋 目录

- [🎯 项目概述](#-项目概述)
- [🏗️ 系统架构](#️-系统架构)
- [🛠️ 技术栈](#️-技术栈)
- [✨ 核心功能](#-核心功能)
- [🚀 快速开始](#-快速开始)
- [📚 API 文档](#-api-文档)
- [🧪 测试](#-测试)
- [🔧 开发指南](#-开发指南)
- [🤝 贡献指南](#-贡献指南)
- [📄 许可证](#-许可证)
- [🗺️ 路线图](#️-路线图)

---

## 🎯 项目概述

Singularity Academy 是一个全栈 AI 驱动的教育平台，结合了现代 Web 技术和先进的人工智能能力。该平台提供：

- 🤖 **AI 智能导师**：基于 LangChain 的对话式学习助手
- 📊 **个性化学习路径**：根据用户能力动态调整课程内容
- 🎥 **多媒体内容生成**：自动生成教学视频和可视化内容
- 🌐 **多语言支持**：支持中文、英文等多种语言界面
- 📱 **响应式设计**：适配桌面端和移动端设备
- 🔒 **安全认证**：JWT 基础的用户认证和授权系统

---

## 🏗️ 系统架构

```mermaid
graph TB
    subgraph "客户端层"
        A[React 前端应用]
        B[移动端浏览器]
    end
    
    subgraph "网关层"
        C[Caddy 反向代理]
    end
    
    subgraph "应用层"
        D[Go/Gin 后端服务]
        E[Python/Sanic AI 引擎]
    end
    
    subgraph "数据层"
        F[(MySQL 数据库)]
        G[文件存储系统]
    end
    
    subgraph "外部服务"
        H[OpenAI API]
        I[其他 AI 服务]
    end
    
    A --> C
    B --> C
    C --> D
    C --> E
    D <--> F
    E --> G
    E --> H
    E --> I
    D <--> E
```

### 架构特点

- **微服务架构**：前端、后端、AI 引擎分离部署
- **反向代理**：Caddy 提供自动 HTTPS 和负载均衡
- **实时通信**：WebSocket 支持实时 AI 对话
- **数据持久化**：MySQL 存储用户数据，文件系统存储媒体内容
- **AI 集成**：LangChain 框架集成多种 AI 模型

---

## 🛠️ 技术栈

### 🖥️ 前端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| **React** | 18.2+ | 用户界面框架 |
| **TypeScript** | 4.9+ | 类型安全的 JavaScript |
| **Chakra UI** | 2.10+ | 现代化 UI 组件库 |
| **React Router** | 6.28+ | 客户端路由管理 |
| **Zustand** | 4.4+ | 轻量级状态管理 |
| **React Hook Form** | 7.54+ | 表单处理和验证 |
| **i18next** | 22.4+ | 国际化支持 |
| **Socket.io Client** | 4.8+ | 实时通信客户端 |
| **Framer Motion** | 10.18+ | 动画和过渡效果 |

### 🔧 后端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| **Go** | 1.23+ | 后端编程语言 |
| **Gin** | 1.10+ | Web 框架 |
| **GORM** | 1.26+ | ORM 数据库操作 |
| **MySQL** | 8.0+ | 关系型数据库 |
| **JWT** | 3.2+ | 用户认证和授权 |
| **Gorilla WebSocket** | 1.5+ | WebSocket 支持 |
| **Viper** | 1.19+ | 配置管理 |

### 🤖 AI 引擎技术

| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.11+ | AI 服务编程语言 |
| **Sanic** | 25.3+ | 异步 Web 框架 |
| **LangChain** | 0.3+ | AI 应用开发框架 |
| **OpenAI** | 1.78+ | GPT 模型集成 |
| **Tortoise ORM** | 0.25+ | 异步 ORM |
| **Pydantic** | 2.11+ | 数据验证和序列化 |

### 🌐 基础设施

| 技术 | 版本 | 用途 |
|------|------|------|
| **Caddy** | 2.6+ | 反向代理和 HTTPS |
| **Docker** | 20.10+ | 容器化部署 |
| **GitHub Actions** | - | CI/CD 自动化 |

---

## ✨ 核心功能

### 🎓 智能学习系统

#### 1. AI 导师对话
- **实时对话**：基于 WebSocket 的即时 AI 交互
- **上下文感知**：记忆对话历史，提供连贯的学习体验
- **多模态支持**：文本、图像、视频内容生成

```python
# AI 导师核心功能示例
async def generate_study_plan(self, material: str) -> Dict:
    """
    根据上传的学习材料生成个性化学习计划
    - 文档内容分析
    - 学习目标设定
    - 进度跟踪机制
    """
    return {
        "manim_script": "# 可视化动画脚本",
        "message": "个性化学习建议",
        "notes": "重点知识总结"
    }
```

#### 2. 文档智能处理
- **多格式支持**：PDF、DOCX、PPTX、CSV 等
- **内容提取**：自动提取文本和结构化信息
- **语义分析**：理解文档内容并生成学习要点

#### 3. 个性化学习路径
- **能力评估**：动态评估学习者当前水平
- **自适应调整**：根据学习进度调整难度和内容
- **成就系统**：激励机制和进度可视化

### 🔐 用户管理系统

#### 1. 安全认证
```go
// JWT 认证中间件
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.JSON(401, gin.H{"error": "未授权访问"})
            c.Abort()
            return
        }
        // 验证 JWT token
        claims, err := validateJWT(token)
        if err != nil {
            c.JSON(401, gin.H{"error": "无效的认证令牌"})
            c.Abort()
            return
        }
        c.Set("user", claims)
        c.Next()
    }
}
```

#### 2. 用户档案管理
- **学习历史**：记录学习轨迹和成就
- **偏好设置**：个性化界面和学习偏好
- **进度统计**：详细的学习数据分析

### 🌐 国际化支持

#### 多语言界面
- **支持语言**：中文（简体/繁体）、英文、西班牙文、法文、德文、日文、阿拉伯文
- **动态切换**：无需刷新页面即可切换语言
- **本地化内容**：根据地区提供相应的学习内容

```typescript
// 语言切换实现
const LANGUAGE_NAMES = {
    en: 'English',
    es: 'Español', 
    fr: 'Français',
    de: 'Deutsch',
    ja: '日本語',
    ar: 'العربية',
    zh: '中文(简体)',
    zh_CN: '中文(繁體)'
};
```

---

## 🚀 快速开始

### 📋 系统要求

- **Node.js** 18.12+ (LTS)
- **Go** 1.23+
- **Python** 3.11+
- **MySQL** 8.0+
- **Git** 2.30+

### 🔧 环境配置

#### 1. 克隆项目
```bash
git clone https://github.com/chrisdsasa/AI-online-School.git
cd AI-online-School
```

#### 2. 数据库设置
```bash
# 创建 MySQL 数据库
mysql -u root -p
CREATE DATABASE singularity_academy;
CREATE USER 'sa_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON singularity_academy.* TO 'sa_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. 环境变量配置

**后端配置 (backend/.env)**
```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=sa_user
DB_PASSWORD=your_password
DB_NAME=singularity_academy

# JWT 配置
JWT_SECRET=your_jwt_secret_key
JWT_EXPIRE_HOURS=24

# 服务器配置
SERVER_PORT=8080
GIN_MODE=debug
```

**AI 引擎配置 (ai_engine/config/config.json)**

```json
{
    "openai": {
        "api_key": "your_openai_api_key",
        "model": "gpt-4",
        "max_tokens": 2000
    },
    "database": {
        "url": "mysql://sa_user:your_password@localhost:3306/singularity_academy"
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8001
    }
}
```

### 🏃‍♂️ 启动服务

#### 1. 启动 AI 引擎
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r 

# 启动服务
python run.py
```

#### 2. 启动后端服务
```bash
cd backend

# 下载 Go 模块
go mod download

# 运行数据库迁移
go run main.go migrate

# 启动服务
go run main.go
```

#### 3. 启动前端应用
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

#### 4. 启动反向代理（可选）
```bash
# 在项目根目录
caddy start
```

### 🌐 访问应用

- **前端应用**: http://localhost:3000
- **后端 API**: http://localhost:8080
- **AI 引擎**: http://localhost:8001
- **完整应用** (通过 Caddy): https://localhost

---

## 📚 API 文档

### 🔐 认证接口

#### 用户注册
```http
POST /api/auth/register
Content-Type: application/json

{
    "name": "用户名",
    "email": "user@example.com", 
    "password": "password123"
}
```

#### 用户登录
```http
POST /api/auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

### 👤 用户管理接口

#### 获取用户信息
```http
GET /api/user/profile
Authorization: Bearer <jwt_token>
```

#### 更新用户信息
```http
PUT /api/user/profile
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "name": "新用户名",
    "preferences": {
        "language": "zh",
        "theme": "dark"
    }
}
```

### 📚 课程管理接口

#### 获取课程列表
```http
GET /api/courses
Authorization: Bearer <jwt_token>
```

#### 创建新课程
```http
POST /api/courses
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "title": "课程标题",
    "description": "课程描述",
    "materials": ["material_id_1", "material_id_2"]
}
```

### 🤖 AI 引擎接口

#### WebSocket 连接
```javascript
// 连接 AI 导师
const socket = io('ws://localhost:8001/ai/dean_ai/{token}?material={filename}');

// 发送消息
socket.emit('message', {
    type: 'question',
    content: '请解释这个概念'
});

// 接收响应
socket.on('response', (data) => {
    console.log('AI 响应:', data);
    // data 结构:
    // {
    //     "manim_script": "动画脚本",
    //     "message": "文本回复", 
    //     "notes": "学习要点"
    // }
});
```

#### 文件上传处理
```http
POST /api/materials/upload
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data

file: <binary_file_data>
```

---

## 🧪 测试

### 🔧 后端测试

```bash
cd backend

# 运行所有测试
go test ./...

# 运行特定包的测试
go test ./auth -v

# 生成测试覆盖率报告
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### ⚛️ 前端测试

```bash
cd frontend

# 运行单元测试
npm test

# 运行测试并生成覆盖率报告
npm test -- --coverage

# 运行 E2E 测试
npm run test:e2e
```

### 🐍 AI 引擎测试

```bash
cd ai_engine

# 安装测试依赖
pip install pytest pytest-asyncio pytest-cov

# 运行测试
pytest tests/ -v

# 生成覆盖率报告
pytest tests/ --cov=apps --cov-report=html
```

### 🧪 集成测试

```bash
# 启动所有服务后运行集成测试
cd test
python integration_tests.py
```

---

## 🔧 开发指南

### 📁 项目结构

```
Singularity Academy/
├── 📁 frontend/                 # React 前端应用
│   ├── 📁 src/
│   │   ├── 📁 components/       # 可复用组件
│   │   ├── 📁 pages/           # 页面组件
│   │   ├── 📁 hooks/           # 自定义 Hooks
│   │   ├── 📁 utils/           # 工具函数
│   │   ├── 📁 locales/         # 国际化文件
│   │   └── 📁 types/           # TypeScript 类型定义
│   ├── 📄 package.json
│   └── 📄 tsconfig.json
├── 📁 backend/                  # Go 后端服务
│   ├── 📁 controllers/         # 控制器
│   ├── 📁 models/              # 数据模型
│   ├── 📁 middlewares/         # 中间件
│   ├── 📁 utils/               # 工具函数
│   ├── 📁 config/              # 配置文件
│   ├── 📄 main.go
│   └── 📄 go.mod
├── 📁 ai_engine/               # Python AI 引擎
│   ├── 📁 apps/                # 应用模块
│   ├── 📁 config/              # 配置文件
│   ├── 📁 docs/                # AI 引擎文档
│   ├── 📄 app.py
│   └── 📄 registry.py
├── 📁 docs/                    # 项目文档
├── 📁 scripts/                 # 部署和工具脚本
├── 📁 test/                    # 测试文件
├── 📄 requirements.txt         # Python 依赖
├── 📄 Caddyfile               # Caddy 配置
├── 📄 docker-compose.yml      # Docker 编排
└── 📄 README.md
```

### 🎨 代码规范

#### TypeScript/React 规范
```typescript
// 组件命名：PascalCase
export const UserProfile: React.FC<UserProfileProps> = ({ user }) => {
    // Hooks 在组件顶部
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    
    // 事件处理函数：handle + 动作
    const handleSubmit = async (data: FormData) => {
        setLoading(true);
        try {
            await updateProfile(data);
            toast.success('更新成功');
        } catch (error) {
            toast.error('更新失败');
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <Box>
            {/* JSX 内容 */}
        </Box>
    );
};
```

#### Go 代码规范
```go
// 包名：小写，简洁
package controllers

// 结构体：PascalCase
type UserController struct {
    userService *services.UserService
}

// 方法：PascalCase，导出方法
func (uc *UserController) GetProfile(c *gin.Context) {
    // 获取用户 ID
    userID, exists := c.Get("userID")
    if !exists {
        c.JSON(http.StatusUnauthorized, gin.H{
            "error": "未授权访问",
        })
        return
    }
    
    // 业务逻辑
    profile, err := uc.userService.GetProfile(userID.(uint))
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{
            "error": "获取用户信息失败",
        })
        return
    }
    
    c.JSON(http.StatusOK, gin.H{
        "data": profile,
    })
}
```

#### Python 代码规范
```python
# 类名：PascalCase
class DeanAIAgent:
    """AI 导师代理类"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm = self._initialize_llm()
    
    async def generate_response(self, message: str) -> Dict[str, str]:
        """
        生成 AI 响应
        
        Args:
            message: 用户输入消息
            
        Returns:
            包含响应内容的字典
        """
        try:
            response = await self.llm.agenerate([message])
            return {
                "message": response.generations[0][0].text,
                "status": "success"
            }
        except Exception as e:
            logger.error(f"生成响应失败: {e}")
            return {
                "message": "抱歉，我现在无法回答您的问题",
                "status": "error"
            }
```

### 🔄 Git 工作流

#### 分支策略
- `main`: 生产环境代码
- `develop`: 开发环境集成分支
- `feature/*`: 功能开发分支
- `hotfix/*`: 紧急修复分支

#### 提交规范
```bash
# 功能开发
git commit -m "✨ feat: 添加用户个人资料页面"

# Bug 修复
git commit -m "🐛 fix: 修复登录状态丢失问题"

# 代码重构
git commit -m "♻️ refactor: 重构 AI 引擎响应处理逻辑"

# 文档更新
git commit -m "📝 docs: 更新 API 文档"

# 性能优化
git commit -m "⚡ perf: 优化数据库查询性能"
```

### 🚀 部署指南

#### Docker 部署
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

#### 生产环境部署
```bash
# 前端构建
cd frontend
npm run build

# 后端构建
cd backend
go build -o main .

# AI 引擎部署
cd ai_engine
pip install -r requirements.txt
python app.py
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！请阅读 [CONTRIBUTING.md](contributing.md) 了解详细的贡献指南。

### 🔧 开发环境设置

1. **Fork 项目**到您的 GitHub 账户
2. **克隆**您的 fork 到本地
3. **创建功能分支**：`git checkout -b feature/amazing-feature`
4. **提交更改**：`git commit -m '✨ feat: 添加惊人的功能'`
5. **推送分支**：`git push origin feature/amazing-feature`
6. **创建 Pull Request**

### 📝 提交 Issue

在提交 Issue 时，请提供：
- 🐛 **Bug 报告**：详细的重现步骤、期望行为、实际行为
- 💡 **功能请求**：清晰的功能描述、使用场景、预期收益
- 📚 **文档改进**：具体的改进建议和理由

### 🔍 代码审查

所有 Pull Request 都需要经过代码审查：
- ✅ 代码符合项目规范
- ✅ 包含适当的测试
- ✅ 文档已更新
- ✅ 通过所有 CI 检查

---

## 📄 许可证

本项目目前为私有项目，暂无开源许可证。如需商业使用或合作，请联系项目维护者。

---

## 🗺️ 路线图

### 🎯 2025 Q1-Q2 目标

#### 🚀 核心功能增强
- [ ] **多模态 AI 集成**
  - 图像识别和生成
  - 语音交互支持
  - 视频内容分析

- [ ] **实时协作功能**
  - 多用户同步学习
  - 实时白板和注释
  - 小组讨论功能

- [ ] **自适应评估引擎**
  - 智能题目生成
  - 学习能力评估
  - 个性化推荐算法

#### 📱 移动端支持
- [ ] **React Native 应用**
  - iOS 和 Android 原生应用
  - 离线学习支持
  - 推送通知系统

#### 🔧 技术优化
- [ ] **性能优化**
  - 数据库查询优化
  - 前端代码分割
  - CDN 内容分发

- [ ] **监控和日志**
  - Prometheus 监控集成
  - ELK 日志分析栈
  - 性能指标仪表板

### 🎯 2025 Q3-Q4 目标

#### 🌐 平台扩展
- [ ] **AI 教学助手市场**
  - 第三方 AI 模型集成
  - 插件系统开发
  - 开发者 API 平台

- [ ] **区块链凭证验证**
  - 学习成果上链
  - NFT 证书系统
  - 去中心化身份验证

#### 🎓 教育生态
- [ ] **机构合作平台**
  - 学校和培训机构接入
  - 课程内容管理系统
  - 教师管理工具

- [ ] **社区功能**
  - 学习者社区
  - 知识分享平台
  - 同伴学习匹配

### 🔮 长期愿景

- **🌍 全球化部署**：多地区数据中心，低延迟访问
- **🧠 AGI 集成**：下一代人工智能模型集成
- **🎮 游戏化学习**：沉浸式学习体验
- **🔬 学习科学研究**：基于数据的学习效果研究

---

## 📞 联系我们

- **项目维护者**: KRYPOTO Team
- **邮箱**: contact@singularityacademy.ai
- **GitHub**: [AI-online-School](https://github.com/chrisdsasa/AI-online-School)
- **文档**: [项目文档](docs/)

---

## 🙏 致谢

感谢所有为 Singularity Academy 项目做出贡献的开发者和用户！

特别感谢以下开源项目：
- [React](https://reactjs.org/) - 用户界面库
- [Go](https://golang.org/) - 后端编程语言
- [LangChain](https://langchain.com/) - AI 应用开发框架
- [Chakra UI](https://chakra-ui.com/) - 现代化 UI 组件库
- [Gin](https://gin-gonic.com/) - Go Web 框架

---

<div align="center">

**🎓 让 AI 重新定义教育，让学习变得更加智能和有趣！**

Made with ❤️ by KRYPOTO Team

</div>

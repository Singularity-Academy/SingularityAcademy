# Dokploy 部署指南

## 部署步骤

### 1. 准备工作

确保您的 GitHub 仓库包含以下文件：
- `docker-compose.yml` (根目录)
- `frontend/Dockerfile`
- `backend/Dockerfile` 
- `Dockerfile` (AI Engine)
- `.env.example`

### 2. 在 Dokploy 中创建应用

1. **登录 Dokploy 控制台**
2. **创建新的 Compose 应用**
   - 选择 "Docker Compose" 类型
   - 连接您的 GitHub 仓库
   - 选择主分支 (main/master)

### 3. 配置环境变量

在 Dokploy 的环境变量设置中添加：

```env
# 必需的环境变量
DB_USER=sa_user
DB_PASSWORD=your_secure_password_here
DB_NAME=singularity_academy
JWT_SECRET=your_jwt_secret_key_minimum_32_chars
OPENAI_API_KEY=sk-your_openai_api_key_here

# 可选的邮件配置
EMAIL_HOST=smtp.exmail.qq.com
EMAIL_PORT=465
EMAIL_USER=your_email@domain.com
EMAIL_PASSWORD=your_email_password
```

### 4. 域名配置

#### 选项 A: 使用 Dokploy 提供的域名
- 应用将在 Dokploy 分配的域名上运行
- 通过端口 1298 访问（Caddy 代理）

#### 选项 B: 使用自定义域名
1. 在 Dokploy 中配置您的域名
2. 更新 DNS 记录指向 Dokploy 服务器
3. 修改 `Caddyfile` 中的端口配置：

```caddyfile
your-domain.com {
    # API 路由反向代理到 8080 端口
    reverse_proxy /api/* backend:8080
    
    # AI 路由反代到 8000端口
    reverse_proxy /ai/* ai-engine:8000
    
    # 其他路由反向代理到 3000 端口
    reverse_proxy /* frontend:3000
    
    # CORS 和 WebSocket 设置
    header {
        Access-Control-Allow-Origin: *
        Access-Control-Allow-Methods: GET, POST, PUT, DELETE
        Access-Control-Allow-Headers: Content-Type, X-Real-IP, Authorization
        Access-Control-Allow-Credentials true
        Access-Control-Allow-WebSockets true
    }
}
```

### 5. 部署配置

确保 Dokploy 中的设置：
- **构建命令**: `docker-compose build`
- **启动命令**: `docker-compose up -d`
- **健康检查**: 启用
- **自动重启**: 启用

### 6. 数据持久化

Docker Compose 配置包含以下持久化卷：
- `mysql_data`: MySQL 数据库数据
- `caddy_data`: Caddy 证书和配置
- `caddy_config`: Caddy 配置缓存

### 7. 服务端口映射

| 服务 | 内部端口 | 外部端口 | 说明 |
|------|----------|----------|------|
| Frontend | 3000 | - | 通过 Caddy 访问 |
| Backend | 8080 | - | 通过 Caddy 访问 |
| AI Engine | 8000 | - | 通过 Caddy 访问 |
| MySQL | 3306 | 3306 | 数据库 |
| Caddy | 1298 | 1298/80/443 | 主入口 |

### 8. 部署后验证

部署完成后，访问您的域名或 Dokploy 提供的 URL：

1. **前端页面**: `https://your-domain.com` 
2. **后端 API**: `https://your-domain.com/api/`
3. **AI API**: `https://your-domain.com/ai/`

### 9. 监控和日志

在 Dokploy 控制台中：
- 查看各服务状态
- 监控资源使用情况
- 查看应用日志
- 设置告警通知

### 10. 常见问题

#### 数据库连接问题
- 确保环境变量正确设置
- 检查 MySQL 服务是否正常启动
- 验证数据库用户权限

#### OpenAI API 问题
- 确认 API 密钥有效
- 检查 API 配额限制
- 验证网络连接

#### 前端无法访问 API
- 检查 Caddy 配置
- 确认服务间网络连接
- 验证 CORS 设置

### 11. 扩展和优化

#### 水平扩展
```yaml
# 在 docker-compose.yml 中为服务添加副本
backend:
  # ... 其他配置
  deploy:
    replicas: 2
```

#### 资源限制
```yaml
backend:
  # ... 其他配置
  deploy:
    resources:
      limits:
        memory: 512M
        cpus: '0.5'
```

### 12. 备份策略

定期备份重要数据：
- MySQL 数据库导出
- Caddy 证书和配置
- 应用配置文件

---

## 快速部署清单

- [ ] GitHub 仓库准备就绪
- [ ] Dokploy 应用创建
- [ ] 环境变量配置
- [ ] 域名设置 (可选)
- [ ] 部署启动
- [ ] 功能测试验证
- [ ] 监控设置
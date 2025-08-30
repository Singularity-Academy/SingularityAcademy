# 🎥 AI Manim 视频生成器 API 使用指南

## 🚀 快速开始

### 1. 启动API服务器
```bash
python3 ai_manim_api.py
```

**API地址**: http://localhost:8888

## 📡 核心功能

### ✨ 主要特点
- **输入**: 文字需求（如"牛顿第一定律"）
- **输出**: 自动生成的教育动画视频
- **AI驱动**: 使用您配置的AI模型（GPT-4, DeepSeek等）
- **即时下载**: 生成后立即可下载

## 🎯 API接口

| 功能 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 🏠 API信息 | GET | `/` | 查看API文档和示例 |
| 🔍 状态检查 | GET | `/status` | 检查API和AI状态 |
| 🎬 **生成视频** | POST | `/generate` | **核心功能：文字→视频** |
| 📥 下载视频 | GET | `/video/{id}` | 下载生成的视频文件 |
| 📋 视频列表 | GET | `/videos` | 查看所有生成的视频 |
| 🤖 模型列表 | GET | `/models` | 查看可用的AI模型 |

## 🎬 核心使用方法

### 第一步：生成视频
```bash
curl -X POST http://localhost:8888/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "牛顿第一定律",
    "title": "物理课程",
    "model": "gpt-4"
  }'
```

**响应示例**：
```json
{
  "success": true,
  "video_id": "a1b2c3d4",
  "download_url": "/video/a1b2c3d4",
  "video_size": "234.5 KB",
  "title": "物理课程",
  "model_used": "gpt-4",
  "scene_name": "NewtonFirstLaw"
}
```

### 第二步：下载视频
```bash
curl -o my_video.mp4 http://localhost:8888/video/a1b2c3d4
```

## 💻 编程示例

### Python 示例
```python
import requests

# 生成视频
response = requests.post('http://localhost:8888/generate', json={
    "text": "圆周运动和向心力",
    "title": "物理动画",
    "model": "gpt-4"  # 可选
})

if response.status_code == 200:
    data = response.json()
    if data['success']:
        video_id = data['video_id']
        print(f"✅ 视频生成成功: {video_id}")
        
        # 下载视频
        video_url = f"http://localhost:8888/video/{video_id}"
        video_response = requests.get(video_url)
        
        with open(f"{data['title']}_{video_id}.mp4", 'wb') as f:
            f.write(video_response.content)
        print("📥 视频下载完成")
    else:
        print(f"❌ 生成失败: {data['error']}")
```

### JavaScript 示例
```javascript
async function generateVideo(text, title) {
    try {
        const response = await fetch('http://localhost:8888/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, title })
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log(`✅ 视频生成成功: ${data.video_id}`);
            return `http://localhost:8888/video/${data.video_id}`;
        } else {
            console.error(`❌ 生成失败: ${data.error}`);
        }
    } catch (error) {
        console.error('请求失败:', error);
    }
}

// 使用示例
generateVideo("三角函数图像", "数学课程").then(downloadUrl => {
    if (downloadUrl) {
        console.log(`📥 下载链接: ${downloadUrl}`);
    }
});
```

## 🔧 配置说明

### 必需文件
- `config.json` - AI模型配置（API密钥等）
- `ai_video_generator.py` - 核心生成器

### 可选参数
- `text` ✅ **必需** - 要生成视频的文字内容
- `title` ⚪ 可选 - 视频标题
- `model` ⚪ 可选 - 指定AI模型（如"gpt-4", "deepseek-chat"）

### 支持的内容类型
- 物理概念（牛顿定律、圆周运动等）
- 数学概念（三角函数、导数等）
- 其他教育内容

## 🧪 测试工具

### 自动测试
```bash
python3 test_ai_api.py
```

### 交互测试
运行测试脚本并选择"2. 交互式测试"

## ⚙️ 系统要求

- Python 3.10+
- Manim Community Edition
- Flask, requests
- 有效的AI API密钥（OpenAI, DeepSeek等）

## 🎉 成功示例

**输入**: `{"text": "牛顿第一定律"}`

**输出**: 
- 🎬 15-30秒动画视频
- 📊 包含公式、图形、动画
- 📝 中文说明文字
- 🎨 专业视觉效果

## 🔍 故障排除

| 问题 | 解决方案 |
|------|----------|
| API不可用 | 检查服务器是否启动在8888端口 |
| AI生成失败 | 检查config.json中的API密钥 |
| 视频渲染失败 | 确认Manim环境配置正确 |
| 中文显示问题 | 使用Text()而非Tex()处理中文 |

---

## 🚀 开始使用

1. **启动API**: `python3 ai_manim_api.py`
2. **测试连接**: 访问 http://localhost:8888/
3. **生成视频**: 使用上述示例代码
4. **享受结果**: 下载您的AI生成视频！

**🎬 您的AI视频生成器已就绪！** 
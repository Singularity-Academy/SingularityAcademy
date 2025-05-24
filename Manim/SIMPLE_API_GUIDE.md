# 🎥 视频生成API - 简单使用指南

## 🚀 快速开始

### 1. 启动API服务器
```bash
python3 final_api.py
```

**API地址**: http://localhost:4567

## 📡 API接口

### ✅ 已实现功能

| 功能 | 接口 | 说明 |
|------|------|------|
| 🏠 首页 | `GET /` | 查看API信息 |
| 🔍 状态 | `GET /status` | 检查API状态 |
| 🎬 生成视频 | `POST /generate` | **核心功能** |
| 📥 下载视频 | `GET /video/{id}` | 获取生成的视频 |

## 🎯 核心使用流程

### 第一步：生成视频
```bash
curl -X POST http://localhost:4567/generate \
  -H "Content-Type: application/json" \
  -d '{"content": "牛顿第一定律"}'
```

**响应示例**：
```json
{
  "success": true,
  "video_name": "video_190235",
  "video_id": "95a9f9dd",
  "video_url": "/video/95a9f9dd",
  "video_size": "146.3 KB",
  "content": "牛顿第一定律",
  "generated_at": "2025-05-24T19:02:39.733766"
}
```

### 第二步：下载视频
```bash
curl -o my_video.mp4 http://localhost:4567/video/95a9f9dd
```

## 💻 编程示例

### Python示例
```python
import requests

# 生成视频
response = requests.post('http://localhost:4567/generate', 
    json={"content": "牛顿第一定律"})

if response.status_code == 200:
    data = response.json()
    if data['success']:
        video_id = data['video_id']
        print(f"✅ 视频生成成功: {video_id}")
        
        # 下载视频
        video_response = requests.get(f'http://localhost:4567/video/{video_id}')
        with open(f'{video_id}.mp4', 'wb') as f:
            f.write(video_response.content)
        print("📥 视频下载完成")
```

### JavaScript示例
```javascript
async function generateVideo(content) {
    try {
        // 生成视频
        const response = await fetch('http://localhost:4567/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({content: content})
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log(`✅ 视频生成成功: ${data.video_id}`);
            
            // 返回下载链接
            return `http://localhost:4567/video/${data.video_id}`;
        }
    } catch (error) {
        console.error('❌ 生成失败:', error);
    }
}

// 使用示例
generateVideo("牛顿第一定律").then(url => {
    if (url) {
        console.log(`📥 下载链接: ${url}`);
    }
});
```

## 🔧 API配置信息

- **端口**: 4567 ✅ (避开了8000, 8080, 5000, 3000, 1298)
- **输入**: 课程内容文字
- **输出**: 
  1. ✅ 视频名字 (`video_name`)
  2. ✅ 视频ID (`video_id`) 
  3. ✅ 视频本身 (通过`/video/{id}`下载)
- **视频质量**: 720p @ 30fps (中等质量)
- **支持格式**: MP4

## 📊 测试结果

✅ **成功测试案例**:
- 输入: "牛顿第一定律"
- 视频ID: 95a9f9dd
- 文件大小: 146.3 KB
- 生成时间: ~30秒
- 下载成功: ✅

## 🎯 特点

### ✅ 优势
- **简单易用**: 只需一个POST请求
- **无复杂配置**: 开箱即用
- **稳定端口**: 4567端口
- **标准格式**: JSON输入/输出
- **快速生成**: 30秒内完成

### 📝 当前限制
- 固定物理模板 (牛顿第一定律)
- 中文文本渲染
- 中等质量输出

## 🚀 扩展建议

如需更多功能，可以考虑：
1. 添加更多预设模板
2. 支持自定义内容
3. 多种质量选项
4. 批量生成功能

---

## 🎉 开始使用

1. **启动API**: `python3 final_api.py`
2. **测试状态**: `curl http://localhost:4567/status`
3. **生成视频**: 使用上述示例代码

**🎬 您的简单视频生成API已就绪！** 
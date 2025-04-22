# React→Go WebSocket 视频/音频流实现指南

> **目标读者：** MirrorChild / Singularity Academy 研发团队全员  
> **版本：** v1.0 ‖ 2025‑04‑22  
> **阅读用时：** ≈ 6 分钟

---

## 📑 目录
1. [系统架构总览](#系统架构总览)
2. [前端媒体采集](#前端媒体采集)
3. [WebSocket 通信层](#WebSocket-通信层)
4. [Go 后端流处理](#Go-后端流处理)
5. [横向扩展与生产部署](#横向扩展与生产部署)
6. [开发约定与规范](#开发约定与规范)
7. [参考链接](#参考链接)

---

## 1. 系统架构总览
<a name="系统架构总览"></a>

### Diagram 1：整体架构
```ascii
+-----------------+         +----------------+         +----------------+
|                 |  WebSocket              |         |                |
|  React Frontend | <------> |  Go Backend  | <------> |  AI Engine    |
|                 |  (Video/Audio)          |         |                |
+-----------------+         +----------------+         +----------------+
```

**说明：**
- **React Frontend**：负责采集/压缩音视频并实时推送；同时接收 AI 反馈并渲染 UI。
- **Go Backend**：维护长连接、做简单缓冲与鉴权，将流转发或预处理后推送至 AI 服务。
- **AI Engine**：声纹识别、语义分析或 CV 推理等；结果通过同一通道回传。

---

## 2. 前端媒体采集
<a name="前端媒体采集"></a>

### Diagram 2：媒体采集流程
```ascii
+------------------+     +------------------+     +------------------+
| User Permissions | --> | Media Capture    | --> | Stream Processing|
| getUserMedia()   |     | Video/Audio      |     | Encode/Compress  |
+------------------+     +------------------+     +------------------+
          |                                               |
          v                                               v
+------------------+                           +------------------+
| Preview Display  |                           | WebSocket Send   |
| <video> element  |                           | Binary Data      |
+------------------+                           +------------------+
```

### 核心实现步骤
1. **权限申请**：`navigator.mediaDevices.getUserMedia({ video:true, audio:true })`。
2. **创建 MediaStream**：将返回的流对象挂载至 `<video>` 进行本地预览。
3. **帧率控制**：低带宽场景建议 `MediaRecorder` + `timeslice=100ms`（≈ 10 fps）。
4. **压缩编码**：
   - 视频：`canvas.captureStream()` & `toBlob('image/webp', 0.6)`。
   - 音频：`AudioContext` → `ScriptProcessor` → PCM 16‑bit。
5. **数据封包**：统一封装 `{ type:'v'|'a', ts:int64, payload:ArrayBuffer }`，便于后端解码。

> 💡 **Tip:** 10 fps / 640×360 / WebP‑0.6 ≈ 120 kbps；音频 16 kHz Mono ≈ 256 kbps → 总带宽 ~ 380 kbps，可满足大部分 4G/Wi‑Fi 网络。

---

## 3. WebSocket 通信层
<a name="WebSocket-通信层"></a>

### Diagram 3：通信与会话管理
```ascii
+-------------------+     +--------------------+     +-------------------+
| WebSocket Connect | --> | Authentication     | --> | Connection Pool   |
| Frontend to Go    |     | JWT Token          |     | User Management   |
+-------------------+     +--------------------+     +-------------------+
          |                                                   |
          v                                                   v
+-------------------+                               +-------------------+
| Binary Data Flow  |                               | Error Handling    |
| Bidirectional     |                               | Reconnect Logic   |
+-------------------+                               +-------------------+
```

### 实现要点
| 主题 | 前端 | 后端 |
|------|------|------|
| **鉴权** | 连接 URL 携带 `token`，或 `ws.send({cmd:'auth', jwt})` | 解析 & 验签 JWT，失败即关闭连接(`4001`) |
| **心跳** | `setInterval(()=>ws.send('ping'),5s);` | 5 s 未收到 `ping` → `Close(4002)` |
| **重连** | `onclose` 30 s 退避重试 | 保留会话 ID，支持断点续传 |
| **分片** | 大于 64 KB 的 Blob 需手动分片发送 | 按序号重组，超时丢弃 |

---

## 4. Go 后端流处理
<a name="Go-后端处理"></a>

### Diagram 4：消息路由与流缓冲
```ascii
+-------------------+     +--------------------+     +-------------------+
| Message Router    | --> | Stream Processing  | --> | AI Engine Router  |
| Types/Formats     |     | Buffer Management  |     | Forward Streams   |
+-------------------+     +--------------------+     +-------------------+
          |                         |                          |
          v                         v                          v
+-------------------+     +--------------------+     +-------------------+
| Client Response   |     | Session Storage    |     | Metrics/Logging   |
| Results/Feedback  |     | State Management   |     | Performance Data  |
+-------------------+     +--------------------+     +-------------------+
```

### 核心实现步骤
1. **类型路由**：
```go
switch pkt.Type {       // "v"|"a"|"cmd"
case "v": handleVideo(pkt)
case "a": handleAudio(pkt)
case "cmd": handleCmd(pkt)
}
```
2. **缓冲池**：使用 `sync.Pool` 降低 GC 压力，按会话维护环形缓冲区。
3. **预处理管道（可选）**：降噪、降采样、H.264 封装等。
4. **转发至 AI**：gRPC/HTTP2 按需推流，支持批处理推理。
5. **结果回写**：将 AI 返回 JSON 直接 `ws.WriteJSON()` 推送前端。
6. **指标埋点**：Prometheus `Histogram` + `Summary` 监控帧延迟、QPS。

---

## 5. 横向扩展与生产部署
<a name="横向扩展与生产部署"></a>

### Diagram 5：多实例与监控
```ascii
+----------------+     +----------------+     +----------------+
| Load Balancer  | --> | Go Instance 1  |     | Redis PubSub   |
| (Caddy/Nginx)  |     | WebSockets     | <-> | Instance Comm  |
+----------------+     +----------------+     +----------------+
        |                      |                      |
        v                      v                      v
+----------------+     +----------------+     +----------------+
| Go Instance 2  |     | Go Instance 3  |     | Monitoring     |
| WebSockets     | <-> | WebSockets     |     | Prometheus/    |
+----------------+     +----------------+     | Grafana        |
                                              +----------------+
```

**关键实践**
- **Sticky Session**：Nginx `ip_hash` or Caddy `lb_policy header`，保证同一用户固定到同一实例。
- **消息广播**：Redis Pub/Sub 或 NATS 进行跨实例指令同步（如全局静音）。
- **文件存储**：长视频存 S3/MinIO，临时缓存用 Redis Stream（30 min TTL）。
- **CI/CD**：GitHub Actions → Docker → Caddy 自动热重载。

---

## 6. 开发约定与规范
<a name="开发约定与规范"></a>

| 类别 | 约定 |
|------|------|
| **代码风格** | 前端遵循 ESLint + Prettier，后端使用 `goimports` + `golangci‑lint` |
| **错误码** | `4xxx` 连接级，`2xxx` 消息级；详见 `/internal/errors.go` |
| **日志** | `zap` 分级：DEBUG→采集细节；INFO→连接事件；WARN→网络抖动；ERROR→业务异常 |
| **环境变量** | `WS_ORIGIN_ALLOW`, `JWT_SECRET`, `AI_ENDPOINT`, `REDIS_URL` |
| **测试** | 前端 `jest` + `vitest`; 后端 `go test -cover`; CI 阶段阈值 ≥ 80% |

---

## 7. 参考链接
<a name="参考链接"></a>

- MDN：[`getUserMedia`](https://developer.mozilla.org/zh-CN/docs/Web/API/MediaDevices/getUserMedia)
- RFC 6455：WebSocket Protocol
- Google WebCodecs / WebTransport 草案
- Go 标准库：`net/http`, `x/net/websocket`
- Prometheus 官网 & Grafana Dashboard 13669（WebSocket 监控模板）

---

> **下一步：**
> 1. 后端 PoC (`ws://localhost:8080/ws`) ✅
> 2. 集成 JWT 鉴权 ⚙️
> 3. 接入 AI Engine (gRPC) 🧠
>
> 👉 请各模块负责人于 **4 月 28 日 18:00 JST** 前提交初版 PR，届时进行线上评审。

---

> **编者：** GPT‑DevOps Bot 


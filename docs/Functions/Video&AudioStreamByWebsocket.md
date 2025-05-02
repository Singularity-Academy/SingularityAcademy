# CourseInteractionPage.tsx 开发文档

## 1. 页面主要功能概述

该页面为"课程互动"核心页面，主要实现以下功能：

- **学习资料上传**：支持拖拽或点击上传多种格式的学习资料（PDF、Word、PPT、图片、视频等），并显示上传进度。
- **资源链接管理**：允许用户添加、删除外部学习资源链接。
- **摄像头与麦克风实时推流**：用户可开启/关闭摄像头和麦克风，将音视频流通过 WebSocket 实时推送到后端 AI 教师。
- **AI 聊天互动**：支持与 AI 教师实时文本对话，消息通过 WebSocket 实时收发，并支持语音播报 AI 回复。
- **全屏切换**：主课程内容区支持全屏显示。
- **会话消息区**：展示用户与 AI 教师的所有对话消息。

## 2. 主要实现方法

### 2.1 状态管理

- 使用 React `useState` 管理消息、输入框、上传文件、进度、摄像头/麦克风状态等。
- 使用 `useRef` 管理 WebSocket 实例、视频 DOM、材料引用等。

### 2.2 文件上传

- 通过 `react-dropzone` 实现拖拽上传。
- 上传接口：`POST /api/courses/materials`
- 上传成功后，后端返回文件名，前端通过 `materialRef.current` 记录。
- 上传进度通过 `onUploadProgress` 实时更新。

### 2.3 资源链接管理

- 用户可通过弹窗输入资源链接，前端校验 URL 合法性后加入列表。
- 支持删除已添加的链接。

### 2.4.1 音频采集与推送

#### 主要函数：`startAudio`

- **功能**：调用浏览器的 `navigator.mediaDevices.getUserMedia({ audio: true })` 获取音频流，利用 `MediaRecorder` 定时采集音频片段，并通过 WebSocket 实时推送到后端。
- **实现细节**：
  - 获取音频流后，保存到 `audioStream` 状态。
  - 创建 `MediaRecorder`，监听 `ondataavailable` 事件，每500ms采集一次音频片段。
  - 采集到的音频片段通过 `FileReader` 转为 ArrayBuffer，随后通过 WebSocket 发送。
  - 若 WebSocket 未连接，则不会发送数据。
  - 错误处理：若获取音频流失败，通过 `toast` 弹窗提示错误。

#### 关键代码片段

```typescript
const startAudio = () => {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then((stream) => {
      setAudioStream(stream);
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = (event) => {
        if (websocketRef.current?.readyState !== WebSocket.OPEN) return;
        const audioBlob = event.data;
        const reader = new FileReader();
        reader.onloadend = () => {
          const buffer = reader.result;
          websocketRef.current?.send(buffer || "")
        };
        reader.readAsArrayBuffer(audioBlob);
      };
      mediaRecorder.start(500);  // 每500ms采集一次
    })
    .catch((error) => toast({
      title: "error accessing media devices",
      description: error,
      status: 'error',
      duration: 3000,
    }));
};
```

### 2.4.2 视频采集与本地预览

#### 主要函数：`startVideo`

- **功能**：调用 `navigator.mediaDevices.getUserMedia({ video: true })` 获取视频流，将其赋值给 `<video>` 组件用于本地预览，并为每个 track 添加 onended 监听。
- **实现细节**：
  - 获取到视频流后，赋值给 `studentVideoRef.current.srcObject`，实现本地预览。
  - 通过 `setVideoStream` 保存流对象到状态。
  - 为每个 track 添加 `onended` 事件监听，便于调试流的生命周期。
  - 通过定时器每2秒输出一次当前 video 的 srcObject，辅助调试。
  - 错误处理：获取失败时弹窗提示。

#### 关键代码片段

```typescript
const startVideo = () => {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      if (studentVideoRef.current) {
        studentVideoRef.current.srcObject = stream;
        console.log("[startVideo] studentVideoRef.current.srcObject:", studentVideoRef.current.srcObject);
        setInterval(() => {
          if (studentVideoRef.current) {
            console.log("[monitor] studentVideoRef.current.srcObject:", studentVideoRef.current.srcObject);
          }
        }, 2000);
      } else {
        console.warn("[startVideo] studentVideoRef.current 不存在");
      }
      setVideoStream(stream);
      stream.getTracks().forEach(track => {
        track.onended = () => {
          console.warn("[monitor] videoStream track ended:", track);
        };
      });
      return stream;
    })
    .catch((error) => toast({
      title: "error accessing media devices",
      description: error,
      status: 'error',
      duration: 3000,
    }));
};
```

### 2.5 WebSocket连接与视频帧推送

#### 主要函数：`connectWebSocket`

- **功能**：建立与后端的 WebSocket 连接，推送音视频流数据，并接收 AI 教师的消息。
- **实现细节**：
  - 调用 `startVideo()` 和 `startAudio()` 开始采集音视频流。
  - 创建 WebSocket 连接，连接地址为 `ws://localhost:8080/api/ws/stream?token=xxx`。
  - 连接成功后，定时（每200ms）从 `<video>` 组件抓取一帧画面，压缩为 JPEG 并通过 WebSocket 发送到后端。
    - 通过 `canvas.drawImage` 抓取画面，`canvas.toBlob` 压缩为 JPEG。
    - 发送前判断 WebSocket 是否处于 OPEN 状态。
  - 通过 setInterval 监控 `sendingVideoTask.current` 是否持续运行，辅助调试。
  - 接收到后端消息后，解析 JSON，更新消息区，并支持语音播报。
  - 连接关闭时，自动调用 `disconnectWebSocket` 进行清理。

#### 关键代码片段

```typescript
const connectWebSocket = () => {
  if (websocketRef.current) return;
  startVideo();
  startAudio();
  setConnecting(true);
  const video = studentVideoRef.current;
  // 代码块太长，此处省略...
};
```

### 2.6 聊天消息管理

- 所有消息通过 `messages` 状态管理，自动滚动到底部。
- 用户消息和 AI 消息样式区分。

### 2.7 认证校验

- 页面加载时校验 Cookie 中是否有 token，无则跳转登录页。

## 3. 主要接口说明

### 3.1 文件上传接口

- **URL**：`/api/courses/materials`
- **方法**：POST
- **请求体**：`FormData`，字段名为 `materials`
- **需带 Token**：是
- **响应示例**：

```json
{
  "message": "uploadSuccessfully",
  "file": "550707222846377484$quadratic function.docx"
}
```

- **用途**：上传学习资料，返回后端存储的文件名。

### 3.2 WebSocket 实时推流接口

- **URL**：`/api/ws/stream?token=<token>`
- **方法**：WebSocket
- **需带 Token**：是
- **发送内容**：
  - 视频帧（JPEG 二进制）
  - 音频片段（二进制）
  - 文本消息（字符串）
- **接收内容**：
  - AI 教师回复（JSON，含 message、manim_script、notes 等）
- **用途**：实现音视频与文本的实时互动。

### 3.3 认证相关接口

- **/api/auth/login**：登录，获取 token
- **/api/auth/register**：注册
- **/api/auth/verify**：邮箱验证
- **/api/me**：获取当前用户信息（需 token）

### 3.4 其他接口

- **/api/courses/list**：课程列表
- **/api/courses/detail/:id**：课程详情

## 4. 关键代码结构说明

- **文件上传**：`handleFileUpload` 方法，调用 `axiosInstance.post(API_ENDPOINTS.COURSE.MATERIALS, formData, ...)`
- **WebSocket 连接**：`connectWebSocket` 方法，管理音视频流采集与推送、消息收发
- **摄像头/麦克风控制**：`startVideo`、`startAudio`、`stopVideo`、`stopAudio`
- **消息发送**：`handleSubmit` 方法，文本消息通过 WebSocket 发送
- **UI 组件**：使用 Chakra UI 组件库实现响应式布局与交互

## 5. 交互流程示意

1. 用户进入页面，校验 token，未登录则跳转登录页。
2. 用户可上传学习资料，资料上传后文件名存储于 `materialRef`。
3. 用户可添加/删除外部资源链接。
4. 用户点击"Turn On"按钮，开启摄像头与麦克风，建立 WebSocket 连接，开始推流。
5. 用户可与 AI 教师进行文本对话，消息通过 WebSocket 实时收发。
6. AI 教师回复自动语音播报，消息区实时展示。
7. 用户可随时关闭摄像头/麦克风，断开 WebSocket 连接。

## 6. 相关参考资料

- frontend/src/pages/course/CourseInteractionPage.tsx
- frontend/src/config/api.ts
- backend/README.md
- backend/ws/stream.go

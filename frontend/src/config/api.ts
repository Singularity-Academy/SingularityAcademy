// 配置 API 和 Socket IO 的基本 URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:1298/api';

// API 接口路径
export const API_ENDPOINTS = {
  ME: `${API_BASE_URL}/me`,
  AUTH: {
    LOGIN: `${API_BASE_URL}/auth/login`,
    REGISTER: `${API_BASE_URL}/auth/register`,
    LOGOUT: `${API_BASE_URL}/auth/logout`,
    VERIFY: `${API_BASE_URL}/auth/verify`,
  },
  COURSE: {
    LIST: `${API_BASE_URL}/courses`,
    DETAIL: (id: string) => `${API_BASE_URL}/courses/${id}`,
    INTERACT: `${API_BASE_URL}/courses/interact`,
  },
  // 注意这里改为 WebSocket 地址，用于连接命名空间
  WS: {
    STREAM: `${API_BASE_URL}/ws/stream`
  }
};

// Axios 配置
export const axiosConfig = {
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
};

// 错误响应接口
export interface ErrorResponse {
  error: string;
  detail: string;
}

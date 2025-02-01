// 配置 API 和 Websocket 的基本 URL
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

// API 接口路径
export const API_ENDPOINTS = {
  ME: `/me`,
  AUTH: {
    LOGIN: `/auth/login`,
    REGISTER: `/auth/register`,
    LOGOUT: `/auth/logout`,
    VERIFY: `/auth/verify`,
  },
  COURSE: {
    LIST: `/courses`,
    DETAIL: (id: string) => `/courses/${id}`,
    INTERACT: `/courses/interact`,
  },
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

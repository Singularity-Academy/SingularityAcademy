const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:1298/api';

export const API_ENDPOINTS = {
  ME: `${API_BASE_URL}/me`,
  AUTH: {
    LOGIN: `${API_BASE_URL}/auth/login`,
    REGISTER: `${API_BASE_URL}/auth/register`,
    LOGOUT: `${API_BASE_URL}/auth/logout`,
  },
  COURSE: {
    LIST: `${API_BASE_URL}/courses`,
    DETAIL: (id: string) => `${API_BASE_URL}/courses/${id}`,
    INTERACT: `${API_BASE_URL}/courses/interact`,
  }
};

export const axiosConfig = {
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
};

export interface ErrorResponse {
  error: string;
  detail: string;
}

import axios, {AxiosError} from 'axios';
import {axiosConfig, ErrorResponse} from '../config/api';
import Cookies from "js-cookie";

const axiosInstance = axios.create(axiosConfig);

// Request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const token = Cookies.get('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status !== 401) return Promise.reject(error)
    const err = error as AxiosError<ErrorResponse>;
    if (err.response?.data?.error !== "Invalid token") return Promise.reject(err);
    Cookies.remove('token');
    window.location.href = '/login';
  }
);

export default axiosInstance;

export function getToastMessage(error: AxiosError<ErrorResponse>) {
    const message: { title: string; description: string; status: 'info' | 'warning' | 'success' | 'error' | 'loading'; duration: number } = {
        title: error.response?.data?.error || "Login failed",
        description: '',
        status: 'error',
        duration: 3000,
    }
    if (error.response?.data?.error != error.response?.data?.detail){
        message.description = error.response?.data?.detail || "Please try again later."
    }
    return message;
}
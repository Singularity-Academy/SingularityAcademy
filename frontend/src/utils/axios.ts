import axios, {AxiosError} from 'axios';
import {API_ENDPOINTS, axiosConfig, ErrorResponse} from '../config/api';
import Cookies from "js-cookie";
import {useToast} from "@chakra-ui/react";
import {useNavigate} from "react-router-dom";

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
    if (err.response?.data?.error !== "Invalid token" && err.response?.data?.error !== "Authorization header is required") return Promise.reject(err);
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

export async function getUserData(toast: (arg0: { title: string; description: string; status: "info" | "warning" | "success" | "error" | "loading"; duration: number; }) => void, navigate: (arg0: string) => void) {
    if (!Cookies.get('token')) {
        navigate('/login'); // 没有 token，跳转到登录页面
        return null;  // Token 不存在时，直接返回 null
    }

    let User = null;
    const cachedUser = localStorage.getItem('user');
    if (cachedUser) {
        User = JSON.parse(cachedUser);
    }
    else {
        try {
            const response = await axiosInstance.get(API_ENDPOINTS.ME);
            User = response.data;
            localStorage.setItem('user', JSON.stringify(response.data)); // 更新缓存
            console.log(User);
        } catch (err) {
            const error = err as AxiosError<ErrorResponse>;
            toast(getToastMessage(error));
        }
    }

    return User;  // 如果获取失败，返回 null
}

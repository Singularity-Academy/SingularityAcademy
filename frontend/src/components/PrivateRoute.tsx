import React, { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import Cookies from 'js-cookie';
import { Box, Center, Spinner } from '@chakra-ui/react';

/**
 * PrivateRoute 组件用于保护需要身份验证的路由
 * 它检查 token 是否存在，如果没有找到则重定向到登录页面
 */
const PrivateRoute = () => {
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // 简单检查 token 是否存在
    const token = Cookies.get('token');
    setIsAuthenticated(!!token);
    setIsCheckingAuth(false);
  }, []);

  if (isCheckingAuth) {
    return (
      <Center h="100vh">
        <Spinner size="xl" color="blue.500" />
      </Center>
    );
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

export default PrivateRoute; 
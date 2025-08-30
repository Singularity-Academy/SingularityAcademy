import React, { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import Cookies from 'js-cookie';
import { Box, Center, Spinner } from '@chakra-ui/react';

/**
 * PrivateRoute component to protect routes that require authentication
 * It checks for token existence and redirects to login if not found
 */
const PrivateRoute = () => {
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Simple check for token existence
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
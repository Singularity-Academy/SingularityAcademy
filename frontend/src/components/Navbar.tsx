import React, { useEffect, useState } from 'react';
import { Box, Flex, Button, HStack, Avatar, Menu, MenuButton, MenuList, MenuItem, useColorModeValue } from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import axiosInstance from "../utils/axios";
import { API_ENDPOINTS } from "../config/api";

const Navbar: React.FC = () => {
  const [userName, setUserName] = useState<string | null>(null);
  const navigate = useNavigate();
  const bgColor = useColorModeValue('white', 'gray.800');
  const token = Cookies.get('token'); // 获取当前的 token

  const handleLogout = () => {
    Cookies.remove('token');
    localStorage.removeItem('userName'); // 清除缓存
    navigate('/login');
  };

  useEffect(() => {
    const cachedUserName = localStorage.getItem('userName'); // 获取缓存的用户名
    if (token) {  // 如果存在 token
      if (cachedUserName) {
        setUserName(cachedUserName); // 如果缓存中有用户名，则直接使用缓存的用户名
      } else {
        // 如果没有缓存的用户名，则发请求获取并缓存
        axiosInstance.get(API_ENDPOINTS.ME)
            .then((response) => {
              const name = response.data.name;
              setUserName(name);
              localStorage.setItem('userName', name); // 缓存用户名
            })
            .catch((error) => {
              console.error(error);
            });
      }
    } else {
      // 如果没有 token，则说明用户已经退出，清除缓存并跳转到登录页面
      localStorage.removeItem('userName');
      setUserName(null); // 清除用户信息
    }
  }, [token]); // 监听 token 的变化

  return (
      <Box bg={bgColor} px={4} boxShadow="sm" position="fixed" width="100%" zIndex={100} top={0}>
        <Flex h={16} alignItems="center" justifyContent="space-between">
          <HStack spacing={8} alignItems="center">
            <Button variant="ghost" onClick={() => navigate('/')}>
              AI Online School
            </Button>
          </HStack>

          <HStack spacing={4}>
            {token ? (
                <>
                  <Button variant="ghost" onClick={() => navigate('/me/homepage')}>
                    Dashboard
                  </Button>
                  <Menu>
                    <MenuButton>
                      <Avatar size="sm" name={userName || "User"} />
                    </MenuButton>
                    <MenuList>
                      <MenuItem onClick={() => navigate('/homepage')}>Profile</MenuItem>
                      <MenuItem onClick={handleLogout}>Logout</MenuItem>
                    </MenuList>
                  </Menu>
                </>
            ) : (
                <Button variant="ghost" onClick={() => navigate('/login')}>
                  Login
                </Button>
            )}
          </HStack>
        </Flex>
      </Box>
  );
};

export default Navbar;

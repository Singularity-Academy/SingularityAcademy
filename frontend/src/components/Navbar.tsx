import React, { useEffect, useState } from 'react';  // 引入 useState 和 useEffect
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Flex,
  Button,
  HStack,
  useColorModeValue,
  Avatar,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Spinner,  // 引入 Spinner 组件
} from '@chakra-ui/react';
import Cookies from 'js-cookie';
import axiosInstance from "../utils/axios";
import { API_ENDPOINTS } from "../config/api";

interface NavbarProps {}

const Navbar: React.FC<NavbarProps> = () => {
  const navigate = useNavigate();
  const bgColor = useColorModeValue('white', 'gray.800');
  const token = Cookies.get('token');

  const [name, setName] = useState('');  // 使用 useState 存储 name
  const [loading, setLoading] = useState(true);  // 新增 loading 状态

  const handleLogout = () => {
    Cookies.remove('token');
    navigate('/login');
  };

  useEffect(() => {
    if (token) {  // 只有在有 token 时才发送请求
      setLoading(true);  // 开始加载
      axiosInstance.get(API_ENDPOINTS.ME).then((response) => {
        setName(response.data.name);  // 设置用户名
        setLoading(false);  // 请求完成，设置 loading 为 false
      }).catch(() => {
        setLoading(false);  // 如果请求失败，设置 loading 为 false
      });
    }
  }, [token]);  // 如果 token 发生变化，重新执行请求

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
                      {loading ? (
                          <Spinner size="sm" />  // 如果正在加载，显示 Spinner
                      ) : (
                          <Avatar size="sm" name={name || "User"} />  // 否则显示头像
                      )}
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

import React, { useEffect, useState } from 'react';
import {
    Box,
    Flex,
    Button,
    HStack,
    Avatar,
    Menu,
    MenuButton,
    MenuList,
    MenuItem,
    useColorModeValue,
    useToast,
    Spinner // 引入 Spinner 组件
} from '@chakra-ui/react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import axiosInstance, {getToastMessage, getUserData} from "../utils/axios";
import { API_ENDPOINTS, ErrorResponse } from "../config/api";
import { AxiosError } from "axios";

const Navbar: React.FC = () => {
    const [user, setUser] = useState<{ id: number; name: string; email: string } | null>(null);
    const [loading, setLoading] = useState(true); // 加载状态
    const toast = useToast();
    const navigate = useNavigate();
    const bgColor = useColorModeValue('white', 'gray.800');
    const token = Cookies.get('token'); // 获取当前的 token

    useEffect(() => {
        const fetchData = async () => {
            if (!Cookies.get('token')) {
                localStorage.removeItem('user');
                return;
            }

            setLoading(true);
            const User = await getUserData(toast, navigate);  // 使用 await 获取用户数据
            if (User) {
                setUser(User);
            }
            setLoading(false);
        };

        fetchData();
    }, []);
    // 如果 token 或 navigate 变化时重新执行

    const handleLogout = () => {
        Cookies.remove('token');
        localStorage.removeItem('user'); // 清除缓存
        navigate("/login")
    };

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
                    !loading ? ( // 如果加载完成，显示正常内容
                        <>
                            <Button variant="ghost" onClick={() => navigate('/me/homepage')}>
                                Dashboard
                            </Button>
                            <Menu>
                                <MenuButton>
                                    <Avatar size="sm" name={(user || { name: 'User' }).name} />
                                </MenuButton>
                                <MenuList>
                                    <MenuItem fontWeight={'bold'} cursor={'default'} background={'none'}>
                                        {(user || { name: 'User' }).name}
                                    </MenuItem>
                                    <MenuItem onClick={() => navigate('/homepage')}>Profile</MenuItem>
                                    <MenuItem onClick={handleLogout}>Logout</MenuItem>
                                </MenuList>
                            </Menu>
                        </>
                    ) : (
                        // 如果正在加载，显示一个旋转的 Spinner
                        <Spinner size="sm" />
                    )) : (<Button variant="ghost" onClick={() => navigate('/login')}>
                    Sing In
                </Button>)}
                </HStack>
            </Flex>
        </Box>
    );
};

export default Navbar;

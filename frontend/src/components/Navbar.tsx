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
    useColorMode, // 导入 useColorMode hook
    useToast,
    Spinner,
    IconButton // 导入 IconButton 用于主题切换按钮
} from '@chakra-ui/react';
import { FaMoon, FaSun } from 'react-icons/fa'; // 导入太阳和月亮图标
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import {getUserData} from "@utils/axios";

const Navbar: React.FC = () => {
    const [user, setUser] = useState<{ id: number; name: string; email: string } | null>(null);
    const [loading, setLoading] = useState(true);
    const toast = useToast();
    const navigate = useNavigate();
    const bgColor = useColorModeValue('white', 'gray.800');
    const token = Cookies.get('token');
    const { colorMode, toggleColorMode } = useColorMode(); // 获取当前主题并提供切换功能

    useEffect(() => {
        const fetchData = async () => {
            if (!Cookies.get('token')) {
                localStorage.removeItem('user');
                return;
            }

            setLoading(true);
            const User = await getUserData(toast, navigate);
            if (User) {
                setUser(User);
            }
            setLoading(false);
        };

        fetchData();
    }, []);

    const handleLogout = () => {
        Cookies.remove('token');
        localStorage.removeItem('user');
        navigate("/login");
    };

    return (
        <Box bg={bgColor} px={4} borderBottomWidth={1} boxShadow="sm" position="fixed" width="100%" zIndex={100} top={0}>
            <Flex h={16} alignItems="center" justifyContent="space-between">
                <HStack spacing={8} alignItems="center">
                    <Button variant="ghost" onClick={() => navigate('/')}>
                        AI Online School
                    </Button>
                </HStack>

                <HStack spacing={4}>
                    {token ? (
                        !loading ? (
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
                            <Spinner size="sm" />
                        )) : (
                        <Button variant="ghost" onClick={() => navigate('/login')}>
                            Sign In
                        </Button>
                    )}

                    {/* 添加切换主题按钮 */}
                    <IconButton
                        icon={colorMode === 'light' ? <FaMoon /> : <FaSun />} // 根据当前模式切换图标
                        aria-label="Toggle theme"
                        onClick={toggleColorMode} // 切换主题
                        variant="ghost"
                    />
                </HStack>
            </Flex>
        </Box>
    );
};

export default Navbar;

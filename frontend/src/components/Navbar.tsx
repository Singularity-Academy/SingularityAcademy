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
    useColorMode,
    useToast,
    Spinner,
    IconButton,
    useMediaQuery // ✅ 改用 useMediaQuery
} from '@chakra-ui/react';
import {FaMoon, FaSun, FaBars, FaGlobe} from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { getUserData } from "@utils/axios";
import { useTranslation } from "react-i18next";

const Navbar: React.FC = () => {
    const [user, setUser] = useState<{ id: number; name: string; email: string } | null>(null);
    const [loading, setLoading] = useState(true);
    const toast = useToast();
    const navigate = useNavigate();
    const bgColor = useColorModeValue('white', 'gray.800');
    const token = Cookies.get('token');
    const { colorMode, toggleColorMode } = useColorMode();
    const { t, i18n } = useTranslation();
    const [isMobile] = useMediaQuery("(max-width: 768px)"); // ✅ 改用 useMediaQuery 更稳定

    useEffect(() => {
        const fetchData = async () => {
            if (!token) {
                localStorage.removeItem('user');
                setUser(null);
                return;
            }
            setLoading(true);
            const User = await getUserData(toast, navigate);
            if (User) setUser(User);
            setLoading(false);
        };

        fetchData();
    }, [token, toast, navigate]);

    const handleLogout = () => {
        Cookies.remove('token');
        localStorage.removeItem('user');
        setUser(null);
        navigate("/login");
    };

    const toggleLanguage = () => {
        const newLanguage = i18n.language === 'en' ? 'zh' : 'en';
        i18n.changeLanguage(newLanguage);
    };

    return (
        <Box
            bg={bgColor}
            px={4}
            borderBottomWidth={1}
            boxShadow="sm"
            position="fixed"
            width="100%"
            zIndex={100}
            top={0}
        >
            <Flex h={16} alignItems="center" justifyContent="space-between">
                {/* 网站标题 */}
                <Button variant="ghost" fontSize={{ base: "sm", md: "lg" }} onClick={() => navigate('/')}>
                    AI Online School
                </Button>

                {/* 右侧内容：手机端用 Menu，下拉显示 */}
                {isMobile ? (
                    <Menu>
                        <MenuButton as={Box}>
                            {token ? (
                                <Avatar size="sm" name={user?.name || 'User'} />
                            ) : (
                                <IconButton icon={<FaBars />} aria-label="Open menu" variant="ghost" />
                            )}
                        </MenuButton>
                        <MenuList>
                            {token ? (
                                <>
                                    {/* 显示用户名 */}
                                    <MenuItem isDisabled fontWeight="bold">{user?.name || 'User'}</MenuItem>
                                    <MenuItem onClick={() => navigate('/me/homepage')}>{t('Navbar.dashboard')}</MenuItem>
                                    <MenuItem onClick={() => navigate('/homepage')}>{t('Navbar.profile')}</MenuItem>
                                    <MenuItem onClick={handleLogout}>{t('Navbar.logout')}</MenuItem>
                                </>
                            ) : (
                                <MenuItem onClick={() => navigate('/login')}>{t('common.signIn')}</MenuItem>
                            )}
                            <MenuItem onClick={toggleColorMode} icon={colorMode === 'light' ? <FaMoon /> : <FaSun />}>
                                {colorMode === 'light' ? t('Navbar.darkMode') : t('Navbar.lightMode')}
                            </MenuItem>
                            <MenuItem onClick={toggleLanguage} icon={<FaGlobe />}>
                                {i18n.language === 'en' ? '中文' : 'English'}
                            </MenuItem>
                        </MenuList>
                    </Menu>
                )
                : (
                    // 桌面端显示按钮
                    <HStack spacing={4}>
                        {token ? (
                            !loading ? (
                                <>
                                    <Button variant="ghost" onClick={() => navigate('/me/homepage')}>
                                        {t('Navbar.dashboard')}
                                    </Button>
                                    <Menu>
                                        <MenuButton>
                                            <Avatar size="sm" name={user?.name || 'User'} />
                                        </MenuButton>
                                        <MenuList>
                                            <MenuItem isDisabled>{user?.name || 'User'}</MenuItem>
                                            <MenuItem onClick={() => navigate('/homepage')}>{t('Navbar.profile')}</MenuItem>
                                            <MenuItem onClick={handleLogout}>{t('Navbar.logout')}</MenuItem>
                                        </MenuList>
                                    </Menu>
                                </>
                            ) : (
                                <Spinner size="sm" />
                            )
                        ) : (
                            <Button variant="ghost" onClick={() => navigate('/login')}>
                                {t('common.signIn')}
                            </Button>
                        )}

                        {/* 主题切换按钮 */}
                        <IconButton
                            icon={colorMode === 'light' ? <FaMoon /> : <FaSun />}
                            aria-label={colorMode === 'light' ? "Switch to dark mode" : "Switch to light mode"}
                            onClick={toggleColorMode}
                            variant="ghost"
                        />

                        {/* 语言切换按钮 */}
                        <Button variant="ghost" onClick={toggleLanguage}>
                            {i18n.language === 'en' ? '中' : 'EN'}
                        </Button>
                    </HStack>
                )}
            </Flex>
        </Box>
    );
};

export default Navbar;

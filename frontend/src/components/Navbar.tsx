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
import { ChevronDownIcon } from '@chakra-ui/icons';

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
        const languages = ['en', 'es', 'fr', 'de', 'ja', 'ar', 'zh', 'zh_CN'];
        const currentIndex = languages.indexOf(i18n.language);
        const nextLanguage = currentIndex === -1 ? 'en' : languages[(currentIndex + 1) % languages.length];
        i18n.changeLanguage(nextLanguage);
    };

    const LANGUAGE_NAMES = {
        en: 'English',
        es: 'Español',
        fr: 'Français',
        de: 'Deutsch',
        ja: '日本語',
        ar: 'العربية',
        zh: '中文(简体)',
        zh_CN: '中文(繁體)'
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
                    Calrif AI 知澜

                </Button> 

                {/* 右侧内容：手机端用 Menu，下拉显示 */}
                {isMobile ? (
                    <Menu>
                        <MenuButton as={Box}>
                            {token ? (
                                <Avatar size="sm" name={user?.name || '用户'} />
                            ) : (
                                <IconButton icon={<FaBars />} aria-label="打开菜单" variant="ghost" />
                            )}
                        </MenuButton>
                        <MenuList>
                            {token ? (
                                <>
                                    {/* 显示用户名 */}
                                    <MenuItem isDisabled fontWeight="bold">{user?.name || '用户'}</MenuItem>
                                    <MenuItem onClick={() => navigate('/me/homepage')}>仪表板</MenuItem>
                                    <MenuItem onClick={() => navigate('/homepage')}>个人资料</MenuItem>
                                    <MenuItem onClick={handleLogout}>退出登录</MenuItem>
                                </>
                            ) : (
                                <MenuItem onClick={() => navigate('/login')}>登录</MenuItem>
                            )}
                            <MenuItem onClick={toggleColorMode} icon={colorMode === 'light' ? <FaMoon /> : <FaSun />}>
                                {colorMode === 'light' ? '深色模式' : '浅色模式'}
                            </MenuItem>
                            <Menu>
                                <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
                                    {LANGUAGE_NAMES[i18n.language as keyof typeof LANGUAGE_NAMES]}
                                </MenuButton>
                                <MenuList>
                                    {['en', 'es', 'fr', 'de', 'ja', 'ar', 'zh', 'zh_CN'].map((lang) => (
                                        <MenuItem key={lang} onClick={() => i18n.changeLanguage(lang)}>
                                            {LANGUAGE_NAMES[lang as keyof typeof LANGUAGE_NAMES]}
                                        </MenuItem>
                                    ))}
                                </MenuList>
                            </Menu>
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
                                        仪表板
                                    </Button>
                                    <Menu>
                                        <MenuButton>
                                            <Avatar size="sm" name={user?.name || '用户'} />
                                        </MenuButton>
                                        <MenuList>
                                            <MenuItem isDisabled>{user?.name || '用户'}</MenuItem>
                                            <MenuItem onClick={() => navigate('/homepage')}>个人资料</MenuItem>
                                            <MenuItem onClick={handleLogout}>退出登录</MenuItem>
                                        </MenuList>
                                    </Menu>
                                </>
                            ) : (
                                <Spinner size="sm" />
                            )
                        ) : (
                            <Button variant="ghost" onClick={() => navigate('/login')}>
                                登录
                            </Button>
                        )}

                        {/* 主题切换按钮 */}
                        <IconButton
                            icon={colorMode === 'light' ? <FaMoon /> : <FaSun />}
                            aria-label={colorMode === 'light' ? "切换到深色模式" : "切换到浅色模式"}
                            onClick={toggleColorMode}
                            variant="ghost"
                        />

                        {/* 语言切换按钮 */}
                        <Menu>
                            <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
                                {LANGUAGE_NAMES[i18n.language as keyof typeof LANGUAGE_NAMES]}
                            </MenuButton>
                            <MenuList>
                                {['en', 'es', 'fr', 'de', 'ja', 'ar', 'zh', 'zh_CN'].map((lang) => (
                                    <MenuItem key={lang} onClick={() => i18n.changeLanguage(lang)}>
                                        {LANGUAGE_NAMES[lang as keyof typeof LANGUAGE_NAMES]}
                                    </MenuItem>
                                ))}
                            </MenuList>
                        </Menu>
                    </HStack>
                )}
            </Flex>
        </Box>
    );
};

export default Navbar;

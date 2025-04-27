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
                            <Button
                              bg="background.secondary"
                              color="black"
                              _hover={{
                                textDecoration: 'underline'
                              }}
                        onClick={() => navigate('/login')}
                            >
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

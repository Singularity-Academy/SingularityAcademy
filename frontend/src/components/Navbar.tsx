import React from 'react';
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
} from '@chakra-ui/react';
import Cookies from 'js-cookie';

interface NavbarProps {}

const Navbar: React.FC<NavbarProps> = () => {
  const navigate = useNavigate();
  const bgColor = useColorModeValue('white', 'gray.800');
  const token = Cookies.get('token');

  const handleLogout = () => {
    Cookies.remove('token');
    navigate('/login');
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
                <>
                  <Button variant="ghost" onClick={() => navigate('/me/homepage')}>
                    Dashboard
                  </Button>
                  <Menu>
                    <MenuButton>
                      <Avatar size="sm" />
                    </MenuButton>
                    <MenuList>
                      <MenuItem onClick={() => navigate('/me/homepage')}>Profile</MenuItem>
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

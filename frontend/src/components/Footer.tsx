import { Box, Grid, GridItem, Link, Text, Flex, Icon, useColorModeValue } from '@chakra-ui/react';
import { ExternalLinkIcon } from '@chakra-ui/icons';

const Footer = () => {
  const linkColor = useColorModeValue('blue.600', 'blue.200');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const hoverBg = useColorModeValue('blue.50', 'gray.700');
  const iconColor = useColorModeValue('blue.500', 'blue.300');

  const chrisLinks = [
    { name: 'ClickMood', url: 'http://clickmood.krymusic.top/' },
    { name: 'Studio', url: 'http://studio.krypoto.top/' },
    { name: 'Photography', url: 'http://photograph.krypoto.top/' },
    { name: 'Blog', url: 'https://chrisdsasa.github.io/' },
    { name: 'Twitter', url: 'https://x.com/KrypotoZ', icon: ExternalLinkIcon }
  ];

  return (
    <Box 
      as="footer" 
      bgGradient={useColorModeValue(
        'linear(to-t, blue.50 0%, white 50%)',
        'linear(to-t, gray.800 0%, gray.900 50%)'
      )}
      borderTopWidth={1}
      borderColor={borderColor}
      mt={16}
      py={12}
      position="relative"
      _before={{
        content: '""',
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: '4px',
        bgGradient: 'linear(to-r, blue.400, purple.400)',
        animation: 'gradientFlow 3s ease infinite'
      }}
    >
      <style>
        {`
          @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
          }
        `}
      </style>

      <Grid 
        templateColumns={{ base: '1fr', md: '2fr repeat(4, 1fr)' }}
        gap={12}
        maxW="7xl"
        mx="auto"
        px={8}
      >
        <GridItem>
          <Text 
            fontSize="2xl" 
            fontWeight="extrabold" 
            mb={4}
            bgGradient="linear(to-r, blue.400, purple.500)"
            bgClip="text"
          >
            创意宇宙建议
          </Text>
          <Text 
            fontSize="lg" 
            color={useColorModeValue('gray.600', 'gray.400')}
            lineHeight="tall"
          >
            探索技术与创意的交汇点。在这些平台上关注我，保持联系。
          </Text>
        </GridItem>

        {chrisLinks.map((link, index) => (
          <GridItem key={index}>
            <Link 
              href={link.url}
              isExternal
              display="block"
              p={3}
              borderRadius="md"
              transition="all 0.2s"
              _hover={{
                transform: 'translateY(-2px)',
                boxShadow: 'lg',
                bg: hoverBg,
                textDecoration: 'none'
              }}
            >
              <Flex align="center">
                {link.icon && (
                  <Icon 
                    as={link.icon} 
                    boxSize={6}
                    mr={3}
                    color={iconColor}
                  />
                )}
                <Text
                  fontSize="lg"
                  fontWeight="medium"
                  color={linkColor}
                >
                  {link.name}
                </Text>
              </Flex>
            </Link>
          </GridItem>
        ))}
      </Grid>
      
      <Flex 
        justify="center" 
        mt={12}
        direction="column" 
        align="center"
      >
        <Text 
          textAlign="center" 
          color={useColorModeValue('gray.600', 'gray.400')}
          fontSize="sm"
          maxW="2xl"
          lineHeight="tall"
        >
          © {new Date().getFullYear()} AI 在线学校。由 KRYPOTO 团队用 ❤️ 精心制作。
          <br />
          感谢贡献者们为全球无障碍教育所做的承诺。
        </Text>
      </Flex>
    </Box>
  );
};

export default Footer;
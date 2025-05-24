import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Heading,
  Text,
  VStack,
  HStack,
  Image,
  SimpleGrid,
  useColorModeValue,
  Avatar,
  Flex,
  Stack,
  Icon,
  useBreakpointValue,
} from '@chakra-ui/react';
import { keyframes } from '@emotion/react';
import { FiArrowRight } from 'react-icons/fi';
import Navbar from '@components/Navbar';
import { useTranslation } from 'react-i18next';
import MImage from '../assets/M.jpg';

interface Feature {
  title: string;
  description: string;
  icon: string;
}

interface Founder {
  name: string;
  role: string;
  bio: string;
  image: string;
}

interface Vision {
  content: string;
  color: string;
}

// Floating animation for hero elements
const float = keyframes`
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
`;

// Fade in animation
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
`;

// Sparkle animation
const sparkle = keyframes`
  0% { transform: scale(0) rotate(0deg); opacity: 0; }
  50% { transform: scale(1) rotate(180deg); opacity: 1; }
  100% { transform: scale(0) rotate(360deg); opacity: 0; }
`;

// Typing cursor blink
const blink = keyframes`
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
`;

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const bgColor = useColorModeValue('#FFE5C4', 'gray.900');
  const buttonBg = useColorModeValue('#F47B4F', '#FFB69B');
  const cardBg = useColorModeValue('white', 'gray.700');
  const { t, i18n, ready } = useTranslation();
  
  const heroHeight = useBreakpointValue({ base: '100vh', md: '100vh' });
  const imageSize = useBreakpointValue({ base: '300px', md: '400px', lg: '500px' });

  // Typing animation state
  const [displayText, setDisplayText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const fullText = "iKUN : Welcome to the Future of Learning";

  useEffect(() => {
    if (currentIndex < fullText.length) {
      const timeout = setTimeout(() => {
        setDisplayText(prev => prev + fullText[currentIndex]);
        setCurrentIndex(prev => prev + 1);
      }, 100);
      return () => clearTimeout(timeout);
    }
  }, [currentIndex, fullText]);

  // Safely get translated resources with fallbacks
  const features: Feature[] = t('HomePage.features', { returnObjects: true }) || [];
  const founders: Founder[] = t('HomePage.founders', { returnObjects: true }) || [];
  const visions: Vision[] = t('HomePage.visions', { returnObjects: true }) || [];

  if (!ready) {
    return (
      <Flex minH="100vh" align="center" justify="center">
        <VStack spacing={4}>
          <Box
            w="60px"
            h="60px"
            border="4px solid"
            borderColor="#FFB69B"
            borderTopColor="#F47B4F"
            borderRadius="full"
            animation={`spin 1s linear infinite`}
          />
          <Text color="#5D5858">Loading translations...</Text>
        </VStack>
      </Flex>
    );
  }

  return (
    <Box bg={bgColor} minH="100vh" overflow="hidden">
      <Box pt='64px'>
        {/* Full-Screen Hero Section with M.jpg Background */}
        <Box
          position="relative"
          height="100vh"
          width="100vw"
          overflow="hidden"
        >
          {/* Full-Screen Background Image */}
          <Box
            position="absolute"
            top="0"
            left="0"
            right="0"
            bottom="0"
            backgroundImage={`url(${MImage})`}
            backgroundSize="cover"
            backgroundPosition="center"
            backgroundRepeat="no-repeat"
            zIndex="1"
          />
          
          {/* Dark Overlay for Better Text Readability */}
          <Box
            position="absolute"
            top="0"
            left="0"
            right="0"
            bottom="0"
            bg="rgba(0, 0, 0, 0.4)"
            zIndex="2"
          />

          {/* Scattered Sparklings */}
          {[...Array(20)].map((_, i) => (
            <Box
              key={i}
              position="absolute"
              top={`${Math.random() * 100}%`}
              left={`${Math.random() * 100}%`}
              w="4px"
              h="4px"
              bg="#FFE5C4"
              borderRadius="50%"
              zIndex="3"
              css={{
                animation: `${sparkle} ${2 + Math.random() * 3}s linear infinite`,
                animationDelay: `${Math.random() * 2}s`,
              }}
              _before={{
                content: '""',
                position: 'absolute',
                top: '-2px',
                left: '-2px',
                right: '-2px',
                bottom: '-2px',
                bg: `radial-gradient(circle, #F47B4F, transparent)`,
                borderRadius: '50%',
                opacity: 0.6,
              }}
            />
          ))}

          {/* Large Sparkles */}
          {[...Array(8)].map((_, i) => (
            <Box
              key={`large-${i}`}
              position="absolute"
              top={`${Math.random() * 100}%`}
              left={`${Math.random() * 100}%`}
              fontSize="20px"
              color="#FFB69B"
              zIndex="3"
              css={{
                animation: `${sparkle} ${3 + Math.random() * 2}s linear infinite`,
                animationDelay: `${Math.random() * 3}s`,
              }}
            >
              ✨
            </Box>
          ))}

          {/* Central Content with Typing Animation */}
          <Flex
            position="absolute"
            top="0"
            left="0"
            right="0"
            bottom="0"
            align="center"
            justify="center"
            zIndex="4"
            direction="column"
          >
            <VStack spacing={8} textAlign="center">
              {/* Typing Animation Slogan */}
              <Box>
                <Heading
                  fontSize={{ base: '3xl', md: '5xl', lg: '7xl' }}
                  fontWeight="900"
                  color="white"
                  textShadow="3px 3px 6px rgba(0,0,0,0.7)"
                  letterSpacing="tight"
                  lineHeight="1.1"
                >
                  {displayText}
                  <Box
                    as="span"
                    display="inline-block"
                    w="4px"
                    h={{ base: '40px', md: '60px', lg: '80px' }}
                    bg="#F47B4F"
                    ml="2"
                    animation={`${blink} 1s linear infinite`}
                  />
                </Heading>
              </Box>

              {/* Subtitle */}
              <Text
                fontSize={{ base: 'xl', md: '2xl', lg: '3xl' }}
                color="white"
                textShadow="2px 2px 4px rgba(0,0,0,0.7)"
                opacity="0.9"
                maxW="4xl"
                px={4}
                animation={`${fadeIn} 2s ease-out 2s both`}
              >
                Discover knowledge beyond imagination with AI-powered education
              </Text>

              {/* Call-to-Action Buttons */}
              <Stack
                direction={{ base: 'column', sm: 'row' }}
                spacing={6}
                animation={`${fadeIn} 1.5s ease-out 3s both`}
              >
                <Button
                  size="xl"
                  h="70px"
                  px="40px"
                  fontSize="xl"
                  fontWeight="700"
                  bg="#F47B4F"
                  color="white"
                  borderRadius="full"
                  _hover={{ 
                    transform: 'translateY(-5px) scale(1.05)',
                    boxShadow: '0 25px 50px rgba(244, 123, 79, 0.4)',
                    bg: '#FFB69B'
                  }}
                  _active={{ transform: 'translateY(-2px) scale(1.02)' }}
                  transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)"
                  rightIcon={<Icon as={FiArrowRight} />}
                  onClick={() => navigate('/register')}
                >
                  Begin Your Journey
                </Button>
                <Button
                  size="xl"
                  h="70px"
                  px="40px"
                  fontSize="xl"
                  fontWeight="700"
                  variant="outline"
                  color="white"
                  borderColor="white"
                  borderWidth="3px"
                  borderRadius="full"
                  _hover={{ 
                    bg: 'rgba(255, 255, 255, 0.15)',
                    transform: 'translateY(-5px) scale(1.05)',
                    boxShadow: '0 25px 50px rgba(255, 255, 255, 0.2)'
                  }}
                  _active={{ transform: 'translateY(-2px) scale(1.02)' }}
                  transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)"
                  onClick={() => navigate('/login')}
                >
                  Explore Now
                </Button>
              </Stack>
            </VStack>
          </Flex>

          {/* Scroll Indicator */}
          <Box
            position="absolute"
            bottom="8"
            left="50%"
            transform="translateX(-50%)"
            zIndex="4"
            animation={`${float} 2s ease-in-out infinite`}
          >
            <VStack spacing={2}>
              <Text color="white" fontSize="sm" opacity="0.8">
                Scroll to explore
              </Text>
              <Box
                w="2px"
                h="30px"
                bg="white"
                opacity="0.6"
                borderRadius="full"
              />
            </VStack>
          </Box>
        </Box>

        {/* Enhanced Features Section */}
        {features?.length > 0 && (
          <FeatureSection features={features} />
        )}

        {/* Enhanced Founders Section */}
        {founders?.length > 0 && (
          <FounderSection founders={founders} />
        )}

        {/* Enhanced Vision Section */}
        {visions?.length > 0 && (
          <VisionSection visions={visions} />
        )}

        {/* Enhanced Contact Section */}
        <Box 
          py={20} 
          bgGradient="linear(135deg, #F47B4F, #5D5858)"
          position="relative"
          overflow="hidden"
        >
          {/* Background Pattern */}
          <Box
            position="absolute"
            top="0"
            left="0"
            right="0"
            bottom="0"
            opacity="0.1"
            backgroundImage="url('data:image/svg+xml,%3Csvg width=%2760%27 height=%2760%27 viewBox=%270 0 60 60%27 xmlns=%27http://www.w3.org/2000/svg%27%3E%3Cg fill=%27none%27 fill-rule=%27evenodd%27%3E%3Cg fill=%27%23FFE5C4%27 fill-opacity=%270.4%27%3E%3Ccircle cx=%2730%27 cy=%2730%27 r=%274%27/%3E%3C/g%3E%3C/svg%3E')"
          />
          
          <Container maxW="container.xl" textAlign="center" position="relative" zIndex="2">
            <VStack spacing={8}>
              <Heading 
                fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
                color="white"
                fontWeight="700"
              >
                {t("HomePage.journey")}
              </Heading>
              <Text 
                fontSize={{ base: 'lg', md: 'xl' }}
                color="white"
                opacity="0.9"
                maxW="3xl"
                lineHeight="1.7"
              >
                {t("HomePage.join")}
              </Text>
              <Button
                size="lg"
                h="60px"
                px="40px"
                fontSize="lg"
                fontWeight="600"
                bg="white"
                color="#F47B4F"
                _hover={{ 
                  transform: 'translateY(-3px)', 
                  boxShadow: '0 20px 40px rgba(0,0,0,0.3)',
                  bg: '#FFE5C4'
                }}
                transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
                rightIcon={<Icon as={FiArrowRight} />}
                onClick={() => navigate('/register')}
              >
                {t('HomePage.start')}
              </Button>
            </VStack>
          </Container>
        </Box>
      </Box>
    </Box>
  );
};

interface FeatureProps {
  title: string;
  description: string;
  icon: string;
}

const FeatureSection = ({ features }: { features: Feature[] }) => {
  const { t } = useTranslation();
  const cardBg = useColorModeValue('white', 'gray.800');
  
  return (
    <Box bg={useColorModeValue('white', 'gray.900')} py={20} position="relative">
      <Container maxW="container.xl">
        <VStack spacing={16}>
          <VStack spacing={4} textAlign="center">
            <Heading 
              fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
              bgGradient="linear(to-r, #F47B4F, #FFB69B)"
              bgClip="text"
              fontWeight="700"
            >
              {t("HomePage.feature")}
            </Heading>
            <Box w="100px" h="4px" bg="#F47B4F" borderRadius="full" />
          </VStack>
          
          <SimpleGrid 
            columns={{ base: 1, md: 2, lg: features.length }} 
            spacing={8}
            w="full"
          >
            {features.map((feature, index) => (
              <FeatureCard key={index} {...feature} index={index} />
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  );
};

interface FounderCardProps {
  name: string;
  role: string;
  bio: string;
  image: string;
}

const FounderSection = ({ founders }: { founders: Founder[] }) => {
  const { t } = useTranslation();
  
  return (
    <Box py={20} bg={useColorModeValue('#FFE5C4', 'gray.800')}>
      <Container maxW="container.xl">
        <VStack spacing={16}>
          <VStack spacing={4} textAlign="center">
            <Heading 
              fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
              bgGradient="linear(to-r, #5D5858, #F47B4F)"
              bgClip="text"
              fontWeight="700"
            >
              {t("HomePage.founder")}
            </Heading>
            <Box w="100px" h="4px" bg="#5D5858" borderRadius="full" />
          </VStack>
          
          <SimpleGrid columns={{ base: 1, md: 2, lg: founders.length }} spacing={10}>
            {founders.map((founder, index) => (
              <FounderCard key={index} {...founder} />
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  );
};

const VisionSection = ({ visions }: { visions: Vision[] }) => {
  const { t } = useTranslation();
  const defaultTextColor = useColorModeValue('#5D5858', 'gray.300');
  
  return (
    <Box bg={useColorModeValue('white', 'gray.900')} py={20}>
      <Container maxW="container.xl">
        <VStack spacing={12} align="center">
          <VStack spacing={4} textAlign="center">
            <Heading 
              fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
              bgGradient="linear(to-r, #FFB69B, #F47B4F)"
              bgClip="text"
              fontWeight="700"
            >
              {t('HomePage.vision')}
            </Heading>
            <Box w="100px" h="4px" bg="#FFB69B" borderRadius="full" />
          </VStack>
          
          <VStack spacing={6} maxW="4xl">
            {visions.map((vision, index) => (
              <Text
                key={index}
                fontSize={{ base: 'lg', md: 'xl', lg: '2xl' }}
                textAlign="center"
                color={vision.color || defaultTextColor}
                lineHeight="1.8"
                fontWeight="400"
              >
                {vision.content}
              </Text>
            ))}
          </VStack>
        </VStack>
      </Container>
    </Box>
  );
};

const FeatureCard: React.FC<FeatureProps & { index: number }> = ({ title, description, icon, index }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const iconBg = useColorModeValue('#FFE5C4', '#F47B4F');
  const titleColor = useColorModeValue('#5D5858', 'white');
  const textColor = useColorModeValue('#5D5858', 'gray.300');
  
  return (
    <VStack
      p={8}
      bg={cardBg}
      borderRadius="20px"
      boxShadow="0 10px 30px rgba(93, 88, 88, 0.15)"
      spacing={6}
      align="center"
      position="relative"
      overflow="hidden"
      _hover={{ 
        transform: 'translateY(-10px)',
        boxShadow: '0 20px 40px rgba(93, 88, 88, 0.25)',
        transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)'
      }}
      _before={{
        content: '""',
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: '4px',
        bgGradient: `linear(to-r, #F47B4F, #FFB69B)`,
      }}
      animation={`${fadeIn} 0.8s ease-out ${index * 0.2}s both`}
    >
      <Box
        fontSize="5xl"
        p={4}
        bg={iconBg}
        borderRadius="full"
        color="#F47B4F"
      >
        {icon}
      </Box>
      <Heading size="lg" textAlign="center" color={titleColor}>
        {title}
      </Heading>
      <Text 
        color={textColor} 
        textAlign="center" 
        lineHeight="1.6"
        fontSize="md"
      >
        {description}
      </Text>
    </VStack>
  );
};

const FounderCard: React.FC<FounderCardProps> = ({ name, role, bio, image }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('#FFB69B', '#F47B4F');
  const nameColor = useColorModeValue('#5D5858', 'white');
  const bioColor = useColorModeValue('#5D5858', 'gray.300');
  
  return (
    <VStack
      p={8}
      bg={cardBg}
      borderRadius="20px"
      boxShadow="0 10px 30px rgba(93, 88, 88, 0.15)"
      spacing={6}
      align="center"
      position="relative"
      overflow="hidden"
      _hover={{ 
        transform: 'translateY(-10px)',
        boxShadow: '0 20px 40px rgba(93, 88, 88, 0.25)',
        transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)'
      }}
      _before={{
        content: '""',
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: '4px',
        bgGradient: `linear(to-r, #5D5858, #F47B4F)`,
      }}
    >
      <Box position="relative">
        {image ? (
          <Image
            src={image}
            alt={name}
            borderRadius="full"
            boxSize="150px"
            objectFit="cover"
            border="4px solid"
            borderColor={borderColor}
          />
        ) : (
          <Avatar 
            size="2xl" 
            name={name} 
            bg="#F47B4F" 
            color="white"
            border="4px solid"
            borderColor={borderColor}
          />
        )}
        <Box
          position="absolute"
          bottom="-10px"
          right="-10px"
          w="40px"
          h="40px"
          bg="#F47B4F"
          borderRadius="full"
          display="flex"
          alignItems="center"
          justifyContent="center"
          color="white"
          fontSize="lg"
        >
          ✨
        </Box>
      </Box>
      
      <VStack spacing={2} textAlign="center">
        <Heading size="lg" color={nameColor}>
          {name}
        </Heading>
        <Text color="#F47B4F" fontWeight="600" fontSize="lg">
          {role}
        </Text>
        <Text 
          color={bioColor} 
          textAlign="center"
          lineHeight="1.6"
          maxW="300px"
        >
          {bio}
        </Text>
      </VStack>
    </VStack>
  );
};

export default HomePage;
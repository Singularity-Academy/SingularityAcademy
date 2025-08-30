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
  Grid,
  GridItem,
} from '@chakra-ui/react';
import { keyframes } from '@emotion/react';
import { FiArrowRight, FiBook, FiUsers, FiZap, FiTarget, FiGlobe, FiStar } from 'react-icons/fi';
import Navbar from '@components/Navbar';
import { useTranslation } from 'react-i18next';

// Import all illustrations
import LogoWithName from '../assets/illus/illus_hero_16.png';
import LogoIcon from '../assets/illus/illus_hero_17.png';
import Illus18 from '../assets/illus/illus_hero_18.png';
import Illus19 from '../assets/illus/illus_hero_19.png';
import Illus20 from '../assets/illus/illus_hero_20.png';
import Illus21 from '../assets/illus/illus_hero_21.png';
import Illus22 from '../assets/illus/illus_hero_22.png';
import Illus23 from '../assets/illus/illus_hero_23.png';
import Illus24 from '../assets/illus/illus_hero_24.png';
import Illus25 from '../assets/illus/illus_hero_25.png';
import Illus26 from '../assets/illus/illus_hero_26.png';

interface Feature {
  title: string;
  description: string;
  icon: string;
  illustration: string;
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

// Enhanced animations
const float = keyframes`
  0% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-15px) rotate(2deg); }
  66% { transform: translateY(-5px) rotate(-1deg); }
  100% { transform: translateY(0px) rotate(0deg); }
`;

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
`;

const sparkle = keyframes`
  0% { transform: scale(0) rotate(0deg); opacity: 0; }
  50% { transform: scale(1) rotate(180deg); opacity: 1; }
  100% { transform: scale(0) rotate(360deg); opacity: 0; }
`;

const blink = keyframes`
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const slideIn = keyframes`
  from { transform: translateX(-100px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
`;

// Curve component for section transitions
const CurveTransition: React.FC<{ 
  topColor: string; 
  bottomColor: string; 
  flip?: boolean;
  height?: string;
}> = ({ topColor, bottomColor, flip = false, height = "100px" }) => (
  <Box position="relative" height={height} overflow="hidden">
    <svg
      width="100%"
      height="100%"
      viewBox="0 0 1200 120"
      preserveAspectRatio="none"
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        transform: flip ? 'scaleY(-1)' : 'none',
      }}
    >
      <path
        d="M0,0 C150,100 350,0 600,50 C850,100 1050,0 1200,50 L1200,120 L0,120 Z"
        fill={topColor}
      />
    </svg>
    <Box
      position="absolute"
      top="0"
      left="0"
      right="0"
      bottom="0"
      bg={bottomColor}
      zIndex="-1"
    />
  </Box>
);

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const bgColor = useColorModeValue('#FFE5C4', 'gray.900');
  const { t, i18n, ready } = useTranslation();
  
  // Typing animation state
  const [displayText, setDisplayText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const fullText = "欢迎来到 ClarifAI - \"看见\"学习，为你而来。";

  useEffect(() => {
    if (currentIndex < fullText.length) {
      const timeout = setTimeout(() => {
        setDisplayText(prev => prev + fullText[currentIndex]);
        setCurrentIndex(prev => prev + 1);
      }, 150);
      return () => clearTimeout(timeout);
    }
  }, [currentIndex, fullText]);

  // Enhanced features with illustrations
  const enhancedFeatures: Feature[] = [
    {
      title: "AI 智能学习",
      description: "体验个性化教育，配备前沿人工智能技术，适应您的学习风格。",
      icon: "🧠",
      illustration: Illus18
    },
    {
      title: "互动体验",
      description: "参与沉浸式学习环境，让复杂概念变得易于理解。",
      icon: "🎯",
      illustration: Illus19
    },
    {
      title: "全球社区",
      description: "与全世界的学习者连接，在我们充满活力的教育生态系统中分享知识。",
      icon: "🌍",
      illustration: Illus20
    },
    {
      title: "刨根问底",
      description: "我们提供深入的解析，帮助你理解复杂的概念。",
      icon: "📊",
      illustration: Illus21
    }
  ];

  // Safely get translated resources with fallbacks
  const features: Feature[] = t('HomePage.features', { returnObjects: true }) || enhancedFeatures;
  const founders: Founder[] = t('HomePage.founders', { returnObjects: true }) || [];
  const visions: Vision[] = t('HomePage.visions', { returnObjects: true }) || [];

  if (!ready) {
    return (
      <Flex minH="100vh" align="center" justify="center" bg={bgColor}>
        <VStack spacing={6}>
          <Image src={LogoIcon} alt="正在加载" w="80px" h="80px" animation={`${pulse} 2s infinite`} />
          <Text color="#5D5858" fontSize="lg">正在加载 ClarifAI...</Text>
        </VStack>
      </Flex>
    );
  }

  return (
    <Box bg={bgColor} minH="100vh" overflow="hidden">
      <Box pt='64px'>
        {/* Hero Section with New Design */}
        <Box
          position="relative"
          minHeight="100vh"
          bgGradient="linear(135deg, #FFE5C4 0%, #FFB69B 50%, #F47B4F 100%)"
          overflow="hidden"
        >
          {/* Animated Background Elements */}
          <Box position="absolute" top="10%" left="5%" animation={`${float} 6s ease-in-out infinite`}>
            <Image src={Illus22} alt="" w="120px" opacity="0.3" />
          </Box>
          <Box position="absolute" top="20%" right="8%" animation={`${float} 8s ease-in-out infinite 2s`}>
            <Image src={Illus23} alt="" w="100px" opacity="0.4" />
          </Box>
          <Box position="absolute" bottom="15%" left="10%" animation={`${float} 7s ease-in-out infinite 1s`}>
            <Image src={Illus24} alt="" w="90px" opacity="0.3" />
          </Box>

          {/* Sparklings */}
          {[...Array(15)].map((_, i) => (
            <Box
              key={i}
              position="absolute"
              top={`${Math.random() * 100}%`}
              left={`${Math.random() * 100}%`}
              w="6px"
              h="6px"
              bg="#F47B4F"
              borderRadius="50%"
              zIndex="2"
              css={{
                animation: `${sparkle} ${3 + Math.random() * 4}s linear infinite`,
                animationDelay: `${Math.random() * 3}s`,
              }}
            />
          ))}

          {/* Main Hero Content */}
          <Container maxW="container.xl" h="100vh">
            <Grid templateColumns={{ base: "1fr", lg: "1fr 1fr" }} h="full" alignItems="center" gap={12}>
              {/* Left Content */}
              <GridItem>
                <VStack spacing={8} align={{ base: "center", lg: "flex-start" }} textAlign={{ base: "center", lg: "left" }}>
                  {/* Logo */}
                  <Image 
                    src={LogoWithName} 
                    alt="ClarifAI" 
                    w={{ base: "250px", md: "300px", lg: "350px" }}
                    animation={`${fadeIn} 1s ease-out`}
                  />

                  {/* Typing Animation */}
                  <Box>
                    <Heading
                      fontSize={{ base: '2xl', md: '4xl', lg: '5xl' }}
                      fontWeight="900"
                      color="#5D5858"
                      letterSpacing="tight"
                      lineHeight="1.2"
                    >
                      {displayText}
                      <Box
                        as="span"
                        display="inline-block"
                        w="4px"
                        h={{ base: '30px', md: '50px', lg: '60px' }}
                        bg="#F47B4F"
                        ml="2"
                        animation={`${blink} 1s linear infinite`}
                      />
                    </Heading>
                  </Box>

                  {/* Subtitle */}
                  <Text
                    fontSize={{ base: 'lg', md: 'xl', lg: '2xl' }}
                    color="#5D5858"
                    opacity="0.8"
                    maxW="600px"
                    lineHeight="1.6"
                    animation={`${fadeIn} 1.5s ease-out 1s both`}
                  >
                    首个AI教育平台，生成个性化知识视频，规划循序渐进的课程，为您提供系统性知识
                    </Text>

                  {/* CTA Buttons */}
                  <Stack
                    direction={{ base: 'column', sm: 'row' }}
                    spacing={4}
                    animation={`${fadeIn} 1.5s ease-out 2s both`}
                  >
                    <Button
                      size="lg"
                      h="60px"
                      px="30px"
                      fontSize="lg"
                      fontWeight="700"
                      bg="#F47B4F"
                      color="white"
                      borderRadius="full"
                      _hover={{ 
                        transform: 'translateY(-3px) scale(1.05)',
                        boxShadow: '0 20px 40px rgba(244, 123, 79, 0.4)',
                        bg: '#E85A2B'
                      }}
                      transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
                      rightIcon={<Icon as={FiArrowRight} />}
                      onClick={() => navigate('/register')}
                    >
                      开始学习
                    </Button>
                    <Button
                      size="lg"
                      h="60px"
                      px="30px"
                      fontSize="lg"
                      fontWeight="700"
                      variant="outline"
                      color="#5D5858"
                      borderColor="#5D5858"
                      borderWidth="2px"
                      borderRadius="full"
                      _hover={{ 
                        bg: 'rgba(93, 88, 88, 0.1)',
                        transform: 'translateY(-3px) scale(1.05)',
                      }}
                      transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
                      onClick={() => navigate('/login')}
                    >
                      探索演示
                    </Button>
                  </Stack>
                </VStack>
              </GridItem>

              {/* Right Content - Main Illustration */}
              <GridItem display={{ base: "none", lg: "block" }}>
                <Box position="relative" h="full" display="flex" alignItems="center" justifyContent="center">
                  <Image 
                    src={Illus25} 
                    alt="AI Learning" 
                    w="500px"
                    animation={`${float} 4s ease-in-out infinite`}
                  />
                  {/* Floating elements around main illustration */}
                  <Box position="absolute" top="10%" left="10%" animation={`${float} 5s ease-in-out infinite 1s`}>
                    <Image src={Illus26} alt="" w="80px" opacity="0.7" />
                  </Box>
                </Box>
              </GridItem>
            </Grid>
          </Container>

          {/* Scroll Indicator */}
          <Box
            position="absolute"
            bottom="8"
            left="50%"
            transform="translateX(-50%)"
            animation={`${float} 2s ease-in-out infinite`}
          >
            <VStack spacing={2}>
              <Text color="#5D5858" fontSize="sm" opacity="0.7">
                了解更多
              </Text>
              <Box w="2px" h="30px" bg="#5D5858" opacity="0.5" borderRadius="full" />
            </VStack>
          </Box>
        </Box>

        {/* Curve Transition */}
        <CurveTransition topColor="#F47B4F" bottomColor="white" />

        {/* Enhanced Features Section */}
        <Box bg="white" py={20} position="relative">
          <Container maxW="container.xl">
            <VStack spacing={16}>
              <VStack spacing={6} textAlign="center">
                <Heading 
                  fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
                  bgGradient="linear(to-r, #F47B4F, #FFB69B)"
                  bgClip="text"
                  fontWeight="700"
                >
                  为什么选择 ClarifAI？
                </Heading>
                <Text fontSize="xl" color="#5D5858" maxW="600px" opacity="0.8">
                  通过我们的创新功能体验教育的未来
                </Text>
                <Box w="100px" h="4px" bg="#F47B4F" borderRadius="full" />
              </VStack>
              
              <SimpleGrid columns={{ base: 1, md: 2 }} spacing={12} w="full">
                {enhancedFeatures.map((feature, index) => (
                  <FeatureCard key={index} {...feature} index={index} />
                ))}
              </SimpleGrid>
            </VStack>
          </Container>
        </Box>

        {/* Curve Transition */}
        <CurveTransition topColor="white" bottomColor="#FFE5C4" />

        {/* Enhanced Founders Section */}
        {founders?.length > 0 && (
          <>
            <FounderSection founders={founders} />
            <CurveTransition topColor="#FFE5C4" bottomColor="white" />
          </>
        )}

        {/* Enhanced Vision Section */}
        {visions?.length > 0 && (
          <>
            <VisionSection visions={visions} />
            <CurveTransition topColor="white" bottomColor="#F47B4F" />
          </>
        )}

        {/* Enhanced Contact Section */}
        <Box 
          py={20} 
          bg="#F47B4F"
          position="relative"
          overflow="hidden"
        >
          {/* Background Illustrations */}
          <Box position="absolute" top="20%" left="5%" opacity="0.1">
            <Image src={Illus22} alt="" w="150px" />
          </Box>
          <Box position="absolute" bottom="20%" right="5%" opacity="0.1">
            <Image src={Illus23} alt="" w="120px" />
          </Box>
          
          <Container maxW="container.xl" textAlign="center" position="relative" zIndex="2">
            <VStack spacing={8}>
              <Heading 
                fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
                color="white"
                fontWeight="700"
              >
                准备好改变您的学习方式了吗？
              </Heading>
              <Text 
                fontSize={{ base: 'lg', md: 'xl' }}
                color="white"
                opacity="0.9"
                maxW="3xl"
                lineHeight="1.7"
              >
                加入数千名已经在 ClarifAI 体验教育未来的学习者
              </Text>
              <Button
                size="xl"
                h="70px"
                px="40px"
                fontSize="xl"
                fontWeight="600"
                bg="white"
                color="#F47B4F"
                _hover={{ 
                  transform: 'translateY(-5px)', 
                  boxShadow: '0 25px 50px rgba(0,0,0,0.3)',
                  bg: '#FFE5C4'
                }}
                transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
                rightIcon={<Icon as={FiArrowRight} />}
                onClick={() => navigate('/register')}
              >
                开始您的旅程
              </Button>
            </VStack>
          </Container>
        </Box>
      </Box>
    </Box>
  );
};

// Enhanced Feature Card Component
interface FeatureProps {
  title: string;
  description: string;
  icon: string;
  illustration: string;
}

const FeatureCard: React.FC<FeatureProps & { index: number }> = ({ 
  title, 
  description, 
  icon, 
  illustration, 
  index 
}) => {
  return (
    <Box
      p={8}
      bg="white"
      borderRadius="24px"
      boxShadow="0 10px 40px rgba(93, 88, 88, 0.1)"
      position="relative"
      overflow="hidden"
      _hover={{ 
        transform: 'translateY(-10px)',
        boxShadow: '0 20px 60px rgba(93, 88, 88, 0.2)',
        transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)'
      }}
      animation={`${fadeIn} 0.8s ease-out ${index * 0.2}s both`}
    >
      <Grid templateColumns="1fr auto" gap={6} alignItems="center">
        <VStack align="flex-start" spacing={4}>
          <Box fontSize="3xl">{icon}</Box>
          <Heading size="lg" color="#5D5858">
            {title}
          </Heading>
          <Text color="#5D5858" opacity="0.8" lineHeight="1.6">
            {description}
          </Text>
        </VStack>
        <Box>
          <Image 
            src={illustration} 
            alt={title} 
            w="120px" 
            h="120px"
            objectFit="contain"
            animation={`${float} 3s ease-in-out infinite ${index * 0.5}s`}
          />
        </Box>
      </Grid>
    </Box>
  );
};

// Keep existing FounderSection and VisionSection components
const FounderSection = ({ founders }: { founders: Founder[] }) => {
  const { t } = useTranslation();
  
  return (
    <Box py={20} bg="#FFE5C4">
      <Container maxW="container.xl">
        <VStack spacing={16}>
          <VStack spacing={4} textAlign="center">
            <Heading 
              fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
              bgGradient="linear(to-r, #5D5858, #F47B4F)"
              bgClip="text"
              fontWeight="700"
            >
              认识我们的创始人
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
    <Box bg="white" py={20}>
      <Container maxW="container.xl">
        <VStack spacing={12} align="center">
          <VStack spacing={4} textAlign="center">
            <Heading 
              fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
              bgGradient="linear(to-r, #FFB69B, #F47B4F)"
              bgClip="text"
              fontWeight="700"
            >
              我们的愿景
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

interface FounderCardProps {
  name: string;
  role: string;
  bio: string;
  image: string;
}

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
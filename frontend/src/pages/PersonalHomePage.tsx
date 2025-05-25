import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Container,
  Heading,
  Text,
  VStack,
  HStack,
  SimpleGrid,
  useColorModeValue,
  Avatar,
  useToast,
  Spinner,
  Flex,
  Icon,
  Image,
  Badge,
  Progress,
  Divider,
  Grid,
  GridItem,
} from '@chakra-ui/react';
import { keyframes } from '@emotion/react';
import {
  FiMail,
  FiMapPin,
  FiCalendar,
  FiCode,
  FiGithub,
  FiLinkedin,
  FiExternalLink,
  FiAward,
  FiTrendingUp,
  FiUsers,
  FiStar,
} from 'react-icons/fi';
import { getUserData } from '@utils/axios';
import Navbar from '@components/Navbar';
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";

// Import illustrations
import LogoIcon from '../assets/illus/illus_hero_17.png';
import Illus18 from '../assets/illus/illus_hero_18.png';
import Illus19 from '../assets/illus/illus_hero_19.png';
import Illus20 from '../assets/illus/illus_hero_20.png';
import Illus21 from '../assets/illus/illus_hero_21.png';
import Illus22 from '../assets/illus/illus_hero_22.png';
import Illus23 from '../assets/illus/illus_hero_23.png';

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

const slideIn = keyframes`
  from { transform: translateX(-50px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const sparkle = keyframes`
  0% { transform: scale(0) rotate(0deg); opacity: 0; }
  50% { transform: scale(1) rotate(180deg); opacity: 1; }
  100% { transform: scale(0) rotate(360deg); opacity: 0; }
`;

// Curve component for section transitions
const CurveTransition: React.FC<{ 
  topColor: string; 
  bottomColor: string; 
  flip?: boolean;
  height?: string;
}> = ({ topColor, bottomColor, flip = false, height = "80px" }) => (
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

const PersonalHomePage: React.FC = () => {
  const toast = useToast();
  const navigate = useNavigate();
  const [user, setUser] = useState<{ id: number; name: string; email: string } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      if (!Cookies.get('token')) {
        localStorage.removeItem('user');
        navigate('/login');
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
  }, [toast, navigate]);

  // Loading state
  if (loading) {
    return (
      <Flex minH="100vh" align="center" justify="center" bg="#FFE5C4">
        <VStack spacing={6}>
          <Image src={LogoIcon} alt="Loading" w="80px" h="80px" animation={`${pulse} 2s infinite`} />
          <Text color="#5D5858" fontSize="lg">正在加载您的个人资料...</Text>
        </VStack>
      </Flex>
    );
  }

  // No user data state
  if (!user) {
    return (
      <Flex minH="100vh" align="center" justify="center" bg="#FFE5C4">
        <VStack spacing={6}>
          <Text color="#5D5858" fontSize="lg">无法加载个人资料数据</Text>
          <Button onClick={() => navigate('/login')} bg="#F47B4F" color="white">
            返回登录
          </Button>
        </VStack>
      </Flex>
    );
  }

  return (
    <Box bg="#FFE5C4" minH="100vh">
      <Box pt="64px">
        {/* Hero Section */}
        <Box
          bgGradient="linear(135deg, #FFE5C4 0%, #FFB69B 50%, #F47B4F 100%)"
          py={20}
          position="relative"
          overflow="hidden"
        >
          {/* Background Illustrations */}
          <Box position="absolute" top="10%" left="5%" opacity="0.2" animation={`${float} 6s ease-in-out infinite`}>
            <Image src={Illus22} alt="" w="120px" />
          </Box>
          <Box position="absolute" top="20%" right="8%" opacity="0.3" animation={`${float} 8s ease-in-out infinite 2s`}>
            <Image src={Illus23} alt="" w="100px" />
          </Box>
          <Box position="absolute" bottom="15%" left="10%" opacity="0.2" animation={`${float} 7s ease-in-out infinite 1s`}>
            <Image src={Illus21} alt="" w="90px" />
          </Box>

          {/* Sparklings */}
          {[...Array(12)].map((_, i) => (
            <Box
              key={i}
              position="absolute"
              top={`${Math.random() * 100}%`}
              left={`${Math.random() * 100}%`}
              w="4px"
              h="4px"
              bg="#F47B4F"
              borderRadius="50%"
              zIndex="2"
              css={{
                animation: `${sparkle} ${3 + Math.random() * 4}s linear infinite`,
                animationDelay: `${Math.random() * 3}s`,
              }}
            />
          ))}

          <Container maxW="container.xl">
            <VStack spacing={12} align="center" position="relative" zIndex="3">
              {/* Profile Header */}
              <VStack spacing={8} textAlign="center">
                <Box position="relative">
                  <Avatar 
                    size="2xl" 
                    name={user.name} 
                    bg="#F47B4F" 
                    color="white"
                    border="6px solid white"
                    boxShadow="0 20px 40px rgba(93, 88, 88, 0.3)"
                    animation={`${fadeIn} 1s ease-out`}
                  />
                  <Box
                    position="absolute"
                    bottom="-5px"
                    right="-5px"
                    w="50px"
                    h="50px"
                    bg="#FFB69B"
                    borderRadius="full"
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                    border="4px solid white"
                    animation={`${pulse} 2s ease-in-out infinite`}
                  >
                    <Image src={LogoIcon} alt="ClarifAI" w="25px" h="25px" />
                  </Box>
                </Box>

                <VStack spacing={4}>
                  <Heading 
                    as="h1" 
                    size="2xl" 
                    color="#5D5858"
                    fontWeight="700"
                    animation={`${fadeIn} 1.2s ease-out`}
                  >
                    你好，我是 {user.name}
                  </Heading>
                  <Text 
                    fontSize="xl" 
                    color="#5D5858" 
                    opacity="0.8"
                    maxW="3xl"
                    lineHeight="1.6"
                    animation={`${fadeIn} 1.4s ease-out`}
                  >
                    一位充满热情的学习者，通过AI驱动的教育探索知识的前沿。
                    欢迎来到我在ClarifAI的学习之旅。
                  </Text>
                </VStack>

                {/* Contact Info */}
                <HStack 
                  spacing={8} 
                  flexWrap="wrap" 
                  justify="center"
                  animation={`${fadeIn} 1.6s ease-out`}
                >
                  <HStack spacing={2}>
                    <Icon as={FiMail} color="#F47B4F" />
                    <Text color="#5D5858" fontSize="md">{user.email}</Text>
                  </HStack>
                  <HStack spacing={2}>
                    <Icon as={FiCalendar} color="#F47B4F" />
                    <Text color="#5D5858" fontSize="md">加入 ClarifAI</Text>
                  </HStack>
                </HStack>

                {/* CTA Buttons */}
                <HStack 
                  spacing={4} 
                  flexWrap="wrap" 
                  justify="center"
                  animation={`${fadeIn} 1.8s ease-out`}
                >
                  <Button
                    size="lg"
                    bg="#F47B4F"
                    color="white"
                    borderRadius="full"
                    rightIcon={<Icon as={FiTrendingUp} />}
                    _hover={{ 
                      transform: 'translateY(-3px) scale(1.05)',
                      boxShadow: '0 20px 40px rgba(244, 123, 79, 0.4)'
                    }}
                    onClick={() => navigate('/learning')}
                  >
                    继续学习
                  </Button>
                  <Button
                    size="lg"
                    variant="outline"
                    color="#5D5858"
                    borderColor="#5D5858"
                    borderWidth="2px"
                    borderRadius="full"
                    rightIcon={<Icon as={FiExternalLink} />}
                    _hover={{ 
                      bg: 'rgba(93, 88, 88, 0.1)',
                      transform: 'translateY(-3px) scale(1.05)'
                    }}
                    onClick={() => window.open('mailto:' + user.email)}
                  >
                    联系我
                  </Button>
                </HStack>
              </VStack>
            </VStack>
          </Container>
        </Box>

        <CurveTransition topColor="#F47B4F" bottomColor="white" />

        {/* Learning Stats Section */}
        <Box bg="white" py={20}>
          <Container maxW="container.xl">
            <VStack spacing={16}>
              <VStack spacing={6} textAlign="center">
                <Heading 
                  fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
                  bgGradient="linear(to-r, #F47B4F, #FFB69B)"
                  bgClip="text"
                  fontWeight="700"
                >
                  学习之旅
                </Heading>
                <Text fontSize="xl" color="#5D5858" maxW="600px" opacity="0.8">
                  在ClarifAI生态系统中跟踪您的进度和成就
                </Text>
                <Box w="100px" h="4px" bg="#F47B4F" borderRadius="full" />
              </VStack>

              <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={8} w="full">
                <StatsCard
                  title="Courses Completed"
                  value="8"
                  icon={FiCode}
                  color="#F47B4F"
                  illustration={Illus18}
                />
                <StatsCard
                  title="Learning Streak"
                  value="12 days"
                  icon={FiTrendingUp}
                  color="#FFB69B"
                  illustration={Illus19}
                />
                <StatsCard
                  title="Total Points"
                  value="2,450"
                  icon={FiStar}
                  color="#5D5858"
                  illustration={Illus20}
                />
                <StatsCard
                  title="Achievements"
                  value="15"
                  icon={FiAward}
                  color="#F47B4F"
                  illustration={Illus21}
                />
              </SimpleGrid>
            </VStack>
          </Container>
        </Box>

        <CurveTransition topColor="white" bottomColor="#FFE5C4" />

        {/* Skills Section */}
        <Box bg="#FFE5C4" py={20}>
          <Container maxW="container.xl">
            <VStack spacing={16}>
              <VStack spacing={6} textAlign="center">
                <Heading 
                  fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
                  bgGradient="linear(to-r, #5D5858, #F47B4F)"
                  bgClip="text"
                  fontWeight="700"
                >
                  Skills & Expertise
                </Heading>
                <Text fontSize="xl" color="#5D5858" maxW="600px" opacity="0.8">
                  Technologies and skills I've mastered through ClarifAI
                </Text>
                <Box w="100px" h="4px" bg="#5D5858" borderRadius="full" />
              </VStack>

              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={8}>
                <SkillCard 
                  title="AI & Machine Learning" 
                  description="Deep understanding of neural networks, deep learning, and AI applications through hands-on projects."
                  progress={85}
                  illustration={Illus18}
                />
                <SkillCard 
                  title="Data Science & Analytics" 
                  description="Proficient in data analysis, visualization, and statistical modeling with Python and R."
                  progress={78}
                  illustration={Illus19}
                />
                <SkillCard 
                  title="Software Engineering" 
                  description="Full-stack development with modern frameworks, cloud technologies, and best practices."
                  progress={92}
                  illustration={Illus20}
                />
              </SimpleGrid>
            </VStack>
          </Container>
        </Box>

        <CurveTransition topColor="#FFE5C4" bottomColor="white" />

        {/* Projects Section */}
        <Box bg="white" py={20}>
          <Container maxW="container.xl">
            <VStack spacing={16}>
              <VStack spacing={6} textAlign="center">
                <Heading 
                  fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
                  bgGradient="linear(to-r, #FFB69B, #F47B4F)"
                  bgClip="text"
                  fontWeight="700"
                >
                  Featured Projects
                </Heading>
                <Text fontSize="xl" color="#5D5858" maxW="600px" opacity="0.8">
                  Real-world applications of knowledge gained through ClarifAI courses
                </Text>
                <Box w="100px" h="4px" bg="#FFB69B" borderRadius="full" />
              </VStack>

              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={8}>
                <ProjectCard 
                  title="AI-Powered Learning Assistant" 
                  description="A personalized tutoring system that adapts to individual learning styles using machine learning algorithms."
                  tech={["Python", "TensorFlow", "React"]}
                  illustration={Illus21}
                />
                <ProjectCard 
                  title="Smart Analytics Dashboard" 
                  description="Real-time data visualization platform for educational metrics with predictive analytics capabilities."
                  tech={["JavaScript", "D3.js", "Node.js"]}
                  illustration={Illus22}
                />
                <ProjectCard 
                  title="Collaborative Learning Platform" 
                  description="A social learning environment that connects students globally for peer-to-peer knowledge sharing."
                  tech={["React", "GraphQL", "PostgreSQL"]}
                  illustration={Illus23}
                />
              </SimpleGrid>
            </VStack>
          </Container>
        </Box>

        <CurveTransition topColor="white" bottomColor="#F47B4F" />

        {/* Contact Section */}
        <Box bg="#F47B4F" py={20} position="relative" overflow="hidden">
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
                Let's Connect & Learn Together
              </Heading>
              <Text 
                fontSize={{ base: 'lg', md: 'xl' }}
                color="white"
                opacity="0.9"
                maxW="3xl"
                lineHeight="1.7"
              >
                I'm always excited to discuss new learning opportunities, collaborate on projects, 
                or share insights from my ClarifAI journey. Let's build the future of education together!
              </Text>
              <HStack spacing={4} flexWrap="wrap" justify="center">
                <Button
                  size="lg"
                  bg="white"
                  color="#F47B4F"
                  leftIcon={<Icon as={FiMail} />}
                  _hover={{ 
                    transform: 'translateY(-3px)', 
                    boxShadow: '0 20px 40px rgba(0,0,0,0.3)'
                  }}
                  onClick={() => window.open('mailto:' + user.email)}
                >
                  Send Email
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  color="white"
                  borderColor="white"
                  borderWidth="2px"
                  leftIcon={<Icon as={FiUsers} />}
                  _hover={{ 
                    bg: 'rgba(255, 255, 255, 0.15)',
                    transform: 'translateY(-3px)'
                  }}
                  onClick={() => navigate('/learning')}
                >
                  Join My Learning
                </Button>
              </HStack>
            </VStack>
          </Container>
        </Box>
      </Box>
    </Box>
  );
};

// Enhanced Component Definitions
interface StatsCardProps {
  title: string;
  value: string;
  icon: any;
  color: string;
  illustration: string;
}

const StatsCard: React.FC<StatsCardProps> = ({ title, value, icon, color, illustration }) => {
  return (
    <Box
      bg="white"
      borderRadius="20px"
      boxShadow="0 10px 40px rgba(93, 88, 88, 0.1)"
      p={8}
      position="relative"
      overflow="hidden"
      _hover={{ 
        transform: 'translateY(-10px)',
        boxShadow: '0 20px 60px rgba(93, 88, 88, 0.2)',
        transition: 'all 0.4s ease'
      }}
      animation={`${fadeIn} 0.8s ease-out`}
    >
      <VStack spacing={6}>
        <Image 
          src={illustration} 
          alt={title} 
          w="80px" 
          h="80px"
          animation={`${float} 3s ease-in-out infinite`}
        />
        <VStack spacing={2} textAlign="center">
          <Icon as={icon} size="24px" color={color} />
          <Text fontSize="sm" color="#5D5858" opacity="0.7">
            {title}
          </Text>
          <Text fontSize="3xl" fontWeight="bold" color="#5D5858">
            {value}
          </Text>
        </VStack>
      </VStack>
    </Box>
  );
};

interface SkillCardProps {
  title: string;
  description: string;
  progress: number;
  illustration: string;
}

const SkillCard: React.FC<SkillCardProps> = ({ title, description, progress, illustration }) => {
  return (
    <Box
      bg="white"
      borderRadius="20px"
      boxShadow="0 10px 40px rgba(93, 88, 88, 0.1)"
      p={8}
      _hover={{ 
        transform: 'translateY(-10px)',
        boxShadow: '0 20px 60px rgba(93, 88, 88, 0.2)',
        transition: 'all 0.4s ease'
      }}
      animation={`${slideIn} 0.8s ease-out`}
    >
      <VStack spacing={6} align="stretch">
        <Flex justify="space-between" align="center">
          <VStack align="flex-start" spacing={2} flex="1">
            <Heading size="lg" color="#5D5858">
              {title}
            </Heading>
            <Text color="#5D5858" opacity="0.8" lineHeight="1.6">
              {description}
            </Text>
          </VStack>
          <Image 
            src={illustration} 
            alt={title} 
            w="80px" 
            h="80px"
            animation={`${float} 3s ease-in-out infinite`}
          />
        </Flex>
        
        <Box>
          <Flex justify="space-between" mb={2}>
            <Text fontSize="sm" color="#5D5858" opacity="0.7">
              Proficiency
            </Text>
            <Text fontSize="sm" fontWeight="bold" color="#F47B4F">
              {progress}%
            </Text>
          </Flex>
          <Progress 
            value={progress} 
            colorScheme="orange" 
            borderRadius="full"
            size="md"
          />
        </Box>
      </VStack>
    </Box>
  );
};

interface ProjectCardProps {
  title: string;
  description: string;
  tech: string[];
  illustration: string;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ title, description, tech, illustration }) => {
  return (
    <Box
      bg="white"
      borderRadius="20px"
      boxShadow="0 10px 40px rgba(93, 88, 88, 0.1)"
      p={8}
      _hover={{ 
        transform: 'translateY(-10px)',
        boxShadow: '0 20px 60px rgba(93, 88, 88, 0.2)',
        transition: 'all 0.4s ease'
      }}
      animation={`${fadeIn} 0.8s ease-out`}
    >
      <VStack spacing={6} align="stretch">
        <Image 
          src={illustration} 
          alt={title} 
          w="100px" 
          h="100px"
          mx="auto"
          animation={`${float} 4s ease-in-out infinite`}
        />
        
        <VStack spacing={4} align="stretch">
          <Heading size="md" color="#5D5858" textAlign="center">
            {title}
          </Heading>
          <Text color="#5D5858" opacity="0.8" lineHeight="1.6" textAlign="center">
            {description}
          </Text>
          
          <HStack spacing={2} flexWrap="wrap" justify="center">
            {tech.map((technology, index) => (
              <Badge 
                key={index}
                colorScheme="orange" 
                borderRadius="full" 
                px={3}
                py={1}
              >
                {technology}
              </Badge>
            ))}
          </HStack>
        </VStack>
        
        <Button
          bg="#F47B4F"
          color="white"
          borderRadius="full"
          rightIcon={<Icon as={FiExternalLink} />}
          _hover={{ 
            bg: '#E85A2B',
            transform: 'scale(1.02)'
          }}
        >
          View Project
        </Button>
      </VStack>
    </Box>
  );
};

export default PersonalHomePage;

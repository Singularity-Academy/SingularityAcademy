import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Heading,
  Text,
  VStack,
  HStack,
  SimpleGrid,
  useColorModeValue,
  Container,
  Icon,
  Image,
  Progress,
  Badge,
  Flex,
  Avatar,
  Divider,
  Grid,
  GridItem,
  useToast,
  Spinner,
} from '@chakra-ui/react';
import { keyframes } from '@emotion/react';
import { StarIcon, TimeIcon, ArrowForwardIcon, ExternalLinkIcon } from '@chakra-ui/icons';
import Navbar from "@components/Navbar";
import { useNavigate } from "react-router-dom";
import { useTranslation } from 'react-i18next';
import Cookies from 'js-cookie';
import { getUserData } from '@utils/axios';

// Import illustrations from HomePage
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
  33% { transform: translateY(-10px) rotate(1deg); }
  66% { transform: translateY(-3px) rotate(-0.5deg); }
  100% { transform: translateY(0px) rotate(0deg); }
`;

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
`;

const slideIn = keyframes`
  from { transform: translateX(-30px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.02); }
  100% { transform: scale(1); }
`;

// Curve component for section transitions
const CurveTransition: React.FC<{ 
  topColor: string; 
  bottomColor: string; 
  flip?: boolean;
  height?: string;
}> = ({ topColor, bottomColor, flip = false, height = "60px" }) => (
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
        d="M0,0 C150,80 350,0 600,40 C850,80 1050,0 1200,40 L1200,120 L0,120 Z"
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

// User data interface
interface UserData {
  id: number;
  name: string;
  email: string;
}

// Extended user data interface for dashboard
interface ExtendedUserData extends UserData {
  level: string;
  progress: number;
  streak: number;
  completedCourses: number;
  totalPoints: number;
}

const LearningPage: React.FC = () => {
  const navigate = useNavigate();
  const toast = useToast();
  const [selectedSection, setSelectedSection] = useState<string>('overview');
  const [user, setUser] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const { t } = useTranslation();

  // Check authentication and fetch user data
  useEffect(() => {
    const fetchUserData = async () => {
    if (!Cookies.get('token')) {
      navigate('/login');
        return;
      }

      setLoading(true);
      const userData = await getUserData(toast, navigate);
      if (userData) {
        setUser(userData);
      }
      setLoading(false);
    };

    fetchUserData();
  }, [navigate, toast]);

  // Create extended user data with mock additional fields
  const getExtendedUserData = (user: UserData | null): ExtendedUserData | null => {
    if (!user) return null;
    
    return {
      ...user,
      level: "高级学习者",
      progress: 75,
      streak: 12,
      completedCourses: 8,
      totalPoints: 2450
    };
  };

  const extendedUserData = getExtendedUserData(user);

  const sidebarItems = [
    { id: 'overview', label: '仪表板', icon: ArrowForwardIcon },
    { id: 'courses', label: '我的课程', icon: ExternalLinkIcon },
    { id: 'meeting', label: 'AI 导师', icon: ExternalLinkIcon },
    { id: 'achievements', label: '成就', icon: StarIcon },
  ];

  const renderContent = () => {
    if (!extendedUserData) return null;
    
    switch (selectedSection) {
      case 'overview':
        return <DashboardContent userData={extendedUserData} />;
      case 'meeting':
        return <MentorSection />;
      case 'courses':
        return <CoursesSection />;
      case 'achievements':
        return <AchievementsSection />;
      default:
        return <DashboardContent userData={extendedUserData} />;
    }
  };

  // Loading state
  if (loading) {
    return (
      <Flex minH="100vh" align="center" justify="center" bg="#FFE5C4">
        <VStack spacing={6}>
          <Image src={LogoIcon} alt="正在加载" w="80px" h="80px" animation={`${pulse} 2s infinite`} />
          <Text color="#5D5858" fontSize="lg">正在加载您的仪表板...</Text>
        </VStack>
      </Flex>
    );
  }

  // No user data state
  if (!user || !extendedUserData) {
  return (
      <Flex minH="100vh" align="center" justify="center" bg="#FFE5C4">
        <VStack spacing={6}>
          <Text color="#5D5858" fontSize="lg">无法加载用户数据</Text>
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
        {/* Hero Header */}
        <Box
          bgGradient="linear(135deg, #FFE5C4 0%, #FFB69B 50%, #F47B4F 100%)"
          py={8}
          position="relative"
          overflow="hidden"
        >
          {/* Background Illustrations */}
          <Box position="absolute" top="20%" left="5%" opacity="0.2" animation={`${float} 6s ease-in-out infinite`}>
            <Image src={Illus22} alt="" w="80px" />
          </Box>
          <Box position="absolute" top="10%" right="8%" opacity="0.3" animation={`${float} 8s ease-in-out infinite 2s`}>
            <Image src={Illus23} alt="" w="60px" />
          </Box>

          <Container maxW="container.xl">
            <Flex align="center" justify="space-between">
              <VStack align="flex-start" spacing={2}>
                <HStack spacing={3}>
                  <Image src={LogoIcon} alt="ClarifAI" w="40px" h="40px" />
                  <Heading color="#5D5858" fontSize="2xl" fontWeight="700">
                    学习仪表板
                  </Heading>
                </HStack>
                <Text color="#5D5858" opacity="0.8" fontSize="lg">
                  欢迎回来，{extendedUserData.name}！准备好继续您的学习之旅了吗？
                </Text>
              </VStack>
              
              <HStack spacing={6} display={{ base: 'none', md: 'flex' }}>
                <VStack spacing={1}>
                  <Text fontSize="2xl" fontWeight="bold" color="#F47B4F">
                    {extendedUserData.streak}
                  </Text>
                  <Text fontSize="sm" color="#5D5858" opacity="0.7">
                    连续天数
                  </Text>
                </VStack>
                <VStack spacing={1}>
                  <Text fontSize="2xl" fontWeight="bold" color="#F47B4F">
                    {extendedUserData.totalPoints}
                  </Text>
                  <Text fontSize="sm" color="#5D5858" opacity="0.7">
                    积分
                  </Text>
                </VStack>
              </HStack>
            </Flex>
          </Container>
        </Box>

        <CurveTransition topColor="#F47B4F" bottomColor="white" />

        {/* Main Content Area */}
        <Box bg="white" minH="calc(100vh - 200px)">
          <Container maxW="container.xl" py={8}>
            <Grid templateColumns={{ base: "1fr", lg: "280px 1fr" }} gap={8}>
              {/* Enhanced Sidebar */}
              <GridItem>
                <Box
                  bg="white"
                  borderRadius="20px"
                  boxShadow="0 10px 40px rgba(93, 88, 88, 0.1)"
                  p={6}
                  position="sticky"
                  top="100px"
                >
                  <VStack spacing={6} align="stretch">
                    {/* User Profile Section */}
                    <VStack spacing={4}>
                      <Avatar 
                        size="lg" 
                        name={extendedUserData.name} 
                        bg="#F47B4F" 
                        color="white"
                        border="3px solid #FFB69B"
                      />
                      <VStack spacing={1}>
                        <Heading size="md" color="#5D5858">
                          {extendedUserData.name}
                        </Heading>
                        <Badge colorScheme="orange" borderRadius="full" px={3}>
                          {extendedUserData.level}
                        </Badge>
                      </VStack>
                      
                      {/* Progress Bar */}
                      <Box w="full">
                        <Flex justify="space-between" mb={2}>
                          <Text fontSize="sm" color="#5D5858" opacity="0.7">
                            总体进度
                          </Text>
                          <Text fontSize="sm" fontWeight="bold" color="#F47B4F">
                            {extendedUserData.progress}%
                          </Text>
                        </Flex>
                        <Progress 
                          value={extendedUserData.progress} 
                          colorScheme="orange" 
                          borderRadius="full"
                          size="md"
                        />
                      </Box>
                    </VStack>

                    <Divider />

                    {/* Navigation Items */}
                    <VStack spacing={2} align="stretch">
                      {sidebarItems.map((item, index) => (
          <Button
                          key={item.id}
                          variant="ghost"
                          justifyContent="flex-start"
                          leftIcon={<Icon as={item.icon} />}
                          onClick={() => setSelectedSection(item.id)}
                          bg={selectedSection === item.id ? '#FFE5C4' : 'transparent'}
                          color={selectedSection === item.id ? '#F47B4F' : '#5D5858'}
                          _hover={{ 
                            bg: '#FFE5C4', 
                            color: '#F47B4F',
                            transform: 'translateX(5px)'
                          }}
                          transition="all 0.3s ease"
                          borderRadius="12px"
                          h="50px"
                          fontSize="md"
                          fontWeight="500"
                          animation={`${slideIn} 0.5s ease-out ${index * 0.1}s both`}
                        >
                          {item.label}
          </Button>
                      ))}
                    </VStack>
        </VStack>
      </Box>
              </GridItem>

      {/* Main Content */}
              <GridItem>
                <Box animation={`${fadeIn} 0.6s ease-out`}>
        {renderContent()}
                </Box>
              </GridItem>
            </Grid>
          </Container>
        </Box>
      </Box>
    </Box>
  );
};

// Dashboard Content Component
const DashboardContent: React.FC<{ userData: ExtendedUserData }> = ({ userData }) => {
  return (
    <VStack spacing={8} align="stretch">
      {/* Stats Cards */}
      <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6}>
        <StatsCard
          title="已完成课程"
          value={userData.completedCourses}
          icon={ExternalLinkIcon}
          color="#F47B4F"
          illustration={Illus18}
        />
        <StatsCard
          title="学习连续天数"
          value={`${userData.streak} 天`}
          icon={ExternalLinkIcon}
          color="#FFB69B"
          illustration={Illus19}
        />
        <StatsCard
          title="总积分"
          value={userData.totalPoints}
          icon={StarIcon}
          color="#5D5858"
          illustration={Illus20}
        />
        <StatsCard
          title="学习时长"
          value="124小时"
          icon={TimeIcon}
          color="#F47B4F"
          illustration={Illus21}
        />
      </SimpleGrid>

      {/* Recent Activity */}
      <Box
        bg="white"
        borderRadius="20px"
        boxShadow="0 10px 40px rgba(93, 88, 88, 0.1)"
        p={8}
      >
        <Heading size="lg" color="#5D5858" mb={6}>
          最近活动
        </Heading>
        <VStack spacing={4} align="stretch">
          <ActivityItem
            title="完成火箭科学模块 3"
            time="2 小时前"
            type="completion"
          />
          <ActivityItem
            title="获得'问题解决者'徽章"
            time="1 天前"
            type="achievement"
          />
          <ActivityItem
            title="开始高等数学课程"
            time="3 天前"
            type="start"
          />
        </VStack>
      </Box>
    </VStack>
  );
};

// Mentor Section Component
const MentorSection: React.FC = () => {
  const navigate = useNavigate();
  
  return (
    <VStack spacing={8} align="stretch">
      <Box textAlign="center">
        <Heading size="xl" color="#5D5858" mb={4}>
          认识您的 AI 导师
        </Heading>
        <Text fontSize="lg" color="#5D5858" opacity="0.8" maxW="2xl" mx="auto">
          与我们专业的 AI 导师联系，为您的学习之旅获得个性化指导和支持。
        </Text>
      </Box>

      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={8}>
        <MentorCard
          name="Hamian"
          role="学术顾问"
          description="获得课程选择、学术规划和整体学习策略的指导。"
          illustration={Illus18}
          onMeet={() => navigate("/principal-ai")}
          color="#F47B4F"
        />
        <MentorCard
          name="Jvein"
          role="学科专家"
          description="深入研究特定学科，获得专家级知识和个性化解释。"
          illustration={Illus19}
          onMeet={() => navigate("/course/interaction?AI=Dean")}
          color="#FFB69B"
        />
      </SimpleGrid>
    </VStack>
  );
};

// Courses Section Component
const CoursesSection: React.FC = () => {
  const courses = [
    {
      title: "Rocket Science 101",
      description: "Master the fundamentals of aerospace engineering and rocket propulsion systems.",
      progress: 85,
      illustration: Illus20,
      difficulty: "Intermediate",
      duration: "8 weeks"
    },
    {
      title: "Advanced Mathematics",
      description: "Deep dive into calculus, linear algebra, and differential equations.",
      progress: 60,
      illustration: Illus21,
      difficulty: "Advanced",
      duration: "12 weeks"
    },
    {
      title: "Engineering Fundamentals",
      description: "Learn the core principles of engineering design and problem-solving.",
      progress: 40,
      illustration: Illus22,
      difficulty: "Beginner",
      duration: "6 weeks"
    }
  ];

  return (
    <VStack spacing={8} align="stretch">
      <Box textAlign="center">
        <Heading size="xl" color="#5D5858" mb={4}>
          Your Learning Path
        </Heading>
        <Text fontSize="lg" color="#5D5858" opacity="0.8">
          Continue your journey with these carefully curated courses.
        </Text>
      </Box>

      <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={8}>
        {courses.map((course, index) => (
          <CourseCard key={index} {...course} />
        ))}
      </SimpleGrid>
    </VStack>
  );
};

// Achievements Section Component
const AchievementsSection: React.FC = () => {
  const achievements = [
    { title: "第一步", description: "完成您的第一门课程", earned: true },
    { title: "连续大师", description: "保持 7 天学习连续", earned: true },
    { title: "问题解决者", description: "解决 50 个练习题", earned: true },
    { title: "知识探索者", description: "完成 10 门课程", earned: false },
    { title: "AI 协作者", description: "进行 20 次 AI 导师会话", earned: false },
    { title: "专家级别", description: "达到高级熟练程度", earned: false },
  ];

  return (
    <VStack spacing={8} align="stretch">
      <Box textAlign="center">
        <Heading size="xl" color="#5D5858" mb={4}>
          您的成就
        </Heading>
        <Text fontSize="lg" color="#5D5858" opacity="0.8">
          庆祝您的学习里程碑并解锁新徽章。
        </Text>
      </Box>

      <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={6}>
        {achievements.map((achievement, index) => (
          <AchievementCard key={index} {...achievement} />
        ))}
      </SimpleGrid>
    </VStack>
  );
};

// Enhanced Component Definitions
interface StatsCardProps {
  title: string;
  value: string | number;
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
      p={6}
      position="relative"
      overflow="hidden"
      _hover={{ 
        transform: 'translateY(-5px)',
        boxShadow: '0 20px 60px rgba(93, 88, 88, 0.2)',
        transition: 'all 0.3s ease'
      }}
      animation={`${pulse} 3s ease-in-out infinite`}
    >
      <Flex justify="space-between" align="center">
        <VStack align="flex-start" spacing={2}>
          <Icon as={icon} size="24px" color={color} />
          <Text fontSize="sm" color="#5D5858" opacity="0.7">
            {title}
          </Text>
          <Text fontSize="2xl" fontWeight="bold" color="#5D5858">
            {value}
          </Text>
        </VStack>
        <Image 
          src={illustration} 
          alt={title} 
          w="60px" 
          h="60px"
          opacity="0.8"
          animation={`${float} 3s ease-in-out infinite`}
        />
      </Flex>
    </Box>
  );
};

interface MentorCardProps {
  name: string;
  role: string;
  description: string;
  illustration: string;
  onMeet: () => void;
  color: string;
}

const MentorCard: React.FC<MentorCardProps> = ({ 
  name, 
  role, 
  description, 
  illustration, 
  onMeet, 
  color 
}) => {
  return (
    <Box
      bg="white"
      borderRadius="20px"
      boxShadow="0 10px 40px rgba(93, 88, 88, 0.1)"
      p={8}
      _hover={{ 
        transform: 'translateY(-5px)',
        boxShadow: '0 20px 60px rgba(93, 88, 88, 0.2)',
        transition: 'all 0.3s ease'
      }}
    >
      <VStack spacing={6}>
        <Image 
          src={illustration} 
          alt={name} 
          w="120px" 
          h="120px"
          animation={`${float} 4s ease-in-out infinite`}
        />
        <VStack spacing={2} textAlign="center">
          <Heading size="lg" color="#5D5858">
            {name}
          </Heading>
          <Badge colorScheme="orange" borderRadius="full" px={3}>
            {role}
          </Badge>
          <Text color="#5D5858" opacity="0.8" lineHeight="1.6">
            {description}
          </Text>
        </VStack>
        <Button
          bg={color}
          color="white"
          size="lg"
          borderRadius="full"
          rightIcon={<ArrowForwardIcon />}
          _hover={{ 
            transform: 'scale(1.05)',
            boxShadow: `0 10px 30px ${color}40`
          }}
          onClick={onMeet}
        >
          安排会议
        </Button>
    </VStack>
    </Box>
  );
};

interface CourseCardProps {
  title: string;
  description: string;
  progress: number;
  illustration: string;
  difficulty: string;
  duration: string;
}

const CourseCard: React.FC<CourseCardProps> = ({ 
  title, 
  description, 
  progress, 
  illustration, 
  difficulty, 
  duration 
}) => {
  const difficultyColor = {
    'Beginner': 'green',
    'Intermediate': 'orange',
    'Advanced': 'red'
  }[difficulty] || 'gray';

  return (
    <Box
      bg="white"
      borderRadius="20px"
      boxShadow="0 10px 40px rgba(93, 88, 88, 0.1)"
      p={8}
      _hover={{ 
        transform: 'translateY(-5px)',
        boxShadow: '0 20px 60px rgba(93, 88, 88, 0.2)',
        transition: 'all 0.3s ease'
      }}
    >
      <VStack spacing={6} align="stretch">
        <Flex justify="space-between" align="center">
          <VStack align="flex-start" spacing={2} flex="1">
            <Heading size="md" color="#5D5858">
              {title}
            </Heading>
            <HStack spacing={3}>
              <Badge colorScheme={difficultyColor} borderRadius="full">
                {difficulty}
              </Badge>
              <Text fontSize="sm" color="#5D5858" opacity="0.7">
                {duration}
              </Text>
            </HStack>
          </VStack>
          <Image 
            src={illustration} 
            alt={title} 
            w="80px" 
            h="80px"
            animation={`${float} 3s ease-in-out infinite`}
          />
        </Flex>
        
        <Text color="#5D5858" opacity="0.8" lineHeight="1.6">
          {description}
        </Text>
        
        <Box>
          <Flex justify="space-between" mb={2}>
            <Text fontSize="sm" color="#5D5858" opacity="0.7">
              Progress
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
        
        <Button
          bg="#F47B4F"
          color="white"
          borderRadius="full"
          rightIcon={<ArrowForwardIcon />}
          _hover={{ 
            bg: '#E85A2B',
            transform: 'scale(1.02)'
          }}
        >
          继续学习
        </Button>
      </VStack>
    </Box>
  );
};

interface ActivityItemProps {
  title: string;
  time: string;
  type: 'completion' | 'achievement' | 'start';
}

const ActivityItem: React.FC<ActivityItemProps> = ({ title, time, type }) => {
  const getIcon = () => {
    switch (type) {
      case 'completion': return ExternalLinkIcon;
      case 'achievement': return StarIcon;
      case 'start': return ArrowForwardIcon;
      default: return ExternalLinkIcon;
    }
  };

  const getColor = () => {
    switch (type) {
      case 'completion': return '#F47B4F';
      case 'achievement': return '#FFB69B';
      case 'start': return '#5D5858';
      default: return '#F47B4F';
    }
  };

  return (
    <Flex align="center" p={4} borderRadius="12px" _hover={{ bg: '#FFE5C4' }} transition="all 0.2s">
      <Box
        p={2}
        borderRadius="full"
        bg={`${getColor()}20`}
        mr={4}
      >
        <ExternalLinkIcon color={getColor()} />
      </Box>
      <Box flex="1">
        <Text fontWeight="500" color="#5D5858">
          {title}
        </Text>
        <Text fontSize="sm" color="#5D5858" opacity="0.6">
          {time}
        </Text>
      </Box>
    </Flex>
  );
};

interface AchievementCardProps {
  title: string;
  description: string;
  earned: boolean;
}

const AchievementCard: React.FC<AchievementCardProps> = ({ title, description, earned }) => {
  return (
    <Box
      bg="white"
      borderRadius="16px"
      boxShadow="0 10px 40px rgba(93, 88, 88, 0.1)"
      p={6}
      opacity={earned ? 1 : 0.6}
      _hover={{ 
        transform: earned ? 'translateY(-3px)' : 'none',
        transition: 'all 0.3s ease'
      }}
    >
      <VStack spacing={4}>
        <Box
          w="60px"
          h="60px"
          borderRadius="full"
          bg={earned ? '#F47B4F' : '#E2E8F0'}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StarIcon 
            boxSize="30px" 
            color={earned ? 'white' : '#A0AEC0'} 
          />
        </Box>
        <VStack spacing={2} textAlign="center">
          <Heading size="sm" color="#5D5858">
            {title}
          </Heading>
          <Text fontSize="sm" color="#5D5858" opacity="0.7">
            {description}
          </Text>
          {earned && (
            <Badge colorScheme="orange" borderRadius="full">
              已获得
            </Badge>
          )}
        </VStack>
    </VStack>
    </Box>
  );
};

export default LearningPage;
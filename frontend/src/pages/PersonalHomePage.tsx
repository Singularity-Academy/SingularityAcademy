import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Container,
  Heading,
  Text,
  VStack,
  SimpleGrid,
  useColorModeValue,
  Avatar,
  useToast,
  Spinner,
} from '@chakra-ui/react';
import {getUserData} from '@utils/axios';
import Navbar from '@components/Navbar';
import Cookies from "js-cookie";
import {useNavigate} from "react-router-dom";

const PersonalHomePage: React.FC = () => {
  const toast = useToast();
  const navigate = useNavigate();
  const [user, setUser] = useState<{ id: number; name: string; email: string } | null>(null);
  const [loading, setLoading] = useState(true);

useEffect(() => {
    const fetchData = async () => {
        if (!Cookies.get('token')) {
            localStorage.removeItem('user');
            return;
        }

        setLoading(true);
        const User = await getUserData(toast, navigate);  // 使用 await 获取用户数据
        if (User) {
            setUser(User);
        }
        setLoading(false);
    };

    fetchData();
}, []);

  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBg = useColorModeValue('white', 'gray.700');

  return (
      <Box bg={bgColor} minH="100vh">
        <Container maxW="container.xl" py={20} mt={16}>
          <VStack spacing={10} align="center">
            {loading ? (
                <Spinner size="xl" />
            ) : (
                <>
                  <Avatar size="2xl" name={user?.name || 'User'} src="path/to/your/photo.jpg" />
                  <Heading as="h1" size="2xl" textAlign="center" bgGradient="linear(to-r, teal.400, blue.500)" bgClip="text">
                    Hello, I'm {user?.name || 'Your Name'}
                  </Heading>
                  <Text fontSize="xl" textAlign="center" maxW="2xl">
                    A passionate developer with a love for creating innovative solutions and a keen interest in AI and web technologies.
                  </Text>
                  <Button size="lg" colorScheme="teal" onClick={() => window.location.href = '/contact'}>
                    Get in Touch
                  </Button>
                </>
            )}
          </VStack>
        </Container>
          <Box bg={cardBg} py={20}>
              <Container maxW="container.xl">
                  <VStack spacing={12}>
                      <Heading textAlign="center" color="blue.500">
                          Skills
                      </Heading>
                      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10}>
                          <SkillCard title="JavaScript" description="Proficient in modern JavaScript and frameworks like React." />
                          <SkillCard title="Python" description="Experienced in Python for data analysis and machine learning." />
                          <SkillCard title="Golang" description="Familiar with building RESTful APIs using Go." />
                      </SimpleGrid>
                  </VStack>
              </Container>
          </Box>

          <Box py={20}>
              <Container maxW="container.xl">
                  <VStack spacing={12}>
                      <Heading textAlign="center" color="blue.500">
                          Projects
                      </Heading>
                      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10}>
                          <ProjectCard title="Project One" description="A web application that does XYZ." />
                          <ProjectCard title="Project Two" description="An AI model that predicts ABC." />
                          <ProjectCard title="Project Three" description="A mobile app for managing tasks." />
                      </SimpleGrid>
                  </VStack>
              </Container>
          </Box>

          <Box bg={cardBg} py={20}>
              <Container maxW="container.xl">
                  <VStack spacing={6} textAlign="center">
                      <Heading color="blue.500">Let's Connect</Heading>
                      <Text fontSize="lg" maxW="2xl">
                          I'm always open to discussing new projects or opportunities. Feel free to reach out!
                      </Text>
                      <Button size="lg" colorScheme="blue" onClick={() => window.location.href = '/contact'}>
                          Contact Me
                      </Button>
                  </VStack>
              </Container>
          </Box>
      </Box>
  );
};

// SkillCard 组件
interface SkillCardProps {
  title: string;
  description: string;
}

const SkillCard: React.FC<SkillCardProps> = ({ title, description }) => {
  return (
      <VStack
          p={8}
          bg={useColorModeValue('white', 'gray.800')}
          borderRadius="lg"
          boxShadow="xl"
          spacing={4}
          align="center"
          _hover={{ transform: 'translateY(-5px)', transition: '0.3s' }}
      >
        <Heading size="md">{title}</Heading>
        <Text color="gray.600" textAlign="center">{description}</Text>
      </VStack>
  );
};

// ProjectCard 组件
interface ProjectCardProps {
  title: string;
  description: string;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ title, description }) => {
  return (
      <VStack
          p={8}
          bg={useColorModeValue('white', 'gray.800')}
          borderRadius="lg"
          boxShadow="xl"
          spacing={4}
          align="center"
          _hover={{ transform: 'translateY(-5px)', transition: '0.3s' }}
      >
        <Heading size="md">{title}</Heading>
        <Text color="gray.600" textAlign="center">{description}</Text>
      </VStack>
  );
};

export default PersonalHomePage;

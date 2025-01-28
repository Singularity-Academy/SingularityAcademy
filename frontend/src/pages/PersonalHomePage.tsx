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
  Spinner,  // 引入 Spinner 组件
} from '@chakra-ui/react';
import axiosInstance, { getToastMessage } from '../utils/axios';
import { API_ENDPOINTS, ErrorResponse } from '../config/api';
import { AxiosError } from 'axios';
import Navbar from '../components/Navbar';

const PersonalHomePage: React.FC = () => {
  const toast = useToast();
  const [user, setUser] = useState<{ id: number; name: string; email: string }>({
    id: 0,
    name: '',
    email: '',
  });
  const [loading, setLoading] = useState(true);  // 新增加载状态

  // 通过 axios 请求后端数据并更新 user 状态
  useEffect(() => {
    axiosInstance
        .get(API_ENDPOINTS.ME)
        .then((response) => {
          setUser(response.data);  // 更新 user 状态
          setLoading(false);  // 请求完成，关闭加载状态
        })
        .catch((err) => {
          const error = err as AxiosError<ErrorResponse>;
          toast(getToastMessage(error));
          setLoading(false);  // 请求失败时关闭加载状态
        });
  }, []); // 依赖数组为空，表示组件挂载时只执行一次

  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBg = useColorModeValue('white', 'gray.700');

  return (
      <Box bg={bgColor} minH="100vh">
        <Navbar />
        <Container maxW="container.xl" py={20} mt={16}>
          <VStack spacing={10} align="center">
            {loading ? (  // 如果加载中，显示 Spinner
                <Spinner size="xl" />
            ) : (
                <>
                  <Avatar size="2xl" name={user.name} src="path/to/your/photo.jpg" />
                  <Heading as="h1" size="2xl" textAlign="center" bgGradient="linear(to-r, teal.400, blue.500)" bgClip="text">
                    Hello, I'm {user.name || 'Your Name'}
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

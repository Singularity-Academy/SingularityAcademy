import React, { useState } from 'react';
import {
  Box,
  Button,
  Heading,
  Text,
  VStack,
  SimpleGrid,
  useColorModeValue,
} from '@chakra-ui/react';
import Navbar from "@components/Navbar";
import {useNavigate} from "react-router-dom";

const LearningPage: React.FC = () => {
  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBg = useColorModeValue('white', 'gray.700');
  const navigate = useNavigate();
  const [selectedSection, setSelectedSection] = useState<string>('overview');

  const renderContent = () => {
    switch (selectedSection) {
      case 'overview':
        return (
          <VStack spacing={10} align="center">
            <Heading as="h1" size="2xl" textAlign="center" color="blue.500">
              Your Learning Journey
            </Heading>
            <Text fontSize="xl" textAlign="center" maxW="2xl">
              Welcome to your personalized learning dashboard. Here, you can track your progress and interact with your AI mentors.
            </Text>
          </VStack>
        );
      case 'meeting':
        return (
          <VStack spacing={6} textAlign="center">
            <Heading color="blue.500">Schedule a Meeting</Heading>
            <Text fontSize="lg" maxW="2xl">
              Choose a meeting with your Principal or Dean to discuss your learning targets and schedule.
            </Text>
            <Button size="lg" colorScheme="blue" onClick={() => navigate("/course/interaction?AI=Principal")}>
              Meet with Principal AI
            </Button>
            <Button size="lg" colorScheme="teal" onClick={() => navigate("/course/interaction?AI=Dean")}>
              Meet with Dean AI
            </Button>
          </VStack>
        );
      case 'courses':
        return (
          <VStack spacing={12}>
            <Heading textAlign="center" color="blue.500">
              Courses You Are Taking
            </Heading>
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10}>
              <CourseCard title="Rocket Science 101" description="An introduction to the principles of rocket science." />
              <CourseCard title="Advanced Mathematics" description="Deep dive into calculus and linear algebra." />
              <CourseCard title="Engineering Fundamentals" description="Learn the basics of engineering design and analysis." />
            </SimpleGrid>
          </VStack>
        );
      default:
        return null;
    }
  };

  return (
    <Box bg={bgColor} minH="100vh" display="flex">
      {/* Sidebar */}
      <Box width="250px" bg={cardBg} p={5} boxShadow="md" mt={16}>
        <VStack spacing={5} align="start">
          <Heading size="md" color="blue.500">Navigation</Heading>
          <Button
            variant="link"
            onClick={() => setSelectedSection('overview')}
            color={selectedSection === 'overview' ? 'blue.500' : 'gray.600'}
          >
            Overview
          </Button>
          <Button
            variant="link"
            onClick={() => setSelectedSection('meeting')}
            color={selectedSection === 'meeting' ? 'blue.500' : 'gray.600'}
          >
            Schedule a Meeting
          </Button>
          <Button
            variant="link"
            onClick={() => setSelectedSection('courses')}
            color={selectedSection === 'courses' ? 'blue.500' : 'gray.600'}
          >
            Courses
          </Button>
        </VStack>
      </Box>

      {/* Main Content */}
      <Box flex="1" p={10} mt={16}>
        {renderContent()}
      </Box>
    </Box>
  );
};

interface DeanCardProps {
  title: string;
  description: string;
}

const DeanCard: React.FC<DeanCardProps> = ({ title, description }) => {
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

interface CourseCardProps {
  title: string;
  description: string;
}

const CourseCard: React.FC<CourseCardProps> = ({ title, description }) => {
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

export default LearningPage; 
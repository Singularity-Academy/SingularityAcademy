import React from 'react';
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
} from '@chakra-ui/react';

const LearningPage: React.FC = () => {
  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBg = useColorModeValue('white', 'gray.700');

  return (
    <Box bg={bgColor} minH="100vh">
      <Container maxW="container.xl" py={20}>
        <VStack spacing={10} align="center">
          <Heading as="h1" size="2xl" textAlign="center" color="blue.500">
            Your Learning Journey
          </Heading>
          <Text fontSize="xl" textAlign="center" maxW="2xl">
            Welcome to your personalized learning dashboard. Here, you can track your progress and interact with your AI mentors.
          </Text>
        </VStack>
      </Container>

      {/* Principal AI Section */}
      <Box bg={cardBg} py={20}>
        <Container maxW="container.xl">
          <VStack spacing={12}>
            <Heading textAlign="center" color="blue.500">
              Meet Your Principal AI
            </Heading>
            <VStack spacing={4} align="center">
              <Avatar size="2xl" name="Principal AI" bg="blue.500" color="white" />
              <Text fontSize="lg" textAlign="center">
                Your Principal AI designs your overall learning path based on your goals. Whether you want to build rockets or explore AI, your path is tailored just for you!
              </Text>
            </VStack>
          </VStack>
        </Container>
      </Box>

      {/* Dean AI Section */}
      <Box py={20}>
        <Container maxW="container.xl">
          <VStack spacing={12}>
            <Heading textAlign="center" color="blue.500">
              Meet Your Dean AI
            </Heading>
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10}>
              <DeanCard title="Physics" description="Breaks down physics into detailed units and steps." />
              <DeanCard title="Mathematics" description="Guides you through mathematical concepts and applications." />
              <DeanCard title="Engineering" description="Provides insights into engineering principles and practices." />
            </SimpleGrid>
          </VStack>
        </Container>
      </Box>

      {/* Courses Section */}
      <Box bg={cardBg} py={20}>
        <Container maxW="container.xl">
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
        </Container>
      </Box>

      {/* Assistant AI Section */}
      <Box py={20}>
        <Container maxW="container.xl" textAlign="center">
          <VStack spacing={6}>
            <Heading color="blue.500">Meet Your Assistant AI</Heading>
            <Text fontSize="lg" maxW="2xl">
              Your Assistant AI is here to help with homework and exercises. Ask questions and get instant feedback!
            </Text>
            <Button size="lg" colorScheme="blue" onClick={() => alert('Chat with your Assistant AI!')}>
              Chat with Assistant AI
            </Button>
          </VStack>
        </Container>
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
import React from 'react';
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
  Divider,
} from '@chakra-ui/react';
import Navbar from '../components/Navbar';
import Cookies from 'js-cookie';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const buttonBg = useColorModeValue('blue.500', 'blue.200');
  const cardBg = useColorModeValue('white', 'gray.700');
  const isLoggedIn = !!Cookies.get('token');

  return (
    <Box bg={bgColor} minH="100vh">
      {isLoggedIn && <Navbar />}
      <Box pt={isLoggedIn ? '64px' : 0}>
        {/* Hero Section */}
        <Container maxW="container.xl" py={20}>
          <VStack spacing={10} align="center">
            <Heading
              as="h1"
              size="2xl"
              textAlign="center"
              bgGradient="linear(to-r, blue.400, purple.500)"
              bgClip="text"
            >
              Welcome to AI Online School
            </Heading>
            
            <Text fontSize="xl" textAlign="center" maxW="2xl">
              Transform your learning experience with AI-powered education. 
              Join our platform to access personalized learning paths and 
              interactive content.
            </Text>

            <HStack spacing={6}>
              <Button
                size="lg"
                bg={buttonBg}
                color="white"
                _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
                onClick={() => navigate('/register')}
              >
                Get Started
              </Button>
              <Button
                size="lg"
                variant="outline"
                _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
                onClick={() => navigate('/login')}
              >
                Sign In
              </Button>
            </HStack>
          </VStack>
        </Container>

        {/* Features Section */}
        <Box bg={cardBg} py={20}>
          <Container maxW="container.xl">
            <VStack spacing={12}>
              <Heading textAlign="center" color="blue.500">
                Key Features
              </Heading>
              <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10}>
                <Feature
                  title="AI-Powered Learning"
                  description="Personalized learning paths adapted to your pace and style"
                  icon="🤖"
                />
                <Feature
                  title="An entire school for your ONLY"
                  description="Every student will have a pesonalized school, a group of educators, including principle, deans, and teachers,."
                  icon="👨‍🏫"
                />
                <Feature
                  title="Interactive Content"
                  description="Engage with dynamic content and real-time feedback"
                  icon="💡"
                />
              </SimpleGrid>
            </VStack>
          </Container>
        </Box>

        {/* Founders Section */}
        <Box py={20}>
          <Container maxW="container.xl">
            <VStack spacing={12}>
              <Heading textAlign="center" color="blue.500">
                Meet Our Founders
              </Heading>
              <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10}>
                <FounderCard
                  name="Jiace Zhao"
                  role="CEO & AI Research Lead"
                  bio="Highschool student, interested in AI and machine learning. Built multiple AI projects and won multiple hackathons."
                  image=""
                />
                <FounderCard
                  name="Di Huang"
                  role = "CTO & Backend Platform Architecture"
                  bio="Ph.D. in Computer Science from MIT, holding Bachelor from University of Oxford."
                  image=""
                />
              </SimpleGrid>
            </VStack>
          </Container>
        </Box>

        {/* Statistics Section */}
        <Box bg={cardBg} py={20}>
          <Container maxW="container.xl">
            <SimpleGrid columns={{ base: 1, md: 4 }} spacing={10}>
              <Stat number="50,000+" label="Active Students" />
              <Stat number="200+" label="Expert Instructors" />
              <Stat number="1,000+" label="Courses" />
              <Stat number="98%" label="Student Satisfaction" />
            </SimpleGrid>
          </Container>
        </Box>

        {/* Contact Section */}
        <Box py={20}>
          <Container maxW="container.xl" textAlign="center">
            <VStack spacing={6}>
              <Heading color="blue.500">Start Your Learning Journey Today</Heading>
              <Text fontSize="lg" maxW="2xl">
               Join Our Community.
              </Text>
              <Button
                size="lg"
                colorScheme="blue"
                onClick={() => navigate('/register')}
              >
                Begin Your Journey
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

const Feature: React.FC<FeatureProps> = ({ title, description, icon }) => {
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
      <Text fontSize="4xl">{icon}</Text>
      <Heading size="md">{title}</Heading>
      <Text color="gray.600" textAlign="center">{description}</Text>
    </VStack>
  );
};

interface FounderCardProps {
  name: string;
  role: string;
  bio: string;
  image: string;
}

const FounderCard: React.FC<FounderCardProps> = ({ name, role, bio, image }) => {
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
        {image ? (
          <Image
            src={image}
            alt={name}
            borderRadius="full"
            boxSize="150px"
            objectFit="cover"
          />
        ) : (
          <Avatar size="2xl" name={name} bg="blue.500" color="white" />
        )}
        <Heading size="md">{name}</Heading>
        <Text color="blue.500" fontWeight="bold">{role}</Text>
        <Text color="gray.600" textAlign="center">{bio}</Text>
      </VStack>
    );
  };

interface StatProps {
  number: string;
  label: string;
}

const Stat: React.FC<StatProps> = ({ number, label }) => {
  return (
    <VStack spacing={2} textAlign="center">
      <Heading size="2xl" color="blue.500">
        {number}
      </Heading>
      <Text fontSize="lg" color="gray.600">
        {label}
      </Text>
    </VStack>
  );
};

export default HomePage; 
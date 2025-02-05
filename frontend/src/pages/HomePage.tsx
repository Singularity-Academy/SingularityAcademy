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
} from '@chakra-ui/react';
import Navbar from '@components/Navbar';
import { useTranslation } from 'react-i18next';

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

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const buttonBg = useColorModeValue('blue.500', 'blue.200');
  const cardBg = useColorModeValue('white', 'gray.700');
  const { t, i18n, ready } = useTranslation();

  // Safely get translated resources with fallbacks
  const features: Feature[] = t('HomePage.features', { returnObjects: true }) || [];
  const founders: Founder[] = t('HomePage.founders', { returnObjects: true }) || [];
  const visions: Vision[] = t('HomePage.visions', { returnObjects: true }) || [];

  if (!ready) {
    return <div>Loading translations...</div>;
  }

  return (
    <Box bg={bgColor} minH="100vh">
      <Box pt='64px'>
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
              {t("HomePage.welcome")}
            </Heading>
            
            <Text fontSize="xl" textAlign="center" maxW="2xl">
              {t("HomePage.description")}
            </Text>

            <HStack spacing={6}>
              <Button
                size="lg"
                bg={buttonBg}
                color="white"
                _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
                onClick={() => navigate('/register')}
              >
                {t("HomePage.getStarted")}
              </Button>
              <Button
                size="lg"
                variant="outline"
                _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
                onClick={() => navigate('/login')}
              >
                {t("common.signIn")}
              </Button>
            </HStack>
          </VStack>
        </Container>

        {/* Features Section */}
        {features?.length > 0 && (
          <FeatureSection features={features} />
        )}

        {/* Founders Section */}
        {founders?.length > 0 && (
          <FounderSection founders={founders} />
        )}

        {/* Statistics Section */}
        {visions?.length > 0 && (
          <VisionSection visions={visions} />
        )}

        {/* Contact Section */}
        <Box py={20}>
          <Container maxW="container.xl" textAlign="center">
            <VStack spacing={6}>
              <Heading color="blue.500">{t("HomePage.journey")}</Heading>
              <Text fontSize="lg" maxW="2xl">
                {t("HomePage.join")}
              </Text>
              <Button
                size="lg"
                colorScheme="blue"
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
  return (
    <Box bg={useColorModeValue('white', 'gray.700')} py={20}>
      <Container maxW="container.xl">
        <VStack spacing={12}>
          <Heading textAlign="center" color="blue.500">
            {t("HomePage.feature")}
          </Heading>
          <SimpleGrid columns={{ base: 1, md: features.length }} spacing={10}>
            {features.map((feature, index) => (
              <FeatureCard key={index} {...feature} />
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
    <Box py={20}>
      <Container maxW="container.xl">
        <VStack spacing={12}>
          <Heading textAlign="center" color="blue.500">
            {t("HomePage.founder")}
          </Heading>
          <SimpleGrid columns={{ base: 1, md: founders.length }} spacing={10}>
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
  return (
    <Box bg={useColorModeValue('white', 'gray.700')} py={20}>
      <Container maxW="container.xl">
        <VStack align="center">
          <Heading color="blue.500" textAlign="center">
            {t('HomePage.vision')}
          </Heading>
          {visions.map((vision, index) => (
            <Text
              key={index}
              fontSize="lg"
              maxW="2xl"
              textAlign="center"
              color={vision.color || undefined}
            >
              {vision.content}
            </Text>
          ))}
        </VStack>
      </Container>
    </Box>
  );
};

const FeatureCard: React.FC<FeatureProps> = ({ title, description, icon }) => {
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

export default HomePage;
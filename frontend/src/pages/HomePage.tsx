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

  // Use same background color for the entire page
  const bgColor = useColorModeValue('background.primary', 'background.dark'); // Beige background
  const cardBg = useColorModeValue('background.secondary', 'gray.700'); // White cards
  const buttonBg = useColorModeValue('accent.black', 'accent.black'); // Black buttons
  const textColor = useColorModeValue('text.primary', 'white');
  const mutedColor = useColorModeValue('text.secondary', 'gray.400');
  const dividerColor = useColorModeValue('gray.300', 'gray.600'); // Slightly darker for more visibility
  const black = useColorModeValue('black', 'white');

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
              color={textColor}
              fontWeight="semibold"
              lineHeight="1.2"
            >
              {t("HomePage.welcome")}
            </Heading>

            <Text fontSize="xl" textAlign="center" maxW="2xl" color={mutedColor}>
              {t("HomePage.description")}
            </Text>

            <HStack spacing={6}>
              <Button
                size="lg"
                bg={buttonBg}
                color="white"
                _hover={{
                  transform: 'translateY(-2px)',
                  boxShadow: 'md',
                  textDecoration: 'underline'
                }}
                onClick={() => navigate('/register')}
                height="56px"
                px={8}
              >
                {t("HomePage.getStarted")}
              </Button>
              <Button
                size="lg"
                variant="outline"
                borderColor="accent.black"
                color="accent.black"
                _hover={{
                  transform: 'translateY(-2px)',
                  boxShadow: 'md',
                  textDecoration: 'underline'
                }}
                onClick={() => navigate('/login')}
                height="56px"
                px={8}
              >
                {t("common.signIn")}
              </Button>
            </HStack>
          </VStack>
        </Container>

        {/* Thicker and shorter divider */}
        <Box py={4}>
          <Divider
            borderColor={black}
            borderWidth="1px"
            maxW="1000px"
            mx="auto"
          />
        </Box>

        {/* Features Section */}
        {features?.length > 0 && (
          <>
            <Container maxW="container.xl" py={20}>
              <VStack spacing={12}>
                <Heading textAlign="center" color={textColor}>
                  {t("HomePage.feature")}
                </Heading>
                <SimpleGrid columns={{ base: 1, md: features.length }} spacing={10}>
                  {features.map((feature, index) => (
                    <FeatureCard key={index} {...feature} />
                  ))}
                </SimpleGrid>
              </VStack>
            </Container>

        <Box py={4}>
          <Divider
            borderColor={black}
            borderWidth="1px"
            maxW="1000px"
            mx="auto"
          />
        </Box>
          </>
        )}

        {/* Founders Section */}
        {founders?.length > 0 && (
          <>
            <Container maxW="container.xl" py={20}>
              <VStack spacing={12}>
                <Heading textAlign="center" color={textColor}>
                  {t("HomePage.founder")}
                </Heading>
                <SimpleGrid columns={{ base: 1, md: founders.length }} spacing={10}>
                  {founders.map((founder, index) => (
                    <FounderCard key={index} {...founder} />
                  ))}
                </SimpleGrid>
              </VStack>
            </Container>

        <Box py={4}>
          <Divider
            borderColor={black}
            borderWidth="1px"
            maxW="1000px"
            mx="auto"
          />
        </Box>
          </>
        )}

        {/* Vision Section */}
        {visions?.length > 0 && (
          <>
            <Container maxW="container.xl" py={20}>
              <VStack align="center">
                <Heading color={textColor} textAlign="center">
                  {t('HomePage.vision')}
                </Heading>
                {/* Small centered divider below heading */}
                <Box py={4}>
                  <Divider
                    borderColor={dividerColor}
                    borderWidth="2px"
                    maxW="100px"
                    mx="auto"
                  />
                </Box>
                {visions.map((vision, index) => (
                  <Text
                    key={index}
                    fontSize="lg"
                    maxW="2xl"
                    textAlign="center"
                    color={vision.color || mutedColor}
                  >
                    {vision.content}
                  </Text>
                ))}
              </VStack>
            </Container>

        <Box py={4}>
          <Divider
            borderColor={black}
            borderWidth="1px"
            maxW="1000px"
            mx="auto"
          />
        </Box>
          </>
        )}

        {/* Contact Section */}
        <Container maxW="container.xl" py={20} textAlign="center">
          <VStack spacing={8}>
            <Heading color={textColor}>{t("HomePage.journey")}</Heading>
            <Text fontSize="lg" maxW="2xl" color={mutedColor}>
              {t("HomePage.join")}
            </Text>
            <Button
              size="lg"
              bg={buttonBg}
              color="white"
              height="56px"
              px={8}
              _hover={{
                transform: 'translateY(-2px)',
                boxShadow: 'md',
                textDecoration: 'underline'
              }}
              onClick={() => navigate('/register')}
            >
              {t('HomePage.start')}
            </Button>
          </VStack>
        </Container>
      </Box>
    </Box>
  );
};

// Feature card with white background to stand out from beige page background
const FeatureCard: React.FC<Feature> = ({ title, description, icon }) => {
  const cardBg = useColorModeValue('background.secondary', 'gray.800'); // White card
  const textColor = useColorModeValue('text.primary', 'white');
  const mutedColor = useColorModeValue('text.secondary', 'gray.400');

  return (
    <VStack
      p={8}
      bg={cardBg}
      borderRadius="xl"
      boxShadow="sm"
      border="1px solid"
      borderColor="gray.100"
      spacing={4}
      align="center"
      _hover={{ transform: 'translateY(-5px)', boxShadow: 'md', transition: '0.3s' }}
    >
      <Text fontSize="4xl">{icon}</Text>
      <Heading size="md" color={textColor}>{title}</Heading>
      <Text color={mutedColor} textAlign="center">{description}</Text>
    </VStack>
  );
};

// Founder card with white background to stand out from beige page background
const FounderCard: React.FC<Founder> = ({ name, role, bio, image }) => {
  const cardBg = useColorModeValue('background.secondary', 'gray.800'); // White card
  const textColor = useColorModeValue('text.primary', 'white');
  const mutedColor = useColorModeValue('text.secondary', 'gray.400');
  const accentColor = useColorModeValue('accent.coral', 'accent.coral');

  return (
    <VStack
      p={8}
      bg={cardBg}
      borderRadius="xl"
      boxShadow="sm"
      border="1px solid"
      borderColor="gray.100"
      spacing={4}
      align="center"
      _hover={{ transform: 'translateY(-5px)', boxShadow: 'md', transition: '0.3s' }}
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
        <Avatar size="2xl" name={name} bg={accentColor} color="white" />
      )}
      <Heading size="md" color={textColor}>{name}</Heading>
      <Text color={accentColor} fontWeight="bold">{role}</Text>
      <Text color={mutedColor} textAlign="center">{bio}</Text>
    </VStack>
  );
};

export default HomePage;
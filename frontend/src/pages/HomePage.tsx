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
import { keyframes } from '@emotion/react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';

// Create motion components
const MotionBox = motion(Box);
const MotionVStack = motion(VStack);
const MotionHeading = motion(Heading);
const MotionText = motion(Text);

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

// Gradient animation
const gradientAnimation = keyframes`
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
`;

// Floating animation
const float = keyframes`
  0% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0px); }
`;

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const bgColor = useColorModeValue('background.primary', 'background.dark');
  const buttonBg = useColorModeValue('accent.black', 'accent.black');
  const textColor = useColorModeValue('text.primary', 'white');
  const mutedColor = useColorModeValue('text.secondary', 'gray.400');
  const accentColor = useColorModeValue('accent.coral', 'accent.coral');
  const black = useColorModeValue('black', 'white');

  const { t, i18n, ready } = useTranslation();

  const features: Feature[] = t('HomePage.features', { returnObjects: true }) || [];
  const founders: Founder[] = t('HomePage.founders', { returnObjects: true }) || [];
  const visions: Vision[] = t('HomePage.visions', { returnObjects: true }) || [];

  if (!ready) {
    return <div>Loading translations...</div>;
  }

  return (
    <Box bg={bgColor} minH="100vh" position="relative" overflow="hidden">
      {/* Animated background gradient */}
      <Box
        position="absolute"
        top="-50%"
        right="-20%"
        width="100%"
        height="100%"
        opacity={0.03}
        background="radial-gradient(circle at 20% 80%, #e89980 0%, transparent 50%)"
        filter="blur(40px)"
        animation={`${gradientAnimation} 15s ease infinite`}
      />

      <Box pt='64px' position="relative">
        {/* Hero Section with animations */}
        <Container maxW="container.xl" py={20}>
          <MotionVStack
            spacing={10}
            align="center"
            initial={{ y: 20 }} // opacity: 0 removed
            animate={{ y: 0 }}   // opacity: 1 removed
            transition={{ duration: 0.8, staggerChildren: 0.2 }} // Restored
          >
            <MotionHeading
              as="h1"
              size="2xl"
              textAlign="center"
              color={textColor}
              fontWeight="semibold"
              lineHeight="1.2"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              bgGradient={`linear(to-r, ${textColor}, ${accentColor})`}
              bgClip="text"
              _hover={{
                bgGradient: `linear(to-l, ${textColor}, ${accentColor})`,
                transition: 'all 0.5s ease',
              }}
            >
              {t("HomePage.welcome")}
            </MotionHeading>

            <MotionText
              fontSize="xl"
              textAlign="center"
              maxW="2xl"
              color={mutedColor}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.5 }}
            >
              {t("HomePage.description")}
            </MotionText>

            <MotionBox
              initial={{ scale: 0.9 }} // opacity: 0 removed
              animate={{ scale: 1 }}   // opacity: 1 removed
              transition={{ delay: 0.6, duration: 0.5 }} // Restored for original animation
            >
              <HStack spacing={6}>
                <Button
                  size="lg"
                  bg={buttonBg}
                  color="white"
                  position="relative"
                  overflow="hidden"
                  _before={{
                    content: '""',
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    width: '0',
                    height: '0',
                    bg: accentColor,
                    borderRadius: 'full',
                    transform: 'translate(-50%, -50%)',
                    transition: 'width 0.6s, height 0.6s',
                    color: 'white',
                  }}
                  _hover={{
                    transform: 'translateY(-2px)',
                    boxShadow: 'lg',
                    _before: {
                      width: '300px',
                      height: '300px',
                    },
                  }}
                  onClick={() => navigate('/register')}
                  height="56px"
                  px={8}
                  zIndex={1}
                >
                  <Text position="relative" zIndex={2}>{t("HomePage.getStarted")}</Text>
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  borderColor="accent.black"
                  color="accent.black"
                  position="relative"
                  overflow="hidden"
                  _hover={{
                    bg: 'accent.black',
                    color: 'white',
                    transform: 'translateY(-2px)',
                    boxShadow: 'lg',
                    borderColor: 'transparent',
                  }}
                  onClick={() => navigate('/login')}
                  height="56px"
                  px={8}
                  transition="all 0.3s ease"
                >
                  {t("common.signIn")}
                </Button>
              </HStack>
            </MotionBox>
          </MotionVStack>
        </Container>

        {/* Modern animated divider */}
        <Box py={4} position="relative">
          <Box
            height="1px"
            maxW="1000px"
            mx="auto"
            bgGradient={`linear(to-r, transparent, ${black}, transparent)`}
            position="relative"
            _after={{
              content: '""',
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: '60px',
              height: "3px",
              bg: accentColor,
              borderRadius: 'full',
            }}
          />
        </Box>

        {/* Features Section with stagger animation */}
        {features?.length > 0 && (
          <>
            <Container maxW="container.xl" py={20}>
              <VStack spacing={12}>
                <MotionHeading
                  textAlign="center"
                  color={textColor}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6 }}
                >
                  {t("HomePage.feature")}
                </MotionHeading>
                <SimpleGrid columns={{ base: 1, md: features.length }} spacing={10}>
                  {features.map((feature, index) => (
                    <MotionBox
                      key={index}
                      initial={{ opacity: 0, y: 30 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ delay: index * 0.1, duration: 0.5 }}
                    >
                      <FeatureCard {...feature} />
                    </MotionBox>
                  ))}
                </SimpleGrid>
              </VStack>
            </Container>

            <Box py={4} position="relative">
              <Box
                height="1px"
                maxW="1000px"
                mx="auto"
                bgGradient={`linear(to-r, transparent, ${black}, transparent)`}
              />
            </Box>
          </>
        )}

        {/* Founders Section with parallax effect */}
        {founders?.length > 0 && (
          <>
            <Container maxW="container.xl" py={20}>
              <VStack spacing={12}>
                <MotionHeading
                  textAlign="center"
                  color={textColor}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6 }}
                >
                  {t("HomePage.founder")}
                </MotionHeading>
                <SimpleGrid columns={{ base: 1, md: founders.length }} spacing={10}>
                  {founders.map((founder, index) => (
                    <MotionBox
                      key={index}
                      initial={{ opacity: 0, scale: 0.9 }}
                      whileInView={{ opacity: 1, scale: 1 }}
                      viewport={{ once: true }}
                      transition={{ delay: index * 0.1, duration: 0.5 }}
                    >
                      <FounderCard {...founder} />
                    </MotionBox>
                  ))}
                </SimpleGrid>
              </VStack>
            </Container>

            <Box py={4} position="relative">
              <Box
                height="1px"
                maxW="1000px"
                mx="auto"
                bgGradient={`linear(to-r, transparent, ${black}, transparent)`}
              />
            </Box>
          </>
        )}

        {/* Vision Section with fade effect */}
        {visions?.length > 0 && (
          <>
            <Container maxW="container.xl" py={20}>
              <VStack align="center" spacing={8}>
                <MotionHeading
                  color={textColor}
                  textAlign="center"
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6 }}
                >
                  {t('HomePage.vision')}
                </MotionHeading>

                <Box
                  width="60px"
                  height="3px"
                  bg={accentColor}
                  borderRadius="full"
                  mb={4}
                />

                {visions.map((vision, index) => (
                  <MotionText
                    key={index}
                    fontSize="lg"
                    maxW="2xl"
                    textAlign="center"
                    color={vision.color || mutedColor}
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.2, duration: 0.8 }}
                  >
                    {vision.content}
                  </MotionText>
                ))}
              </VStack>
            </Container>

            <Box py={4} position="relative">
              <Box
                height="1px"
                maxW="1000px"
                mx="auto"
                bgGradient={`linear(to-r, transparent, ${black}, transparent)`}
              />
            </Box>
          </>
        )}

        {/* Contact Section with CTA animation */}
        <Container maxW="container.xl" py={20} textAlign="center">
          <MotionVStack
            spacing={8}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <Heading color={textColor}>{t("HomePage.journey")}</Heading>
            <Text fontSize="lg" maxW="2xl" color={mutedColor}>
              {t("HomePage.join")}
            </Text>
            <MotionBox
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Button
                size="lg"
                bg={buttonBg}
                color="white"
                height="56px"
                px={8}
                boxShadow="xl"
                _hover={{
                  bg: 'gray.700',
                  transform: 'translateY(-2px)',
                  boxShadow: '2xl',
                }}
                onClick={() => navigate('/register')}
              >
                {t('HomePage.start')}
              </Button>
            </MotionBox>
          </MotionVStack>
        </Container>
      </Box>
    </Box>
  );
};

// Enhanced Feature Card
const FeatureCard: React.FC<Feature> = ({ title, description, icon }) => {
  const cardBg = useColorModeValue('background.secondary', 'gray.800');
  const textColor = useColorModeValue('text.primary', 'white');
  const mutedColor = useColorModeValue('text.secondary', 'gray.400');
  const accentColor = useColorModeValue('accent.coral', 'accent.coral');

  return (
    <VStack
      p={8}
      bg={cardBg}
      borderRadius="2xl"
      boxShadow="xl"
      border="1px solid"
      borderColor="gray.100"
      spacing={4}
      align="center"
      position="relative"
      overflow="hidden"
      _before={{
        content: '""',
        position: 'absolute',
        top: '-50%',
        right: '-50%',
        width: '200%',
        height: '200%',
        bg: `radial-gradient(circle, ${accentColor}22 0%, transparent 70%)`,
        opacity: 0,
        transition: 'opacity 0.3s ease',
      }}
      _hover={{
        transform: 'translateY(-8px)',
        boxShadow: '2xl',
        borderColor: accentColor,
        _before: {
          opacity: 1,
        },
      }}
      transition="all 0.3s ease"
      cursor="pointer"
    >
      <Box
        fontSize="4xl"
        animation={`${float} 3s ease-in-out infinite`}
      >
        {icon}
      </Box>
      <Heading size="md" color={textColor}>{title}</Heading>
      <Text color={mutedColor} textAlign="center">{description}</Text>
    </VStack>
  );
};

// Enhanced Founder Card
const FounderCard: React.FC<Founder> = ({ name, role, bio, image }) => {
  const cardBg = useColorModeValue('background.secondary', 'gray.800');
  const textColor = useColorModeValue('text.primary', 'white');
  const mutedColor = useColorModeValue('text.secondary', 'gray.400');
  const accentColor = useColorModeValue('accent.coral', 'accent.coral');

  return (
    <VStack
      p={8}
      bg={cardBg}
      borderRadius="2xl"
      boxShadow="xl"
      border="1px solid"
      borderColor="gray.100"
      spacing={4}
      align="center"
      position="relative"
      overflow="hidden"
      _hover={{
        transform: 'translateY(-8px) rotateY(5deg)',
        boxShadow: '2xl',
        borderColor: accentColor,
      }}
      transition="all 0.3s ease"
      cursor="pointer"
      style={{ transformStyle: 'preserve-3d' }}
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
            borderColor={accentColor}
            _hover={{
              borderColor: textColor,
            }}
            transition="all 0.3s ease"
          />
        ) : (
          <Avatar
            size="2xl"
            name={name}
            bg={accentColor}
            color="white"
            border="4px solid"
            borderColor={accentColor}
          />
        )}
        <Box
          position="absolute"
          bottom="-5px"
          right="-5px"
          width="40px"
          height="40px"
          bg={accentColor}
          borderRadius="full"
          display="flex"
          alignItems="center"
          justifyContent="center"
          fontSize="20px"
          boxShadow="lg"
        >
          ✨
        </Box>
      </Box>
      <Heading size="md" color={textColor}>{name}</Heading>
      <Text
        color={accentColor}
        fontWeight="bold"
        textTransform="uppercase"
        fontSize="sm"
        letterSpacing="wider"
      >
        {role}
      </Text>
      <Text color={mutedColor} textAlign="center">{bio}</Text>
    </VStack>
  );
};

export default HomePage;

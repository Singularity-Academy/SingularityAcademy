import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
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
  Flex,
  Stack,
  Icon,
  useBreakpointValue,  
  Grid,
  GridItem,
  Badge,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  List,
  ListItem,
  ListIcon,
  Link,
  Divider,
  Image,
} from '@chakra-ui/react';
// All icons replaced with Chakra UI icons
import { ExternalLinkIcon, ArrowForwardIcon, CheckIcon, LockIcon } from '@chakra-ui/icons';

interface CTACallbacks {
  onCTAClick?: (action: string, section: string) => void;
}

interface HeaderProps extends CTACallbacks {}

interface HeroProps extends CTACallbacks {}

interface GetInvolvedProps extends CTACallbacks {}

interface CTAProps extends CTACallbacks {}

// Header Component
const Header: React.FC<HeaderProps> = ({ onCTAClick }) => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  
  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'zh' : 'en';
    i18n.changeLanguage(newLang);
  };

  const handleGetStarted = () => {
    onCTAClick?.('get_started', 'header');
    const joinSection = document.getElementById('join-section');
    joinSection?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <Box
      position="fixed"
      top={0}
      left={0}
      right={0}
      zIndex={1000}
      bg={useColorModeValue('white', 'gray.800')}
      borderBottom="1px"
      borderColor={useColorModeValue('gray.200', 'gray.700')}
      backdropFilter="blur(10px)"
      boxShadow="sm"
    >
      <Container maxW="container.xl">
        <Flex h={16} alignItems="center" justifyContent="space-between">
          <HStack spacing={4}>
            <Icon as={ExternalLinkIcon} w={8} h={8} color="purple.500" />
            <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
              Singularity Academy
            </Heading>
          </HStack>
          
          <HStack spacing={4}>
            <Button
              variant="ghost"
              leftIcon={<ExternalLinkIcon />}
              onClick={toggleLanguage}
              size="sm"
            >
              {i18n.language === 'en' ? '中文' : 'EN'}
            </Button>
            <Button
              colorScheme="purple"
              size="sm"
              onClick={handleGetStarted}
            >
              {t('hero.ctaPrimary')}
            </Button>
          </HStack>
        </Flex>
      </Container>
    </Box>
  );
};

// Hero Component
const Hero: React.FC<HeroProps> = ({ onCTAClick }) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  
  const handlePrimaryCTA = () => {
    onCTAClick?.('start_free', 'hero');
    navigate('/signup');
  };
  
  const handleSecondaryCTA = () => {
    onCTAClick?.('become_mentor', 'hero');
    navigate('/become-mentor');
  };

  return (
    <Box
      minH="100vh"
      bgGradient="linear(135deg, purple.50 0%, green.50 50%, blue.50 100%)"
      pt={16}
      position="relative"
      overflow="hidden"
    >
      <Container maxW="container.xl" h="100vh">
        <Grid templateColumns={{ base: "1fr", lg: "1fr 1fr" }} h="full" alignItems="center" gap={12}>
          <GridItem>
            <VStack spacing={8} align={{ base: "center", lg: "flex-start" }} textAlign={{ base: "center", lg: "left" }}>
              <Heading
                fontSize={{ base: '3xl', md: '4xl', lg: '5xl' }}
                fontWeight="900"
                bgGradient="linear(to-r, purple.600, green.500)"
                bgClip="text"
                letterSpacing="tight"
                lineHeight="1.1"
              >
                {t('hero.title')}
              </Heading>
              
              <Text
                fontSize={{ base: 'lg', md: 'xl', lg: '2xl' }}
                color={useColorModeValue('gray.600', 'gray.300')}
                maxW="600px"
                lineHeight="1.6"
              >
                {t('hero.subtitle')}
              </Text>
              
              <HStack wrap="wrap" spacing={2} justify={{ base: "center", lg: "flex-start" }}>
                {(t('hero.badges', { returnObjects: true }) as string[]).map((badge, index) => (
                  <Badge key={index} colorScheme="purple" variant="subtle" px={3} py={1}>
                    {badge}
                  </Badge>
                ))}
              </HStack>
              
              <Text
                fontSize="md"
                color={useColorModeValue('gray.500', 'gray.400')}
                fontStyle="italic"
                maxW="500px"
              >
                {t('hero.note')}
              </Text>
              
              <Stack direction={{ base: 'column', sm: 'row' }} spacing={4}>
                <Button
                  size="lg"
                  colorScheme="purple"
                  rightIcon={<ArrowForwardIcon />}
                  onClick={handlePrimaryCTA}
                  _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
                  transition="all 0.2s"
                >
                  {t('hero.ctaPrimary')}
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  colorScheme="green"
                  onClick={handleSecondaryCTA}
                  _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
                  transition="all 0.2s"
                >
                  {t('hero.ctaSecondary')}
                </Button>
              </Stack>
            </VStack>
          </GridItem>
          
          <GridItem display={{ base: "none", lg: "block" }}>
            <Flex justify="center" align="center" h="full">
              <Icon as={ExternalLinkIcon} w={64} h={64} color="purple.400" opacity={0.8} />
            </Flex>
          </GridItem>
        </Grid>
      </Container>
    </Box>
  );
};

// Stats Component
const StatsSection: React.FC = () => {
  const { t } = useTranslation();
  const stats = t('glance.items', { returnObjects: true }) as Array<{ label: string; value: string }>;
  
  return (
    <Box py={20} bg={useColorModeValue('white', 'gray.800')}>
      <Container maxW="container.xl">
        <VStack spacing={12}>
          <Heading
            fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
            textAlign="center"
            color={useColorModeValue('gray.800', 'white')}
          >
            {t('glance.title')}
          </Heading>
          
          <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={8} w="full">
            {stats.map((stat, index) => (
              <VStack
                key={index}
                p={8}
                bg={useColorModeValue('gray.50', 'gray.700')}
                borderRadius="xl"
                textAlign="center"
                spacing={4}
                _hover={{ transform: 'translateY(-4px)', boxShadow: 'lg' }}
                transition="all 0.2s"
              >
                <Text fontSize="3xl" fontWeight="bold" color="purple.500">
                  {stat.value}
                </Text>
                <Text fontSize="lg" color={useColorModeValue('gray.600', 'gray.300')}>
                  {stat.label}
                </Text>
              </VStack>
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  );
};

// Mission Component
const MissionSection: React.FC = () => {
  const { t } = useTranslation();
  const whoList = t('mission.whoList', { returnObjects: true }) as string[];
  
  return (
    <Box py={20} bg={useColorModeValue('gray.50', 'gray.900')}>
      <Container maxW="container.xl">
        <Grid templateColumns={{ base: "1fr", lg: "1fr 1fr" }} gap={12}>
          <GridItem>
            <VStack spacing={6} align="flex-start">
              <Heading
                fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
                color={useColorModeValue('gray.800', 'white')}
              >
                {t('mission.title')}
              </Heading>
              <Text
                fontSize="lg"
                color={useColorModeValue('gray.600', 'gray.300')}
                lineHeight="1.8"
              >
                {t('mission.body')}
              </Text>
              <Text
                fontSize="md"
                color="green.500"
                fontWeight="semibold"
                p={4}
                bg={useColorModeValue('green.50', 'green.900')}
                borderRadius="md"
                borderLeft="4px solid"
                borderColor="green.500"
              >
                {t('mission.note')}
              </Text>
            </VStack>
          </GridItem>
          
          <GridItem>
            <VStack spacing={6} align="flex-start">
              <Heading
                fontSize={{ base: 'xl', md: '2xl' }}
                color={useColorModeValue('gray.800', 'white')}
              >
                {t('mission.whoTitle')}
              </Heading>
              <List spacing={4}>
                {whoList.map((item, index) => (
                  <ListItem key={index} display="flex" alignItems="flex-start">
                    <ListIcon as={CheckIcon} color="purple.500" mt={1} />
                    <Text color={useColorModeValue('gray.600', 'gray.300')} lineHeight="1.6">
                      {item}
                    </Text>
                  </ListItem>
                ))}
              </List>
            </VStack>
          </GridItem>
        </Grid>
      </Container>
    </Box>
  );
};

// Offer Component
const OfferSection: React.FC = () => {
  const { t } = useTranslation();
  const bullets = t('offer.bullets', { returnObjects: true }) as string[];
  
  const icons = [ExternalLinkIcon, ExternalLinkIcon, ExternalLinkIcon, ExternalLinkIcon, ExternalLinkIcon, ExternalLinkIcon, ExternalLinkIcon];
  
  return (
    <Box py={20} bg={useColorModeValue('white', 'gray.800')}>
      <Container maxW="container.xl">
        <VStack spacing={12}>
          <VStack spacing={6} textAlign="center">
            <Heading
              fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
              color={useColorModeValue('gray.800', 'white')}
            >
              {t('offer.title')}
            </Heading>
            <Text
              fontSize="lg"
              color={useColorModeValue('gray.600', 'gray.300')}
              maxW="3xl"
              lineHeight="1.8"
            >
              {t('offer.intro')}
            </Text>
          </VStack>
          
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={8} w="full">
            {bullets.map((bullet, index) => {
              const IconComponent = icons[index] || CheckIcon;
              return (
                <VStack
                  key={index}
                  p={6}
                  bg={useColorModeValue('gray.50', 'gray.700')}
                  borderRadius="xl"
                  align="flex-start"
                  spacing={4}
                  _hover={{ transform: 'translateY(-2px)', boxShadow: 'md' }}
                  transition="all 0.2s"
                >
                  <Icon as={IconComponent} w={8} h={8} color="green.500" />
                  <Text
                    color={useColorModeValue('gray.700', 'gray.200')}
                    lineHeight="1.6"
                  >
                    {bullet}
                  </Text>
                </VStack>
              );
            })}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  );
};

// Success Stories Component
const SuccessStoriesSection: React.FC = () => {
  const { t } = useTranslation();
  const stories = t('successStories.stories', { returnObjects: true }) as Array<{
    title: string;
    summary: string;
    content: string;
  }>;
  
  return (
    <Box py={20} bg={useColorModeValue('gray.50', 'gray.900')}>
      <Container maxW="container.xl">
        <VStack spacing={12}>
          <Heading
            fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
            textAlign="center"
            color={useColorModeValue('gray.800', 'white')}
          >
            {t('successStories.title')}
          </Heading>
          
          <Accordion allowMultiple w="full">
            {stories.map((story, index) => (
              <AccordionItem key={index} border="none" mb={4}>
                <AccordionButton
                  p={6}
                  bg={useColorModeValue('white', 'gray.800')}
                  borderRadius="xl"
                  _hover={{ bg: useColorModeValue('gray.50', 'gray.700') }}
                  _expanded={{ bg: useColorModeValue('purple.50', 'purple.900') }}
                >
                  <Box flex="1" textAlign="left">
                    <Heading size="md" color={useColorModeValue('gray.800', 'white')} mb={2}>
                      {story.title}
                    </Heading>
                    <Text color={useColorModeValue('gray.600', 'gray.300')}>
                      {story.summary}
                    </Text>
                  </Box>
                  <AccordionIcon />
                </AccordionButton>
                <AccordionPanel
                  p={6}
                  bg={useColorModeValue('white', 'gray.800')}
                  borderBottomRadius="xl"
                >
                  <Text
                    color={useColorModeValue('gray.700', 'gray.200')}
                    lineHeight="1.8"
                  >
                    {story.content}
                  </Text>
                </AccordionPanel>
              </AccordionItem>
            ))}
          </Accordion>
        </VStack>
      </Container>
    </Box>
  );
};

// How It Works Component
const HowItWorksSection: React.FC = () => {
  const { t } = useTranslation();
  const steps = t('howItWorks.steps', { returnObjects: true }) as Array<{
    title: string;
    description: string;
  }>;
  
  return (
    <Box py={20} bg={useColorModeValue('white', 'gray.800')}>
      <Container maxW="container.xl">
        <VStack spacing={12}>
          <Heading
            fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
            textAlign="center"
            color={useColorModeValue('gray.800', 'white')}
          >
            {t('howItWorks.title')}
          </Heading>
          
          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={8} w="full">
            {steps.map((step, index) => (
              <VStack
                key={index}
                p={8}
                bg={useColorModeValue('gray.50', 'gray.700')}
                borderRadius="xl"
                textAlign="center"
                spacing={6}
                position="relative"
                _hover={{ transform: 'translateY(-4px)', boxShadow: 'lg' }}
                transition="all 0.2s"
              >
                <Box
                  w={12}
                  h={12}
                  bg="purple.500"
                  borderRadius="full"
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                  color="white"
                  fontSize="xl"
                  fontWeight="bold"
                >
                  {index + 1}
                </Box>
                <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                  {step.title}
                </Heading>
                <Text color={useColorModeValue('gray.600', 'gray.300')} lineHeight="1.6">
                  {step.description}
                </Text>
              </VStack>
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  );
};

// Early Outcomes Component
const OutcomesSection: React.FC = () => {
  const { t } = useTranslation();
  const outcomes = t('outcomes.items', { returnObjects: true }) as string[];
  
  return (
    <Box py={20} bg={useColorModeValue('green.50', 'green.900')}>
      <Container maxW="container.xl">
        <VStack spacing={12}>
          <Heading
            fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
            textAlign="center"
            color={useColorModeValue('gray.800', 'white')}
          >
            {t('outcomes.title')}
          </Heading>
          
          <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} w="full">
            {outcomes.map((outcome, index) => (
              <HStack
                key={index}
                p={6}
                bg={useColorModeValue('white', 'gray.800')}
                borderRadius="xl"
                spacing={4}
                _hover={{ transform: 'translateX(4px)' }}
                transition="all 0.2s"
              >
                <Icon as={CheckIcon} color="green.500" w={6} h={6} flexShrink={0} />
                <Text color={useColorModeValue('gray.700', 'gray.200')} lineHeight="1.6">
                  {outcome}
                </Text>
              </HStack>
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  );
};

// Safeguarding Component
const SafeguardingSection: React.FC = () => {
  const { t } = useTranslation();
  const safeguardingItems = t('safeguarding.content', { returnObjects: true }) as string[];
  
  return (
    <Box py={20} bg={useColorModeValue('blue.50', 'blue.900')}>
      <Container maxW="container.xl">
        <VStack spacing={12}>
          <VStack spacing={4} textAlign="center">
            <Icon as={LockIcon} w={16} h={16} color="blue.500" />
            <Heading
              fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
              color={useColorModeValue('gray.800', 'white')}
            >
              {t('safeguarding.title')}
            </Heading>
          </VStack>
          
          <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} w="full">
            {safeguardingItems.map((item, index) => (
              <HStack
                key={index}
                p={6}
                bg={useColorModeValue('white', 'gray.800')}
                borderRadius="xl"
                spacing={4}
                align="flex-start"
              >
                <Icon as={LockIcon} color="blue.500" w={6} h={6} flexShrink={0} mt={1} />
                <Text color={useColorModeValue('gray.700', 'gray.200')} lineHeight="1.6">
                  {item}
                </Text>
              </HStack>
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  );
};

// Respect System Component
const RespectSystemSection: React.FC = () => {
  const { t } = useTranslation();
  
  return (
    <Box py={20} bg={useColorModeValue('orange.50', 'orange.900')}>
      <Container maxW="container.xl">
        <VStack spacing={8} textAlign="center">
          <Icon as={ExternalLinkIcon} w={16} h={16} color="orange.500" />
          <Heading
            fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
            color={useColorModeValue('gray.800', 'white')}
          >
            {t('respectSystem.title')}
          </Heading>
          <Text
            fontSize="lg"
            color={useColorModeValue('gray.700', 'gray.200')}
            maxW="4xl"
            lineHeight="1.8"
          >
            {t('respectSystem.content')}
          </Text>
        </VStack>
      </Container>
    </Box>
  );
};

// Get Involved Component
const GetInvolvedSection: React.FC<GetInvolvedProps> = ({ onCTAClick }) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const sections = t('getInvolved.sections', { returnObjects: true }) as Array<{
    title: string;
    description: string;
    cta: string;
  }>;
  
  const handleCTA = (action: string) => {
    onCTAClick?.(action, 'get_involved');
    
    // Navigate based on the action
    if (action.includes('mentor')) {
      navigate('/become-mentor');
    } else if (action.includes('partner')) {
      navigate('/partner-with-us');
    } else if (action.includes('support') || action.includes('mission')) {
      navigate('/support-mission');
    }
  };
  
  return (
    <Box py={20} bg={useColorModeValue('white', 'gray.800')}>
      <Container maxW="container.xl">
        <VStack spacing={12}>
          <Heading
            fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
            textAlign="center"
            color={useColorModeValue('gray.800', 'white')}
          >
            {t('getInvolved.title')}
          </Heading>
          
          <SimpleGrid columns={{ base: 1, md: 2 }} spacing={8} w="full">
            {sections.map((section, index) => (
              <VStack
                key={index}
                p={8}
                bg={useColorModeValue('gray.50', 'gray.700')}
                borderRadius="xl"
                spacing={6}
                align="flex-start"
                _hover={{ transform: 'translateY(-4px)', boxShadow: 'lg' }}
                transition="all 0.2s"
              >
                <Heading size="lg" color={useColorModeValue('gray.800', 'white')}>
                  {section.title}
                </Heading>
                <Text color={useColorModeValue('gray.600', 'gray.300')} lineHeight="1.6">
                  {section.description}
                </Text>
                <Button
                  colorScheme="purple"
                  variant="outline"
                  onClick={() => handleCTA(section.cta.toLowerCase().replace(/\s+/g, '_'))}
                >
                  {section.cta}
                </Button>
              </VStack>
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  );
};

// FAQ Component
const FAQSection: React.FC = () => {
  const { t } = useTranslation();
  const faqItems = t('faq.items', { returnObjects: true }) as Array<{
    question: string;
    answer: string;
  }>;
  
  return (
    <Box py={20} bg={useColorModeValue('gray.50', 'gray.900')}>
      <Container maxW="container.xl">
        <VStack spacing={12}>
          <Heading
            fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
            textAlign="center"
            color={useColorModeValue('gray.800', 'white')}
          >
            {t('faq.title')}
          </Heading>
          
          <Accordion allowMultiple w="full" maxW="4xl">
            {faqItems.map((item, index) => (
              <AccordionItem key={index} border="none" mb={4}>
                <AccordionButton
                  p={6}
                  bg={useColorModeValue('white', 'gray.800')}
                  borderRadius="xl"
                  _hover={{ bg: useColorModeValue('gray.50', 'gray.700') }}
                  _expanded={{ bg: useColorModeValue('purple.50', 'purple.900') }}
                >
                  <Box flex="1" textAlign="left">
                    <Text fontWeight="semibold" color={useColorModeValue('gray.800', 'white')}>
                      {item.question}
                    </Text>
                  </Box>
                  <AccordionIcon />
                </AccordionButton>
                <AccordionPanel
                  p={6}
                  bg={useColorModeValue('white', 'gray.800')}
                  borderBottomRadius="xl"
                >
                  <Text color={useColorModeValue('gray.700', 'gray.200')} lineHeight="1.6">
                    {item.answer}
                  </Text>
                </AccordionPanel>
              </AccordionItem>
            ))}
          </Accordion>
        </VStack>
      </Container>
    </Box>
  );
};

// CTA Section Component
const CTASection: React.FC<CTAProps> = ({ onCTAClick }) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  
  const handleCTA = () => {
    onCTAClick?.('start_journey', 'cta');
    navigate('/signup');
  };
  
  return (
    <Box
      id="join-section"
      py={20}
      bgGradient="linear(135deg, purple.600 0%, green.500 100%)"
      position="relative"
      overflow="hidden"
    >
      <Container maxW="container.xl" textAlign="center" position="relative" zIndex={2}>
        <VStack spacing={8}>
          <Heading
            fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
            color="white"
            fontWeight="700"
          >
            {t('cta.title')}
          </Heading>
          <Text
            fontSize={{ base: 'lg', md: 'xl' }}
            color="white"
            opacity={0.9}
            maxW="3xl"
            lineHeight="1.7"
          >
            {t('cta.subtitle')}
          </Text>
          <Button
            size="xl"
            h="60px"
            px="40px"
            fontSize="xl"
            fontWeight="600"
            bg="white"
            color="purple.600"
            _hover={{
              transform: 'translateY(-3px)',
              boxShadow: '0 20px 40px rgba(0,0,0,0.2)',
              bg: 'gray.50'
            }}
            transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)"
            rightIcon={<ArrowForwardIcon />}
            onClick={handleCTA}
          >
            {t('cta.button')}
          </Button>
        </VStack>
      </Container>
    </Box>
  );
};

// Footer Component
const Footer: React.FC = () => {
  const { t, i18n } = useTranslation();
  
  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'zh' : 'en';
    i18n.changeLanguage(newLang);
  };
  
  return (
    <Box bg={useColorModeValue('gray.800', 'gray.900')} color="white" py={12}>
      <Container maxW="container.xl">
        <Grid templateColumns={{ base: "1fr", md: "repeat(4, 1fr)" }} gap={8}>
          <GridItem>
            <VStack align="flex-start" spacing={4}>
              <HStack>
                <Icon as={ExternalLinkIcon} w={6} h={6} color="purple.400" />
                <Text fontWeight="bold" fontSize="lg">Singularity Academy</Text>
              </HStack>
              <Text fontSize="sm" color="gray.400" lineHeight="1.6">
                {i18n.language === 'en' 
                  ? 'Empowering homeschoolers with AI-driven education'
                  : '用AI驱动的教育赋能在家教育者'
                }
              </Text>
            </VStack>
          </GridItem>
          
          <GridItem>
            <VStack align="flex-start" spacing={4}>
              <Text fontWeight="semibold">{t('footer.contact.title')}</Text>
              <VStack align="flex-start" spacing={2}>
                <HStack>
                  <ExternalLinkIcon w={4} h={4} color="gray.400" />
                  <Text fontSize="sm" color="gray.400">{t('footer.contact.email')}</Text>
                </HStack>
                <HStack>
                  <ExternalLinkIcon w={4} h={4} color="gray.400" />
                  <Text fontSize="sm" color="gray.400">{t('footer.contact.phone')}</Text>
                </HStack>
              </VStack>
            </VStack>
          </GridItem>
          
          <GridItem>
            <VStack align="flex-start" spacing={4}>
              <Text fontWeight="semibold">Links</Text>
              <VStack align="flex-start" spacing={2}>
                <Link fontSize="sm" color="gray.400" _hover={{ color: 'white' }}>
                  {t('footer.links.about')}
                </Link>
                <Link fontSize="sm" color="gray.400" _hover={{ color: 'white' }}>
                  {t('footer.links.privacy')}
                </Link>
                <Link fontSize="sm" color="gray.400" _hover={{ color: 'white' }}>
                  {t('footer.links.terms')}
                </Link>
                <Link fontSize="sm" color="gray.400" _hover={{ color: 'white' }}>
                  {t('footer.links.support')}
                </Link>
              </VStack>
            </VStack>
          </GridItem>
          
          <GridItem>
            <VStack align="flex-start" spacing={4}>
              <Text fontWeight="semibold">Social</Text>
              <HStack spacing={4}>
                <ExternalLinkIcon w={5} h={5} color="gray.400" _hover={{ color: 'white' }} cursor="pointer" />
                <ExternalLinkIcon w={5} h={5} color="gray.400" _hover={{ color: 'white' }} cursor="pointer" />
                <ExternalLinkIcon w={5} h={5} color="gray.400" _hover={{ color: 'white' }} cursor="pointer" />
              </HStack>
              <Button
                size="sm"
                variant="outline"
                colorScheme="gray"
                leftIcon={<ExternalLinkIcon />}
                onClick={toggleLanguage}
              >
                {i18n.language === 'en' ? '中文' : 'EN'}
              </Button>
            </VStack>
          </GridItem>
        </Grid>
        
        <Divider my={8} borderColor="gray.600" />
        
        <Text textAlign="center" fontSize="sm" color="gray.400">
          {t('footer.copyright')}
        </Text>
      </Container>
    </Box>
  );
};

// Main HomePage Component
const HomePage: React.FC<CTACallbacks> = ({ onCTAClick }) => {
  const { t } = useTranslation();
  
  // SEO Meta tags (would be handled by React Helmet in a real app)
  React.useEffect(() => {
    document.title = t('meta.title');
    
    // Update meta description
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription) {
      metaDescription.setAttribute('content', t('meta.description'));
    }
  }, [t]);
  
  return (
    <Box>
      <Header onCTAClick={onCTAClick} />
      <Hero onCTAClick={onCTAClick} />
      <StatsSection />
      <MissionSection />
      <OfferSection />
      <SuccessStoriesSection />
      <HowItWorksSection />
      <OutcomesSection />
      <SafeguardingSection />
      <RespectSystemSection />
      <GetInvolvedSection onCTAClick={onCTAClick} />
      <FAQSection />
      <CTASection onCTAClick={onCTAClick} />
      <Footer />
    </Box>
  );
};

export default HomePage;
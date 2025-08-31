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
  FormControl,
  FormLabel,
  Input,
  Textarea,
  Select,
  Checkbox,
  useColorModeValue,
  useToast,
  Grid,
  GridItem,
  Divider,
  RadioGroup,
  Radio,
  Stack,
  Badge,
  SimpleGrid,
  Link,
} from '@chakra-ui/react';
import { ArrowBackIcon, CheckIcon } from '@chakra-ui/icons';
import { saveFormSubmission, createFormSubmission } from '../utils/formSubmission';

interface SignupFormData {
  // Personal Information
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  dateOfBirth: string;
  country: string;
  city: string;
  
  // Educational Background
  currentEducationLevel: string;
  institution: string;
  fieldOfStudy: string;
  graduationYear: string;
  
  // Learning Preferences
  learningGoals: string[];
  preferredSubjects: string[];
  learningStyle: string;
  timeCommitment: string;
  
  // Technical Information
  deviceType: string;
  internetConnection: string;
  technicalSkillLevel: string;
  
  // Accessibility
  accessibilityNeeds: string;
  languagePreference: string;
  
  // Motivation
  motivation: string;
  expectations: string;
  
  // Agreements
  termsAccepted: boolean;
  privacyAccepted: boolean;
  communicationConsent: boolean;
}

const SignupPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const toast = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const [formData, setFormData] = useState<SignupFormData>({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    dateOfBirth: '',
    country: '',
    city: '',
    currentEducationLevel: '',
    institution: '',
    fieldOfStudy: '',
    graduationYear: '',
    learningGoals: [],
    preferredSubjects: [],
    learningStyle: '',
    timeCommitment: '',
    deviceType: '',
    internetConnection: '',
    technicalSkillLevel: '',
    accessibilityNeeds: '',
    languagePreference: 'English',
    motivation: '',
    expectations: '',
    termsAccepted: false,
    privacyAccepted: false,
    communicationConsent: false,
  });

  const handleInputChange = (field: keyof SignupFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleArrayChange = (field: 'learningGoals' | 'preferredSubjects', value: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: checked 
        ? [...prev[field], value]
        : prev[field].filter(item => item !== value)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!formData.firstName || !formData.lastName || !formData.email) {
      toast({
        title: 'Required Fields Missing',
        description: 'Please fill in all required fields.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }
    
    if (!formData.termsAccepted || !formData.privacyAccepted) {
      toast({
        title: 'Agreement Required',
        description: 'Please accept the terms and privacy policy.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    setIsSubmitting(true);
    
    try {
      const submission = createFormSubmission('signup', formData);
      await saveFormSubmission(submission);
      
      toast({
        title: 'Welcome to Singularity Academy!',
        description: 'Your registration has been submitted successfully. We will contact you soon with next steps to begin your learning journey.',
        status: 'success',
        duration: 7000,
        isClosable: true,
      });
      
      // Reset form
      setFormData({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        dateOfBirth: '',
        country: '',
        city: '',
        currentEducationLevel: '',
        institution: '',
        fieldOfStudy: '',
        graduationYear: '',
        learningGoals: [],
        preferredSubjects: [],
        learningStyle: '',
        timeCommitment: '',
        deviceType: '',
        internetConnection: '',
        technicalSkillLevel: '',
        accessibilityNeeds: '',
        languagePreference: 'English',
        motivation: '',
        expectations: '',
        termsAccepted: false,
        privacyAccepted: false,
        communicationConsent: false,
      });
      
    } catch (error) {
      toast({
        title: 'Registration Failed',
        description: 'There was an error submitting your registration. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const learningGoalOptions = [
    'Academic Excellence',
    'Career Advancement',
    'Personal Development',
    'Skill Building',
    'Test Preparation',
    'Language Learning',
    'Creative Expression',
    'Technical Skills'
  ];

  const subjectOptions = [
    'Mathematics',
    'Science',
    'English/Language Arts',
    'History',
    'Geography',
    'Computer Science',
    'Arts',
    'Music',
    'Foreign Languages',
    'Business',
    'Engineering',
    'Medicine'
  ];

  return (
    <Box minH="100vh" bg={useColorModeValue('gray.50', 'gray.900')} py={8}>
      <Container maxW="container.lg">
        <VStack spacing={8} align="stretch">
          {/* Header */}
          <HStack>
            <Button
              leftIcon={<ArrowBackIcon />}
              variant="ghost"
              onClick={() => navigate('/')}
            >
              Back to Home
            </Button>
          </HStack>
          
          <VStack spacing={4} textAlign="center">
            <Heading
              fontSize={{ base: '2xl', md: '3xl', lg: '4xl' }}
              color={useColorModeValue('gray.800', 'white')}
            >
              Start Your Learning Journey
            </Heading>
            <Text
              fontSize="lg"
              color={useColorModeValue('gray.600', 'gray.300')}
              maxW="2xl"
            >
              Join Singularity Academy and experience personalized AI-powered education.
              Fill out this form to get started with your customized learning experience.
            </Text>
          </VStack>

          {/* Benefits */}
          <Box
            bg={useColorModeValue('white', 'gray.800')}
            p={6}
            borderRadius="xl"
            boxShadow="md"
          >
            <VStack spacing={4}>
              <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                What You'll Get
              </Heading>
              <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} w="full">
                <VStack>
                  <Badge colorScheme="purple" p={2} borderRadius="md">
                    AI Principal
                  </Badge>
                  <Text fontSize="sm" textAlign="center" color={useColorModeValue('gray.600', 'gray.300')}>
                    Personalized learning path and academic guidance
                  </Text>
                </VStack>
                <VStack>
                  <Badge colorScheme="green" p={2} borderRadius="md">
                    AI Teachers
                  </Badge>
                  <Text fontSize="sm" textAlign="center" color={useColorModeValue('gray.600', 'gray.300')}>
                    24/7 subject-specific tutoring and support
                  </Text>
                </VStack>
                <VStack>
                  <Badge colorScheme="blue" p={2} borderRadius="md">
                    AI Dean
                  </Badge>
                  <Text fontSize="sm" textAlign="center" color={useColorModeValue('gray.600', 'gray.300')}>
                    Administrative support and progress tracking
                  </Text>
                </VStack>
              </SimpleGrid>
            </VStack>
          </Box>

          {/* Form */}
          <Box
            bg={useColorModeValue('white', 'gray.800')}
            p={8}
            borderRadius="xl"
            boxShadow="lg"
          >
            <form onSubmit={handleSubmit}>
              <VStack spacing={8} align="stretch">
                {/* Personal Information */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Personal Information
                  </Heading>
                  
                  <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={4}>
                    <GridItem>
                      <FormControl isRequired>
                        <FormLabel>First Name</FormLabel>
                        <Input
                          value={formData.firstName}
                          onChange={(e) => handleInputChange('firstName', e.target.value)}
                          placeholder="Enter your first name"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl isRequired>
                        <FormLabel>Last Name</FormLabel>
                        <Input
                          value={formData.lastName}
                          onChange={(e) => handleInputChange('lastName', e.target.value)}
                          placeholder="Enter your last name"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl isRequired>
                        <FormLabel>Email</FormLabel>
                        <Input
                          type="email"
                          value={formData.email}
                          onChange={(e) => handleInputChange('email', e.target.value)}
                          placeholder="Enter your email address"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Phone</FormLabel>
                        <Input
                          value={formData.phone}
                          onChange={(e) => handleInputChange('phone', e.target.value)}
                          placeholder="Enter your phone number"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Date of Birth</FormLabel>
                        <Input
                          type="date"
                          value={formData.dateOfBirth}
                          onChange={(e) => handleInputChange('dateOfBirth', e.target.value)}
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Country</FormLabel>
                        <Input
                          value={formData.country}
                          onChange={(e) => handleInputChange('country', e.target.value)}
                          placeholder="Enter your country"
                        />
                      </FormControl>
                    </GridItem>
                  </Grid>
                </VStack>

                <Divider />

                {/* Educational Background */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Educational Background
                  </Heading>
                  
                  <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={4}>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Current Education Level</FormLabel>
                        <Select
                          value={formData.currentEducationLevel}
                          onChange={(e) => handleInputChange('currentEducationLevel', e.target.value)}
                          placeholder="Select your education level"
                        >
                          <option value="elementary">Elementary School</option>
                          <option value="middle">Middle School</option>
                          <option value="high">High School</option>
                          <option value="undergraduate">Undergraduate</option>
                          <option value="graduate">Graduate</option>
                          <option value="professional">Professional</option>
                          <option value="other">Other</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Institution</FormLabel>
                        <Input
                          value={formData.institution}
                          onChange={(e) => handleInputChange('institution', e.target.value)}
                          placeholder="Enter your school/university"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Field of Study</FormLabel>
                        <Input
                          value={formData.fieldOfStudy}
                          onChange={(e) => handleInputChange('fieldOfStudy', e.target.value)}
                          placeholder="Enter your major/field of study"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Expected Graduation Year</FormLabel>
                        <Input
                          value={formData.graduationYear}
                          onChange={(e) => handleInputChange('graduationYear', e.target.value)}
                          placeholder="e.g., 2025"
                        />
                      </FormControl>
                    </GridItem>
                  </Grid>
                </VStack>

                <Divider />

                {/* Learning Preferences */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Learning Preferences
                  </Heading>
                  
                  <FormControl>
                    <FormLabel>Learning Goals (Select all that apply)</FormLabel>
                    <SimpleGrid columns={{ base: 2, md: 4 }} spacing={3}>
                      {learningGoalOptions.map((goal) => (
                        <Checkbox
                          key={goal}
                          isChecked={formData.learningGoals.includes(goal)}
                          onChange={(e) => handleArrayChange('learningGoals', goal, e.target.checked)}
                        >
                          {goal}
                        </Checkbox>
                      ))}
                    </SimpleGrid>
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Preferred Subjects (Select all that apply)</FormLabel>
                    <SimpleGrid columns={{ base: 2, md: 4 }} spacing={3}>
                      {subjectOptions.map((subject) => (
                        <Checkbox
                          key={subject}
                          isChecked={formData.preferredSubjects.includes(subject)}
                          onChange={(e) => handleArrayChange('preferredSubjects', subject, e.target.checked)}
                        >
                          {subject}
                        </Checkbox>
                      ))}
                    </SimpleGrid>
                  </FormControl>
                  
                  <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={4}>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Learning Style</FormLabel>
                        <Select
                          value={formData.learningStyle}
                          onChange={(e) => handleInputChange('learningStyle', e.target.value)}
                          placeholder="Select your learning style"
                        >
                          <option value="visual">Visual</option>
                          <option value="auditory">Auditory</option>
                          <option value="kinesthetic">Kinesthetic</option>
                          <option value="reading">Reading/Writing</option>
                          <option value="mixed">Mixed</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Time Commitment</FormLabel>
                        <Select
                          value={formData.timeCommitment}
                          onChange={(e) => handleInputChange('timeCommitment', e.target.value)}
                          placeholder="Select time commitment"
                        >
                          <option value="1-2 hours/week">1-2 hours per week</option>
                          <option value="3-5 hours/week">3-5 hours per week</option>
                          <option value="6-10 hours/week">6-10 hours per week</option>
                          <option value="10+ hours/week">10+ hours per week</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                  </Grid>
                </VStack>

                <Divider />

                {/* Technical Information */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Technical Information
                  </Heading>
                  
                  <Grid templateColumns={{ base: '1fr', md: '1fr 1fr 1fr' }} gap={4}>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Primary Device</FormLabel>
                        <Select
                          value={formData.deviceType}
                          onChange={(e) => handleInputChange('deviceType', e.target.value)}
                          placeholder="Select device type"
                        >
                          <option value="laptop">Laptop</option>
                          <option value="desktop">Desktop</option>
                          <option value="tablet">Tablet</option>
                          <option value="smartphone">Smartphone</option>
                          <option value="multiple">Multiple devices</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Internet Connection</FormLabel>
                        <Select
                          value={formData.internetConnection}
                          onChange={(e) => handleInputChange('internetConnection', e.target.value)}
                          placeholder="Select connection type"
                        >
                          <option value="high-speed">High-speed broadband</option>
                          <option value="moderate">Moderate speed</option>
                          <option value="limited">Limited/slow connection</option>
                          <option value="mobile">Mobile data only</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Technical Skill Level</FormLabel>
                        <Select
                          value={formData.technicalSkillLevel}
                          onChange={(e) => handleInputChange('technicalSkillLevel', e.target.value)}
                          placeholder="Select skill level"
                        >
                          <option value="beginner">Beginner</option>
                          <option value="intermediate">Intermediate</option>
                          <option value="advanced">Advanced</option>
                          <option value="expert">Expert</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                  </Grid>
                </VStack>

                <Divider />

                {/* Accessibility & Language */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Accessibility & Language
                  </Heading>
                  
                  <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={4}>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Language Preference</FormLabel>
                        <Select
                          value={formData.languagePreference}
                          onChange={(e) => handleInputChange('languagePreference', e.target.value)}
                        >
                          <option value="English">English</option>
                          <option value="Chinese">中文 (Chinese)</option>
                          <option value="Spanish">Español</option>
                          <option value="French">Français</option>
                          <option value="German">Deutsch</option>
                          <option value="Other">Other</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Accessibility Needs</FormLabel>
                        <Input
                          value={formData.accessibilityNeeds}
                          onChange={(e) => handleInputChange('accessibilityNeeds', e.target.value)}
                          placeholder="e.g., screen reader, large text, captions"
                        />
                      </FormControl>
                    </GridItem>
                  </Grid>
                </VStack>

                <Divider />

                {/* Motivation */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Tell Us About Yourself
                  </Heading>
                  
                  <FormControl>
                    <FormLabel>What motivates you to learn with AI?</FormLabel>
                    <Textarea
                      value={formData.motivation}
                      onChange={(e) => handleInputChange('motivation', e.target.value)}
                      placeholder="Share what excites you about AI-powered learning"
                      rows={3}
                    />
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>What are your expectations?</FormLabel>
                    <Textarea
                      value={formData.expectations}
                      onChange={(e) => handleInputChange('expectations', e.target.value)}
                      placeholder="What do you hope to achieve through our platform?"
                      rows={3}
                    />
                  </FormControl>
                </VStack>

                <Divider />

                {/* Agreements */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Agreements
                  </Heading>
                  
                  <VStack spacing={3} align="stretch">
                    <Checkbox
                      isChecked={formData.termsAccepted}
                      onChange={(e) => handleInputChange('termsAccepted', e.target.checked)}
                    >
                      I accept the{' '}
                      <Link color="purple.500" href="#" textDecoration="underline">
                        Terms of Service
                      </Link>{' '}
                      *
                    </Checkbox>
                    
                    <Checkbox
                      isChecked={formData.privacyAccepted}
                      onChange={(e) => handleInputChange('privacyAccepted', e.target.checked)}
                    >
                      I accept the{' '}
                      <Link color="purple.500" href="#" textDecoration="underline">
                        Privacy Policy
                      </Link>{' '}
                      *
                    </Checkbox>
                    
                    <Checkbox
                      isChecked={formData.communicationConsent}
                      onChange={(e) => handleInputChange('communicationConsent', e.target.checked)}
                    >
                      I consent to receive educational updates and communications
                    </Checkbox>
                  </VStack>
                </VStack>

                {/* Submit Button */}
                <Button
                  type="submit"
                  colorScheme="purple"
                  size="lg"
                  isLoading={isSubmitting}
                  loadingText="Creating Your Account..."
                  rightIcon={<CheckIcon />}
                  _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
                  transition="all 0.2s"
                >
                  Start Learning Journey
                </Button>
                
                <Text fontSize="sm" color={useColorModeValue('gray.500', 'gray.400')} textAlign="center">
                  By signing up, you'll receive personalized learning recommendations and access to our AI-powered educational platform.
                </Text>
              </VStack>
            </form>
          </Box>
        </VStack>
      </Container>
    </Box>
  );
};

export default SignupPage;
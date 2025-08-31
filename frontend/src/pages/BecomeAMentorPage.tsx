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
  Icon,
  Divider,
} from '@chakra-ui/react';
import { ArrowBackIcon, CheckIcon } from '@chakra-ui/icons';
import { saveFormSubmission, createFormSubmission } from '../utils/formSubmission';

interface MentorFormData {
  // Personal Information
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  country: string;
  city: string;
  
  // Professional Background
  currentRole: string;
  company: string;
  yearsExperience: string;
  education: string;
  expertise: string[];
  
  // Mentoring Information
  mentorshipExperience: string;
  availableHours: string;
  preferredAgeGroup: string;
  subjects: string[];
  languages: string[];
  
  // Motivation
  motivation: string;
  goals: string;
  additionalInfo: string;
  
  // Agreements
  backgroundCheck: boolean;
  termsAccepted: boolean;
  privacyAccepted: boolean;
}

const BecomeAMentorPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const toast = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const [formData, setFormData] = useState<MentorFormData>({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    country: '',
    city: '',
    currentRole: '',
    company: '',
    yearsExperience: '',
    education: '',
    expertise: [],
    mentorshipExperience: '',
    availableHours: '',
    preferredAgeGroup: '',
    subjects: [],
    languages: [],
    motivation: '',
    goals: '',
    additionalInfo: '',
    backgroundCheck: false,
    termsAccepted: false,
    privacyAccepted: false,
  });

  const handleInputChange = (field: keyof MentorFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleArrayChange = (field: keyof MentorFormData, value: string, checked: boolean) => {
    setFormData(prev => {
      const currentArray = prev[field] as string[];
      if (checked) {
        return { ...prev, [field]: [...currentArray, value] };
      } else {
        return { ...prev, [field]: currentArray.filter(item => item !== value) };
      }
    });
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
      const submission = createFormSubmission('mentor', formData);
      await saveFormSubmission(submission);
      
      toast({
        title: 'Application Submitted!',
        description: 'Thank you for your interest in becoming a mentor. We will review your application and contact you soon.',
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
        country: '',
        city: '',
        currentRole: '',
        company: '',
        yearsExperience: '',
        education: '',
        expertise: [],
        mentorshipExperience: '',
        availableHours: '',
        preferredAgeGroup: '',
        subjects: [],
        languages: [],
        motivation: '',
        goals: '',
        additionalInfo: '',
        backgroundCheck: false,
        termsAccepted: false,
        privacyAccepted: false,
      });
      
    } catch (error) {
      toast({
        title: 'Submission Failed',
        description: 'There was an error submitting your application. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const expertiseOptions = [
    'Mathematics', 'Science', 'Technology', 'Engineering', 'Arts', 'Languages',
    'Business', 'Psychology', 'Education', 'Healthcare', 'Social Sciences'
  ];
  
  const subjectOptions = [
    'Elementary Math', 'Advanced Math', 'Physics', 'Chemistry', 'Biology',
    'Computer Science', 'Programming', 'English', 'Literature', 'History',
    'Geography', 'Art', 'Music', 'Physical Education'
  ];
  
  const languageOptions = [
    'English', 'Chinese (Mandarin)', 'Spanish', 'French', 'German', 'Japanese',
    'Korean', 'Arabic', 'Portuguese', 'Russian', 'Italian'
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
              Become a Mentor
            </Heading>
            <Text
              fontSize="lg"
              color={useColorModeValue('gray.600', 'gray.300')}
              maxW="2xl"
            >
              Join our community of dedicated mentors and help shape the future of education.
              Share your expertise and make a meaningful impact on students' lives.
            </Text>
          </VStack>

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
                        <FormLabel>Country</FormLabel>
                        <Input
                          value={formData.country}
                          onChange={(e) => handleInputChange('country', e.target.value)}
                          placeholder="Enter your country"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>City</FormLabel>
                        <Input
                          value={formData.city}
                          onChange={(e) => handleInputChange('city', e.target.value)}
                          placeholder="Enter your city"
                        />
                      </FormControl>
                    </GridItem>
                  </Grid>
                </VStack>

                <Divider />

                {/* Professional Background */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Professional Background
                  </Heading>
                  <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={4}>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Current Role</FormLabel>
                        <Input
                          value={formData.currentRole}
                          onChange={(e) => handleInputChange('currentRole', e.target.value)}
                          placeholder="e.g., Software Engineer, Teacher"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Company/Organization</FormLabel>
                        <Input
                          value={formData.company}
                          onChange={(e) => handleInputChange('company', e.target.value)}
                          placeholder="Enter your company name"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Years of Experience</FormLabel>
                        <Select
                          value={formData.yearsExperience}
                          onChange={(e) => handleInputChange('yearsExperience', e.target.value)}
                          placeholder="Select experience level"
                        >
                          <option value="0-2">0-2 years</option>
                          <option value="3-5">3-5 years</option>
                          <option value="6-10">6-10 years</option>
                          <option value="11-15">11-15 years</option>
                          <option value="16+">16+ years</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Education Level</FormLabel>
                        <Select
                          value={formData.education}
                          onChange={(e) => handleInputChange('education', e.target.value)}
                          placeholder="Select education level"
                        >
                          <option value="high-school">High School</option>
                          <option value="bachelor">Bachelor's Degree</option>
                          <option value="master">Master's Degree</option>
                          <option value="phd">PhD</option>
                          <option value="other">Other</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                  </Grid>
                  
                  <FormControl>
                    <FormLabel>Areas of Expertise</FormLabel>
                    <Grid templateColumns={{ base: '1fr', md: 'repeat(3, 1fr)' }} gap={2}>
                      {expertiseOptions.map((option) => (
                        <Checkbox
                          key={option}
                          isChecked={formData.expertise.includes(option)}
                          onChange={(e) => handleArrayChange('expertise', option, e.target.checked)}
                        >
                          {option}
                        </Checkbox>
                      ))}
                    </Grid>
                  </FormControl>
                </VStack>

                <Divider />

                {/* Mentoring Information */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Mentoring Information
                  </Heading>
                  
                  <FormControl>
                    <FormLabel>Previous Mentoring Experience</FormLabel>
                    <Textarea
                      value={formData.mentorshipExperience}
                      onChange={(e) => handleInputChange('mentorshipExperience', e.target.value)}
                      placeholder="Describe any previous mentoring, teaching, or coaching experience"
                      rows={3}
                    />
                  </FormControl>
                  
                  <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={4}>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Available Hours per Week</FormLabel>
                        <Select
                          value={formData.availableHours}
                          onChange={(e) => handleInputChange('availableHours', e.target.value)}
                          placeholder="Select availability"
                        >
                          <option value="1-2">1-2 hours</option>
                          <option value="3-5">3-5 hours</option>
                          <option value="6-10">6-10 hours</option>
                          <option value="11+">11+ hours</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Preferred Age Group</FormLabel>
                        <Select
                          value={formData.preferredAgeGroup}
                          onChange={(e) => handleInputChange('preferredAgeGroup', e.target.value)}
                          placeholder="Select age group"
                        >
                          <option value="elementary">Elementary (6-11)</option>
                          <option value="middle">Middle School (12-14)</option>
                          <option value="high">High School (15-18)</option>
                          <option value="adult">Adult Learners (18+)</option>
                          <option value="any">Any Age Group</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                  </Grid>
                  
                  <FormControl>
                    <FormLabel>Subjects You Can Mentor</FormLabel>
                    <Grid templateColumns={{ base: '1fr', md: 'repeat(3, 1fr)' }} gap={2}>
                      {subjectOptions.map((option) => (
                        <Checkbox
                          key={option}
                          isChecked={formData.subjects.includes(option)}
                          onChange={(e) => handleArrayChange('subjects', option, e.target.checked)}
                        >
                          {option}
                        </Checkbox>
                      ))}
                    </Grid>
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Languages You Speak</FormLabel>
                    <Grid templateColumns={{ base: '1fr', md: 'repeat(3, 1fr)' }} gap={2}>
                      {languageOptions.map((option) => (
                        <Checkbox
                          key={option}
                          isChecked={formData.languages.includes(option)}
                          onChange={(e) => handleArrayChange('languages', option, e.target.checked)}
                        >
                          {option}
                        </Checkbox>
                      ))}
                    </Grid>
                  </FormControl>
                </VStack>

                <Divider />

                {/* Motivation */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Motivation & Goals
                  </Heading>
                  
                  <FormControl>
                    <FormLabel>Why do you want to become a mentor?</FormLabel>
                    <Textarea
                      value={formData.motivation}
                      onChange={(e) => handleInputChange('motivation', e.target.value)}
                      placeholder="Share your motivation for becoming a mentor"
                      rows={4}
                    />
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>What are your goals as a mentor?</FormLabel>
                    <Textarea
                      value={formData.goals}
                      onChange={(e) => handleInputChange('goals', e.target.value)}
                      placeholder="Describe what you hope to achieve as a mentor"
                      rows={3}
                    />
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Additional Information</FormLabel>
                    <Textarea
                      value={formData.additionalInfo}
                      onChange={(e) => handleInputChange('additionalInfo', e.target.value)}
                      placeholder="Any additional information you'd like to share"
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
                      isChecked={formData.backgroundCheck}
                      onChange={(e) => handleInputChange('backgroundCheck', e.target.checked)}
                    >
                      I agree to undergo a background check if selected as a mentor
                    </Checkbox>
                    
                    <Checkbox
                      isChecked={formData.termsAccepted}
                      onChange={(e) => handleInputChange('termsAccepted', e.target.checked)}
                    >
                      I accept the Terms of Service and Mentor Guidelines *
                    </Checkbox>
                    
                    <Checkbox
                      isChecked={formData.privacyAccepted}
                      onChange={(e) => handleInputChange('privacyAccepted', e.target.checked)}
                    >
                      I accept the Privacy Policy *
                    </Checkbox>
                  </VStack>
                </VStack>

                {/* Submit Button */}
                <Button
                  type="submit"
                  colorScheme="purple"
                  size="lg"
                  isLoading={isSubmitting}
                  loadingText="Submitting Application..."
                  rightIcon={<CheckIcon />}
                  _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
                  transition="all 0.2s"
                >
                  Submit Application
                </Button>
              </VStack>
            </form>
          </Box>
        </VStack>
      </Container>
    </Box>
  );
};

export default BecomeAMentorPage;
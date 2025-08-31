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
  RadioGroup,
  Radio,
  Stack,
  Badge,
  SimpleGrid,
} from '@chakra-ui/react';
import { ArrowBackIcon, CheckIcon } from '@chakra-ui/icons';
import { saveFormSubmission, createFormSubmission } from '../utils/formSubmission';

interface DonationFormData {
  // Donor Information
  donorType: 'individual' | 'organization';
  firstName: string;
  lastName: string;
  organizationName: string;
  email: string;
  phone: string;
  country: string;
  city: string;
  
  // Donation Details
  donationType: 'one-time' | 'monthly' | 'annual';
  amount: string;
  customAmount: string;
  currency: string;
  
  // Purpose
  donationPurpose: string;
  specificProgram: string;
  
  // Recognition
  isAnonymous: boolean;
  publicRecognition: boolean;
  dedicationMessage: string;
  
  // Additional
  motivation: string;
  additionalInfo: string;
  newsletter: boolean;
  updates: boolean;
  
  // Agreements
  termsAccepted: boolean;
  privacyAccepted: boolean;
}

const SupportMissionPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const toast = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const [formData, setFormData] = useState<DonationFormData>({
    donorType: 'individual',
    firstName: '',
    lastName: '',
    organizationName: '',
    email: '',
    phone: '',
    country: '',
    city: '',
    donationType: 'one-time',
    amount: '',
    customAmount: '',
    currency: 'USD',
    donationPurpose: '',
    specificProgram: '',
    isAnonymous: false,
    publicRecognition: false,
    dedicationMessage: '',
    motivation: '',
    additionalInfo: '',
    newsletter: false,
    updates: false,
    termsAccepted: false,
    privacyAccepted: false,
  });

  const handleInputChange = (field: keyof DonationFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!formData.email) {
      toast({
        title: 'Required Fields Missing',
        description: 'Please fill in all required fields.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }
    
    if (formData.donorType === 'individual' && (!formData.firstName || !formData.lastName)) {
      toast({
        title: 'Name Required',
        description: 'Please enter your first and last name.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }
    
    if (formData.donorType === 'organization' && !formData.organizationName) {
      toast({
        title: 'Organization Name Required',
        description: 'Please enter your organization name.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }
    
    if (!formData.amount && !formData.customAmount) {
      toast({
        title: 'Donation Amount Required',
        description: 'Please select or enter a donation amount.',
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
      const submission = createFormSubmission('donation', formData);
      await saveFormSubmission(submission);
      
      toast({
        title: 'Donation Submitted!',
        description: 'Thank you for your generous support! Your donation information has been recorded and we will contact you with next steps.',
        status: 'success',
        duration: 7000,
        isClosable: true,
      });
      
      // Reset form
      setFormData({
        donorType: 'individual',
        firstName: '',
        lastName: '',
        organizationName: '',
        email: '',
        phone: '',
        country: '',
        city: '',
        donationType: 'one-time',
        amount: '',
        customAmount: '',
        currency: 'USD',
        donationPurpose: '',
        specificProgram: '',
        isAnonymous: false,
        publicRecognition: false,
        dedicationMessage: '',
        motivation: '',
        additionalInfo: '',
        newsletter: false,
        updates: false,
        termsAccepted: false,
        privacyAccepted: false,
      });
      
    } catch (error) {
      toast({
        title: 'Submission Failed',
        description: 'There was an error submitting your donation. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const donationAmounts = [
    { value: '25', label: '$25' },
    { value: '50', label: '$50' },
    { value: '100', label: '$100' },
    { value: '250', label: '$250' },
    { value: '500', label: '$500' },
    { value: '1000', label: '$1,000' },
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
              Support Our Mission
            </Heading>
            <Text
              fontSize="lg"
              color={useColorModeValue('gray.600', 'gray.300')}
              maxW="2xl"
            >
              Your donation helps us provide quality AI-powered education to students worldwide.
              Every contribution makes a difference in shaping the future of learning.
            </Text>
          </VStack>

          {/* Impact Stats */}
          <Box
            bg={useColorModeValue('white', 'gray.800')}
            p={6}
            borderRadius="xl"
            boxShadow="md"
          >
            <VStack spacing={4}>
              <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                Your Impact
              </Heading>
              <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} w="full">
                <VStack>
                  <Text fontSize="2xl" fontWeight="bold" color="purple.500">$25</Text>
                  <Text fontSize="sm" textAlign="center" color={useColorModeValue('gray.600', 'gray.300')}>
                    Provides 1 month of AI tutoring for a student
                  </Text>
                </VStack>
                <VStack>
                  <Text fontSize="2xl" fontWeight="bold" color="green.500">$100</Text>
                  <Text fontSize="sm" textAlign="center" color={useColorModeValue('gray.600', 'gray.300')}>
                    Sponsors a complete course for a student
                  </Text>
                </VStack>
                <VStack>
                  <Text fontSize="2xl" fontWeight="bold" color="blue.500">$500</Text>
                  <Text fontSize="sm" textAlign="center" color={useColorModeValue('gray.600', 'gray.300')}>
                    Funds technology infrastructure for 10 students
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
                {/* Donor Type */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Donor Information
                  </Heading>
                  
                  <FormControl>
                    <FormLabel>I am donating as:</FormLabel>
                    <RadioGroup
                      value={formData.donorType}
                      onChange={(value: 'individual' | 'organization') => handleInputChange('donorType', value)}
                    >
                      <Stack direction="row" spacing={6}>
                        <Radio value="individual">Individual</Radio>
                        <Radio value="organization">Organization</Radio>
                      </Stack>
                    </RadioGroup>
                  </FormControl>
                  
                  {formData.donorType === 'individual' ? (
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
                    </Grid>
                  ) : (
                    <FormControl isRequired>
                      <FormLabel>Organization Name</FormLabel>
                      <Input
                        value={formData.organizationName}
                        onChange={(e) => handleInputChange('organizationName', e.target.value)}
                        placeholder="Enter organization name"
                      />
                    </FormControl>
                  )}
                  
                  <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={4}>
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

                {/* Donation Details */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Donation Details
                  </Heading>
                  
                  <FormControl>
                    <FormLabel>Donation Type</FormLabel>
                    <RadioGroup
                      value={formData.donationType}
                      onChange={(value: 'one-time' | 'monthly' | 'annual') => handleInputChange('donationType', value)}
                    >
                      <Stack direction={{ base: 'column', md: 'row' }} spacing={6}>
                        <Radio value="one-time">One-time</Radio>
                        <Radio value="monthly">
                          <HStack>
                            <Text>Monthly</Text>
                            <Badge colorScheme="green" size="sm">Recurring</Badge>
                          </HStack>
                        </Radio>
                        <Radio value="annual">
                          <HStack>
                            <Text>Annual</Text>
                            <Badge colorScheme="blue" size="sm">Recurring</Badge>
                          </HStack>
                        </Radio>
                      </Stack>
                    </RadioGroup>
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Donation Amount</FormLabel>
                    <SimpleGrid columns={{ base: 2, md: 3 }} spacing={3} mb={4}>
                      {donationAmounts.map((amount) => (
                        <Button
                          key={amount.value}
                          variant={formData.amount === amount.value ? 'solid' : 'outline'}
                          colorScheme={formData.amount === amount.value ? 'purple' : 'gray'}
                          onClick={() => {
                            handleInputChange('amount', amount.value);
                            handleInputChange('customAmount', '');
                          }}
                        >
                          {amount.label}
                        </Button>
                      ))}
                    </SimpleGrid>
                    
                    <HStack>
                      <Select
                        value={formData.currency}
                        onChange={(e) => handleInputChange('currency', e.target.value)}
                        w="100px"
                      >
                        <option value="USD">USD</option>
                        <option value="EUR">EUR</option>
                        <option value="GBP">GBP</option>
                        <option value="CAD">CAD</option>
                        <option value="AUD">AUD</option>
                      </Select>
                      <Input
                        placeholder="Custom amount"
                        value={formData.customAmount}
                        onChange={(e) => {
                          handleInputChange('customAmount', e.target.value);
                          handleInputChange('amount', '');
                        }}
                        type="number"
                        min="1"
                      />
                    </HStack>
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Donation Purpose</FormLabel>
                    <Select
                      value={formData.donationPurpose}
                      onChange={(e) => handleInputChange('donationPurpose', e.target.value)}
                      placeholder="Select donation purpose"
                    >
                      <option value="general">General Support</option>
                      <option value="scholarships">Student Scholarships</option>
                      <option value="technology">Technology Infrastructure</option>
                      <option value="content">Content Development</option>
                      <option value="teacher-training">Teacher Training</option>
                      <option value="research">Research & Development</option>
                      <option value="accessibility">Accessibility Programs</option>
                    </Select>
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Specific Program (Optional)</FormLabel>
                    <Input
                      value={formData.specificProgram}
                      onChange={(e) => handleInputChange('specificProgram', e.target.value)}
                      placeholder="e.g., AI Math Tutoring, Science Lab Access"
                    />
                  </FormControl>
                </VStack>

                <Divider />

                {/* Recognition */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Recognition Preferences
                  </Heading>
                  
                  <VStack spacing={3} align="stretch">
                    <Checkbox
                      isChecked={formData.isAnonymous}
                      onChange={(e) => handleInputChange('isAnonymous', e.target.checked)}
                    >
                      I prefer to remain anonymous
                    </Checkbox>
                    
                    <Checkbox
                      isChecked={formData.publicRecognition}
                      onChange={(e) => handleInputChange('publicRecognition', e.target.checked)}
                      isDisabled={formData.isAnonymous}
                    >
                      I consent to public recognition (website, reports, etc.)
                    </Checkbox>
                  </VStack>
                  
                  <FormControl>
                    <FormLabel>Dedication Message (Optional)</FormLabel>
                    <Textarea
                      value={formData.dedicationMessage}
                      onChange={(e) => handleInputChange('dedicationMessage', e.target.value)}
                      placeholder="In honor of... or In memory of..."
                      rows={2}
                    />
                  </FormControl>
                </VStack>

                <Divider />

                {/* Additional Information */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Additional Information
                  </Heading>
                  
                  <FormControl>
                    <FormLabel>What motivates your donation?</FormLabel>
                    <Textarea
                      value={formData.motivation}
                      onChange={(e) => handleInputChange('motivation', e.target.value)}
                      placeholder="Share what inspired you to support our mission"
                      rows={3}
                    />
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Additional Comments</FormLabel>
                    <Textarea
                      value={formData.additionalInfo}
                      onChange={(e) => handleInputChange('additionalInfo', e.target.value)}
                      placeholder="Any additional information or special requests"
                      rows={2}
                    />
                  </FormControl>
                  
                  <VStack spacing={3} align="stretch">
                    <Checkbox
                      isChecked={formData.newsletter}
                      onChange={(e) => handleInputChange('newsletter', e.target.checked)}
                    >
                      Subscribe to our newsletter
                    </Checkbox>
                    
                    <Checkbox
                      isChecked={formData.updates}
                      onChange={(e) => handleInputChange('updates', e.target.checked)}
                    >
                      Receive updates on how my donation is being used
                    </Checkbox>
                  </VStack>
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
                      I accept the Terms of Service and Donation Policy *
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
                  loadingText="Processing Donation..."
                  rightIcon={<CheckIcon />}
                  _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
                  transition="all 0.2s"
                >
                  {formData.donationType === 'one-time' ? 'Donate Now' : `Start ${formData.donationType} Donation`}
                </Button>
                
                <Text fontSize="sm" color={useColorModeValue('gray.500', 'gray.400')} textAlign="center">
                  This form collects your donation information. You will be contacted with secure payment instructions.
                </Text>
              </VStack>
            </form>
          </Box>
        </VStack>
      </Container>
    </Box>
  );
};

export default SupportMissionPage;
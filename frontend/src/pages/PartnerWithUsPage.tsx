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
} from '@chakra-ui/react';
import { ArrowBackIcon, CheckIcon } from '@chakra-ui/icons';
import { saveFormSubmission, createFormSubmission } from '../utils/formSubmission';

interface PartnerFormData {
  // Organization Information
  organizationName: string;
  organizationType: string;
  website: string;
  foundedYear: string;
  size: string;
  
  // Contact Information
  contactName: string;
  contactTitle: string;
  email: string;
  phone: string;
  country: string;
  city: string;
  
  // Partnership Details
  partnershipType: string;
  partnershipGoals: string;
  resources: string[];
  timeline: string;
  budget: string;
  
  // Organization Details
  mission: string;
  targetAudience: string;
  currentPrograms: string;
  experience: string;
  
  // Collaboration
  proposedCollaboration: string;
  expectedOutcomes: string;
  additionalInfo: string;
  
  // Agreements
  termsAccepted: boolean;
  privacyAccepted: boolean;
}

const PartnerWithUsPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const toast = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const [formData, setFormData] = useState<PartnerFormData>({
    organizationName: '',
    organizationType: '',
    website: '',
    foundedYear: '',
    size: '',
    contactName: '',
    contactTitle: '',
    email: '',
    phone: '',
    country: '',
    city: '',
    partnershipType: '',
    partnershipGoals: '',
    resources: [],
    timeline: '',
    budget: '',
    mission: '',
    targetAudience: '',
    currentPrograms: '',
    experience: '',
    proposedCollaboration: '',
    expectedOutcomes: '',
    additionalInfo: '',
    termsAccepted: false,
    privacyAccepted: false,
  });

  const handleInputChange = (field: keyof PartnerFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleArrayChange = (field: keyof PartnerFormData, value: string, checked: boolean) => {
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
    if (!formData.organizationName || !formData.contactName || !formData.email) {
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
      const submission = createFormSubmission('partner', formData);
      await saveFormSubmission(submission);
      
      toast({
        title: 'Partnership Application Submitted!',
        description: 'Thank you for your interest in partnering with us. We will review your application and contact you soon.',
        status: 'success',
        duration: 7000,
        isClosable: true,
      });
      
      // Reset form
      setFormData({
        organizationName: '',
        organizationType: '',
        website: '',
        foundedYear: '',
        size: '',
        contactName: '',
        contactTitle: '',
        email: '',
        phone: '',
        country: '',
        city: '',
        partnershipType: '',
        partnershipGoals: '',
        resources: [],
        timeline: '',
        budget: '',
        mission: '',
        targetAudience: '',
        currentPrograms: '',
        experience: '',
        proposedCollaboration: '',
        expectedOutcomes: '',
        additionalInfo: '',
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

  const resourceOptions = [
    'Funding', 'Technology', 'Content Development', 'Marketing Support',
    'Research Collaboration', 'Student Access', 'Teacher Training',
    'Infrastructure', 'Data Analytics', 'Legal Support'
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
              Partner With Us
            </Heading>
            <Text
              fontSize="lg"
              color={useColorModeValue('gray.600', 'gray.300')}
              maxW="2xl"
            >
              Join forces with Singularity Academy to revolutionize education.
              Together, we can create innovative learning experiences and expand our impact.
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
                {/* Organization Information */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Organization Information
                  </Heading>
                  <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={4}>
                    <GridItem colSpan={{ base: 1, md: 2 }}>
                      <FormControl isRequired>
                        <FormLabel>Organization Name</FormLabel>
                        <Input
                          value={formData.organizationName}
                          onChange={(e) => handleInputChange('organizationName', e.target.value)}
                          placeholder="Enter your organization name"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Organization Type</FormLabel>
                        <Select
                          value={formData.organizationType}
                          onChange={(e) => handleInputChange('organizationType', e.target.value)}
                          placeholder="Select organization type"
                        >
                          <option value="educational-institution">Educational Institution</option>
                          <option value="technology-company">Technology Company</option>
                          <option value="nonprofit">Non-Profit Organization</option>
                          <option value="government">Government Agency</option>
                          <option value="foundation">Foundation</option>
                          <option value="startup">Startup</option>
                          <option value="corporation">Corporation</option>
                          <option value="other">Other</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Website</FormLabel>
                        <Input
                          value={formData.website}
                          onChange={(e) => handleInputChange('website', e.target.value)}
                          placeholder="https://www.example.com"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Founded Year</FormLabel>
                        <Input
                          type="number"
                          value={formData.foundedYear}
                          onChange={(e) => handleInputChange('foundedYear', e.target.value)}
                          placeholder="e.g., 2020"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Organization Size</FormLabel>
                        <Select
                          value={formData.size}
                          onChange={(e) => handleInputChange('size', e.target.value)}
                          placeholder="Select size"
                        >
                          <option value="1-10">1-10 employees</option>
                          <option value="11-50">11-50 employees</option>
                          <option value="51-200">51-200 employees</option>
                          <option value="201-1000">201-1000 employees</option>
                          <option value="1000+">1000+ employees</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                  </Grid>
                </VStack>

                <Divider />

                {/* Contact Information */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Contact Information
                  </Heading>
                  <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={4}>
                    <GridItem>
                      <FormControl isRequired>
                        <FormLabel>Contact Name</FormLabel>
                        <Input
                          value={formData.contactName}
                          onChange={(e) => handleInputChange('contactName', e.target.value)}
                          placeholder="Enter contact person's name"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Contact Title</FormLabel>
                        <Input
                          value={formData.contactTitle}
                          onChange={(e) => handleInputChange('contactTitle', e.target.value)}
                          placeholder="e.g., CEO, Director, Manager"
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
                          placeholder="Enter email address"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Phone</FormLabel>
                        <Input
                          value={formData.phone}
                          onChange={(e) => handleInputChange('phone', e.target.value)}
                          placeholder="Enter phone number"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Country</FormLabel>
                        <Input
                          value={formData.country}
                          onChange={(e) => handleInputChange('country', e.target.value)}
                          placeholder="Enter country"
                        />
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>City</FormLabel>
                        <Input
                          value={formData.city}
                          onChange={(e) => handleInputChange('city', e.target.value)}
                          placeholder="Enter city"
                        />
                      </FormControl>
                    </GridItem>
                  </Grid>
                </VStack>

                <Divider />

                {/* Partnership Details */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Partnership Details
                  </Heading>
                  
                  <FormControl>
                    <FormLabel>Type of Partnership</FormLabel>
                    <RadioGroup
                      value={formData.partnershipType}
                      onChange={(value) => handleInputChange('partnershipType', value)}
                    >
                      <Stack direction="column" spacing={2}>
                        <Radio value="strategic">Strategic Partnership</Radio>
                        <Radio value="technology">Technology Partnership</Radio>
                        <Radio value="content">Content Partnership</Radio>
                        <Radio value="funding">Funding Partnership</Radio>
                        <Radio value="research">Research Collaboration</Radio>
                        <Radio value="distribution">Distribution Partnership</Radio>
                        <Radio value="other">Other</Radio>
                      </Stack>
                    </RadioGroup>
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Partnership Goals</FormLabel>
                    <Textarea
                      value={formData.partnershipGoals}
                      onChange={(e) => handleInputChange('partnershipGoals', e.target.value)}
                      placeholder="Describe what you hope to achieve through this partnership"
                      rows={3}
                    />
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Resources You Can Provide</FormLabel>
                    <Grid templateColumns={{ base: '1fr', md: 'repeat(2, 1fr)' }} gap={2}>
                      {resourceOptions.map((option) => (
                        <Checkbox
                          key={option}
                          isChecked={formData.resources.includes(option)}
                          onChange={(e) => handleArrayChange('resources', option, e.target.checked)}
                        >
                          {option}
                        </Checkbox>
                      ))}
                    </Grid>
                  </FormControl>
                  
                  <Grid templateColumns={{ base: '1fr', md: '1fr 1fr' }} gap={4}>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Preferred Timeline</FormLabel>
                        <Select
                          value={formData.timeline}
                          onChange={(e) => handleInputChange('timeline', e.target.value)}
                          placeholder="Select timeline"
                        >
                          <option value="immediate">Immediate (1-3 months)</option>
                          <option value="short-term">Short-term (3-6 months)</option>
                          <option value="medium-term">Medium-term (6-12 months)</option>
                          <option value="long-term">Long-term (1+ years)</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                    <GridItem>
                      <FormControl>
                        <FormLabel>Budget Range (Optional)</FormLabel>
                        <Select
                          value={formData.budget}
                          onChange={(e) => handleInputChange('budget', e.target.value)}
                          placeholder="Select budget range"
                        >
                          <option value="under-10k">Under $10,000</option>
                          <option value="10k-50k">$10,000 - $50,000</option>
                          <option value="50k-100k">$50,000 - $100,000</option>
                          <option value="100k-500k">$100,000 - $500,000</option>
                          <option value="500k+">$500,000+</option>
                          <option value="non-monetary">Non-monetary</option>
                        </Select>
                      </FormControl>
                    </GridItem>
                  </Grid>
                </VStack>

                <Divider />

                {/* Organization Details */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    About Your Organization
                  </Heading>
                  
                  <FormControl>
                    <FormLabel>Mission Statement</FormLabel>
                    <Textarea
                      value={formData.mission}
                      onChange={(e) => handleInputChange('mission', e.target.value)}
                      placeholder="Describe your organization's mission and values"
                      rows={3}
                    />
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Target Audience</FormLabel>
                    <Textarea
                      value={formData.targetAudience}
                      onChange={(e) => handleInputChange('targetAudience', e.target.value)}
                      placeholder="Who does your organization serve?"
                      rows={2}
                    />
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Current Programs/Services</FormLabel>
                    <Textarea
                      value={formData.currentPrograms}
                      onChange={(e) => handleInputChange('currentPrograms', e.target.value)}
                      placeholder="Describe your current programs, services, or products"
                      rows={3}
                    />
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Relevant Experience</FormLabel>
                    <Textarea
                      value={formData.experience}
                      onChange={(e) => handleInputChange('experience', e.target.value)}
                      placeholder="Describe any relevant experience in education, technology, or partnerships"
                      rows={3}
                    />
                  </FormControl>
                </VStack>

                <Divider />

                {/* Collaboration */}
                <VStack spacing={4} align="stretch">
                  <Heading size="md" color={useColorModeValue('gray.800', 'white')}>
                    Proposed Collaboration
                  </Heading>
                  
                  <FormControl>
                    <FormLabel>Collaboration Proposal</FormLabel>
                    <Textarea
                      value={formData.proposedCollaboration}
                      onChange={(e) => handleInputChange('proposedCollaboration', e.target.value)}
                      placeholder="Describe your specific ideas for collaboration with Singularity Academy"
                      rows={4}
                    />
                  </FormControl>
                  
                  <FormControl>
                    <FormLabel>Expected Outcomes</FormLabel>
                    <Textarea
                      value={formData.expectedOutcomes}
                      onChange={(e) => handleInputChange('expectedOutcomes', e.target.value)}
                      placeholder="What outcomes do you expect from this partnership?"
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
                      isChecked={formData.termsAccepted}
                      onChange={(e) => handleInputChange('termsAccepted', e.target.checked)}
                    >
                      I accept the Terms of Service and Partnership Guidelines *
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
                  colorScheme="green"
                  size="lg"
                  isLoading={isSubmitting}
                  loadingText="Submitting Application..."
                  rightIcon={<CheckIcon />}
                  _hover={{ transform: 'translateY(-2px)', boxShadow: 'lg' }}
                  transition="all 0.2s"
                >
                  Submit Partnership Application
                </Button>
              </VStack>
            </form>
          </Box>
        </VStack>
      </Container>
    </Box>
  );
};

export default PartnerWithUsPage;
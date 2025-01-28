import React from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Text,
  useToast,
  Container,
  Heading,
  Link,
} from '@chakra-ui/react';
import {API_ENDPOINTS, ErrorResponse} from "../../config/api";
import axiosInstance, {getToastMessage} from "../../utils/axios";
import {AxiosError} from "axios";
import Navbar from "../../components/Navbar";

interface RegisterFormInputs {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

const RegisterPage: React.FC = () => {
  const { register, handleSubmit, watch, formState: { errors } } = useForm<RegisterFormInputs>();
  const navigate = useNavigate();
  const toast = useToast();

  const onSubmit = async (data: RegisterFormInputs) => {
    try {
      await axiosInstance.post(API_ENDPOINTS.AUTH.REGISTER, data);
      toast({
        title: 'Registration successful',
        description: 'Please login with your credentials',
        status: 'success',
        duration: 3000,
      });
      navigate('/login');
    } catch (err) {
      const error = err as AxiosError<ErrorResponse>;
      toast(getToastMessage(error));
    }
  };

  return (
      <><Navbar/><Container maxW="container.sm" py={10} mt={16}>
        <VStack spacing={8}>
          <Heading>Create Account</Heading>
          <Box w="100%" p={8} borderWidth={1} borderRadius="lg" boxShadow="lg">
            <form onSubmit={handleSubmit(onSubmit)}>
              <VStack spacing={4}>
                <FormControl isInvalid={!!errors.name}>
                  <FormLabel>Full Name</FormLabel>
                  <Input
                      {...register('name', {
                        required: 'Name is required',
                        minLength: {
                          value: 2,
                          message: 'Name must be at least 2 characters',
                        },
                      })} />
                  {errors.name && (
                      <Text color="red.500" fontSize="sm">
                        {errors.name.message}
                      </Text>
                  )}
                </FormControl>

                <FormControl isInvalid={!!errors.email}>
                  <FormLabel>Email</FormLabel>
                  <Input
                      type="email"
                      {...register('email', {
                        required: 'Email is required',
                        pattern: {
                          value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                          message: 'Invalid email address',
                        },
                      })} />
                  {errors.email && (
                      <Text color="red.500" fontSize="sm">
                        {errors.email.message}
                      </Text>
                  )}
                </FormControl>

                <FormControl isInvalid={!!errors.password}>
                  <FormLabel>Password</FormLabel>
                  <Input
                      type="password"
                      {...register('password', {
                        required: 'Password is required',
                        minLength: {
                          value: 6,
                          message: 'Password must be at least 6 characters',
                        },
                      })} />
                  {errors.password && (
                      <Text color="red.500" fontSize="sm">
                        {errors.password.message}
                      </Text>
                  )}
                </FormControl>

                <FormControl isInvalid={!!errors.confirmPassword}>
                  <FormLabel>Confirm Password</FormLabel>
                  <Input
                      type="password"
                      {...register('confirmPassword', {
                        validate: value => value === watch('password') || 'Passwords do not match',
                      })} />
                  {errors.confirmPassword && (
                      <Text color="red.500" fontSize="sm">
                        {errors.confirmPassword.message}
                      </Text>
                  )}
                </FormControl>

                <Button
                    type="submit"
                    colorScheme="blue"
                    width="100%"
                    size="lg"
                    mt={4}
                >
                  Sign Up
                </Button>
              </VStack>
            </form>
          </Box>
          <Text>
            Already have an account?{' '}
            <Link color="blue.500" onClick={() => navigate('/login')}>
              Sign in
            </Link>
          </Text>
        </VStack>
      </Container></>
  );
}; // End of RegisterPage component

export default RegisterPage;
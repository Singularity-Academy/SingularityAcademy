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
import {API_ENDPOINTS, ErrorResponse} from "@/config/api";
import axiosInstance, {getToastMessage} from "@utils/axios";
import {AxiosError} from "axios";
import Navbar from "@components/Navbar";
import {useTranslation} from "react-i18next";

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
  const { t } = useTranslation();

  const onSubmit = async (data: RegisterFormInputs) => {
    try {
      await axiosInstance.post(API_ENDPOINTS.AUTH.REGISTER, data);
      toast({
        title: t("api.auth.registrationSuccessful"),
        description: t("api.auth.loginWithCredentials"),
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
          <Heading>{ t('RegisterPage.createAccount') }</Heading>
          <Box w="100%" p={8} borderWidth={1} borderRadius="lg" boxShadow="lg">
            <form onSubmit={handleSubmit(onSubmit)}>
              <VStack spacing={4}>
                <FormControl isInvalid={!!errors.name}>
                  <FormLabel>{ t('common.fullName') }</FormLabel>
                  <Input
                      {...register('name', {
                        required: t('auth.nameIsRequired'),
                        minLength: {
                          value: 2,
                          message: t('auth.name2Characters'),
                        },
                      })} />
                  {errors.name && (
                      <Text color="red.500" fontSize="sm">
                        {errors.name.message}
                      </Text>
                  )}
                </FormControl>

                <FormControl isInvalid={!!errors.email}>
                  <FormLabel>{t('common.email')}</FormLabel>
                  <Input
                      type="email"
                      {...register('email', {
                        required: t('auth.emailIsRequired'),
                        pattern: {
                          value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                          message: t('auth.invalidEmailAddress'),
                        },
                      })} />
                  {errors.email && (
                      <Text color="red.500" fontSize="sm">
                        {errors.email.message}
                      </Text>
                  )}
                </FormControl>

                <FormControl isInvalid={!!errors.password}>
                  <FormLabel>{t('common.password')}</FormLabel>
                  <Input
                      type="password"
                      {...register('password', {
                        required: t('auth.passwordIsRequired'),
                        minLength: {
                          value: 6,
                          message: t('auth.password6Characters'),
                        },
                      })} />
                  {errors.password && (
                      <Text color="red.500" fontSize="sm">
                        {errors.password.message}
                      </Text>
                  )}
                </FormControl>

                <FormControl isInvalid={!!errors.confirmPassword}>
                  <FormLabel>{ t('common.confirmPassword') }</FormLabel>
                  <Input
                      type="password"
                      {...register('confirmPassword', {
                        validate: value => value === watch('password') || t('auth.passwordsDoNotMatch'),
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
                  { t('common.signUp') }
                </Button>
              </VStack>
            </form>
          </Box>
          <Text>
            { t("RegisterPage.alreadyHaveAnAccount") }{' '}
            <Link color="blue.500" onClick={() => navigate('/login')}>
              { t('common.signIn') }
            </Link>
          </Text>
        </VStack>
      </Container></>
  );
}; // End of RegisterPage component

export default RegisterPage;
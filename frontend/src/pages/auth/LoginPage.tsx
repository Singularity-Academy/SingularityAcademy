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

import Cookies from 'js-cookie';
import {API_ENDPOINTS, ErrorResponse} from '@/config/api';
import axiosInstance, {getToastMessage} from '@utils/axios';
import {AxiosError} from "axios";
import Navbar from "@components/Navbar";
import {useTranslation} from "react-i18next";

interface LoginFormInputs {
  email: string;
  password: string;
}

const LoginPage: React.FC = () => {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginFormInputs>();
  const navigate = useNavigate();
  const toast = useToast();
  const { t } = useTranslation();

  const onSubmit = async (data: LoginFormInputs) => {
    try {
      const response = await axiosInstance.post(API_ENDPOINTS.AUTH.LOGIN, data);
      const { token } = response.data;
      Cookies.set('token', token, { expires: 30, secure: false, sameSite: 'strict' });
      toast({
        title: t('api.auth.loginSuccessful'),
        status: 'success',
        duration: 3000,
      });
      navigate('/dashboard');
    } catch (err) {
      const error = err as AxiosError<ErrorResponse>;
      toast(getToastMessage(error));
    }
  };

  return (
      <><Navbar/><Container maxW="container.sm" py={10} mt={16}>
        <VStack spacing={8}>
          <Heading>{t("LoginPage.wellcomeBack")}</Heading>
          <Box w="100%" p={8} borderWidth={1} borderRadius="lg" boxShadow="lg">
            <form onSubmit={handleSubmit(onSubmit)}>
              <VStack spacing={4}>
                <FormControl isInvalid={!!errors.email}>
                  <FormLabel>{t("common.email")}</FormLabel>
                  <Input
                      type="email"
                      {...register('email', {
                        required: t('auth.emailIsRequired'),
                        pattern: {
                          value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                          message: t('auth.invalidEmailAddress'),
                        },
                      })} />
                  {errors.email && <Text color="red.500" fontSize="sm">{errors.email.message}</Text>}
                </FormControl>

                <FormControl isInvalid={!!errors.password}>
                  <FormLabel>{t("common.password")}</FormLabel>
                  <Input
                      type="password"
                      {...register('password', {
                        required:  t('auth.passwordIsRequired'),
                        minLength: {
                          value: 6,
                          message:  t('auth.password6Characters'),
                        },
                      })} />
                  {errors.password && <Text color="red.500" fontSize="sm">{errors.password.message}</Text>}
                </FormControl>

                <Button
                    type="submit"
                    colorScheme="blue"
                    width="100%"
                    size="lg"
                    mt={4}
                    isLoading={isSubmitting} // loading indicator
                >
                  { t('common.signIn') }
                </Button>
              </VStack>
            </form>
          </Box>
          <Text>
            { t('LoginPage.doNotHaveAnAccount') }{' '}
            <Link color="blue.500" onClick={() => navigate('/register')}>
              { t("common.signUp") }
            </Link>
          </Text>
        </VStack>
      </Container></>
  );
};

export default LoginPage;

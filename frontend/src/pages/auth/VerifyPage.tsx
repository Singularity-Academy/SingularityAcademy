import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  Box,
  Container,
  VStack,
  Heading,
  Text,
  useToast,
  Button,
} from '@chakra-ui/react';
import { API_ENDPOINTS } from '@/config/api';
import axiosInstance, { getToastMessage } from '@/utils/axios';
import { AxiosError } from 'axios';
import { ErrorResponse as ApiErrorResponse } from '@/config/api';
import { motion, Variants } from 'framer-motion';
import { FaCheckCircle, FaTimesCircle, FaHourglassHalf } from 'react-icons/fa';
import Navbar from "@components/Navbar";

interface ErrorResponse extends ApiErrorResponse {
  message: string;
  status: number;
  error: string;
  detail: string;
}

const VerifyPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const toast = useToast();
  const [verificationStatus, setVerificationStatus] = useState<'verifying' | 'success' | 'error'>('verifying');

  const fadeIn: Variants = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 }
  };

  const founderMessage = {
    title: "欢迎加入我们的学习社区！",
    message: "我们很高兴您加入我们革新在线教育的使命。让我们一起创造非凡的学习之旅。",
    founders: [
      { name: "Jiace Zhao", role: "CEO & 联合创始人" },
      { name: "Di Huang", role: "CTO & 联合创始人" }
    ]
  };

  useEffect(() => {
    const verifyEmail = async () => {
      const token = searchParams.get('token');
      
      if (!token) {
        setVerificationStatus('error');
        toast({
          title: '验证失败',
          description: '无效的验证链接',
          status: 'error',
          duration: 5000,
        });
        return;
      }

      try {
        await axiosInstance.post(API_ENDPOINTS.AUTH.VERIFY, { token });
        setVerificationStatus('success');
        toast({
          title: '邮箱已验证',
          description: '您的邮箱已成功验证',
          status: 'success',
          duration: 5000,
        });
      } catch (error) {
        setVerificationStatus('error');
        const err = error as AxiosError<ErrorResponse>;
        toast(getToastMessage(err));
      }
    };

    verifyEmail();
  }, [searchParams, toast]);

  return (
      <Container maxW="container.md" py={20} mt={16}>
        <motion.div initial="initial" animate="animate" variants={fadeIn}>
          <VStack spacing={12} align="center">
            <Box w="100%" p={8} borderWidth={1} borderRadius="lg" boxShadow="lg">
              <VStack spacing={8}>
                <Heading
                    size="xl"
                    bgGradient="linear(to-r, blue.400, purple.500)"
                    bgClip="text"
                >
                  邮箱验证
                </Heading>

                {verificationStatus === 'verifying' && (
                    <motion.div
                        animate={{rotate: 360}}
                        transition={{duration: 2, repeat: Infinity, ease: "linear"}}
                    >
                      <VStack spacing={4}>
                        <FaHourglassHalf size="60px" color="#4299E1"/>
                        <Text fontSize="xl">正在验证您的邮箱...</Text>
                      </VStack>
                    </motion.div>
                )}

                {verificationStatus === 'success' && (
                    <motion.div
                        initial={{scale: 0}}
                        animate={{scale: 1}}
                        transition={{type: "spring", stiffness: 260, damping: 20}}
                    >
                      <VStack spacing={6}>
                        <FaCheckCircle size="80px" color="#48BB78"/>
                        <Text
                            color="green.500"
                            fontSize="2xl"
                            fontWeight="bold"
                        >
                          您的邮箱已成功验证！
                        </Text>
                        <Button
                            size="lg"
                            colorScheme="blue"
                            onClick={() => navigate('/login')}
                            _hover={{transform: 'translateY(-2px)', boxShadow: 'lg'}}
                            transition="all 0.2s"
                        >
                          前往登录
                        </Button>
                      </VStack>
                    </motion.div>
                )}

                {verificationStatus === 'error' && (
                    <motion.div
                        initial={{scale: 0}}
                        animate={{scale: 1}}
                        transition={{type: "spring", stiffness: 260, damping: 20}}
                    >
                      <VStack spacing={6}>
                        <FaTimesCircle size="80px" color="#E53E3E"/>
                        <Text
                            color="red.500"
                            fontSize="xl"
                            fontWeight="bold"
                        >
                          验证失败。请重试或请求新的验证链接。
                        </Text>
                        <Button
                            size="lg"
                            colorScheme="blue"
                            onClick={() => navigate('/login')}
                            _hover={{transform: 'translateY(-2px)', boxShadow: 'lg'}}
                            transition="all 0.2s"
                        >
                          返回登录
                        </Button>
                      </VStack>
                    </motion.div>
                )}
              </VStack>
            </Box>

            {verificationStatus === 'success' && (
                <motion.div
                    initial={{opacity: 0, y: 30}}
                    animate={{opacity: 1, y: 0}}
                    transition={{delay: 0.5, duration: 0.8}}
                >
                  <Box
                      p={8}
                      bg="rgba(255, 255, 255, 0.95)"
                      borderRadius="xl"
                      boxShadow="xl"
                      w="100%"
                      textAlign="center"
                  >
                    <VStack spacing={6}>
                      <Heading
                          size="md"
                          bgGradient="linear(to-r, blue.400, purple.500)"
                          bgClip="text"
                      >
                        {founderMessage.title}
                      </Heading>
                      <Text fontSize="lg" color="gray.600">
                        {founderMessage.message}
                      </Text>
                      <VStack spacing={2}>
                        {founderMessage.founders.map((founder, index) => (
                            <Text key={index} fontSize="md" color="gray.500">
                              {founder.name} - {founder.role}
                            </Text>
                        ))}
                      </VStack>
                    </VStack>
                  </Box>
                </motion.div>
            )}
          </VStack>
        </motion.div>
      </Container>
  );
};

export default VerifyPage; 
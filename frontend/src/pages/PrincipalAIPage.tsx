import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Flex,
  Heading,
  Text,
  Input,
  IconButton,
  useColorModeValue,
  VStack,
  HStack,
  Card,
  CardBody,
  useToast,
} from '@chakra-ui/react';
import { FaPaperPlane, FaVideo, FaVideoSlash, FaExpand } from 'react-icons/fa';
import Navbar from '@components/Navbar';
import { useTranslation } from 'react-i18next';
import './../styles/ParticleBackground.css';
import logger from '@utils/logger';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  metadata?: any;
  timestamp?: string;
}

interface WSMessage {
  type: string;
  message_id: string;
  content: any;
  timestamp: string;
  message?: string;
  messages?: Message[];
}

const formatTimestamp = (timestamp?: string) => {
  if (!timestamp) return '';
  try {
    const date = new Date(timestamp);
    return isNaN(date.getTime()) ? 'Invalid Time' : date.toLocaleTimeString();
  } catch {
    return 'Invalid Time';
  }
};

const MessageBubble: React.FC<{ message: Message }> = ({ message }) => {
  const isAssistant = message.role === 'assistant';
  const bgColor = useColorModeValue(isAssistant ? 'blue.50' : 'green.50', isAssistant ? 'blue.900' : 'green.900');
  const borderColor = useColorModeValue(isAssistant ? 'blue.200' : 'green.200', isAssistant ? 'blue.700' : 'green.700');
  const textColor = useColorModeValue('gray.800', 'white');
  const timestampColor = useColorModeValue('gray.500', 'gray.400');
  const metadataBgColor = useColorModeValue('whiteAlpha.600', 'blackAlpha.600');
  const toast = useToast();

  const handleAddCourse = (course: { name: string; description: string }) => {
    const ws = (window as any).__principalAIWS__ as WebSocket;
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'course',
        content: {
          type: 'create',
          name: course.name,
          description: course.description,
        },
      }));
      toast({
        title: 'Course Added',
        description: `${course.name} was added.`,
        status: 'success',
        duration: 3000,
      });
    } else {
      toast({
        title: 'WebSocket Error',
        description: 'Connection is not open.',
        status: 'error',
        duration: 3000,
      });
    }
  };

  return (
    <Box
      maxW="80%"
      alignSelf={isAssistant ? 'flex-start' : 'flex-end'}
      bg={bgColor}
      color={textColor}
      p={4}
      borderRadius="lg"
      borderWidth="1px"
      borderColor={borderColor}
      boxShadow="sm"
    >
      <Text whiteSpace="pre-wrap">{message.content}</Text>

      {message.metadata?.courses && (
        <Box mt={2} p={2} bg={metadataBgColor} borderRadius="md">
          <Text fontSize="xs" color={timestampColor} mb={2}>SUGGESTED COURSES</Text>
          <VStack align="stretch">
            {message.metadata.courses.map((course: any, index: number) => (
              <Box key={index} p={3} bg="white" border="0.4px solid black" borderRadius="15px">
                <Heading size="sm" color="darkred" mb={1}>{course.name}</Heading>
                <Text>{course.description}</Text>
                <Text
                  mt={2}
                  color="blue"
                  fontSize="0.9em"
                  fontWeight="semibold"
                  cursor="pointer"
                  onClick={() => handleAddCourse(course)}
                >
                  + ADD COURSE
                </Text>
              </Box>
            ))}
          </VStack>
        </Box>
      )}

      {message.timestamp && (
        <Text fontSize="xs" color={timestampColor} mt={2}>
          {formatTimestamp(message.timestamp)}
        </Text>
      )}
    </Box>
  );
};

const PrincipalAIPage: React.FC = () => {
  const { t } = useTranslation();
  const toast = useToast();
  const particleColor = useColorModeValue('#3182ce', '#90cdf4');
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
    if (!token) return;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ai/principal-ai/ws/chat`);
    (window as any).__principalAIWS__ = ws;
    wsRef.current = ws;

    ws.onopen = () => {
      ws.send(JSON.stringify({ type: 'auth', token }));
    };

    ws.onmessage = (event) => {
      try {
        const data: WSMessage = JSON.parse(event.data);
        switch (data.type) {
          case 'auth_success': break;
          case 'history_messages':
            setMessages(data.messages || []);
            break;
          case 'metadata':
            setMessages(prev => {
              const updated = [...prev];
              const last = updated.pop();
              if (last && last.role === 'assistant') {
                updated.push({ ...last, metadata: data.content });
              } else if (last) {
                updated.push(last);
              }
              return updated;
            });
            break;
          case 'error':
            toast({ title: 'WebSocket Error', description: data.content.message, status: 'error' });
            break;
          default:
            if (data) {
              setMessages(prev => {
                const updated = [...prev];
                const last = updated.pop();
                if (last && last.role === 'assistant') {
                  updated.push({ ...last, content: last.content + event.data });
                } else if (last) {
                  updated.push(last);
                }
                return updated;
              });
            }
        }
      } catch (err) {
        logger.error('Message parse failed:', err);
      }
    };

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, []);

  const handleSendMessage = () => {
    if (!inputMessage.trim() || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;

    const userMessage: Message = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    };
    const assistantPlaceholder: Message = {
      role: 'assistant',
      content: '',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage, assistantPlaceholder]);
    wsRef.current.send(JSON.stringify({
      type: 'message',
      content: inputMessage,
      model_id: 'deepseek-v3'
    }));
    setInputMessage('');
  };

  useEffect(() => {
    chatContainerRef.current?.scrollTo(0, chatContainerRef.current.scrollHeight);
  }, [messages]);

  return (
    <Box minH="100vh" bg={useColorModeValue('gray.50', 'gray.900')} position="relative">
      <div className="particle-container" />
      <Navbar />
      <Flex position="relative" zIndex={2} flex={1} p={8} gap={8} direction={{ base: 'column', lg: 'row' }}>
        <Card flex={2} bg="transparent" backdropFilter="blur(10px)" boxShadow="xl">
          <CardBody p={0}>
            <Box bg={useColorModeValue('whiteAlpha.800', 'blackAlpha.600')} p={6} borderRadius="lg" h="full">
              <Box position="relative" h="70vh" borderRadius="xl" bg="gray.800" boxShadow="2xl">
                <video autoPlay muted loop style={{ width: '100%', height: '100%', objectFit: 'cover' }} src="/ai-principal-presentation.mp4" />
                <HStack position="absolute" bottom="4" left="4" spacing="3">
                  <IconButton aria-label="Toggle video" icon={<FaVideo />} variant="ghost" color="white" />
                  <IconButton aria-label="Fullscreen" icon={<FaExpand />} onClick={() => document.documentElement.requestFullscreen()} variant="ghost" color="white" />
                </HStack>
              </Box>
            </Box>
          </CardBody>
        </Card>
        <Card flex={1} bg={useColorModeValue('whiteAlpha.800', 'blackAlpha.600')} backdropFilter="blur(10px)">
          <CardBody display="flex" flexDirection="column" p={4}>
            <Heading size="lg" mb={4} color="blue.500">{t('PrincipalAI.title')}</Heading>
            <Box ref={chatContainerRef} flex="1" overflowY="auto" mb={4} borderRadius="md" bg={useColorModeValue('blackAlpha.50', 'whiteAlpha.50')} p={4} maxH="60vh" h="60vh">
              <VStack spacing={4} align="stretch">
                {messages.map((msg, idx) => <MessageBubble key={idx} message={msg} />)}
              </VStack>
            </Box>
            <HStack>
              <Input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder={t('PrincipalAI.inputPlaceholder')}
                bg={useColorModeValue('white', 'gray.800')}
              />
              <IconButton
                aria-label={t('PrincipalAI.send')}
                icon={<FaPaperPlane />}
                onClick={handleSendMessage}
              />
            </HStack>
          </CardBody>
        </Card>
      </Flex>
    </Box>
  );
};

export default PrincipalAIPage;
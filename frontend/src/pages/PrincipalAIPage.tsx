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
  Button,
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
      
      // Trigger global event to refresh course lists
      setTimeout(() => {
        window.dispatchEvent(new Event('courseAdded'));
      }, 1000); // Small delay to ensure backend processing
      
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
  
  // Move all useColorModeValue calls to component top level
  const bgColor = useColorModeValue('#FFE5C4', 'gray.900');
  const videoBgColor = useColorModeValue('rgba(255, 255, 255, 0.9)', 'blackAlpha.600');
  const chatBgColor = useColorModeValue('rgba(255, 255, 255, 0.9)', 'blackAlpha.600');
  const statusTextColor = useColorModeValue('#5D5858', 'gray.400');
  const chatAreaBg = useColorModeValue('blackAlpha.50', 'whiteAlpha.50');
  const welcomeTextColor = useColorModeValue('#5D5858', 'gray.400');
  const inputBg = useColorModeValue('white', 'gray.800');
  
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const connectWebSocket = () => {
    const token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
    if (!token) {
      toast({
        title: 'Authentication Error',
        description: 'Please login to access Principal AI',
        status: 'error',
        duration: 5000,
      });
      return;
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ai/principal-ai/ws/chat`);
    (window as any).__principalAIWS__ = ws;
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      ws.send(JSON.stringify({ type: 'auth', token }));
      toast({
        title: 'Connected',
        description: 'Connected to Principal AI',
        status: 'success',
        duration: 2000,
      });
    };

    ws.onmessage = (event) => {
      try {
        // 首先尝试解析为 JSON
        const data: WSMessage = JSON.parse(event.data);
        
        switch (data.type) {
          case 'auth_success': 
            logger.info('Authentication successful');
            break;
            
          case 'history_messages':
            setMessages(data.messages || []);
            break;
            
          case 'start':
            // AI 开始响应，创建新的助手消息
            setIsTyping(true);
            setMessages(prev => [
              ...prev,
              {
                role: 'assistant',
                content: '',
                timestamp: data.timestamp
              }
            ]);
            break;
            
          case 'stream':
          case 'markdown':
            // 流式消息内容
            setMessages(prev => {
              const updated = [...prev];
              const lastMessage = updated[updated.length - 1];
              if (lastMessage && lastMessage.role === 'assistant') {
                lastMessage.content += data.content || '';
              }
              return updated;
            });
            break;
            
          case 'complete':
            // 消息完成
            setIsTyping(false);
            logger.info('Message stream completed');
            break;
            
          case 'reset_success':
            // 重置成功
            setMessages([]);
            toast({
              title: 'Chat Reset',
              description: 'Chat history cleared successfully',
              status: 'success',
              duration: 2000,
            });
            break;
            
          case 'metadata':
            // 处理课程建议等元数据
            setMessages(prev => {
              const updated = [...prev];
              const lastMessage = updated[updated.length - 1];
              if (lastMessage && lastMessage.role === 'assistant') {
                lastMessage.metadata = data.content;
              }
              return updated;
            });
            break;
            
          case 'error':
            setIsTyping(false);
            toast({ 
              title: 'AI Error', 
              description: data.content?.message || 'Unknown error', 
              status: 'error' 
            });
            break;
            
          default:
            logger.warn('Unknown message type:', data.type);
        }
      } catch (err) {
        // 如果不是 JSON，可能是纯文本流式消息
        logger.info('Received non-JSON message, treating as stream content');
        
        // 检查是否是纯文本消息
        if (typeof event.data === 'string' && event.data.trim()) {
          setMessages(prev => {
            const updated = [...prev];
            const lastMessage = updated[updated.length - 1];
            if (lastMessage && lastMessage.role === 'assistant') {
              lastMessage.content += event.data;
            }
            return updated;
          });
        }
      }
    };

    ws.onerror = (error) => {
      logger.error('WebSocket error:', error);
      setIsConnected(false);
      setIsTyping(false);
      toast({
        title: 'Connection Error',
        description: 'Failed to connect to AI service',
        status: 'error',
        duration: 5000,
      });
    };

    ws.onclose = (event) => {
      logger.info(`WebSocket closed: ${event.code} ${event.reason}`);
      setIsConnected(false);
      setIsTyping(false);
      if (event.code !== 1000) {
        toast({
          title: 'Connection Lost',
          description: 'Connection to AI service was lost',
          status: 'warning',
          duration: 3000,
        });
      }
    };
  };

  const resetChat = () => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      toast({
        title: 'Connection Error',
        description: 'Not connected to AI service',
        status: 'error',
        duration: 2000,
      });
      return;
    }

    // 发送重置消息到后端
    wsRef.current.send(JSON.stringify({ type: 'reset' }));
    
    toast({
      title: 'Resetting Chat',
      description: 'Clearing conversation history...',
      status: 'info',
      duration: 1000,
    });
  };

  useEffect(() => {
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [toast]);

  const handleSendMessage = () => {
    if (!inputMessage.trim() || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;

    const userMessage: Message = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
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
    <Box minH="100vh" bg={bgColor} position="relative">
      <div className="particle-container" />
      <Navbar />
      <Flex position="relative" zIndex={2} flex={1} p={8} gap={8} direction={{ base: 'column', lg: 'row' }}>
        <Card flex={2} bg="rgba(255, 255, 255, 0.1)" backdropFilter="blur(10px)" boxShadow="xl">
          <CardBody p={0}>
            <Box bg={videoBgColor} p={6} borderRadius="lg" h="full">
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
        <Card flex={1} bg={chatBgColor} backdropFilter="blur(10px)">
          <CardBody display="flex" flexDirection="column" p={4}>
            <HStack justify="space-between" mb={4}>
              <VStack align="start" spacing={0}>
                <Heading size="lg" color="#F47B4F">{t('PrincipalAI.title') || 'Principal AI'}</Heading>
                <HStack spacing={2}>
                  <Box 
                    w="8px" 
                    h="8px" 
                    borderRadius="full" 
                    bg={isConnected ? 'green.400' : 'red.400'} 
                  />
                  <Text fontSize="xs" color={statusTextColor}>
                    {isConnected ? 'Connected' : 'Disconnected'}
                  </Text>
                  {isTyping && (
                    <Text fontSize="xs" color="#F47B4F">
                      • AI is thinking...
                    </Text>
                  )}
                </HStack>
              </VStack>
              <Button 
                size="sm" 
                colorScheme="orange" 
                variant="outline" 
                onClick={resetChat}
                isDisabled={!isConnected}
              >
                Reset Chat
              </Button>
            </HStack>
            
            <Box ref={chatContainerRef} flex="1" overflowY="auto" mb={4} borderRadius="md" bg={chatAreaBg} p={4} maxH="60vh" h="60vh">
              <VStack spacing={4} align="stretch">
                {messages.length === 0 && (
                  <Box textAlign="center" py={8}>
                    <Text color={welcomeTextColor} fontSize="sm">
                      👋 Hello! I'm Principal, your AI course recommendation assistant. 
                      <br />
                      Tell me about your learning interests and I'll help you find the perfect courses!
                    </Text>
                  </Box>
                )}
                {messages.map((msg, idx) => <MessageBubble key={idx} message={msg} />)}
              </VStack>
            </Box>
            
            <HStack>
              <Input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder={t('PrincipalAI.inputPlaceholder') || "Ask me about courses..."}
                bg={inputBg}
                borderColor="#FFB69B"
                _focus={{ borderColor: '#F47B4F' }}
                isDisabled={!isConnected || isTyping}
              />
              <IconButton
                aria-label={t('PrincipalAI.send') || 'Send'}
                icon={<FaPaperPlane />}
                onClick={handleSendMessage}
                colorScheme="orange"
                isDisabled={!isConnected || isTyping || !inputMessage.trim()}
              />
            </HStack>
          </CardBody>
        </Card>
      </Flex>
    </Box>
  );
};

export default PrincipalAIPage;
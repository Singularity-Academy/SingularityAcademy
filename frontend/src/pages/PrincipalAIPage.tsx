import React, { useState, useRef, useEffect, useReducer } from 'react';
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
  message_id: string;
}

interface WSMessage {
  type: string;
  message_id: string;
  content: any;
  timestamp: string;
  message?: string;
  messages?: Message[];
}

type MessageAction = 
  | { type: 'APPEND_TOKEN'; token: string }
  | { type: 'START_MESSAGE'; timestamp: string; message_id?: string }
  | { type: 'COMPLETE_MESSAGE' }
  | { type: 'SET_METADATA'; metadata: any }
  | { type: 'RESET_MESSAGES' }
  | { type: 'SET_HISTORY'; messages: Message[] }
  | { type: 'ADD_MESSAGE'; message: Message };

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
        title: '课程已添加',
        description: `${course.name} 已添加。`,
        status: 'success',
        duration: 3000,
      });
      
      // Trigger global event to refresh course lists
      setTimeout(() => {
        window.dispatchEvent(new Event('courseAdded'));
      }, 1000); // Small delay to ensure backend processing
      
    } else {
      toast({
        title: 'WebSocket 错误',
        description: '连接未打开。',
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
          <Text fontSize="xs" color={timestampColor} mb={2}>推荐课程</Text>
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
                  + 添加课程
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

const messageReducer = (state: Message[], action: MessageAction): Message[] => {
  switch (action.type) {
    case 'START_MESSAGE':
      return [...state, {
        role: 'assistant',
        content: '',
        timestamp: action.timestamp,
        message_id: action.message_id || ''
      }];
      
    case 'APPEND_TOKEN':
      const updated = [...state];
      const lastMessage = updated[updated.length - 1];
      if (lastMessage && lastMessage.role === 'assistant') {
        // Ensure content is a string and append token
        lastMessage.content = (lastMessage.content || '') + action.token;
      }
      return updated;
      
    case 'SET_METADATA':
      const withMetadata = [...state];
      const currentMessage = withMetadata[withMetadata.length - 1];
      if (currentMessage && currentMessage.role === 'assistant') {
        currentMessage.metadata = action.metadata;
      }
      return withMetadata;
      
    case 'RESET_MESSAGES':
      return [];
      
    case 'SET_HISTORY':
      return action.messages;
      
    case 'COMPLETE_MESSAGE':
      // No state change needed, just a signal
      return state;
      
    case 'ADD_MESSAGE':
      return [...state, action.message];
      
    default:
      return state;
  }
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
  
  const [messages, dispatch] = useReducer(messageReducer, []);
  const [inputMessage, setInputMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const connectWebSocket = () => {
    const token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
    if (!token) {
      toast({
        title: '认证错误',
        description: '请登录以访问 Principal AI',
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
        title: '已连接',
        description: '已连接到 Principal AI',
        status: 'success',
        duration: 2000,
      });
    };

    ws.onmessage = (event) => {
      try {
        const message = event.data;
        
        if (typeof message === 'string' && message.trim().startsWith('{')) {
          logger.debug(`[WebSocket] Received JSON message: ${JSON.stringify(message)}`);
          const data: WSMessage = JSON.parse(message);
          logger.debug(`[WebSocket] Parsed JSON content: ${JSON.stringify(data, null, 2)}`);
          
          switch (data.type) {
            case 'auth_success': 
              logger.info('Authentication successful');
              break;
              
            case 'history_messages':
              if (data.messages) {
                dispatch({ type: 'SET_HISTORY', messages: data.messages });
              }
              break;
              
            case 'start':
              setIsTyping(true);
              dispatch({ 
                type: 'START_MESSAGE', 
                timestamp: data.timestamp,
                message_id: data.message_id 
              });
              break;
              
            case 'token':
              // Handle streaming tokens
              dispatch({ type: 'APPEND_TOKEN', token: data.content });
              break;
              
            case 'complete':
              setIsTyping(false);
              dispatch({ type: 'COMPLETE_MESSAGE' });
              logger.info('Message stream completed');
              break;
              
            case 'message-reset-success':
              dispatch({ type: 'RESET_MESSAGES' });
              toast({
                title: '聊天重置',
                description: '聊天记录已成功清除',
                status: 'success',
                duration: 2000,
              });
              break;
              
            case 'metadata':
              dispatch({ type: 'SET_METADATA', metadata: data.content });
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
              logger.warn(`Unknown JSON message type: ${data.type}`);
          }
        } else if (typeof message === 'string' && message.trim()) {
          // Handle raw streaming tokens
          dispatch({ type: 'APPEND_TOKEN', token: message });
        }
      } catch (err) {
        logger.error('[WebSocket] Error parsing message:', err);
      }
    };

    ws.onerror = (error) => {
      logger.error('[WebSocket] Error:', error);
      setIsConnected(false);
      setIsTyping(false);
      toast({
        title: '连接错误',
        description: '无法连接到 AI 服务',
        status: 'error',
        duration: 5000,
      });
    };

    ws.onclose = (event) => {
      logger.info(`[WebSocket] Closed: ${event.code} ${event.reason}`);
      setIsConnected(false);
      setIsTyping(false);
      if (event.code !== 1000) {
        toast({
          title: '连接丢失',
          description: '与 AI 服务的连接已丢失',
          status: 'warning',
          duration: 3000,
        });
      }
    };
  };

  const resetChat = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'message-reset' }));
      dispatch({ type: 'RESET_MESSAGES' });
    }
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

  const sendMessage = (content: string) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      toast({
        title: '连接错误',
        description: '无法连接到 AI 服务',
        status: 'error',
        duration: 3000,
      });
      return;
    }

    const timestamp = new Date().toISOString();
    const message_id = `user-${Date.now()}`;

    // Add user message to state
    dispatch({ 
      type: 'ADD_MESSAGE',
      message: {
        role: 'user',
        content,
        timestamp,
        message_id
      }
    });

    // Send message to backend
    wsRef.current.send(JSON.stringify({ 
      type: 'message', 
      content,
      timestamp,
      message_id
    }));

    // Clear input after sending
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
                    {isConnected ? '已连接' : '已断开'}
                  </Text>
                  {isTyping && (
                    <Text fontSize="xs" color="#F47B4F">
                      • AI 正在思考...
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
                重置聊天
              </Button>
            </HStack>
            
            <Box ref={chatContainerRef} flex="1" overflowY="auto" mb={4} borderRadius="md" bg={chatAreaBg} p={4} maxH="60vh" h="60vh">
              <VStack spacing={4} align="stretch">
                {messages.length === 0 && (
                  <Box textAlign="center" py={8}>
                    <Text color={welcomeTextColor} fontSize="sm">
                      👋 你好！我是 Principal，您的 AI 课程推荐助手。
                      <br />
                      告诉我您的学习兴趣，我会帮您找到完美的课程！
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
                onKeyDown={(e) => e.key === 'Enter' && sendMessage(inputMessage)}
                placeholder={t('PrincipalAI.inputPlaceholder') || "询问我关于课程的问题..."}
                bg={inputBg}
                borderColor="#FFB69B"
                _focus={{ borderColor: '#F47B4F' }}
                isDisabled={!isConnected || isTyping}
              />
              <IconButton
                aria-label={t('PrincipalAI.send') || 'Send'}
                icon={<FaPaperPlane />}
                onClick={() => sendMessage(inputMessage)}
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
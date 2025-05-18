import React, { useState, useRef, useEffect, useCallback } from 'react';
import { 
  Box, 
  Flex, 
  Heading, 
  Text, 
  Input, 
  IconButton, 
  useColorModeValue,
  Avatar,
  Card,
  CardBody,
  VStack,
  HStack,
  useToast
} from '@chakra-ui/react';
import { FaPaperPlane, FaVideo, FaVideoSlash, FaExpand } from 'react-icons/fa';
import Navbar from '@components/Navbar';
import { useTranslation } from 'react-i18next';
import './../styles/ParticleBackground.css';
import logger from '@utils/logger';

interface Message {
  role: 'user' | 'assistant';
  content: string | { text: string; [key: string]: any };
  timestamp?: string;
}

interface StreamChunk {
  content: string | { text: string; [key: string]: any };
  messageId: string;
  timestamp: string;
  isFinal: boolean;
  error?: string;
}

const MessageBubble: React.FC<{ message: Message }> = ({ message }) => {
  const isAssistant = message.role === 'assistant';
  
  // Move all useColorModeValue hooks to the top level
  const assistantBgColor = useColorModeValue('blue.50', 'blue.900');
  const userBgColor = useColorModeValue('green.50', 'green.900');
  const textColor = useColorModeValue('gray.800', 'white');
  const assistantBorderColor = useColorModeValue('blue.200', 'blue.700');
  const userBorderColor = useColorModeValue('green.200', 'green.700');
  const timestampColor = useColorModeValue('gray.500', 'gray.400');
  
  // Compute the actual colors based on role
  const bgColor = isAssistant ? assistantBgColor : userBgColor;
  const borderColor = isAssistant ? assistantBorderColor : userBorderColor;
  
  // Helper function to check if content is XML
  const isXmlContent = (content: string): boolean => {
    return content.trim().startsWith('<') && content.trim().endsWith('>');
  };

  // Helper function to extract XML from JSON if needed
  const extractRawContent = (content: any): string => {
    if (typeof content === 'string') {
      // Check if this might be a stringified JSON containing XML
      try {
        const parsed = JSON.parse(content);
        if (parsed && typeof parsed === 'object') {
          // Look in common fields where XML might be stored
          if (typeof parsed.text === 'string' && isXmlContent(parsed.text)) {
            return parsed.text;
          }
          if (typeof parsed.content === 'string' && isXmlContent(parsed.content)) {
            return parsed.content;
          }
          // If no XML found in sub-fields, stringify the whole object
          return JSON.stringify(parsed, null, 2);
        }
      } catch (e) {
        // Not JSON, return as is
        return content;
      }
    } else if (typeof content === 'object') {
      // Direct object, check fields for XML
      if (typeof content.text === 'string' && isXmlContent(content.text)) {
        return content.text;
      }
      if (typeof content.content === 'string' && isXmlContent(content.content)) {
        return content.content;
      }
      // No XML fields found, stringify the whole object
      return JSON.stringify(content, null, 2);
    }
    
    // Default case: return as string
    return String(content);
  };
  
  // Display raw content, but extract XML if it's wrapped in JSON
  const displayContent = extractRawContent(message.content);

  // Format timestamp safely
  const formatTimestamp = (timestamp: string | undefined): string => {
    if (!timestamp) return '';
    
    try {
      // Fix the invalid format with both offset and Z suffix
      let fixedTimestamp = timestamp;
      if (timestamp.includes('+') && timestamp.endsWith('Z')) {
        // Remove the Z at the end if there's already a timezone offset
        fixedTimestamp = timestamp.slice(0, -1);
      }
      
      const date = new Date(fixedTimestamp);
      return isNaN(date.getTime()) 
        ? 'Invalid Time' 
        : date.toLocaleTimeString();
    } catch (e) {
      console.error('Error formatting timestamp:', e);
      return 'Invalid Time';
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
      <Text whiteSpace="pre-wrap">
        {displayContent}
      </Text>
      
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
  const [studyPlan] = useState<string[]>([
    t('PrincipalAI.physics'),
    t('PrincipalAI.mathematics'),
    t('PrincipalAI.engineering'),
    t('PrincipalAI.computerScience')
  ]);
  const [videoActive, setVideoActive] = useState(true);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const connectWebSocket = async () => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        logger.debug("WebSocket already connected");
        return;
      }

      try {
        // Get the auth token from cookies
        const token = document.cookie
          .split("; ")
          .find((row) => row.startsWith("token="))
          ?.split("=")[1];

        if (!token) {
          logger.error("No auth token found in cookies");
          setError("Authentication required. Please log in.");
          return;
        }

        const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        const wsUrl = `${protocol}//${window.location.host}/ai/principal-ai/ws/chat`;
        logger.debug(`Connecting to WebSocket at ${wsUrl}`);

        // Create WebSocket
        const ws = new WebSocket(wsUrl);
        wsRef.current = ws;

        ws.onopen = () => {
          logger.info("WebSocket connection opened, sending authentication");
          // Send authentication message
          ws.send(JSON.stringify({
            type: "auth",
            token: token
          }));
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            logger.debug("Received WebSocket message:", data);

            // Handle different message types
            switch (data.type) {
              case "auth_success":
                logger.info("Authentication successful:", data.message);
                setError(null);
                setIsConnected(true);
                break;
              case "history_messages":
                // Handle history messages
                logger.info(`Received ${data.messages.length} history messages`);
                if (data.messages && Array.isArray(data.messages)) {
                  // Before we process messages, add a debug log to see the raw format
                  logger.debug("Raw history messages:", JSON.stringify(data.messages.slice(0, 2)));
                  
                  // Process and add history messages to the chat - maintain original content structure
                  const formattedMessages = data.messages.map((msg: any) => {
                    return {
                      role: msg.role === 'user' ? 'user' : 'assistant',
                      content: msg.content, // Keep content as is without parsing
                      timestamp: msg.timestamp
                    };
                  });
                  
                  setMessages(formattedMessages);
                }
                break;
              case "error":
                logger.error("WebSocket error:", data.error);
                setError(data.error);
                if (data.status_code === 401) {
                  // Handle authentication errors
                  ws.close();
                  // Optionally redirect to login
                  // window.location.href = "/login";
                }
                break;
              case "token":
                // Handle token streaming by updating the existing empty assistant message
                setMessages(prev => {
                  const lastMessage = prev[prev.length - 1];
                  if (lastMessage && lastMessage.role === "assistant") {
                    // Get current content - could be string or object
                    const currentContent = lastMessage.content;
                    let updatedContent: string | { text: string; [key: string]: any };
                    
                    if (typeof currentContent === 'object') {
                      // If current content is an object, append to text property or create one
                      updatedContent = {
                        ...currentContent,
                        text: (currentContent.text || '') + data.content
                      };
                    } else {
                      // If string, just append
                      updatedContent = currentContent + data.content;
                    }

                    // Update existing assistant message
                    return [
                      ...prev.slice(0, -1),
                      { 
                        ...lastMessage, 
                        content: updatedContent
                      }
                    ];
                  }
                  return prev;
                });
                break;
              case "chunk":
                // Handle chunk streaming by updating the existing empty assistant message
                setMessages(prev => {
                  const lastMessage = prev[prev.length - 1];
                  // Keep content as is without extracting text field
                  const contentToAdd = data.content;
                    
                  if (lastMessage && lastMessage.role === "assistant") {
                    // Log the content types for debugging
                    logger.debug("Content types:", {
                      lastMessageContentType: typeof lastMessage.content,
                      contentToAddType: typeof contentToAdd
                    });
                    
                    let updatedContent: string | { text: string; [key: string]: any };
                    
                    // Combine the contents appropriately
                    if (typeof lastMessage.content === 'object' && typeof contentToAdd === 'object') {
                      // Both objects - merge them
                      updatedContent = {
                        ...lastMessage.content,
                        ...contentToAdd,
                        text: (lastMessage.content.text || '') + 
                              ((contentToAdd as any).text || '')
                      };
                    } else if (typeof lastMessage.content === 'object') {
                      // Last message is object, content to add is string
                      updatedContent = {
                        ...lastMessage.content,
                        text: (lastMessage.content.text || '') + 
                              (typeof contentToAdd === 'string' ? contentToAdd : '')
                      };
                    } else if (typeof contentToAdd === 'object') {
                      // Last message is string, content to add is object
                      const textContent = typeof lastMessage.content === 'string' ? lastMessage.content : '';
                      updatedContent = {
                        ...(contentToAdd as { [key: string]: any }),
                        text: textContent + ((contentToAdd as any).text || '')
                      };
                    } else {
                      // Both are strings
                      updatedContent = (lastMessage.content || '') + (contentToAdd || '');
                    }
                    
                    return [
                      ...prev.slice(0, -1),
                      { ...lastMessage, content: updatedContent }
                    ];
                  }
                  return prev;
                });
                break;
              default:
                logger.warn("Unknown message type:", data.type);
            }
          } catch (e) {
            logger.error("Error parsing WebSocket message:", e);
          }
        };

        ws.onerror = (error) => {
          logger.error("WebSocket error:", error);
          setError("Connection error occurred");
          setIsConnected(false);
        };

        ws.onclose = (event) => {
          logger.info(`WebSocket closed with code ${event.code}`);
          setIsConnected(false);
          if (event.code === 1008) {
            // Policy Violation (auth error)
            setError("Authentication failed. Please log in again.");
          } else if (event.code !== 1000) {
            // Not a normal closure
            setError("Connection closed unexpectedly");
          }
        };

      } catch (error) {
        logger.error("Error setting up WebSocket:", error);
        setError("Failed to establish connection");
        setIsConnected(false);
      }
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) {
        logger.debug("Cleaning up WebSocket connection");
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, []); // Empty dependency array since we only want to connect once

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;

    const message: Message = {
        role: 'user',
        content: inputMessage,
        timestamp: new Date().toISOString()
    };

    // Add user message first
    setMessages(prev => [...prev, message]);
    
    // Immediately add an empty assistant message
    setMessages(prev => [
      ...prev, 
      { 
        role: 'assistant', 
        content: '',
        timestamp: new Date().toISOString()
      }
    ]);
    
    setInputMessage('');
    setIsLoading(true);

    try {
        wsRef.current.send(JSON.stringify({
            type: "message",
            content: inputMessage,
            model_id: "deepseek-v3"  // Using default model
        }));
        logger.debug("Sent message to WebSocket:", { type: "message", content: inputMessage, model_id: "deepseek-v3" });
    } catch (error) {
        logger.error('Error sending message:', error);
        toast({
            title: t('PrincipalAI.sendError'),
            status: 'error',
            duration: 5000,
            isClosable: true,
        });
    } finally {
        setIsLoading(false);
    }
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    // Simple particle generator
    const createParticle = () => {
      const particle = document.createElement('div');
      particle.className = 'particle';
      
      const size = Math.random() * 3 + 2;
      const left = Math.random() * 100;
      const duration = Math.random() * 5 + 5;

      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      particle.style.left = `${left}%`;
      particle.style.animationDuration = `${duration}s`;
      particle.style.color = particleColor;

      document.querySelector('.particle-container')?.appendChild(particle);

      particle.addEventListener('animationend', () => {
        particle.remove();
      });
    };

    const interval = setInterval(createParticle, 300);
    return () => clearInterval(interval);
  }, [particleColor]);

  return (
    <Box 
      minH="100vh" 
      bg={useColorModeValue('gray.50', 'gray.900')}
      position="relative"
    >
      <div className="particle-container" />
      <Navbar />
      
      <Flex
        position="relative"
        zIndex="2"
        flex="1"
        p={8}
        gap={8}
        direction={{ base: 'column', lg: 'row' }}
      >
        {/* Video Conference Section */}
        <Card flex="2" bg="transparent" backdropFilter="blur(10px)" boxShadow="xl">
          <CardBody position="relative" p={0} overflow="hidden">
            <Box
              bg={useColorModeValue('whiteAlpha.800', 'blackAlpha.600')}
              p={6}
              borderRadius="lg"
              h="full"
            >
              {/* AI Video Feed */}
              <Box
                position="relative"
                h="70vh"
                borderRadius="xl"
                overflow="hidden"
                bg="gray.800"
                boxShadow="2xl"
              >
                <video
                  autoPlay
                  muted
                  loop
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                  src="/ai-principal-presentation.mp4"
                />
                
                {/* Screen Sharing Overlay */}
                <Box
                  position="absolute"
                  bottom="20px"
                  right="20px"
                  w="300px"
                  h="200px"
                  bg="gray.900"
                  borderRadius="md"
                  boxShadow="dark-lg"
                  overflow="hidden"
                >
                  <Box
                    bg="gray.800"
                    p={4}
                    color="white"
                    fontSize="sm"
                    fontFamily="monospace"
                  >
                    <Text>📚 Study Plan Generator v1.0</Text>
                    <Box mt={2}>
                      {studyPlan.map((course, index) => (
                        <Text key={index} color="green.300">› {course}</Text>
                      ))}
                    </Box>
                  </Box>
                </Box>

                <HStack position="absolute" bottom="4" left="4" spacing="3">
                  <IconButton
                    aria-label="Toggle video"
                    icon={videoActive ? <FaVideo /> : <FaVideoSlash />}
                    onClick={() => setVideoActive(!videoActive)}
                    variant="ghost"
                    color="white"
                  />
                  <IconButton
                    aria-label="Fullscreen"
                    icon={<FaExpand />}
                    onClick={() => document.documentElement.requestFullscreen()}
                    variant="ghost"
                    color="white"
                  />
                </HStack>
              </Box>
            </Box>
          </CardBody>
        </Card>

        {/* Chat Section */}
        <Card flex="1" bg={useColorModeValue('whiteAlpha.800', 'blackAlpha.600')} backdropFilter="blur(10px)">
          <CardBody display="flex" flexDirection="column" p={4}>
            <Heading size="lg" mb={4} color="blue.500">
              {t('PrincipalAI.title')}
            </Heading>
            
            <Box
              ref={chatContainerRef}
              flex="1"
              overflowY="auto"
              mb={4}
              borderRadius="md"
              bg={useColorModeValue('blackAlpha.50', 'whiteAlpha.50')}
              p={4}
              maxH="60vh"
              h="60vh"
              css={{
                '&::-webkit-scrollbar': {
                  width: '8px',
                },
                '&::-webkit-scrollbar-track': {
                  background: useColorModeValue('gray.100', 'gray.700'),
                  borderRadius: '8px',
                },
                '&::-webkit-scrollbar-thumb': {
                  background: useColorModeValue('gray.300', 'gray.600'),
                  borderRadius: '8px',
                },
              }}
            >
              <VStack spacing={4} align="stretch">
                {messages.map((message, index) => (
                  <MessageBubble key={index} message={message} />
                ))}
              </VStack>
            </Box>

            <Box p={4} borderTopWidth="1px" borderColor={useColorModeValue('gray.200', 'gray.700')}>
              <HStack>
                <Input
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder={t('PrincipalAI.inputPlaceholder')}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  bg={useColorModeValue('white', 'gray.800')}
                  isDisabled={isLoading || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN}
                />
                <IconButton
                  aria-label={t('PrincipalAI.send')}
                  icon={<FaPaperPlane />}
                  onClick={handleSendMessage}
                  isLoading={isLoading}
                  isDisabled={isLoading || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN}
                />
              </HStack>
            </Box>
          </CardBody>
        </Card>
      </Flex>
    </Box>
  );
};

export default PrincipalAIPage; 
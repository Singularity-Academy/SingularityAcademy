import React, { useEffect, useRef, useState, useCallback } from 'react';
import {
  Box,
  Button,
  Container,
  Flex,
  Input,
  VStack,
  Text,
  useColorModeValue,
  IconButton,
  Heading,
  useToast,
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
// import { useCookies } from 'react-cookie';
import axiosInstance from '@utils/axios';
import { API_ENDPOINTS } from '@/config/api';
import Cookies from "js-cookie";
import Navbar from "@components/Navbar";

const CourseInteractionPage: React.FC = () => {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
  const [inputValue, setInputValue] = useState('');
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  // const [cookies, setCookie] = useCookies(['auth']);

  const studentVideoRef = useRef<HTMLVideoElement>(null);
  const videoAreaRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const toast = useToast();
  const wsRef = useRef<WebSocket | null>(null);

  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBg = useColorModeValue('white', 'gray.700');

 useEffect(() => {
   // Check if user is authenticated
   if (!Cookies.get('token')) {
     window.location.href = '/login'; // Redirect to login page if not authenticated
   }
 }, [Cookies.get('token')]);

  useEffect(() => {
    // Scroll to bottom when messages update
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  // Add WebSocket connection setup
  useEffect(() => {
    // Create WebSocket connection for video streaming
    const ws = new WebSocket('ws://localhost:1298/ws/video');
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connection established');
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      toast({
        title: 'Connection Error',
        description: 'Failed to establish video connection',
        status: 'error',
        duration: 3000,
      });
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Update toggleCamera function
  const toggleCamera = async () => {
    try {
      if (!isCameraOn) {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: true, 
          audio: false 
        });
        
        if (studentVideoRef.current) {
          studentVideoRef.current.srcObject = stream;
        }
        
        // Set up MediaRecorder
        const recorder = new MediaRecorder(stream, {
          mimeType: 'video/webm;codecs=vp8,opus'
        });
        
        recorder.ondataavailable = (event) => {
          if (event.data.size > 0 && wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(event.data);
          }
        };

        recorder.onstop = () => {
          setIsStreaming(false);
        };

        setMediaRecorder(recorder);
        setIsCameraOn(true);
        
        // Start recording
        recorder.start(1000); // Send video data every 1 second
        setIsStreaming(true);

        toast({
          title: 'Camera activated',
          description: 'Video stream started',
          status: 'success',
          duration: 2000,
        });
      } else {
        // Stop recording and streaming
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
          mediaRecorder.stop();
        }

        const stream = studentVideoRef.current?.srcObject as MediaStream;
        stream?.getTracks().forEach(track => track.stop());
        
        if (studentVideoRef.current) {
          studentVideoRef.current.srcObject = null;
        }

        setIsCameraOn(false);
        setIsStreaming(false);
        setMediaRecorder(null);
      }
    } catch (error) {
      console.error('Camera error:', error);
      toast({
        title: 'Camera error',
        description: 'Unable to access camera. Please check permissions.',
        status: 'error',
        duration: 3000,
      });
    }
  };

  // Fullscreen toggle function
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      videoAreaRef.current?.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  // AI Chat function
  const handleSubmit = async () => {
    if (!inputValue.trim()) return;

    const userMessage = { role: 'user', content: inputValue.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');

    try {
      const response = await axiosInstance.post(API_ENDPOINTS.COURSE.INTERACT, {
        messages: [...messages, userMessage],
      });

      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: response.data.content },
      ]);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to get AI response',
        status: 'error',
        duration: 3000,
      });
    }
  };

  // Add cleanup effect
  useEffect(() => {
    return () => {
      if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (studentVideoRef.current?.srcObject) {
        const stream = studentVideoRef.current.srcObject as MediaStream;
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [mediaRecorder]);

  return (
      <><Navbar/><Box bg={bgColor} minH="100vh" p={4} mt={16}>
        <Container maxW="container.xl">
          <Flex direction={{base: 'column', lg: 'row'}} gap={6}>
            {/* Main Video Area */}
            <Box flex="2" ref={videoAreaRef} bg={cardBg} borderRadius="lg" p={4} position="relative">
              <Box
                  bg="gray.800"
                  h="500px"
                  borderRadius="md"
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
              >
                <Text color="white">Main Course Content</Text>
              </Box>
              <IconButton
                  aria-label="Toggle fullscreen"
                  icon={isFullscreen ? <ViewOffIcon/> : <ViewIcon/>}
                  position="absolute"
                  bottom={4}
                  right={4}
                  onClick={toggleFullscreen}/>
            </Box>

            {/* Side Panel */}
            <VStack flex="1" spacing={4}>
              {/* Student Camera */}
              <Box w="100%" bg={cardBg} borderRadius="lg" p={4}>
                <Flex justify="space-between" mb={2}>
                  <Heading size="sm">Your Camera</Heading>
                  <Button
                      size="sm"
                      colorScheme={isCameraOn ? 'red' : 'green'}
                      onClick={toggleCamera}
                      isLoading={isStreaming}
                      loadingText="Streaming"
                  >
                    {isCameraOn ? 'Turn Off' : 'Turn On'}
                  </Button>
                </Flex>
                <Box
                    w="100%"
                    h="200px"
                    bg="gray.700"
                    borderRadius="md"
                    overflow="hidden"
                >
                  <video
                      ref={studentVideoRef}
                      style={{width: '100%', height: '100%', objectFit: 'cover'}}
                      playsInline
                      autoPlay
                      muted/>
                </Box>
              </Box>

              {/* Chat Area */}
              <Box
                  w="100%"
                  bg={cardBg}
                  borderRadius="lg"
                  p={4}
                  flex={1}
                  maxH="400px"
                  overflowY="auto"
                  ref={chatContainerRef}
              >
                <VStack spacing={4} align="stretch">
                  {messages.map((msg, index) => (
                      <Box
                          key={index}
                          bg={msg.role === 'user' ? 'blue.50' : 'gray.50'}
                          p={3}
                          borderRadius="md"
                      >
                        <Text fontWeight="bold">
                          {msg.role === 'user' ? 'You' : 'AI Teacher'}
                        </Text>
                        <Text>{msg.content}</Text>
                      </Box>
                  ))}
                </VStack>
              </Box>

              {/* Input Area */}
              <Flex w="100%">
                <Input
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Ask your question..."
                    mr={2}
                    onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}/>
                <Button colorScheme="blue" onClick={handleSubmit}>
                  Send
                </Button>
              </Flex>
            </VStack>
          </Flex>
        </Container>
      </Box></>
  );
};

export default CourseInteractionPage;
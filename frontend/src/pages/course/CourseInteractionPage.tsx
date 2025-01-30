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
import {useNavigate} from "react-router-dom";

declare class ImageCapture {
  constructor(track: MediaStreamTrack);
  grabFrame(): Promise<ImageBitmap>;
  takePhoto(): Promise<Blob>;
}

const CourseInteractionPage: React.FC = () => {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
  const [inputValue, setInputValue] = useState('');
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [connecting, setConnecting] = useState(false);
  const [recording, setRecording] = useState(false);
  const [audioStream, setAudioStream] = useState<MediaStream | null>(null);
  const [videoStream, setVideoStream] = useState<MediaStream | null>(null);
  const websocketRef = useRef<WebSocket | null>(null);
  const sendingVideoTask = useRef<any | null>(null);

  const studentVideoRef = useRef<HTMLVideoElement>(null);
  const videoAreaRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const toast = useToast();
  const navigate = useNavigate();
  const wsRef = useRef<WebSocket | null>(null);

  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBg = useColorModeValue('white', 'gray.700');

  const startAudio = () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
          setAudioStream(stream);
          const mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.ondataavailable = (event) => {
            if (websocketRef.current?.readyState !== WebSocket.OPEN) return;
            const audioBlob = event.data;
            const reader = new FileReader();
            reader.onloadend = () => {
              const buffer = reader.result;
              // Send the audio buffer via WebSocket
              websocketRef.current?.send(buffer || "")
            };
            reader.readAsArrayBuffer(audioBlob);
          };
          mediaRecorder.start(500);  // Capture every 1 second of audio
        })
        .catch((error) => toast({
            title: "error accessing media devices",
            description: error,
            status: 'error',
            duration: 3000,
        }));
  };

  const startVideo = () => {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      if (studentVideoRef.current) {
        studentVideoRef.current.srcObject = stream;
      }
      setVideoStream(stream);
    })
    .catch((error) => toast({
        title: "error accessing media devices",
        description: error,
        status: 'error',
        duration: 3000,
      })
    );
  };

  const connectWebSocket = () => {
    if (websocketRef.current) return; // 如果已经连接了，就不重复连接
    startVideo();
    startAudio();
    setConnecting(true);
    const ws = new WebSocket(`${API_ENDPOINTS.WS.STREAM}?token=${Cookies.get('token') || ''}`);

    ws.onopen = () => {
      toast({
        title: 'connect successful',
        status: 'success',
        duration: 3000,
      });
      setConnecting(false);
      setRecording(true);
    };

    ws.onclose = (closeEvent) => {
      if (closeEvent.code != 1000){
        toast({
          title: 'connection closed',
          description: closeEvent.reason,
          status: 'error',
          duration: 3000,
        });
      }
      else {
        toast({
          title: 'close successful',
          status: 'success',
          duration: 3000,
        });
      }
      setRecording(false);
      setConnecting(false);
      websocketRef.current = null; // 清空 WebSocket 实例
    };

    websocketRef.current = ws;
  };

  // 断开 WebSocket
  const disconnectWebSocket = () => {
    if (websocketRef.current) {
      stopVideo()
      stopAudio();
      websocketRef.current.close(1000);
      websocketRef.current = null;
      setRecording(false);
      setConnecting(false);
    }
  };

  const stopAudio = () => {
    if (audioStream) {
      // 停止所有的视频流轨道
      audioStream.getTracks().forEach(track => track.stop());
      setAudioStream(null);
    }
    if (mediaRecorder) {
      mediaRecorder.stop();
    }
  };

  const stopVideo = () => {
    if (videoStream) {
      // 停止所有的视频流轨道
      videoStream.getTracks().forEach(track => track.stop());
      setVideoStream(null);
    }
    // 清除视频元素的 srcObject
    if (studentVideoRef.current) {
      studentVideoRef.current.srcObject = null;
    }
    if (!sendingVideoTask.current) return;
    clearInterval(sendingVideoTask.current)
    sendingVideoTask.current = null
  };


  // 切换连接状态
  const toggleConnect = () => {
    if (recording) {
      disconnectWebSocket();
    } else {
      connectWebSocket();
    }
  };

  // 组件卸载时清理 WebSocket 连接
  useEffect(() => {
    return () => {
      stopVideo()
      stopAudio()
      disconnectWebSocket();
    };
  }, []);

 useEffect(() => {
   // Check if user is authenticated
   if (!Cookies.get('token')) {
     navigate('/login'); // Redirect to login page if not authenticated
   }
 }, [Cookies.get('token')]);

  useEffect(() => {
    // Scroll to bottom when messages update
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

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

  useEffect(() => {
    const intervalId = setInterval(async () => {
      if (!videoStream) return;

      const videoTrack = videoStream.getVideoTracks()[0];

      // Check if the video track is still active and enabled
      if (!videoTrack || videoTrack.readyState !== 'live' || !videoTrack.enabled) {
        console.warn("Video track is not in a valid state");
        return;
      }

      const imageCapture = new ImageCapture(videoTrack);

      // Check WebSocket connection
      if (websocketRef.current?.readyState !== WebSocket.OPEN) return;

      // Capture image and send it
      try {
        const blob = await imageCapture.takePhoto();
        websocketRef.current?.send(await blob.arrayBuffer());
      } catch (error) {
        console.error("Error capturing photo:", error);
      }
    }, 1000 / 2);

    // Clean up the interval on component unmount
    return () => clearInterval(intervalId);
  }, [videoStream]);



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
                      colorScheme={recording ? 'red' : 'green'}
                      onClick={toggleConnect}
                      isLoading={connecting}
                      loadingText="Connetcing"
                  >
                    {recording ? 'Turn Off' : 'Turn On'}
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
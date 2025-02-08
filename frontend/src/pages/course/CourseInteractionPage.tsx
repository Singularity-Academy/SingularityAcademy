import React, { useEffect, useRef, useState } from 'react';
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
  Progress,
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon, SmallCloseIcon } from '@chakra-ui/icons';
import axiosInstance from '@utils/axios';
import { API_ENDPOINTS } from '@/config/api';
import Cookies from "js-cookie";
import {useNavigate} from "react-router-dom";
import { FaFileUpload, FaLink } from 'react-icons/fa';
import { useDropzone } from 'react-dropzone';
import { w3cwebsocket as W3CWebSocket } from "websocket";

declare class ImageCapture {
  constructor(track: MediaStreamTrack);
  takePhoto(): Promise<Blob>;
}

const CourseInteractionPage: React.FC = () => {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
  const [inputValue, setInputValue] = useState('');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [mediaRecorder] = useState<MediaRecorder | null>(null);
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
  const chatUserBg = useColorModeValue('blue.50', 'blue.500');
  const chatTeacherBg = useColorModeValue('gray.50', 'gray.500');

  const [uploadingFiles, setUploadingFiles] = useState<File[]>([]);
  const [uploadProgress, setUploadProgress] = useState<{ [key: string]: number }>({});
  const [resourceLinks, setResourceLinks] = useState<string[]>([]);

  const ALLOWED_FILE_TYPES = {
    'application/pdf': ['.pdf'],
    'application/msword': ['.doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'application/vnd.ms-powerpoint': ['.ppt'],
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
    'application/vnd.apple.pages': ['.pages'],
    'application/vnd.apple.numbers': ['.numbers'],
    'text/csv': ['.csv'],
    'video/*': ['.mp4', '.mov', '.avi'],
    'image/*': ['.png', '.jpg', '.jpeg']
  };

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
      videoAreaRef.current?.requestFullscreen()
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  // Declare a new Ref for the Dean AI WebSocket
  const deanAIWebSocketRef = useRef<WebSocket | null>(null);
  const userId = Cookies.get('token');

  // Establish WebSocket connection to Dean AI Agent
  useEffect(() => {
    deanAIWebSocketRef.current = new WebSocket(`${API_ENDPOINTS.WS.STREAM}?token=${Cookies.get('token')}`);

    deanAIWebSocketRef.current.onopen = () => {
      console.log('Dean AI WebSocket connected');
    };

    deanAIWebSocketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const aiMessage = { role: 'assistant', content: data.message };
      setMessages(prev => [...prev, aiMessage]);

      // 如果有 manim_script，可以在前端显示或发送到后端处理
      if (data.manim_script) {
        // 处理 manim_script，例如发送到后端渲染
      }

      // 如果有 notes，可以显示给用户
      if (data.notes) {
        // 显示 notes，例如更新一个笔记区域
      }

      // Use Web Speech API to read the message aloud
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(data.message);
        window.speechSynthesis.speak(utterance);
      } else {
        console.warn('Speech Synthesis not supported in this browser.');
      }
    };

    deanAIWebSocketRef.current.onclose = () => {
      console.log('Dean AI WebSocket disconnected');
    };

    deanAIWebSocketRef.current.onerror = (error) => {
      console.log('Dean AI WebSocket error:', error);
    };

    // Clean up function
    return () => {
      if (deanAIWebSocketRef.current) {
        deanAIWebSocketRef.current.close();
      }
    };
  }, []);

  // Modify the handleSubmit function to send messages via WebSocket
  const handleSubmit = () => {
    if (!inputValue.trim()) return;

    const userMessage = { role: 'user', content: inputValue.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');

    // Send the message via WebSocket
    if (deanAIWebSocketRef.current && deanAIWebSocketRef.current.readyState === WebSocket.OPEN) {
      deanAIWebSocketRef.current.send(inputValue.trim());
    } else {
      toast({
        title: 'Error',
        description: 'WebSocket is not connected.',
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

  const handleFileUpload = async (acceptedFiles: File[]) => {
    const formData = new FormData();

    acceptedFiles.forEach(file => {
      formData.append('materials', file);
      setUploadingFiles(prev => [...prev, file]);
    });

    try {
      const response = await axiosInstance.post(API_ENDPOINTS.COURSE.MATERIALS, formData, {
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / (progressEvent.total || 1)
          );
          setUploadProgress(prev => ({
            ...prev,
            [acceptedFiles[0].name]: percentCompleted
          }));
        }
      });

      toast({
        title: 'Upload successful',
        description: `${acceptedFiles.length} files uploaded successfully`,
        status: 'success',
        duration: 3000,
      });
    } catch (error) {
      toast({
        title: 'Upload failed',
        description: 'Error uploading materials',
        status: 'error',
        duration: 3000,
      });
    } finally {
      setUploadingFiles([]);
      setUploadProgress({});
    }
  };

  const handleAddLink = () => {
    const url = prompt('Enter resource URL:');
    if (url && isValidUrl(url)) {
      setResourceLinks(prev => [...prev, url]);
    }
  };

  const isValidUrl = (urlString: string) => {
    try {
      return Boolean(new URL(urlString));
    } catch (e) {
      return false;
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: handleFileUpload,
    accept: ALLOWED_FILE_TYPES,
    multiple: true,
    maxSize: 100 * 1024 * 1024 // 100MB
  });

  return (<Box bg={bgColor} minH="100vh" p={4}>
        <Container maxW="container.xl">
          <Flex direction={{base: 'column', lg: 'row'}} gap={6}>
            {/* Main Video Area */}
            <Box flex="2" ref={videoAreaRef} bg={cardBg} borderRadius="lg" p={4} position="relative" >
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
              {/* Upload Section */}
              <Box w="100%" bg={cardBg} borderRadius="lg" p={4}>
                <Heading size="sm" mb={4}>Upload Learning Materials</Heading>
                
                {/* Drag & Drop Zone */}
                <Box
                  {...getRootProps()}
                  border="2px dashed"
                  borderColor={isDragActive ? 'blue.500' : 'gray.300'}
                  borderRadius="md"
                  p={6}
                  textAlign="center"
                  cursor="pointer"
                  _hover={{ borderColor: 'blue.300' }}
                  mb={4}
                >
                  <input {...getInputProps()} />
                  <VStack spacing={3}>
                    <FaFileUpload size={40} color={isDragActive ? '#3182ce' : '#718096'} />
                    <Text>
                      {isDragActive 
                        ? 'Drop files here' 
                        : 'Drag & drop files or click to select'}
                    </Text>
                    <Text fontSize="sm" color="gray.500">
                      Supported formats: PDF, DOC, PPT, CSV, Images, Videos (max 100MB)
                    </Text>
                  </VStack>
                </Box>

                {/* Upload Progress */}
                {uploadingFiles.map((file, index) => (
                  <Box key={index} mb={2}>
                    <Flex justify="space-between" mb={1}>
                      <Text fontSize="sm">{file.name}</Text>
                      <Text fontSize="sm">{uploadProgress[file.name] || 0}%</Text>
                    </Flex>
                    <Progress 
                      value={uploadProgress[file.name] || 0}
                      size="xs"
                      colorScheme="blue"
                      borderRadius="full"
                    />
                  </Box>
                ))}

                {/* Resource Links Section */}
                <VStack mt={4} align="stretch">
                  <Button 
                    leftIcon={<FaLink />}
                    colorScheme="blue"
                    variant="outline"
                    onClick={handleAddLink}
                  >
                    Add Resource Link
                  </Button>
                  
                  {resourceLinks.map((link, index) => (
                    <Flex key={index} align="center" p={2} bg={ bgColor } borderRadius="md">
                      <Text fontSize="sm" isTruncated flex={1}>{link}</Text>
                      <IconButton
                        aria-label="Remove link"
                        icon={<SmallCloseIcon />}
                        size="xs"
                        onClick={() => setResourceLinks(prev => prev.filter((_, i) => i !== index))}
                      />
                    </Flex>
                  ))}
                </VStack>
              </Box>

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
                          bg={msg.role === 'user' ? chatUserBg : chatTeacherBg}
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
                    onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}/>
                <Button colorScheme="blue" onClick={handleSubmit}>
                  Send
                </Button>
              </Flex>
            </VStack>
          </Flex>
        </Container>
      </Box>
  );
};

export default CourseInteractionPage;
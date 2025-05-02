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
import {AI_ENDPOINTS, API_ENDPOINTS} from '@/config/api';
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
  const materialRef = useRef<string>("");

  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBg = useColorModeValue('white', 'gray.700');
  const chatUserBg = useColorModeValue('blue.50', 'blue.500');
  const chatTeacherBg = useColorModeValue('gray.50', 'gray.500');

  const [uploadingFiles, setUploadingFiles] = useState<File[]>([]);
  const [uploadProgress, setUploadProgress] = useState<{ [key: string]: number }>({});
  const [resourceLinks, setResourceLinks] = useState<string[]>([]);

  // Add a state variable to track authentication status
  const [authenticated, setAuthenticated] = useState(false);

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
          // audio stream logic
          const mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.ondataavailable = (event) => {
            if (websocketRef.current?.readyState !== WebSocket.OPEN) return;
            const audioBlob = event.data;
            const reader = new FileReader();
            reader.onloadend = () => {
              const buffer = reader.result;
              // 测试是否在发送音频数据
              // console.log("发送音频数据，字节长度:", buffer ? (buffer as ArrayBuffer).byteLength : 0);
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
        // 日志：每次分配流时输出当前 srcObject
        console.log("[startVideo] studentVideoRef.current.srcObject:", studentVideoRef.current.srcObject);
        // 新增：持续监控 srcObject 是否被清空
        setInterval(() => {
          if (studentVideoRef.current) {
            console.log("[monitor] studentVideoRef.current.srcObject:", studentVideoRef.current.srcObject);
          }
        }, 2000);
      } else {
        console.warn("[startVideo] studentVideoRef.current 不存在");
      }
      setVideoStream(stream);
      // 新增：持续监控 videoStream 的 track 状态
      stream.getTracks().forEach(track => {
        track.onended = () => {
          console.warn("[monitor] videoStream track ended:", track);
        };
      });
      return stream;
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
    
    // First handle connection and authentication, then start media
    setConnecting(true);
    setAuthenticated(false);
    
    const ws = new WebSocket(`ws://localhost:1298/ai/ws/stream`);
    
    // Define all event handlers before setting the reference

    ws.onopen = () => {
      console.log('Dean AI WebSocket connected');
      
      // Send authentication message immediately after connection
      const token = Cookies.get('token');
      if (!token) {
        toast({
          title: 'Authentication error',
          description: 'No auth token found',
          status: 'error',
          duration: 3000,
        });
        ws.close();
        return;
      }
      
      const authMessage = JSON.stringify({
        type: "auth",
        token: token
      });
      ws.send(authMessage);
      console.log('Authentication message sent');
      
      toast({
        title: 'Connecting to AI',
        description: 'Authenticating...',
        status: 'info',
        duration: 2000,
      });
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Received message:', data);
        
        // Handle authentication response
        if (data.status === "success" && data.health === "ok") {
          console.log("Authentication successful");
          setAuthenticated(true);
          setConnecting(false);
          setRecording(true);
          
          toast({
            title: 'Connected successfully',
            description: 'Authentication successful',
            status: 'success',
            duration: 3000,
          });
          
          // Only start media streams after successful authentication
          startVideo();
          startAudio();
          
          // Start video frame capture
          const video = studentVideoRef.current;
          if (video) {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            sendingVideoTask.current = setInterval(() => {
              if (!video || !ctx || websocketRef.current?.readyState !== WebSocket.OPEN) return;
              // 降低分辨率
              const targetWidth = 320;
              const targetHeight = 240;
              canvas.width = targetWidth;
              canvas.height = targetHeight;
              ctx.drawImage(video, 0, 0, targetWidth, targetHeight);
              canvas.toBlob((blob) => {
                if (blob && websocketRef.current?.readyState === WebSocket.OPEN) {
                  blob.arrayBuffer().then(buffer => {
                    websocketRef.current?.send(buffer);
                  });
                }
              }, 'image/jpeg', 0.7);
            }, 200); // 200ms 一帧
            
            // 新增：监控 setInterval 是否持续运行
            setInterval(() => {
              console.log("[monitor] sendingVideoTask.current:", sendingVideoTask.current);
            }, 2000);
          }
        } 
        // Handle authentication error
        else if (data.status === "error") {
          console.error("Authentication error:", data.message);
          setConnecting(false);
          toast({
            title: 'Authentication failed',
            description: data.message || 'Could not authenticate with the server',
            status: 'error',
            duration: 5000,
          });
          // Close the connection on auth failure
          ws.close(1000, "Authentication failed");
        }
        // Handle regular messages
        else if (data.message) {
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
        }
      } catch (error) {
        console.error("Error parsing message:", error);
        console.log("Raw message:", event.data);
        
        // For non-JSON responses that might be from early debugging
        if (typeof event.data === 'string' && event.data.startsWith('Received:')) {
          console.log("Received acknowledgment from server");
        }
      }
    }
    
    ws.onclose = (closeEvent) => {
      setAuthenticated(false);
      setRecording(false);
      
      if (closeEvent.code !== 1000) {
        console.error("WebSocket closed with code:", closeEvent.code);
        toast({
          title: 'Connection closed',
          description: closeEvent.reason || 'The connection was closed unexpectedly',
          status: 'error',
          duration: 3000,
        });
      } else {
        toast({
          title: 'Disconnected',
          description: 'Connection closed successfully',
          status: 'success',
          duration: 3000,
        });
      }
      websocketRef.current = null; // 清空 WebSocket 实例
      disconnectWebSocket();
    };
    
    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      toast({
        title: 'Connection error',
        description: 'Failed to connect to the server',
        status: 'error',
        duration: 3000,
      });
      setConnecting(false);
    };

    // Set the WebSocket reference after defining all event handlers
    websocketRef.current = ws;
  };

  // 断开 WebSocket
  const disconnectWebSocket = () => {
    console.log('Disconnecting WebSocket');
    
    // Stop media streams
    stopVideo();
    stopAudio();
    
    // Update state
    setRecording(false);
    setConnecting(false);
    setAuthenticated(false);
    
    // Close WebSocket connection if it exists
    if (websocketRef.current) {
      console.log('Closing WebSocket connection');
      try {
        // 1000 is normal closure status code
        websocketRef.current.close(1000, "User disconnected");
        websocketRef.current = null;
        console.log('WebSocket disconnected successfully');
      } catch (error) {
        console.error('Error closing WebSocket:', error);
      }
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
      videoStream.getTracks().forEach(track => {
        track.stop();
        // 日志：track.stop 被调用
        console.log("[stopVideo] track.stop 被调用:", track);
      });
      setVideoStream(null);
      // 日志：stopVideo 被调用时输出
      console.log("[stopVideo] setVideoStream(null) 已调用");
    }
    // 清除视频元素的 srcObject
    if (studentVideoRef.current) {
      studentVideoRef.current.srcObject = null;
      console.log("[stopVideo] studentVideoRef.current.srcObject 已清空");
    }
    if (!sendingVideoTask.current) return;
    clearInterval(sendingVideoTask.current)
    sendingVideoTask.current = null
    // 日志：stopVideo 完成所有清理
    console.log("[stopVideo] 完成所有清理");
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

  // Modify the handleSubmit function to send messages via WebSocket
  const handleSubmit = () => {
    if (!inputValue.trim()) return;

    const userMessage = { role: 'user', content: inputValue.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');

    // Send the message via WebSocket
    if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
      websocketRef.current.send(inputValue.trim());
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

      materialRef.current = response.data?.file

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
                  <Flex align="center">
                    {authenticated && recording && (
                      <Box 
                        w="10px" 
                        h="10px" 
                        borderRadius="full" 
                        bg="green.500" 
                        mr={2} 
                        animation="pulse 1.5s infinite"
                        sx={{
                          "@keyframes pulse": {
                            "0%": { opacity: 1 },
                            "50%": { opacity: 0.5 },
                            "100%": { opacity: 1 }
                          }
                        }}
                      />
                    )}
                    <Button
                      size="sm"
                      colorScheme={recording ? 'red' : 'green'}
                      onClick={toggleConnect}
                      isLoading={connecting}
                      loadingText="Connecting"
                    >
                      {recording ? 'Turn Off' : 'Turn On'}
                    </Button>
                  </Flex>
                </Flex>
                <Box position="relative">
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
                      muted
                    />
                  </Box>
                  
                  {connecting && !authenticated && (
                    <Flex 
                      position="absolute" 
                      top="0" 
                      left="0" 
                      right="0" 
                      bottom="0" 
                      bg="blackAlpha.700" 
                      zIndex="10"
                      justify="center"
                      align="center"
                      direction="column"
                      borderRadius="md"
                    >
                      <Text color="white" mb={2} fontWeight="bold">
                        Authenticating...
                      </Text>
                      <Progress 
                        size="xs" 
                        isIndeterminate 
                        colorScheme="blue" 
                        w="80%" 
                        borderRadius="full"
                      />
                    </Flex>
                  )}
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
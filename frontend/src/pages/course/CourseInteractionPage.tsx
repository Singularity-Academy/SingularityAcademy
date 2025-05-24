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
import { AxiosProgressEvent } from 'axios';

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
          let audioPacketId = 0;
          mediaRecorder.ondataavailable = (event) => {
            if (websocketRef.current?.readyState !== WebSocket.OPEN) return;
            const audioBlob = event.data;
            const reader = new FileReader();
            reader.onloadend = () => {
              // Get base64 data
              const base64data = reader.result as string;
              // Extract just the base64 part (remove the data:audio/wav;base64, prefix)
              const base64EncodedAudio = base64data.split(',')[1];
              // Send audio data in JSON format
              const audioPacket = {
                packet_id: audioPacketId++,
                time: Date.now(),
                video: null,
                audio: base64EncodedAudio,
              };
              
              // Send as JSON string
              websocketRef.current?.send(JSON.stringify(audioPacket));
            };
            // Read as base64 instead of ArrayBuffer
            reader.readAsDataURL(audioBlob);
          };
          mediaRecorder.start(500);  // Capture every 0.5 seconds of audio
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
    if (websocketRef.current) return; // If already connected, don't reconnect
    startVideo();
    startAudio();
    setConnecting(true);
    const video = studentVideoRef.current;
    const base_url = window.location.host;
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${base_url}/ai/dean/ws`);

    ws.onopen = () => {
      console.log('Dean AI WebSocket connected');
      toast({
        title: 'connect successful',
        status: 'success',
        duration: 3000,
      });
      // Send authentication token and wait for response
      ws.send(JSON.stringify({
        type: 'auth',
        token: Cookies.get('token')
      }));
      setConnecting(false);
      // Wait for auth response before starting video - don't start streaming yet
    };
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        // Handle auth response
        if (data.type === 'auth_response') {
          if (data.status === 'success') {
            setRecording(true);
            startVideoStreaming(video, ws);
          } else {
            toast({
              title: 'Authentication failed',
              description: data.message || 'Invalid credentials',
              status: 'error',
              duration: 3000,
            });
            disconnectWebSocket();
            return;
          }
          return;
        }
        
        // Handle regular messages
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
      } catch (err) {
        console.error('Error processing message:', err);
      }
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
      websocketRef.current = null; // 清空 WebSocket 实例
      disconnectWebSocket();
    };

    websocketRef.current = ws;
  };

  // 断开 WebSocket
  const disconnectWebSocket = () => {
    console.log('disconnectWebSocket');
    // 日志：disconnectWebSocket 被调用
    stopVideo()
    stopAudio();
    setRecording(false);
    setConnecting(false);
    if (websocketRef.current) {
      websocketRef.current.close(1000);
      websocketRef.current = null;
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
        onUploadProgress: (progressEvent: AxiosProgressEvent) => {
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

  // Function to start streaming video frames
  const startVideoStreaming = (video: HTMLVideoElement | null, ws: WebSocket) => {
    if (!video) return;
    
    let packetId = 0;
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    sendingVideoTask.current = setInterval(() => {
      if (!video || !ctx || ws.readyState !== WebSocket.OPEN) return;
      
      // 降低分辨率
      const targetWidth = 320;
      const targetHeight = 240;
      canvas.width = targetWidth;
      canvas.height = targetHeight;
      ctx.drawImage(video, 0, 0, targetWidth, targetHeight);
      
      // Convert frame to base64 instead of binary
      canvas.toBlob((blob) => {
        if (blob && ws.readyState === WebSocket.OPEN) {
          const reader = new FileReader();
          reader.onloadend = () => {
            // Get base64 data string
            const base64data = reader.result as string;
            // Extract the base64 part (remove the data:image/jpeg;base64, prefix)
            const base64EncodedFrame = base64data.split(',')[1];
            
            // Create packet according to Python backend spec
            const videoPacket = {
              packet_id: packetId++,
              time: Date.now(),
              video: base64EncodedFrame,
              audio: null // We're only sending video for now
            };
            
            // Send as JSON string
            ws.send(JSON.stringify(videoPacket));
          };
          reader.readAsDataURL(blob);
        }
      }, 'image/jpeg', 0.7);
    }, 200); // 200ms 一帧
    
    // 新增：监控 setInterval 是否持续运行
    setInterval(() => {
      console.log("[monitor] sendingVideoTask.current:", sendingVideoTask.current);
    }, 2000);
  };

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
                        <Text whiteSpace="pre-wrap">{msg.content}</Text>
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
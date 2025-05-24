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
  Progress,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Textarea,
  Badge,
  Link,
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon, SmallCloseIcon } from '@chakra-ui/icons';
import axiosInstance from '@utils/axios';
import {API_ENDPOINTS} from '@/config/api';
import Cookies from "js-cookie";
import {useNavigate} from "react-router-dom";
import { FaFileUpload, FaLink } from 'react-icons/fa';
import { useDropzone } from 'react-dropzone';
import { AxiosProgressEvent } from 'axios';
import { logger } from '../../utils/logger';

declare class ImageCapture {
  constructor(track: MediaStreamTrack);
  takePhoto(): Promise<Blob>;
}

interface VideoGenerationStatus {
  video_uuid: string;
  status: 'idle' | 'processing' | 'completed' | 'failed' | 'cancelled' | 'disconnected';
  progress: number;
  message: string;
  error: string | null;
  download_url: string | null;
}

interface Message {
  role: string;
  content: string;
}

interface UploadProgress {
  [key: string]: number;
}

// Video generation configuration matching backend config.json
const VIDEO_GENERATION_CONFIG = {
  default_model: "gpt-4",
  models: {
    "gpt-4": {
      name: "GPT-4",
      model_id: "gpt-4",
      api_key: "Link_T1ZLmLhcIhZvOX9bRYFM4agbjY0CNwIpCbScjEe0GG",
      api_base: "https://api.link-ai.tech/v1",
      temperature: 0.7,
      max_tokens: 2000,
      streaming: true,
      timeout: 60,
      retry_attempts: 3,
      description: "OpenAI's most capable model, optimized for complex mathematical and educational content generation"
    },
    "gpt-4-turbo": {
      name: "GPT-4 Turbo",
      model_id: "gpt-4-1106-preview",
      api_key: "Link_T1ZLmLhcIhZvOX9bRYFM4agbjY0CNwIpCbScjEe0GG",
      api_base: "https://api.link-ai.tech/v1",
      temperature: 0.7,
      max_tokens: 2000,
      streaming: true,
      timeout: 60,
      retry_attempts: 3,
      description: "Latest GPT-4 model with improved performance and lower cost, ideal for educational animations"
    },
    "gpt-3.5-turbo": {
      name: "GPT-3.5 Turbo",
      model_id: "gpt-3.5-turbo",
      api_key: "Link_T1ZLmLhcIhZvOX9bRYFM4agbjY0CNwIpCbScjEe0GG",
      api_base: "https://api.link-ai.tech/v1",
      temperature: 0.7,
      max_tokens: 2000,
      streaming: true,
      timeout: 60,
      retry_attempts: 3,
      description: "Fast and cost-effective model, suitable for basic mathematical animations"
    },
    "deepseek-v3": {
      name: "Deepseek Chat v3",
      model_id: "deepseek-chat",
      api_key: "sk-f4035b1b6ee54b58871ed85d2e53e21f",
      api_base: "https://api.deepseek.com/v1",
      temperature: 0.7,
      max_tokens: 2000,
      streaming: true,
      timeout: 60,
      retry_attempts: 3,
      description: "Deepseek's latest model with strong performance on coding and mathematical reasoning tasks"
    }
  },
  manim_settings: {
    quality: "medium",
    preview: true,
    frame_rate: 30,
    resolution: "1080p",
    quality_options: {
      low: {
        flag: "-ql",
        resolution: "480p",
        frame_rate: 15,
        description: "Fast rendering for quick previews"
      },
      medium: {
        flag: "-qm",
        resolution: "720p",
        frame_rate: 30,
        description: "Balanced quality and rendering speed"
      },
      high: {
        flag: "-qh",
        resolution: "1080p",
        frame_rate: 60,
        description: "High quality for final output"
      },
      "4k": {
        flag: "-qk",
        resolution: "2160p",
        frame_rate: 60,
        description: "Ultra high quality for professional use"
      }
    }
  },
  output_settings: {
    output_dir: "ai_generated_videos",
    keep_intermediate_files: true,
    auto_backup: true,
    max_video_duration: 120,
    video_format: "mp4",
    audio_enabled: false
  },
  generation_settings: {
    scene_planning: {
      include_formulas: true,
      include_animations: true,
      include_colors: true,
      chinese_support: true,
      max_scene_complexity: "medium"
    },
    code_generation: {
      add_comments: true,
      use_meaningful_names: true,
      include_error_handling: false,
      optimize_for_readability: true
    },
    fallback_enabled: true,
    debug_mode: false
  },
  ui_settings: {
    language: "zh-CN",
    show_progress: true,
    verbose_logging: true,
    color_output: true
  }
};

const CourseInteractionPage: React.FC = () => {
  // UI-related state and hooks
  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBg = useColorModeValue('white', 'gray.700');
  const chatUserBg = useColorModeValue('blue.50', 'blue.900');
  const chatTeacherBg = useColorModeValue('gray.50', 'gray.700');
  const [isFullscreen, setIsFullscreen] = useState(false);
  const { isOpen: isVideoModalOpen, onOpen: onVideoModalOpen, onClose: onVideoModalClose } = useDisclosure();
  const videoAreaRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // File upload and resource links state
  const [uploadingFiles, setUploadingFiles] = useState<File[]>([]);
  const [uploadProgress, setUploadProgress] = useState<UploadProgress>({});
  const [resourceLinks, setResourceLinks] = useState<string[]>([]);

  // File upload related
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles: File[]) => {
      setUploadingFiles(prev => [...prev, ...acceptedFiles]);
      // Handle file upload
      console.log('Files dropped:', acceptedFiles);
    },
    accept: {
      'video/*': ['.mp4', '.mov', '.avi'],
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    maxSize: 100 * 1024 * 1024 // 100MB
  });

  const handleAddLink = () => {
    const url = prompt('Enter resource URL:');
    if (url && isValidUrl(url)) {
      setResourceLinks(prev => [...prev, url]);
    }
  };

  const isValidUrl = (urlString: string): boolean => {
    try {
      return Boolean(new URL(urlString));
    } catch (e) {
      return false;
    }
  };

  // State declarations
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isGeneratingVideo, setIsGeneratingVideo] = useState(false);
  const [videoGenerationText, setVideoGenerationText] = useState("Newton's 3rd law");
  const [videoGenerationError, setVideoGenerationError] = useState<string | null>(null);
  const [audioStream, setAudioStream] = useState<MediaStream | null>(null);
  const [videoStream, setVideoStream] = useState<MediaStream | null>(null);
  const [videoGenerationStatus, setVideoGenerationStatus] = useState<VideoGenerationStatus>({
    video_uuid: '',
    status: 'idle',
    progress: 0,
    message: '',
    error: null,
    download_url: null
  });

  // Refs
  const wsRef = useRef<WebSocket | null>(null);
  const videoGenerationWs = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const studentVideoRef = useRef<HTMLVideoElement>(null);
  const websocketRef = useRef<WebSocket | null>(null);
  const toast = useToast();

  // WebSocket connection and handlers
  const connectVideoGenerationWs = useCallback(() => {
    const ws = videoGenerationWs.current;
    if (ws?.readyState === WebSocket.OPEN) {
      logger.debug("Video generation WebSocket already connected");
      return;
    }

    // Get token from cookies
    const token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
    if (!token) {
      logger.error("No authentication token found in cookies");
      setVideoGenerationError("Authentication token not found");
      return;
    }

    // Construct WebSocket URL using current protocol and host
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const base_url = window.location.host;
    const wsUrl = `${protocol}//${base_url}/ai/dean/video-generator`;
    
    logger.info(`Connecting to video generation WebSocket at ${wsUrl}`);
    
    try {
      const newWs = new WebSocket(wsUrl);
      videoGenerationWs.current = newWs;
      
      newWs.onopen = () => {
        logger.info("Video generation WebSocket connected");
        // Send authentication message immediately after connection
        const authMessage = {
          type: "auth",
          token: token
        };
        newWs.send(JSON.stringify(authMessage));
        logger.debug("Sent authentication message");
      };

      newWs.onmessage = (event) => {
        const data = JSON.parse(event.data);
        logger.debug("Received video generation message:", data);

        if (data.type === "auth_response") {
          if (data.status === "success") {
            logger.info("Video generation WebSocket authenticated successfully");
          } else {
            logger.error("Video generation WebSocket authentication failed:", data.message);
            setVideoGenerationError("Authentication failed: " + data.message);
            newWs.close();
          }
          return;
        }

        if (data.type === "status") {
          setVideoGenerationStatus(prev => ({
            ...prev,
            video_uuid: data.video_uuid || prev.video_uuid,
            status: data.status,
            progress: data.progress || prev.progress,
            message: data.message || prev.message,
            error: data.error || prev.error,
            download_url: data.download_url || prev.download_url
          }));

          if (data.status === "completed" || data.status === "failed" || data.status === "cancelled") {
            setIsGeneratingVideo(false);
          }
        }
      };

      newWs.onerror = (error) => {
        logger.error("Video generation WebSocket error:", error);
        setVideoGenerationError("Connection error occurred");
      };

      newWs.onclose = () => {
        logger.info("Video generation WebSocket closed");
        setVideoGenerationStatus(prev => ({
          ...prev,
          status: "disconnected"
        }));
      };

    } catch (error) {
      logger.error("Failed to connect to video generation WebSocket:", error);
      setVideoGenerationError("Failed to establish connection");
    }
  }, []);

  const sendVideoGenerationRequest = useCallback((text: string) => {
    const ws = videoGenerationWs.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      logger.error("Cannot send request: WebSocket not connected");
      setVideoGenerationError("Not connected to server");
      return;
    }

    const request = {
      type: "generate",
      text: text.trim(),
      title: "AI Generated Video",
      config: VIDEO_GENERATION_CONFIG  // Include the config in the request
    };

    try {
      ws.send(JSON.stringify(request));
      setVideoGenerationStatus(prev => ({
        ...prev,
        status: "processing",
        progress: 0,
        message: "Starting video generation...",
        error: null,
        download_url: null
      }));
      setIsGeneratingVideo(true);
    } catch (error) {
      logger.error("Failed to send video generation request:", error);
      setVideoGenerationError("Failed to send request");
    }
  }, []);

  const startVideoGeneration = useCallback(() => {
    if (!videoGenerationText.trim()) {
      toast({
        title: "Error",
        description: "Please enter some text to generate a video",
        status: "error",
        duration: 3000,
      });
      return;
    }

    const ws = videoGenerationWs.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      logger.info("WebSocket not connected, attempting to connect...");
      connectVideoGenerationWs();
      // Wait for connection and then send request
      setTimeout(() => {
        const ws = videoGenerationWs.current;
        if (ws?.readyState === WebSocket.OPEN) {
          sendVideoGenerationRequest(videoGenerationText);
        } else {
          toast({
            title: "Connection Error",
            description: "Failed to connect to server",
            status: "error",
            duration: 3000,
          });
        }
      }, 1000);
    } else {
      sendVideoGenerationRequest(videoGenerationText);
    }
  }, [videoGenerationText, connectVideoGenerationWs, sendVideoGenerationRequest, toast]);

  const cancelVideoGeneration = useCallback(() => {
    const ws = videoGenerationWs.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      logger.error("Cannot cancel: WebSocket not connected");
      return;
    }

    const { video_uuid } = videoGenerationStatus;
    if (!video_uuid) {
      logger.error("Cannot cancel: No active video generation");
      return;
    }

    try {
      ws.send(JSON.stringify({
        type: "cancel",
        video_uuid
      }));
      logger.info("Sent video generation cancellation request");
    } catch (error) {
      logger.error("Failed to send cancellation request:", error);
    }
  }, [videoGenerationStatus]);

  // Effects
  useEffect(() => {
    connectVideoGenerationWs();
    return () => {
      const ws = videoGenerationWs.current;
      if (ws) {
        ws.close();
        videoGenerationWs.current = null;
      }
    };
  }, [connectVideoGenerationWs]);

  // Audio/Video recording functions
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
          description: error.message || String(error),
          status: 'error',
          duration: 3000,
        }));
  };

  const stopAudio = () => {
    if (audioStream) {
      audioStream.getTracks().forEach((track: MediaStreamTrack) => track.stop());
      setAudioStream(null);
    }
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
  };

  const startVideo = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      });
      
      if (studentVideoRef.current) {
        studentVideoRef.current.srcObject = stream;
        await studentVideoRef.current.play();
      }
      
      setVideoStream(stream);
      setIsRecording(true);
      
      toast({
        title: "Recording started",
        status: "success",
        duration: 3000,
      });
    } catch (error) {
      console.error("Error accessing media devices:", error);
      toast({
        title: "Error",
        description: "Failed to access camera and microphone",
        status: "error",
        duration: 3000,
      });
    }
  };

  const stopVideo = () => {
    if (videoStream) {
      videoStream.getTracks().forEach(track => track.stop());
      setVideoStream(null);
    }
    
    if (studentVideoRef.current) {
      studentVideoRef.current.srcObject = null;
    }
    
    setIsRecording(false);
    toast({
      title: "Recording stopped",
      status: "info",
      duration: 3000,
    });
  };

  const downloadVideo = async () => {
    if (!videoGenerationStatus?.download_url) return;

    try {
      // Update the URL to use /ai prefix instead of /api
      const downloadUrl = videoGenerationStatus.download_url.replace('/api/', '/ai/');
      const response = await axiosInstance.get(downloadUrl, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `ai_video_${videoGenerationStatus.video_uuid}.mp4`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      toast({
        title: 'Download failed',
        description: 'Could not download the video',
        status: 'error',
        duration: 3000,
      });
    }
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      videoAreaRef.current?.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  // Chat message handling
  const handleSubmit = useCallback(() => {
    if (!inputValue.trim()) return;

    const userMessage = { role: 'user', content: inputValue.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');

    if (websocketRef.current?.readyState === WebSocket.OPEN) {
      websocketRef.current.send(JSON.stringify({
        type: 'message',
        content: inputValue.trim()
      }));
    } else {
      toast({
        title: 'Error',
        description: 'WebSocket is not connected.',
        status: 'error',
        duration: 3000,
      });
    }
  }, [inputValue, toast]);

  // Auto-scroll chat to bottom when new messages arrive
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <Box bg={bgColor} minH="100vh" p={4}>
      <Container maxW="container.xl">
        <Flex direction={{base: 'column', lg: 'row'}} gap={6}>
          {/* Main Content Area */}
          <Box flex="2" ref={videoAreaRef} bg={cardBg} borderRadius="lg" p={4} position="relative">
            <Flex justify="space-between" mb={4}>
              <Heading size="md">Course Content</Heading>
              <Button
                colorScheme="blue"
                onClick={onVideoModalOpen}
                leftIcon={<FaFileUpload />}
              >
                Generate AI Video
              </Button>
            </Flex>
            
            {/* Video Generation Status */}
            {videoGenerationStatus && (
              <Box mb={4} p={4} bg={cardBg} borderRadius="md" borderWidth="1px">
                <Flex justify="space-between" align="center" mb={2}>
                  <Text fontWeight="bold">Video Generation Status</Text>
                  <Badge
                    colorScheme={
                      videoGenerationStatus.status === 'completed' ? 'green' :
                      videoGenerationStatus.status === 'failed' ? 'red' :
                      videoGenerationStatus.status === 'cancelled' ? 'gray' : 'blue'
                    }
                  >
                    {videoGenerationStatus.status.toUpperCase()}
                  </Badge>
                </Flex>
                {videoGenerationStatus.message && (
                  <Text fontSize="sm" mb={2}>{videoGenerationStatus.message}</Text>
                )}
                {videoGenerationStatus.error && (
                  <Text fontSize="sm" color="red.500" mb={2}>{videoGenerationStatus.error}</Text>
                )}
                <Progress
                  value={videoGenerationStatus.progress}
                  size="sm"
                  colorScheme="blue"
                  mb={2}
                />
                <Flex justify="flex-end" gap={2}>
                  {videoGenerationStatus.status === 'processing' && (
                    <Button
                      size="sm"
                      colorScheme="red"
                      onClick={cancelVideoGeneration}
                      isDisabled={!isGeneratingVideo}
                    >
                      Cancel
                    </Button>
                  )}
                  {videoGenerationStatus.status === 'completed' && (
                    <Button
                      size="sm"
                      colorScheme="green"
                      onClick={downloadVideo}
                    >
                      Download Video
                    </Button>
                  )}
                </Flex>
              </Box>
            )}

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
              onClick={toggleFullscreen}
            />
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
              {uploadingFiles.map((file: File, index: number) => (
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
                
                {resourceLinks.map((link: string, index: number) => (
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
                    colorScheme={isRecording ? 'red' : 'green'}
                    onClick={startVideo}
                    isLoading={isRecording}
                    loadingText="Recording"
                >
                  {isRecording ? 'Turn Off' : 'Turn On'}
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

      {/* Video Generation Modal */}
      <Modal isOpen={isVideoModalOpen} onClose={onVideoModalClose} size="xl">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Generate AI Educational Video</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <VStack spacing={4} align="stretch">
              <Text>
                Enter a description of the educational content you want to generate a video for.
                The AI will create an animated video explaining the concept.
              </Text>
              <Textarea
                value={videoGenerationText}
                onChange={(e) => setVideoGenerationText(e.target.value)}
                placeholder="Describe the educational content you want to explain in the video..."
                size="lg"
                rows={6}
              />
              <Text fontSize="sm" color="gray.500">
                Maximum 300 characters. The video will be generated using AI animation.
              </Text>
              <Button
                colorScheme="blue"
                onClick={startVideoGeneration}
                isLoading={isGeneratingVideo}
                loadingText="Generating..."
                isDisabled={!videoGenerationText.trim() || isGeneratingVideo}
              >
                Generate Video
              </Button>
            </VStack>
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  );
};

export default CourseInteractionPage;
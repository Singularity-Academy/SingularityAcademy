import React, { useState, useRef, useEffect } from 'react';
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
  HStack
} from '@chakra-ui/react';
import { FaPaperPlane, FaVideo, FaVideoSlash, FaExpand } from 'react-icons/fa';
import Navbar from '@components/Navbar';
import { useTranslation } from 'react-i18next';
import './../styles/ParticleBackground.css';

interface Message {
  content: string;
  isAI: boolean;
  timestamp: string;
}

const PrincipalAIPage: React.FC = () => {
  const { t } = useTranslation();
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

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const newMessage = {
      content: inputMessage,
      isAI: false,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        content: t('PrincipalAI.response', { goal: inputMessage }),
        isAI: true,
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
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
            >
              <VStack spacing={4} align="stretch">
                {messages.map((msg, index) => (
                  <Flex
                    key={index}
                    direction={msg.isAI ? 'row' : 'row-reverse'}
                    gap={3}
                    align="flex-start"
                  >
                    <Avatar
                      name={msg.isAI ? t('PrincipalAI.name') : 'You'}
                      src={msg.isAI ? '/ai-principal-avatar.png' : ''}
                      size="sm"
                    />
                    <Box
                      p={3}
                      borderRadius="lg"
                      bg={msg.isAI ? 'blue.50' : 'purple.50'}
                      maxW="80%"
                      position="relative"
                      _before={{
                        content: '""',
                        position: 'absolute',
                        top: '10px',
                        [msg.isAI ? 'left' : 'right']: '-8px',
                        w: '0',
                        h: '0',
                        borderTop: '8px solid transparent',
                        borderBottom: '8px solid transparent',
                        borderLeft: msg.isAI ? '8px solid #BEE3F8' : 'none',
                        borderRight: !msg.isAI ? '8px solid #E9D8FD' : 'none'
                      }}
                    >
                      <Text fontSize="sm" color="gray.500" mb={1}>
                        {msg.timestamp}
                      </Text>
                      <Text>{msg.content}</Text>
                    </Box>
                  </Flex>
                ))}
              </VStack>
            </Box>

            <HStack>
              <Input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder={t('PrincipalAI.placeholder')}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                bg={useColorModeValue('white', 'gray.800')}
              />
              <IconButton
                colorScheme="blue"
                aria-label="Send message"
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
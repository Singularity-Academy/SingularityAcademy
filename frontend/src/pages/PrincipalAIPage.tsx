import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  VStack, 
  Heading, 
  Text, 
  Input, 
  Button, 
  useColorModeValue,
  SimpleGrid,
  Card,
  CardBody,
  Avatar,
  Flex,
  IconButton
} from '@chakra-ui/react';
import { FaPaperPlane } from 'react-icons/fa';
import Navbar from '@components/Navbar';
import { useTranslation } from 'react-i18next';

interface Message {
  content: string;
  isAI: boolean;
}

const PrincipalAIPage: React.FC = () => {
  const { t } = useTranslation();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [studyPlan, setStudyPlan] = useState<string[]>([]);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const cardBg = useColorModeValue('white', 'gray.800');

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    // Add user message
    const newMessages = [...messages, { content: inputMessage, isAI: false }];
    setMessages(newMessages);
    setInputMessage('');

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        content: t('PrincipalAI.response', { goal: inputMessage }),
        isAI: true
      };
      setMessages([...newMessages, aiResponse]);
      
      // Generate sample study plan
      setStudyPlan([
        t('PrincipalAI.physics'),
        t('PrincipalAI.mathematics'),
        t('PrincipalAI.engineering'),
        t('PrincipalAI.computerScience')
      ]);
    }, 1000);
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <Box minH="100vh" display="flex" flexDirection="column">
      <Navbar />
      
      <Flex flex="1" p={8} gap={8} direction={{ base: 'column', lg: 'row' }}>
        {/* Chat Section */}
        <Card flex="1" bg={cardBg}>
          <CardBody>
            <VStack spacing={6} align="stretch">
              <Heading size="xl" color="blue.500">
                {t('PrincipalAI.title')}
              </Heading>
              
              <Box
                ref={chatContainerRef}
                h="60vh"
                overflowY="auto"
                p={4}
                borderRadius="md"
                bg={useColorModeValue('gray.50', 'gray.700')}
              >
                <VStack spacing={4} align="start">
                  {messages.map((msg, index) => (
                    <Flex key={index} gap={3} w="100%">
                      <Avatar 
                        name={msg.isAI ? t('PrincipalAI.name') : 'You'}
                        src={msg.isAI ? '/ai-principal.png' : ''}
                      />
                      <Box
                        p={4}
                        borderRadius="lg"
                        bg={msg.isAI ? 'blue.50' : 'gray.100'}
                        flex="1"
                      >
                        <Text fontWeight="bold" mb={2}>
                          {msg.isAI ? t('PrincipalAI.name') : t('PrincipalAI.you')}
                        </Text>
                        <Text>{msg.content}</Text>
                      </Box>
                    </Flex>
                  ))}
                </VStack>
              </Box>

              <Flex gap={2}>
                <Input
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder={t('PrincipalAI.placeholder')}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                />
                <IconButton
                  colorScheme="blue"
                  aria-label="Send message"
                  icon={<FaPaperPlane />}
                  onClick={handleSendMessage}
                />
              </Flex>
            </VStack>
          </CardBody>
        </Card>

        {/* Study Plan Section */}
        {studyPlan.length > 0 && (
          <Card w={{ base: '100%', lg: '400px' }} bg={cardBg}>
            <CardBody>
              <VStack spacing={4} align="stretch">
                <Heading size="lg" color="green.600">
                  {t('PrincipalAI.studyPlan')}
                </Heading>
                {studyPlan.map((course, index) => (
                  <Flex
                    key={index}
                    p={3}
                    borderRadius="md"
                    bg="green.50"
                    align="center"
                    gap={2}
                  >
                    <Text>📘</Text>
                    <Text fontWeight="medium">{course}</Text>
                  </Flex>
                ))}
              </VStack>
            </CardBody>
          </Card>
        )}
      </Flex>
    </Box>
  );
};

export default PrincipalAIPage; 
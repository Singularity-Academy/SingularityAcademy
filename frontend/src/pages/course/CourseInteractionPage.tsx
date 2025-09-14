import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Send, User, Bot, Bookmark } from 'lucide-react';

interface ToolCall {
  name: string;
  parameters?: any;
  result?: any;
  status?: 'pending' | 'completed' | 'error';
}

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  rawContent?: string;
  timestamp: Date;
  isStreaming?: boolean;
  toolCalls?: ToolCall[];
}

interface Course {
  id: string;
  title: string;
  description: string;
  instructor: string;
  createdAt: string;
  grade_level?: string;
  duration?: string;
  format?: string;
}

const CourseInteractionPage = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [courses] = useState<Course[]>([]);
  const [currentStreamingMessageId, setCurrentStreamingMessageId] = useState<string | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const connectWebSocket = useCallback(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ai/principal-ai/ws/chat`;
    
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
      
      // Send authentication
      const token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
      if (token && wsRef.current) {
        wsRef.current.send(JSON.stringify({ token }));
      }
    };

    wsRef.current.onmessage = (event) => {
      try {
        // Display everything as raw data - no processing at all
        const rawData = event.data;
        console.log('Received raw data:', rawData);
        
        // Try to detect if this might be a response_start to create new message container
        let shouldCreateNewMessage = false;
        try {
          const parsed = JSON.parse(rawData);
          if (parsed.type === 'response_start') {
            shouldCreateNewMessage = true;
          }
        } catch {
          // Not JSON, that's fine - just display as raw
        }
        
        // Create new message if this looks like a response start
        if (shouldCreateNewMessage && !currentStreamingMessageId) {
          const newMessageId = generateMessageId();
          setCurrentStreamingMessageId(newMessageId);
          setMessages(prev => [...prev, {
            id: newMessageId,
            type: 'assistant',
            content: rawData,
            rawContent: rawData,
            isStreaming: true,
            toolCalls: [],
            timestamp: new Date()
          }]);
        } else if (currentStreamingMessageId) {
          // Append to existing message
          setMessages(prev => prev.map(msg => 
            msg.id === currentStreamingMessageId 
              ? { 
                  ...msg, 
                  content: msg.content + '\n' + rawData,
                  rawContent: (msg.rawContent || '') + '\n' + rawData
                }
              : msg
          ));
        } else {
          // No current message, create a new one for any data
          const newMessageId = generateMessageId();
          setCurrentStreamingMessageId(newMessageId);
          setMessages(prev => [...prev, {
            id: newMessageId,
            type: 'assistant',
            content: rawData,
            rawContent: rawData,
            isStreaming: true,
            toolCalls: [],
            timestamp: new Date()
          }]);
        }
        
        // Check if this might be a response_end to stop streaming
        try {
          const parsed = JSON.parse(rawData);
          if (parsed.type === 'response_end' && currentStreamingMessageId) {
            setMessages(prev => prev.map(msg => 
              msg.id === currentStreamingMessageId 
                ? { ...msg, isStreaming: false }
                : msg
            ));
            setCurrentStreamingMessageId(null);
            setIsLoading(false);
          }
        } catch {
          // Not JSON, that's fine
        }
        
    } catch (error) {
        console.error('Error handling WebSocket message:', error);
      }
    };

    wsRef.current.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
      setCurrentStreamingMessageId(null);
    };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }, [currentStreamingMessageId]);

  const generateMessageId = () => {
    return Date.now().toString() + Math.random().toString(36).substr(2, 9);
  };

  const sendMessage = () => {
    if (!inputValue.trim() || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      return;
    }

    const userMessage: Message = {
      id: generateMessageId(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    wsRef.current.send(JSON.stringify({
      type: 'message',
      content: inputValue,
      timestamp: new Date().toISOString(),
      message_id: `user-${Date.now()}`
    }));

    setInputValue('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  useEffect(() => {
    connectWebSocket();
    return () => {
      wsRef.current?.close();
    };
  }, [connectWebSocket]);

  const renderToolCall = (toolCall: ToolCall) => (
    <div key={toolCall.name} className="bg-blue-50 border border-blue-200 rounded-lg p-3 mt-2">
      <div className="flex items-center justify-between">
        <span className="font-medium text-blue-800">🔧 {toolCall.name}</span>
        <span className={`px-2 py-1 rounded text-xs ${
          toolCall.status === 'completed' ? 'bg-green-100 text-green-800' :
          toolCall.status === 'error' ? 'bg-red-100 text-red-800' :
          'bg-yellow-100 text-yellow-800'
        }`}>
          {toolCall.status}
        </span>
      </div>
      {toolCall.parameters && (
        <div className="mt-2 text-sm text-gray-600">
          <strong>Parameters:</strong> {JSON.stringify(toolCall.parameters, null, 2)}
        </div>
      )}
      {toolCall.result && (
        <div className="mt-2 text-sm text-gray-700">
          <strong>Result:</strong> {JSON.stringify(toolCall.result, null, 2)}
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Chat Section */}
      <div className="w-1/2 flex flex-col">
        {/* Header */}
        <div className="bg-white shadow-sm border-b p-4">
          <h1 className="text-2xl font-bold text-gray-800">AI Principal Chat</h1>
          <div className="flex items-center mt-2">
            <div className={`w-3 h-3 rounded-full mr-2 ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
            <span className="text-sm text-gray-600">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-3xl px-4 py-2 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white text-gray-800 shadow-sm border'
                }`}
              >
                <div className="flex items-start space-x-2">
                  {message.type === 'assistant' && <Bot className="w-5 h-5 mt-1 text-blue-500" />}
                  {message.type === 'user' && <User className="w-5 h-5 mt-1" />}
                  <div className="flex-1">
                    <div className="whitespace-pre-wrap">{message.content}</div>
                    {message.isStreaming && (
                      <div className="animate-pulse text-gray-400">●</div>
                    )}
                    {message.toolCalls && message.toolCalls.length > 0 && (
                      <div className="mt-2">
                        {message.toolCalls.map(renderToolCall)}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="bg-white border-t p-4">
          <div className="flex space-x-2">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask the AI Principal anything..."
              className="flex-1 resize-none border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              disabled={!isConnected || isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={!isConnected || isLoading || !inputValue.trim()}
              className="bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
              aria-label="Send message"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Course Blackboard Section */}
      <div className="w-1/2 bg-slate-900 text-white flex flex-col">
        {/* Blackboard Header */}
        <div className="bg-slate-800 p-4 border-b border-slate-700">
          <h2 className="text-2xl font-bold text-white flex items-center">
            <Bookmark className="w-6 h-6 mr-2" />
            Course Blackboard
          </h2>
          <p className="text-slate-300 text-sm mt-1">
            {courses.length} courses available
          </p>
        </div>

        {/* Courses Display */}
        <div className="flex-1 overflow-y-auto p-6">
          {courses.length === 0 ? (
            <div className="text-center text-slate-400 mt-20">
              <Bookmark className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p className="text-lg">No courses yet</p>
              <p className="text-sm">Ask the AI Principal to create or find courses for you!</p>
            </div>
          ) : (
            <div className="space-y-6">
              {courses.map((course) => (
                <div
                  key={course.id}
                  className="bg-slate-800 border border-slate-600 rounded-lg p-6 shadow-lg hover:bg-slate-700 transition-colors"
                >
                  <h3 className="font-bold text-xl text-white mb-3 border-b border-slate-600 pb-2">
                    {course.title}
                  </h3>
                  <p className="text-slate-300 mb-4 leading-relaxed">
                    {course.description}
                  </p>
                  <div className="grid grid-cols-1 gap-2 text-sm">
                    <div className="flex items-center">
                      <span className="text-slate-400 w-20">Grade:</span>
                      <span className="text-white font-medium">{course.grade_level}</span>
                    </div>
                    <div className="flex items-center">
                      <span className="text-slate-400 w-20">Duration:</span>
                      <span className="text-white font-medium">{course.duration}</span>
                    </div>
                    <div className="flex items-center">
                      <span className="text-slate-400 w-20">Format:</span>
                      <span className="text-white font-medium">{course.format}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CourseInteractionPage;
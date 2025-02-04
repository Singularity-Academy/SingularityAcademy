import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ChakraProvider, CSSReset } from '@chakra-ui/react';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import HomePage from './pages/HomePage';
import theme from './theme';
import PersonalHomePage from './pages/PersonalHomePage';
import LearningPage from './pages/LearningPage';
import CourseInteractionPage from './pages/course/CourseInteractionPage';
import VerifyPage from './pages/auth/VerifyPage';
import { useTranslation } from 'react-i18next';
import Footer from './components/Footer';

const App: React.FC = () => {
  const { i18n } = useTranslation();

  return (
    <ChakraProvider theme={theme}>
      <CSSReset />
      <div 
        dir={i18n.language === 'ar' ? 'rtl' : 'ltr'}
        style={{
          fontFamily: i18n.language === 'ar' ? "'Noto Sans Arabic', sans-serif" : "inherit",
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        <Router>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path='/homepage' element={<PersonalHomePage />} />
            <Route path='/me/homepage' element={<LearningPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
            <Route path="/course/interaction" element={<CourseInteractionPage />} />
            <Route path="/auth/verify" element={<VerifyPage />} />
          </Routes>
          <Footer />
        </Router>
      </div>
    </ChakraProvider>
  );
};

export default App; 
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import {Box, ChakraProvider, CSSReset} from '@chakra-ui/react';
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';
import HomePage from './pages/HomePage';
import theme from './theme';
import PersonalHomePage from './pages/PersonalHomePage';
import LearningPage from './pages/LearningPage';
import CourseInteractionPage from './pages/course/CourseInteractionPage';
import VerifyPage from './pages/auth/VerifyPage';
import BecomeAMentorPage from './pages/BecomeAMentorPage';
import PartnerWithUsPage from './pages/PartnerWithUsPage';
import SupportMissionPage from './pages/SupportMissionPage';
import SignupPage from './pages/SignupPage';
import { useTranslation } from 'react-i18next';
import Footer from './components/Footer';
import PrincipalAIPage from './pages/PrincipalAIPage';
import Navbar from "@components/Navbar";
import PrivateRoute from './components/PrivateRoute';

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
          <Navbar />
            <Box mt={16}>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/auth/verify" element={<VerifyPage />} />
                <Route path="/signup" element={<SignupPage />} />
                <Route path="/become-mentor" element={<BecomeAMentorPage />} />
                <Route path="/partner-with-us" element={<PartnerWithUsPage />} />
                <Route path="/support-mission" element={<SupportMissionPage />} />
                
                {/* Protected Routes */}
                <Route element={<PrivateRoute />}>
                  <Route path='/homepage' element={<PersonalHomePage />} />
                  <Route path='/me/homepage' element={<LearningPage />} />
                  <Route path="/course/interaction" element={<CourseInteractionPage />} />
                  <Route path="/principal-ai" element={<PrincipalAIPage />} />
                </Route>
                
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </Box>
          <Footer />
        </Router>
      </div>
    </ChakraProvider>
  );
};

export default App;
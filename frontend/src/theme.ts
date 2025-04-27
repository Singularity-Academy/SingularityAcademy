import { extendTheme, type ThemeConfig } from '@chakra-ui/react';

const config: ThemeConfig = {
  initialColorMode: 'light',
  useSystemColorMode: true,
};

const theme = extendTheme({
  config,
  fonts: {
    heading: 'Inter, sans-serif',
    body: 'Inter, sans-serif',
  },
  colors: {
    brand: {
      50: '#E6F6FF',
      100: '#BAE3FF',
      200: '#7CC4FA',
      300: '#47A3F3',
      400: '#2186EB',
      500: '#0967D2',
      600: '#0552B5',
      700: '#03449E',
      800: '#01337D',
      900: '#002159',
    },
    // Claude-like colors
    background: {
      primary: '#f8f6f1',
      secondary: '#ffffff',
      dark: '#18181b',
    },
    accent: {
      coral: '#e89980',
      black: '#18181b',
    },
    text: {
      primary: '#18181b',
      secondary: '#4b5563',
      muted: '#6b7280',
    },
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: '500',
        borderRadius: 'md',
      },
      variants: {
        solid: {
          bg: 'accent.black',
          color: 'white',
          _hover: {
            bg: 'blackAlpha.800',
          },
        },
        outline: {
          borderColor: 'accent.black',
          color: 'accent.black',
        },
        brand: {
          bg: 'brand.500',
          color: 'white',
          _hover: {
            bg: 'brand.600',
          },
        },
      },
    },
    Card: {
      baseStyle: {
        container: {
          backgroundColor: 'background.secondary',
          borderRadius: 'xl',
          boxShadow: 'sm',
          overflow: 'hidden',
          transition: 'all 0.3s ease-in-out',
          _hover: {
            boxShadow: 'md',
          },
        },
      },
    },
    Heading: {
      baseStyle: {
        fontWeight: '600',
        color: 'text.primary',
      },
    },
    Text: {
      baseStyle: {
        color: 'text.primary',
      },
    },
  },
  styles: {
    global: {
      body: {
        bg: 'background.primary',
        color: 'text.primary',
      },
    },
  },
});

export default theme;
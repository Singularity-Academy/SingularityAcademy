import { extendTheme, type ThemeConfig } from '@chakra-ui/react';

const config: ThemeConfig = {
  initialColorMode: 'light',
  useSystemColorMode: true,
};

const theme = extendTheme({
  config,
  fonts: {
    heading: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    body: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
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
    // Enhanced Claude-like colors with gradients
    background: {
      primary: '#f8f6f1',
      secondary: '#ffffff',
      dark: '#18181b',
      gradient: 'linear-gradient(135deg, #f8f6f1 0%, #fefefe 100%)',
    },
    accent: {
      coral: '#e89980',
      coralLight: '#f0b5a2',
      coralDark: '#d67a5f',
      black: '#18181b',
      gradient: 'linear-gradient(135deg, #e89980 0%, #f0b5a2 100%)',
    },
    text: {
      primary: '#18181b',
      secondary: '#4b5563',
      muted: '#6b7280',
      light: '#9ca3af',
    },
    // Glass morphism colors
    glass: {
      white: 'rgba(255, 255, 255, 0.1)',
      black: 'rgba(0, 0, 0, 0.1)',
      border: 'rgba(255, 255, 255, 0.2)',
    },
  },
  shadows: {
    'soft': '0 2px 15px 0 rgba(0, 0, 0, 0.05)',
    'medium': '0 4px 20px 0 rgba(0, 0, 0, 0.08)',
    'large': '0 10px 40px 0 rgba(0, 0, 0, 0.1)',
    'xl': '0 20px 60px 0 rgba(0, 0, 0, 0.15)',
    '2xl': '0 25px 80px 0 rgba(0, 0, 0, 0.2)',
    'inner-soft': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    'coral': '0 4px 20px 0 rgba(232, 153, 128, 0.3)',
    'coral-lg': '0 10px 40px 0 rgba(232, 153, 128, 0.4)',
  },
  radii: {
    none: '0',
    sm: '0.125rem',
    base: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    '2xl': '1rem',
    '3xl': '1.5rem',
    full: '9999px',
  },
  transitions: {
    property: {
      common: 'background-color, border-color, color, fill, stroke, opacity, box-shadow, transform',
      colors: 'background-color, border-color, color, fill, stroke',
      dimensions: 'width, height',
      position: 'left, right, top, bottom',
      background: 'background-color, background-image, background-position',
    },
    easing: {
      'ease-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
      'ease-out': 'cubic-bezier(0, 0, 0.2, 1)',
      'ease-in': 'cubic-bezier(0.4, 0, 1, 1)',
      'spring': 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
    },
    duration: {
      'ultra-fast': '50ms',
      faster: '100ms',
      fast: '150ms',
      normal: '200ms',
      slow: '300ms',
      slower: '400ms',
      'ultra-slow': '500ms',
    },
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: '500',
        borderRadius: 'xl',
        transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
        _focus: {
          boxShadow: '0 0 0 3px rgba(232, 153, 128, 0.3)',
        },
      },
      variants: {
        solid: {
          bg: 'accent.black',
          color: 'white',
          boxShadow: 'medium',
          _hover: {
            bg: 'blackAlpha.800',
            transform: 'translateY(-2px)',
            boxShadow: 'large',
            _disabled: {
              bg: 'accent.black',
              transform: 'none',
              boxShadow: 'medium',
            },
          },
          _active: {
            bg: 'blackAlpha.900',
            transform: 'translateY(0)',
            boxShadow: 'soft',
          },
        },
        outline: {
          borderColor: 'accent.black',
          color: 'accent.black',
          _hover: {
            bg: 'accent.black',
            color: 'white',
            transform: 'translateY(-2px)',
            boxShadow: 'medium',
          },
          _active: {
            bg: 'blackAlpha.900',
            color: 'white',
            transform: 'translateY(0)',
          },
        },
        ghost: {
          color: 'text.primary',
          _hover: {
            bg: 'gray.100',
            color: 'accent.coral',
          },
          _active: {
            bg: 'gray.200',
          },
        },
        brand: {
          bg: 'accent.coral',
          color: 'white',
          boxShadow: 'coral',
          _hover: {
            bg: 'accent.coralDark',
            transform: 'translateY(-2px)',
            boxShadow: 'coral-lg',
            _disabled: {
              bg: 'accent.coral',
              transform: 'none',
              boxShadow: 'coral',
            },
          },
          _active: {
            bg: 'accent.coralDark',
            transform: 'translateY(0)',
            boxShadow: 'soft',
          },
        },
        glass: {
          bg: 'glass.white',
          backdropFilter: 'blur(10px)',
          border: '1px solid',
          borderColor: 'glass.border',
          color: 'text.primary',
          _hover: {
            bg: 'glass.black',
            transform: 'translateY(-2px)',
            boxShadow: 'large',
          },
        },
      },
      sizes: {
        lg: {
          h: '56px',
          fontSize: 'lg',
          px: '32px',
        },
      },
    },
    Card: {
      baseStyle: {
        container: {
          backgroundColor: 'background.secondary',
          borderRadius: '2xl',
          boxShadow: 'medium',
          overflow: 'hidden',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          border: '1px solid',
          borderColor: 'gray.100',
          _hover: {
            boxShadow: 'xl',
            transform: 'translateY(-4px)',
          },
        },
      },
      variants: {
        elevated: {
          container: {
            boxShadow: 'xl',
            _hover: {
              boxShadow: '2xl',
            },
          },
        },
        outline: {
          container: {
            boxShadow: 'none',
            border: '2px solid',
            borderColor: 'gray.200',
          },
        },
        glass: {
          container: {
            bg: 'glass.white',
            backdropFilter: 'blur(10px)',
            border: '1px solid',
            borderColor: 'glass.border',
          },
        },
      },
    },
    Heading: {
      baseStyle: {
        fontWeight: '600',
        color: 'text.primary',
        letterSpacing: '-0.02em',
      },
      sizes: {
        '2xl': {
          fontSize: ['2xl', '3xl', '4xl'],
          lineHeight: '1.2',
        },
        xl: {
          fontSize: ['xl', '2xl', '3xl'],
          lineHeight: '1.3',
        },
      },
    },
    Text: {
      baseStyle: {
        color: 'text.primary',
        lineHeight: '1.6',
      },
      variants: {
        muted: {
          color: 'text.muted',
        },
        secondary: {
          color: 'text.secondary',
        },
      },
    },
    Input: {
      variants: {
        filled: {
          field: {
            bg: 'gray.50',
            _hover: {
              bg: 'gray.100',
            },
            _focus: {
              bg: 'white',
              borderColor: 'accent.coral',
              boxShadow: '0 0 0 1px var(--chakra-colors-accent-coral)',
            },
          },
        },
        outline: {
          field: {
            borderColor: 'gray.300',
            _hover: {
              borderColor: 'gray.400',
            },
            _focus: {
              borderColor: 'accent.coral',
              boxShadow: '0 0 0 1px var(--chakra-colors-accent-coral)',
            },
          },
        },
      },
    },
    Menu: {
      baseStyle: {
        list: {
          borderRadius: 'xl',
          boxShadow: 'xl',
          border: 'none',
          py: '2',
          bg: 'white',
          overflow: 'hidden',
        },
        item: {
          py: '3',
          px: '4',
          transition: 'all 0.2s',
          _hover: {
            bg: 'gray.50',
          },
          _focus: {
            bg: 'gray.50',
          },
        },
        divider: {
          my: '2',
          borderColor: 'gray.200',
        },
      },
    },
    Divider: {
      baseStyle: {
        borderColor: 'gray.200',
        opacity: 0.6,
      },
      variants: {
        gradient: {
          borderImage: 'linear-gradient(to right, transparent, var(--chakra-colors-gray-300), transparent) 1',
        },
      },
    },
  },
  styles: {
    global: (props: any) => ({
      'html, body': {
        bg: props.colorMode === 'dark' ? 'background.dark' : 'background.primary',
        color: props.colorMode === 'dark' ? 'white' : 'text.primary',
        lineHeight: 'base',
        scrollBehavior: 'smooth',
      },
      '*::selection': {
        bg: 'accent.coral',
        color: 'white',
      },
      '*::-webkit-scrollbar': {
        width: '8px',
        height: '8px',
      },
      '*::-webkit-scrollbar-track': {
        bg: 'gray.100',
      },
      '*::-webkit-scrollbar-thumb': {
        bg: 'gray.400',
        borderRadius: 'full',
        _hover: {
          bg: 'gray.500',
        },
      },
      // Smooth transitions for color mode
      'body, .chakra-ui-light, .chakra-ui-dark': {
        transition: 'background-color 0.2s ease-in-out, color 0.2s ease-in-out',
      },
    }),
  },
  semanticTokens: {
    colors: {
      'chakra-body-text': { _light: 'text.primary', _dark: 'white' },
      'chakra-body-bg': { _light: 'background.primary', _dark: 'background.dark' },
      'chakra-border-color': { _light: 'gray.200', _dark: 'gray.700' },
      'chakra-placeholder-color': { _light: 'gray.500', _dark: 'gray.400' },
    },
  },
});

export default theme;
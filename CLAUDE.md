# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Singularity Academy is a full-stack AI-powered educational platform combining modern web technologies with advanced AI capabilities. The project consists of three main components:

- **Frontend**: Nuxt 4 (Vue 3) application with Naive UI and TailwindCSS
- **Backend**: Go/Gin REST API with MySQL database  
- **AI Engine**: Python/Sanic service with LangChain for AI tutoring and Manim for video generation

## Development Commands

### Frontend (Nuxt 4)
```bash
cd frontend
yarn install          # Install dependencies
yarn dev              # Start development server (port 3000)
yarn build            # Build for production
yarn generate         # Generate static site
yarn preview          # Preview production build
```

### Backend (Go)
```bash
cd backend
go mod download       # Download dependencies
go run .              # Start development server (port 8080)
go build -o main .    # Build binary
go test ./...         # Run tests
```

### AI Engine (Python)
```bash
cd .                  # Run from project root
pip install -r requirements.txt  # Install dependencies
python run.py         # Start AI engine (port 8001)
python run.py --log-level TRACE  # Start with verbose logging
```

### Full Stack Development
```bash
./scripts/start.sh    # Start all services (frontend, backend, AI engine, Caddy)
```

## Architecture Overview

### Frontend Architecture
- **Framework**: Nuxt 4 with Vue 3 Composition API
- **UI Library**: Naive UI components with auto-import
- **Styling**: TailwindCSS 4.x with SCSS support
- **State Management**: Pinia with persistence
- **Internationalization**: @nuxtjs/i18n with 7 languages (zh, en, es, fr, de, ja, ar)
- **Icons**: Lucide icons with auto-import
- **Type Safety**: TypeScript with auto-generated types

### Backend Architecture
- **Framework**: Gin (Go web framework)
- **Database**: MySQL with GORM ORM
- **Authentication**: JWT tokens with middleware
- **CORS**: Configured for cross-origin requests
- **WebSocket**: Gorilla WebSocket for real-time communication
- **Configuration**: Viper for config management

### AI Engine Architecture
- **Framework**: Sanic (async Python web framework)
- **AI/ML**: LangChain for LLM orchestration, OpenAI API integration
- **Video Generation**: Manim for mathematical animations
- **Database**: Tortoise ORM for async database operations
- **File Handling**: Support for PDF, DOCX, PPTX, CSV document processing

## Key Directories

```
frontend/
├── app/
│   ├── components/     # Vue components
│   ├── pages/         # Page routes
│   ├── stores/        # Pinia stores
│   ├── locales/       # i18n translations
│   └── types/         # TypeScript definitions
├── nuxt.config.ts     # Nuxt configuration
└── package.json

backend/
├── auth/              # Authentication logic
├── controllers/       # Request handlers
├── models/            # Database models
├── middlewares/       # HTTP middlewares
├── config/            # Database and SMTP config
└── main.go           # Application entry point

ai_engine/
├── apps/             # AI application modules
│   ├── ai/          # Core AI logic
│   ├── course/      # Course management
│   ├── principal/   # AI principal agent
│   └── Manim/       # Video generation
├── config/          # Configuration files
└── app.py          # Sanic application
```

## Database Schema

The project uses MySQL for persistent storage with the following models:
- **User**: Authentication and profile information
- Course and material relationships are handled through the AI engine

## API Endpoints

### Backend (Port 8080)
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login  
- `POST /api/auth/verify` - Email verification
- `GET /api/me` - Get current user info (requires JWT)
- `POST /api/courses/materials` - Upload course materials (requires JWT)
- `GET /api/ws/stream` - WebSocket connection for real-time features

### AI Engine (Port 8001)
- WebSocket endpoints for AI tutoring at `/ai/dean_ai/{token}`
- Manim video generation endpoints
- Document processing and analysis

## Development Workflow

1. **Environment Setup**: Ensure Node.js 18+, Go 1.23+, Python 3.11+, and MySQL 8.0+ are installed
2. **Database**: Create MySQL database and configure connection in backend config
3. **Dependencies**: Run installation commands for each service
4. **Development**: Use `./scripts/start.sh` for full-stack development or start services individually
5. **Testing**: Each service has its own test suite - run them in their respective directories

## Configuration

- **Frontend**: Configuration in `nuxt.config.ts`
- **Backend**: Environment variables and config files in `backend/config/`
- **AI Engine**: JSON configuration files in `ai_engine/config/`
- **Proxy**: Caddy configuration in `Caddyfile` for reverse proxy setup

## Branch Strategy

- `main`: Production-ready code
- `feat/*`: Feature development branches (current: `feat/nuxt-migration`)
- Use conventional commits for clear history

## Notes

- The project is currently migrating to Nuxt 4, with the frontend being modernized
- AI engine includes sophisticated video generation using Manim for educational content
- Multi-language support is built-in with comprehensive i18n setup
- WebSocket integration enables real-time AI tutoring experiences
- Caddy handles HTTPS and reverse proxy in production deployments
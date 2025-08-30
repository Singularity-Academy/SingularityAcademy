# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Frontend (React/TypeScript)
```bash
cd frontend
npm install          # Install dependencies
npm start            # Start dev server (http://localhost:3000)
npm run build        # Build for production
npm test             # Run tests
npm test -- --coverage  # Run tests with coverage report
```

### Backend (Go/Gin)
```bash
cd backend
go mod download      # Download dependencies
go run main.go       # Start backend server (http://localhost:8080)
go run . migrate     # Run database migrations
go test ./...        # Run all tests
go test ./... -v     # Run tests with verbose output
go test -coverprofile=coverage.out ./...  # Run tests with coverage
go tool cover -html=coverage.out          # Generate coverage HTML report
go build -o main .   # Build for production
```

### AI Engine (Python/Sanic)
```bash
# From project root
pip install -r requirements.txt    # Install dependencies
python run.py                      # Start AI engine (http://localhost:8000)
python run.py --log-level TRACE    # Start with verbose logging
python run.py --host 0.0.0.0 --port 8001  # Custom host/port
pytest tests/ -v                   # Run tests (if pytest is installed)
pytest tests/ --cov=apps --cov-report=html  # Run tests with coverage
```

### Full Application
```bash
./scripts/start.sh   # Start all services (requires bash)
# Application accessible at http://localhost:1298 via Caddy proxy

# Docker deployment
docker-compose up -d  # Start all services with Docker
docker-compose down   # Stop all Docker services
docker-compose logs -f  # View logs from all services

# Manual Caddy server management
caddy start          # Start Caddy server
caddy stop           # Stop Caddy server
caddy reload         # Reload Caddyfile configuration
```

## Architecture Overview

This is a microservices-based AI education platform with:

- **Frontend**: React 18 + TypeScript + Chakra UI + i18next (multilingual)
- **Backend**: Go 1.23 + Gin + GORM + MySQL/SQLite + JWT auth
- **AI Engine**: Python 3.11 + Sanic + LangChain + OpenAI integration
- **Proxy**: Caddy server for routing and HTTPS
- **Database**: MySQL (production) / SQLite (development)

### Service Communication
- Frontend (port 3000) ↔ Caddy (port 1298) ↔ Backend (port 8080)
- Frontend ↔ Caddy ↔ AI Engine (port 8000)
- WebSocket connections for real-time AI chat at `/ai/*` endpoints
- Cross-service authentication via JWT tokens
- Caddy handles CORS and WebSocket upgrades automatically

### Key Directories
```
├── frontend/src/          # React components, pages, utils
│   ├── pages/            # Main application pages
│   ├── components/       # Reusable UI components  
│   └── locales/          # i18n translation files
├── backend/              # Go backend service
│   ├── controllers/      # HTTP route handlers
│   ├── models/          # Database models (GORM)
│   ├── middlewares/     # Auth, CORS, validation middleware
│   └── config/          # Database and SMTP configuration
├── ai_engine/            # Python AI service
│   ├── apps/            # AI modules (chat, video generation)
│   └── config/          # AI service configuration
└── scripts/             # Deployment and utility scripts
```

## Development Notes

### Database Configuration
- Backend uses GORM for ORM with auto-migration
- MySQL connection configured in `backend/config/config.yml`
- SQLite fallback for local development
- User model with JWT-based authentication

### AI Engine Features
- LangChain integration for conversational AI
- Manim integration for educational video generation  
- WebSocket support for real-time chat
- Multi-modal content generation (text, video, animations)
- Document processing (PDF, DOCX, PPTX, CSV support)
- Video rendering with configurable quality (720p30, 1080p60)
- Async request handling with Sanic framework

### Frontend Features
- Multi-language support (7 languages including Chinese, English, Japanese)
- Responsive design with Chakra UI
- Socket.io client for WebSocket connections
- React Router for SPA navigation
- Zustand for state management
- React Hook Form for form validation
- File upload with drag-and-drop (react-dropzone)
- Particle background effects (tsparticles)

### Authentication Flow
1. User registers/logs in via backend API
2. Backend issues JWT token
3. Frontend stores token for API requests
4. AI Engine validates tokens for WebSocket connections

### Testing
- Frontend: Jest + React Testing Library (react-app-rewired)
- Backend: Go's built-in testing package with coverage reports
- AI Engine: pytest with async support and coverage reports
- Integration tests available in `/test` directory
- Test coverage HTML reports can be generated for all services

## Common Tasks

### Adding New API Endpoints
1. Define route in `backend/main.go`
2. Create handler in appropriate controller
3. Add middleware for auth/validation as needed
4. Update frontend API client calls

### Adding New AI Features
1. Create new module in `ai_engine/apps/`
2. Register module in `ai_engine/registry.py`
3. Configure prompts in `ai_engine/apps/ai/prompts/`
4. Update frontend to consume new WebSocket events

### Database Changes
1. Modify models in `backend/models/`
2. Run `go run main.go migrate` for auto-migration
3. Update any affected API responses

### Internationalization
1. Add new keys to translation files in `frontend/src/locales/`
2. Use `useTranslation` hook in React components
3. Language switching handled by i18next browser detection
4. Supported languages: en, zh, es, fr, de, ja, ar

### Working with Manim Video Generation
1. Video generation requests go through AI Engine WebSocket
2. Generated videos stored in `ai_engine/apps/Manim/ai_generated_videos/`
3. Videos rendered at configurable quality (720p30, 1080p60)
4. Manim scripts are auto-generated by LangChain integration
5. Use `ai_engine/apps/Manim/client.py` for testing video generation

### Environment Configuration
- Backend config: `backend/config/config.yml`
- AI Engine config: `ai_engine/config/config.json`
- Frontend uses environment variables for API endpoints
- Database can be MySQL (production) or SQLite (development)
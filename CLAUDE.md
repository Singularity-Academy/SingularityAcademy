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
```

### Backend (Go/Gin)
```bash
cd backend
go mod download      # Download dependencies
go run main.go       # Start backend server (http://localhost:8080)
go run . migrate     # Run database migrations
go test ./...        # Run tests
go build -o main .   # Build for production
```

### AI Engine (Python/Sanic)
```bash
# From project root
pip install -r requirements.txt    # Install dependencies
python run.py                      # Start AI engine (http://localhost:8000)
python run.py --log-level TRACE    # Start with verbose logging
```

### Full Application
```bash
./scripts/start.sh   # Start all services (requires bash)
# Application accessible at http://localhost:1298 via Caddy proxy
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
- WebSocket connections for real-time AI chat
- Cross-service authentication via JWT tokens

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

### Frontend Features
- Multi-language support (7 languages including Chinese, English, Japanese)
- Responsive design with Chakra UI
- Socket.io client for WebSocket connections
- React Router for SPA navigation
- Zustand for state management

### Authentication Flow
1. User registers/logs in via backend API
2. Backend issues JWT token
3. Frontend stores token for API requests
4. AI Engine validates tokens for WebSocket connections

### Testing
- Frontend: Jest + React Testing Library
- Backend: Go's built-in testing package
- AI Engine: pytest with async support
- Integration tests available in `/test` directory

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
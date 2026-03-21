# Project File Structure Overview

This is your project's complete file structure:

```
📁 Prompt-injection/
│
├── 📄 README.md                    # Project overview & introduction
├── 📄 SETUP_INSTRUCTIONS.md        # Detailed setup guide
├── 📄 ARCHITECTURE.md              # System design & architecture
├── 📄 ROADMAP.md                   # Future features & improvements
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 .gitignore                   # Git ignore rules
├── 📄 .env.example                 # Environment variables template
├── 📄 setup.sh                     # Quick start script
├── 📄 docker-compose.yml           # Docker configuration
│
├── 📁 frontend/                    # React frontend application
│   ├── 📄 package.json             # Node dependencies
│   ├── 📄 vite.config.js           # Vite build config
│   ├── 📄 index.html               # HTML entry point
│   ├── 📄 Dockerfile               # Docker image for frontend
│   │
│   ├── 📁 src/                     # Source code
│   │   ├── 📄 index.jsx            # React entry point
│   │   ├── 📄 App.jsx              # Root component
│   │   │
│   │   ├── 📁 pages/               # Page components
│   │   │   └── 📄 PromptAnalyzer.jsx   # Main analyzer page
│   │   │
│   │   ├── 📁 components/          # Reusable components
│   │   │   ├── 📄 PromptInput.jsx      # Input component
│   │   │   ├── 📄 AnalysisResult.jsx   # Results display
│   │   │   ├── 📄 VulnerabilityTest.jsx # Test results
│   │   │   └── 📄 FixSuggestions.jsx    # Fixes component
│   │   │
│   │   ├── 📁 services/            # API communication
│   │   │   └── 📄 api.js               # Axios API client
│   │   │
│   │   └── 📁 styles/              # CSS styling
│   │       ├── 📄 index.css            # Global styles
│   │       ├── 📄 App.css              # App styles
│   │       ├── 📄 PromptAnalyzer.css   # Analyzer styles
│   │       ├── 📄 PromptInput.css      # Input styles
│   │       ├── 📄 AnalysisResult.css   # Results styles
│   │       ├── 📄 VulnerabilityTest.css # Test styles
│   │       └── 📄 FixSuggestions.css    # Fixes styles
│   │
│   └── 📁 public/                  # Static assets
│
├── 📁 backend/                     # Python FastAPI backend
│   ├── 📄 main.py                  # FastAPI entry point
│   ├── 📄 requirements.txt          # Python dependencies
│   ├── 📄 Dockerfile               # Docker image for backend
│   │
│   ├── 📁 config/                  # Configuration
│   │   ├── 📄 __init__.py           # Package init
│   │   ├── 📄 settings.py           # App settings
│   │   └── 📄 logging.py            # Logging config
│   │
│   ├── 📁 api/                     # API routes
│   │   ├── 📄 __init__.py           # Package init
│   │   └── 📄 routes.py             # API endpoints
│   │
│   ├── 📁 services/                # Business logic
│   │   ├── 📄 __init__.py           # Package init
│   │   ├── 📄 model_service.py      # ML model handling
│   │   └── 📄 gemini_service.py     # Gemini API integration
│   │
│   ├── 📁 utils/                   # Utility functions
│   │   ├── 📄 __init__.py           # Package init
│   │   └── 📄 validators.py         # Input validation
│   │
│   └── 📁 tests/                   # Unit tests
│       └── 📄 README.md             # Test documentation
│
└── 📁 models/                      # ML models & data
    ├── 📄 README.md                # Model documentation
    │
    ├── 📁 trained_model/           # Serialized models
    │   ├── 📄 model.pkl             # Main ML model
    │   └── 📄 config.json           # Model config
    │
    └── 📁 preprocessing/           # Data preprocessing
        ├── 📄 preprocessor.pkl      # Feature transformer
        └── 📄 preprocess.py         # Preprocessing functions
```

## Directory Descriptions

### Root Level
- **Documentation**: README, SETUP, ARCHITECTURE, ROADMAP
- **Configuration**: .env, .gitignore, docker-compose.yml
- **Scripts**: setup.sh for quick setup

### Frontend (`/frontend`)
- **React application** for user interface
- **Components**: Reusable React components for each feature
- **Pages**: Main application pages/flows
- **Services**: API client for backend communication
- **Styles**: CSS3 styling for all components
- **Build artifacts**: dist/, node_modules/ (in .gitignore)

### Backend (`/backend`)
- **API Routes**: FastAPI endpoints for requests
- **Services**: Business logic and external integrations
- **Configuration**: Settings and logging setup
- **Utils**: Helper functions and validators
- **Tests**: Unit tests for services and API

### Models (`/models`)
- **Trained Model**: Your pre-trained ML model binary
- **Preprocessor**: Feature vectorizer/transformer
- **Documentation**: How to prepare models

## Key Files to Know

| File | Purpose |
|------|---------|
| `/backend/main.py` | FastAPI application entry point |
| `/frontend/src/index.jsx` | React application entry point |
| `/backend/services/model_service.py` | ML model inference |
| `/backend/services/gemini_service.py` | Gemini API integration |
| `/backend/requirements.txt` | Python dependencies |
| `/frontend/package.json` | Node.js dependencies |
| `/.env.example` | Environment variable template |
| `/SETUP_INSTRUCTIONS.md` | How to get started |

## Getting Started

1. Read [README.md](README.md) for project overview
2. Follow [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) to set up
3. Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand design
4. See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

## Quick Commands

```bash
# Setup
bash setup.sh

# Backend
cd backend && source venv/bin/activate && python main.py

# Frontend
cd frontend && npm run dev

# Build
cd frontend && npm run build

# Docker
docker-compose up

# API Docs
http://localhost:8000/docs
```

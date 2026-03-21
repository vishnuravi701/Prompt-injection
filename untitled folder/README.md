# Prompt Injection Prevention & Education Website

A web-based educational platform that helps users understand and defend against prompt injection attacks. Users can test prompts using our trained ML model, receive real-time testing via Gemini API, and get actionable fixes and recommendations.

## Project Structure

```
├── frontend/              # React/Vue frontend application
│   ├── src/
│   │   ├── components/   # Reusable React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client services
│   │   └── styles/       # CSS/styling
│   ├── public/           # Static assets
│   └── package.json
│
├── backend/              # Python FastAPI backend
│   ├── api/              # API routes/endpoints
│   ├── services/         # Business logic
│   │   ├── model_service.py      # Model inference
│   │   ├── gemini_service.py     # Gemini API integration
│   │   └── prompt_analyzer.py    # Prompt analysis
│   ├── utils/            # Utility functions
│   ├── config/           # Configuration
│   ├── main.py           # Main FastAPI application
│   └── requirements.txt
│
├── models/               # ML model files
│   ├── trained_model/    # Serialized model files
│   └── preprocessing/    # Data preprocessing scripts
│
└── .env                  # Environment variables
```

## Key Features

1. **Prompt Detection**: ML model classifies prompts as legitimate or injection attempts
2. **Live Testing**: Gemini API testing shows real-world vulnerability
3. **Fix Suggestions**: Automated recommendations to secure prompts
4. **Education**: Step-by-step breakdowns of what went wrong
5. **Verification**: Show improved prompts working correctly

## Tech Stack

- **Frontend**: React/HTML5/CSS3/JavaScript
- **Backend**: Python FastAPI
- **ML Model**: Scikit-learn/TensorFlow/PyTorch
- **External API**: Google Gemini API
- **Database**: Optional (for history/analytics)

## Setup Instructions

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Environment Variables

See `.env` file for required configuration:
- `GEMINI_API_KEY`
- `MODEL_PATH`
- `FLASK_PORT`
- Other settings

## API Endpoints

- `POST /api/analyze` - Analyze a prompt for injection
- `POST /api/test-vulnerable` - Test prompt vulnerability with Gemini
- `POST /api/fix-prompt` - Get fix suggestions
- `GET /api/history` - User's analysis history

## License

MIT

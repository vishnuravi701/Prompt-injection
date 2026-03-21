# Architecture & Design Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│  - Prompt Input                                                 │
│  - Analysis Display                                             │
│  - Vulnerability Test Results                                  │
│  - Fix Suggestions & Improved Prompt                           │
└────────────┬────────────────────────────────────────────────────┘
             │ HTTP/REST API
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI + Python)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ API Routes   │  │   Services   │  │  Utilities   │          │
│  │              │  │              │  │              │          │
│  │ /api/analyze │─▶│ Model Svc    │  │ Validators   │          │
│  │ /api/test    │─▶│ Gemini Svc   │  │ Logging      │          │
│  │ /api/fix     │─▶│              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────┬────────────────────────────────────┬────────────────┘
             │                                    │
             ▼                                    ▼
    ┌─────────────────┐            ┌─────────────────────┐
    │  Trained Model  │            │  Gemini API         │
    │  (Local ML)     │            │  (google-generativeai)
    └─────────────────┘            └─────────────────────┘
```

## Data Flow

### 1. Prompt Analysis Flow
```
User Input → Frontend → POST /api/analyze → Model Service
                            ▼
                    Preprocessing Layer
                            ▼
                    ML Model Prediction
                            ▼
                    Risk Score + Confidence
                            ▼
                    Frontend Display
```

### 2. Vulnerability Test Flow
```
Detected Injection → Frontend → POST /api/test-vulnerable
                                   ▼
                            Gemini Service
                                   ▼
                            Send Prompt to Gemini
                                   ▼
                            Analyze Response
                                   ▼
                            Return Results
                                   ▼
                            Frontend Display
```

### 3. Fix Suggestion Flow
```
Vulnerable Prompt → Frontend → POST /api/fix-prompt
                                   ▼
                            Gemini Service
                                   ▼
                            Generate Fixes
                                   ▼
                            Improved Prompt
                                   ▼
                     Parse & Return Fixes
                                   ▼
                            Frontend Display
                                   ▼
                        Optional: Test Improved
```

## Component Responsibilities

### Frontend Components
- **PromptInput**: Accepts user input and example prompts
- **AnalysisResult**: Displays ML model analysis with risk visualization
- **VulnerabilityTest**: Shows Gemini API test results
- **FixSuggestions**: Presents fixes and improved prompts

### Backend Services
- **ModelService**: Loads ML model, handles predictions, manages model state
- **GeminiService**: Integrates with Gemini API, tests vulnerabilities, generates fixes
- **API Routes**: Express endpoints, handle validation, orchestrate services

### Supporting Files
- **validators.py**: Input validation and sanitization
- **settings.py**: Configuration management
- **logger**: Application logging

## Key APIs

### POST /api/analyze
Analyzes prompt for injection patterns.
```json
Request: { "prompt": "user input" }
Response: {
  "is_injection": boolean,
  "confidence": float,
  "risk_score": float,
  "explanation": string
}
```

### POST /api/test-vulnerable
Tests prompt with Gemini API.
```json
Request: {
  "prompt": "vulnerable prompt",
  "system_instruction": "optional"
}
Response: {
  "success": boolean,
  "response": string,
  "vulnerability_detected": boolean,
  "analysis": string
}
```

### POST /api/fix-prompt
Gets fixes for vulnerable prompt.
```json
Request: { "prompt": "vulnerable prompt" }
Response: {
  "success": boolean,
  "fixes": [string],
  "improved_prompt": string,
  "explanation": string
}
```

## Technology Choices

| Component | Technology | Reason |
|-----------|-----------|--------|
| Frontend Framework | React | Fast, component-based, great ecosystem |
| Build Tool | Vite | Fast development, modern tooling |
| Backend Framework | FastAPI | High performance, async support, auto docs |
| ML Model | sklearn/PyTorch | Flexibility, easy to integrate |
| External API | Gemini | Powerful model, good for testing |
| Styling | CSS3 | Simple, fast, responsive |
| API Communication | Axios | Simple HTTP client |

## Scalability Considerations

### Current Design (Development)
- Single backend server
- Local model loading
- Direct Gemini API calls
- In-memory request handling

### Future Improvements
- Model caching layer
- Request queuing (Celery/RabbitMQ)
- Database for history/analytics
- Load balancing
- Model versioning
- API rate limiting
- Caching for repeated prompts

## Security Considerations

1. **API Key Management**
   - Store in environment variables
   - Never expose in frontend code
   - Use .env files (not in git)

2. **Input Validation**
   - Sanitize all user inputs
   - Rate limiting on endpoints
   - Request size limits

3. **CORS Configuration**
   - Whitelist frontend origins
   - Only allow necessary methods

4. **Error Handling**
   - Don't expose internal error details
   - Log errors securely
   - Return user-friendly messages

## Deployment Architecture

### Local Development
```
User Machine
├── Frontend (npm run dev) → port 3000
└── Backend (python main.py) → port 8000
```

### Docker Compose
```
Docker Host
├── Backend Container → port 8000
├── Frontend Container → port 3000
└── Volumes → models
```

### Production (Azure/Cloud)
```
Load Balancer
├── Frontend (Static Site Hosting)
└── Backend (App Service/Container)
    └── Models (Blob Storage/Mounted)
```

## Configuration Management

Environment variables control:
- Model paths
- API keys
- Port numbers
- CORS origins
- Logging levels

See `.env.example` for all variables.

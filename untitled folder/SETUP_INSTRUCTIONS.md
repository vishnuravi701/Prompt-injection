# Setup Instructions

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Git

## Backend Setup

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create and activate virtual environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
# Copy the example and update with your settings
cp ../.env.example ../.env

# Edit .env and add:
# - Your Gemini API key
# - Path to your trained model
# - Other configuration
```

### 5. Run backend server
```bash
python main.py
```

Backend will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

## Frontend Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Configure environment variables
Create a `.env` file:
```
REACT_APP_API_URL=http://localhost:8000
```

### 4. Run development server
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Model Setup

### 1. Prepare your trained model
- Place your trained model in `models/trained_model/model.pkl`
- Place your preprocessor in `models/preprocessing/preprocessor.pkl`

### 2. Update model path in `.env`
```
MODEL_PATH=./models/trained_model/model.pkl
PREPROCESSOR_PATH=./models/preprocessing/preprocessor.pkl
```

## Running the Full Application

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
python main.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

### Terminal 3 (Optional) - Monitor logs
```bash
tail -f logs/backend.log
```

## Verification

1. **Backend Health Check**
   ```bash
   curl http://localhost:8000/health
   ```

2. **API Documentation**
   Open `http://localhost:8000/docs` in browser

3. **Frontend**
   Open `http://localhost:3000` in browser

## Troubleshooting

### "Module not found" errors
- Ensure virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Gemini API errors
- Verify `GEMINI_API_KEY` is set in `.env`
- Check API key is valid in Google Cloud Console
- Ensure API is enabled for your project

### Model not loading
- Verify paths in `.env` are correct
- Check model files exist and are readable
- Check model format matches expected type (pickle, h5, pt)

### Port conflicts
- Change `BACKEND_PORT` or `FRONTEND_PORT` in `.env`
- Or kill existing processes: `lsof -ti:8000 -ti:3000 | xargs kill -9`

### CORS errors
- Add frontend URL to `CORS_ORIGINS` in `.env`
- Restart backend server

## Production Deployment

See deployment documentation in `DEPLOYMENT.md` for:
- Docker containerization
- Azure deployment
- Environment configuration
- Security best practices

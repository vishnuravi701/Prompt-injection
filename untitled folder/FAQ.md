# Frequently Asked Questions

## Setup & Installation

**Q: I get "ModuleNotFoundError" when running the backend**
A: Make sure your virtual environment is activated:
```bash
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

**Q: Node modules are missing**
A: Install them with:
```bash
cd frontend
npm install
```

**Q: Model files are not found**
A: Check that your model paths in `.env` are correct and files exist:
```bash
ls -la models/trained_model/
ls -la models/preprocessing/
```

## API & Integration

**Q: How do I get a Gemini API key?**
A: 
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

**Q: What model format do you support?**
A: We primarily use pickle (.pkl) format for scikit-learn models. You can also use:
- TensorFlow/Keras (.h5)
- PyTorch (.pt/.pth)

**Q: Can I use a different LLM instead of Gemini?**
A: Yes! Modify `backend/services/gemini_service.py` to use OpenAI, Anthropic, or other APIs.

**Q: The CORS errors - what should I do?**
A: Update `CORS_ORIGINS` in `.env` to include your frontend URL:
```
CORS_ORIGINS=http://localhost:3000,http://example.com
```

## Frontend Issues

**Q: Styling looks broken**
A: Make sure CSS files are imported in the components. Check browser console for errors.

**Q: API calls are failing**
A: Check that:
1. Backend is running (`python main.py`)
2. `REACT_APP_API_URL` is correct in `.env`
3. API endpoints match between frontend and backend

**Q: The page is blank after loading**
A: Check browser console (F12) for JavaScript errors.

## Backend Issues

**Q: Model predictions are always returning the same value**
A: Your model might not be trained well or needs preprocessing. Verify:
1. Model file is correct
2. Preprocessor is properly configured
3. Input format matches training data

**Q: Gemini API returns errors**
A: Check:
1. API key is valid
2. API is enabled in Google Cloud Console
3. You have quota available
4. Internet connection is working

## Deployment Questions

**Q: Can I deploy to Azure?**
A: Yes! See deployment documentation or use Azure Container Instances/App Service.

**Q: How do I scale this?**
A: For production:
1. Use a database for history
2. Add caching layer (Redis)
3. Use load balancer
4. Containerize and orchestrate with Kubernetes

**Q: What about security?**
A: Review [ARCHITECTURE.md](ARCHITECTURE.md) security section. Key points:
1. Never commit `.env` files
2. Use environment variables for secrets
3. Validate all user input
4. Use HTTPS in production
5. Implement rate limiting

## Model & ML Questions

**Q: How accurate is the model?**
A: That depends on your training data. Test it with:
```bash
python -c "from backend.services.model_service import get_model_service; m = get_model_service(); print(m.predict('test prompt'))"
```

**Q: Can I update the model without restarting?**
A: Currently, you need to restart the backend. For production, implement model hot-reloading.

**Q: How long does analysis take?**
A: Typically < 100ms for model, 1-5s for Gemini API calls (depending on network)

## Performance

**Q: The app is slow**
A: Check:
1. Network latency (Gemini API calls)
2. Model size (consider quantization)
3. Frontend bundle size (npm run build --analyze)
4. Backend CPU/memory usage

**Q: Can I cache results?**
A: Yes! implement caching in `gemini_service.py` for repeated prompts.

## General

**Q: Can I use this commercially?**
A: Check the LICENSE file in the project root.

**Q: How do I contribute?**
A: See [CONTRIBUTING.md](CONTRIBUTING.md)

**Q: I found a bug, what should I do?**
A: Create a GitHub issue with:
1. Description
2. Steps to reproduce
3. Expected vs actual behavior
4. Environment details

**Q: Can I fork/modify this?**
A: Yes! Subject to the license. Please give credit and link back.

## Still Have Questions?

- Check [README.md](README.md)
- Review [ARCHITECTURE.md](ARCHITECTURE.md)
- Check [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)
- Open a GitHub Issue
- See inline comments in source code

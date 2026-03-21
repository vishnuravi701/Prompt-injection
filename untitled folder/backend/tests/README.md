# Testing directory for backend tests

## Test Files Structure

- `test_api.py` - API endpoint tests
- `test_model_service.py` - Model service tests
- `test_gemini_service.py` - Gemini API integration tests
- `test_validators.py` - Input validation tests

## Running Tests

```bash
cd backend
pytest
pytest -v
pytest --cov=. --cov-report=html
```

## Test Coverage

- Unit tests for each service
- Integration tests for API endpoints
- Mock external services (Gemini API)
- Validation tests

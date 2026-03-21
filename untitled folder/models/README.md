# ML Models Directory

This directory contains the machine learning models and preprocessing utilities for prompt injection detection.

## Structure

### `/trained_model/`
Place your trained ML model files here:
- `model.pkl` - The main classifier model (scikit-learn or similar)
- `model.h5` - Alternative: TensorFlow/Keras model
- `model.pt` - Alternative: PyTorch model
- `config.json` - Model configuration and metadata

### `/preprocessing/`
Data preprocessing and feature extraction:
- `preprocessor.pkl` - Vectorizer/transformer (TfidfVectorizer, CountVectorizer, etc.)
- `preprocess.py` - Preprocessing functions
- `feature_extraction.py` - Feature engineering functions

## Model Requirements

Your model should:
1. Accept a list/array of prompts as strings
2. Return binary predictions (0 = safe, 1 = injection)
3. Provide probability scores for each prediction
4. Be serialized and loadable with pickle or respective format

### Example Loading
```python
import pickle

# Load model and preprocessor
with open('trained_model/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('preprocessing/preprocessor.pkl', 'rb') as f:
    preprocessor = pickle.load(f)

# Use
processed = preprocessor.transform(['your prompt'])
prediction = model.predict(processed)
probability = model.predict_proba(processed)
```

## Dataset

Your training dataset should include:
- Legitimate prompts (normal user inputs)
- Injection attempt prompts (prompt injection attacks)
- Clear binary labels

Common injection patterns to detect:
- Instruction overrides ("Ignore previous instructions...")
- Jailbreak attempts ("You are now in dev mode...")
- System prompt extraction ("What is your system prompt?")
- Role manipulation ("Pretend you are...")
- Context switching ("Ignore all above and...")

## Model Performance

Aim for:
- Balanced accuracy across both classes
- High precision (minimize false positives)
- Good recall (catch actual injections)
- Consider precision-recall trade-off based on use case

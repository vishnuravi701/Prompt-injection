"""
Model Service - Handles ML model inference for prompt injection detection
"""

import os
import pickle
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    logger.warning("transformers or torch not installed")
    TRANSFORMERS_AVAILABLE = False


class ModelService:
    """Service for loading and running the ML model"""
    
    def __init__(self, model_path: str = None, preprocessor_path: str = None):
        """Initialize model service"""
        self.model_path = model_path or os.getenv("MODEL_PATH", "./models/trained_model")
        ##self.preprocessor_path = preprocessor_path or os.getenv("PREPROCESSOR_PATH", "./models/preprocessing/preprocessor.pkl")
        
        self.model = None
        self.preprocessor = None
        self.load_model()
    
    def load_model(self):
        try:
            if not TRANSFORMERS_AVAILABLE:
                logger.warning("transformers/torch not available, using heuristic fallback")
                return

            if os.path.exists(self.model_path):
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
                self.model.eval()
                logger.info(f"Model loaded from {self.model_path}")
            else:
                logger.warning(f"Model path not found at {self.model_path}, using heuristic fallback")

        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self.model = None
            self.tokenizer = None
    
    def predict(self, prompt: str) -> dict:
        try:
            # always run heuristic pre-check first
            heuristic = self._heuristic_prediction(prompt)
            if heuristic.get("is_injection", False):
                return heuristic

            if self.model is None or self.tokenizer is None:
                return self._heuristic_prediction(prompt)

            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )

            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=-1)

            # label 1 = injection, label 0 = safe
            injection_prob = float(probabilities[0][1])
            is_injection = injection_prob > 0.5
            confidence = injection_prob if is_injection else float(probabilities[0][0])

            return {
                "is_injection": is_injection,
                "confidence": confidence,
                "risk_score": round(injection_prob * 100, 1),
                "explanation": self._generate_explanation(is_injection, confidence),
                "model_status": "loaded",
                "attack_type": "prompt_injection" if is_injection else "safe"
            }

        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return self._heuristic_prediction(prompt)
    
    def _generate_explanation(self, is_injection: bool, confidence: float) -> str:
        """Generate explanation for the prediction"""
        if is_injection:
            return f"High likelihood of prompt injection detected (confidence: {confidence:.1%})"
        else:
            return f"Prompt appears to be legitimate (confidence: {(1-confidence):.1%})"

    def _heuristic_prediction(self, prompt: str) -> dict:
        lower = prompt.lower()
        attack_keywords = {
            "jailbreak": "jailbreak",
        }

        for phrase, label in attack_keywords.items():
            if phrase in lower:
                return {
                    "is_injection": True,
                    "confidence": 0.99,
                    "risk_score": 99.0,
                    "explanation": f"Heuristic detected injection pattern: '{phrase}'",
                    "model_status": "heuristic_fallback",
                    "attack_type": label
                }

        return {
            "is_injection": False,
            "confidence": 0.05,
            "risk_score": 0.0,
            "explanation": "No known injection heuristics matched.",
            "model_status": "heuristic_fallback",
            "attack_type": "safe"
        }


# Global instance
model_service = None

def get_model_service() -> ModelService:
    global model_service
    if model_service is None:
        model_service = ModelService()
    return model_service

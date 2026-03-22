"""
Model Service - Handles ML model inference for prompt injection detection
"""

import os
import pickle
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ModelService:
    """Service for loading and running the ML model"""
    
    def __init__(self, model_path: str = None, preprocessor_path: str = None):
        """Initialize model service"""
        self.model_path = model_path or os.getenv("MODEL_PATH", "./models/trained_model/model.pkl")
        self.preprocessor_path = preprocessor_path or os.getenv("PREPROCESSOR_PATH", "./models/preprocessing/preprocessor.pkl")
        
        self.model = None
        self.preprocessor = None
        self.load_model()
    
    def load_model(self):
        """Load trained model and preprocessor"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info(f"Model loaded from {self.model_path}")
            else:
                logger.warning(f"Model file not found at {self.model_path}. Using mock model.")
                self.model = None
            
            if os.path.exists(self.preprocessor_path):
                with open(self.preprocessor_path, 'rb') as f:
                    self.preprocessor = pickle.load(f)
                logger.info(f"Preprocessor loaded from {self.preprocessor_path}")
            else:
                logger.warning(f"Preprocessor file not found at {self.preprocessor_path}")
                self.preprocessor = None
                
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self.model = None
            self.preprocessor = None
    
    def predict(self, prompt: str) -> dict:
        """
        Predict if prompt is injection attempt
        
        Returns:
            dict: {
                "is_injection": bool,
                "confidence": float (0-1),
                "risk_score": float (0-100),
                "explanation": str
            }
        """
        try:
            if self.model is None:
                logger.warning("Model not loaded, using heuristic fallback for injection detection")
                return self._heuristic_prediction(prompt)
            
            # Always run heuristic pre-check for high-risk phrases in addition to loaded model
            heuristic = self._heuristic_prediction(prompt)
            if heuristic.get("is_injection", False):
                logger.info("Heuristic injection intercept triggered")
                return heuristic

            # Preprocess the prompt
            if self.preprocessor:
                processed_prompt = self.preprocessor.transform([prompt])
            else:
                # Mock preprocessing if preprocessor not available
                processed_prompt = [prompt]
            
            # Get prediction
            prediction = self.model.predict(processed_prompt)
            probability = self.model.predict_proba(processed_prompt)
            
            # Parse results
            is_injection = bool(prediction[0])
            confidence = max(probability[0])
            risk_score = (confidence * 100) if is_injection else 0.0
            
            return {
                "is_injection": is_injection,
                "confidence": float(confidence),
                "risk_score": float(risk_score),
                "explanation": self._generate_explanation(is_injection, confidence),
                "model_status": "loaded",
                "attack_type": "prompt_injection" if is_injection else "safe"
            }
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return {
                "is_injection": False,
                "confidence": 0.0,
                "risk_score": 0.0,
                "explanation": f"Error during analysis: {str(e)}",
                "model_status": "error"
            }
    
    def _generate_explanation(self, is_injection: bool, confidence: float) -> str:
        """Generate explanation for the prediction"""
        if is_injection:
            return f"High likelihood of prompt injection detected (confidence: {confidence:.1%})"
        else:
            return f"Prompt appears to be legitimate (confidence: {(1-confidence):.1%})"

    def _heuristic_prediction(self, prompt: str) -> dict:
        """Fallback heuristic detection for prompt injection when model is missing."""
        lower = prompt.lower()
        attack_keywords = {
            "jailbreak": "jailbreak",
            "ignore previous instructions": "instruction_override",
            "disable your content filters": "content_filter_bypass",
            "bypass": "instruction_override",
            "never mind": "instruction_override",
            "don't follow rules": "instruction_override",
            "go ahead and": "instruction_override",
            "ignore {any}": "instruction_override"
        }

        for phrase, label in attack_keywords.items():
            if phrase in lower:
                return {
                    "is_injection": True,
                    "confidence": 0.99,
                    "risk_score": 99.0,
                    "explanation": f"Heuristic detected prompt injection pattern: '{phrase}'",
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
    """Get or create model service instance"""
    global model_service
    if model_service is None:
        model_service = ModelService()
    return model_service

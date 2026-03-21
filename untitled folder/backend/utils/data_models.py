"""
Data handling and analysis utilities
"""

import json
from typing import List, Dict, Any


class PromptAnalysisResult:
    """Data class for prompt analysis results"""
    
    def __init__(self, prompt: str, is_injection: bool, confidence: float, 
                 risk_score: float, explanation: str):
        self.prompt = prompt
        self.is_injection = is_injection
        self.confidence = confidence
        self.risk_score = risk_score
        self.explanation = explanation
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "prompt": self.prompt,
            "is_injection": self.is_injection,
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "explanation": self.explanation
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())


class VulnerabilityTestResult:
    """Data class for vulnerability test results"""
    
    def __init__(self, success: bool, response: str, vulnerability_detected: bool, 
                 analysis: str, error: str = None):
        self.success = success
        self.response = response
        self.vulnerability_detected = vulnerability_detected
        self.analysis = analysis
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "response": self.response,
            "vulnerability_detected": self.vulnerability_detected,
            "analysis": self.analysis,
            "error": self.error
        }


class FixSuggestionResult:
    """Data class for fix suggestion results"""
    
    def __init__(self, success: bool, fixes: List[str], improved_prompt: str, 
                 explanation: str, error: str = None):
        self.success = success
        self.fixes = fixes
        self.improved_prompt = improved_prompt
        self.explanation = explanation
        self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "fixes": self.fixes,
            "improved_prompt": self.improved_prompt,
            "explanation": self.explanation,
            "error": self.error
        }


def batch_analyze_prompts(prompts: List[str], analyzer) -> List[Dict[str, Any]]:
    """Analyze multiple prompts in batch"""
    results = []
    for prompt in prompts:
        result = analyzer.predict(prompt)
        results.append(result)
    return results


def export_results_to_json(results: List[Dict], filepath: str) -> None:
    """Export analysis results to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)


def load_results_from_json(filepath: str) -> List[Dict]:
    """Load analysis results from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def filter_results_by_risk(results: List[Dict], min_risk: float) -> List[Dict]:
    """Filter results by minimum risk score"""
    return [r for r in results if r.get('risk_score', 0) >= min_risk]


def calculate_statistics(results: List[Dict]) -> Dict[str, Any]:
    """Calculate statistics from analysis results"""
    if not results:
        return {}
    
    total = len(results)
    injections = sum(1 for r in results if r.get('is_injection', False))
    safe = total - injections
    avg_confidence = sum(r.get('confidence', 0) for r in results) / total
    avg_risk_score = sum(r.get('risk_score', 0) for r in results) / total
    
    return {
        "total_prompts": total,
        "injections_detected": injections,
        "safe_prompts": safe,
        "injection_rate": (injections / total * 100) if total > 0 else 0,
        "average_confidence": avg_confidence,
        "average_risk_score": avg_risk_score
    }

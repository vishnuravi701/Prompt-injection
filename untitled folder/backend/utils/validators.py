"""
Input validation utilities
"""

def validate_prompt(prompt: str, min_length: int = 1, max_length: int = 5000) -> tuple[bool, str]:
    """
    Validate prompt input
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not prompt or not isinstance(prompt, str):
        return False, "Prompt must be a non-empty string"
    
    prompt = prompt.strip()
    
    if len(prompt) < min_length:
        return False, f"Prompt must be at least {min_length} character(s)"
    
    if len(prompt) > max_length:
        return False, f"Prompt must not exceed {max_length} characters"
    
    return True, ""


def sanitize_prompt(prompt: str) -> str:
    """
    Sanitize prompt input (basic cleaning)
    """
    return prompt.strip()

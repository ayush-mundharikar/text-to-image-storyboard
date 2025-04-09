def validate_prompt(prompt: str) -> bool:
    """
    Checks if the given prompt is not empty or just whitespace.
    Returns True if valid, False otherwise.
    """
    return bool(prompt and prompt.strip())

def split_prompts(text):
    return [line.strip() for line in text.strip().split('\n') if line.strip()]

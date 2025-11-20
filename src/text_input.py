# src/text_input.py
from rich.console import Console

console = Console()

def get_text_input(prompt="👉 Enter command: "):
    """Get text input from user"""
    try:
        text = input(prompt)
        return text.strip()
    except (EOFError, KeyboardInterrupt):
        return ""

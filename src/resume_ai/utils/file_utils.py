"""Utility functions for file operations."""
import os
import re
from typing import Optional

def ensure_extension(filename: str, extension: str = '.docx') -> str:
    """Ensure the filename has the specified extension."""
    if not filename.lower().endswith(extension.lower()):
        return f"{filename}{extension}"
    return filename

def clean_text_for_filename(text: str) -> str:
    """Clean text to be used in a filename."""
    # Remove special characters and extra spaces
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'\s+', '-', text)
    return text

def get_unique_filename(base_name: str, extension: str = '.docx') -> str:
    """Generate a unique filename by appending a number if it already exists."""
    filename = f"{base_name}{extension}"
    counter = 1
    
    while os.path.exists(filename):
        name, ext = os.path.splitext(base_name)
        filename = f"{name}-{counter}{extension}"
        counter += 1
        
    return filename

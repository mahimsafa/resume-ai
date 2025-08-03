"""Utility functions for the Resume AI application."""
from pathlib import Path
import re
from typing import Optional, Tuple, Dict, Any
import os

def ensure_extension(file_path: str, extension: str) -> str:
    """Ensure the file has the specified extension.
    
    Args:
        file_path: The file path to check
        extension: The desired extension (with or without dot)
        
    Returns:
        The file path with the correct extension
    """
    if not extension.startswith('.'):
        extension = f'.{extension}'
    return str(Path(file_path).with_suffix(extension))

def get_unique_filename(directory: str, base_name: str, extension: str) -> str:
    """Generate a unique filename by appending a number if the file exists.
    
    Args:
        directory: Directory where the file will be saved
        base_name: Base name of the file
        extension: File extension (with or without dot)
        
    Returns:
        A unique filename with the given extension
    """
    if not extension.startswith('.'):
        extension = f'.{extension}'
        
    counter = 1
    file_path = Path(directory) / f"{base_name}{extension}"
    
    while file_path.exists():
        file_path = Path(directory) / f"{base_name}_{counter}{extension}"
        counter += 1
        
    return str(file_path)

def clean_text_for_filename(text: str) -> str:
    """Clean text to be used in a filename.
    
    Args:
        text: The text to clean
        
    Returns:
        Cleaned text suitable for a filename
    """
    # Remove special characters and replace spaces with hyphens
    cleaned = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace spaces and multiple hyphens with a single hyphen
    cleaned = re.sub(r'[-\s]+', '-', cleaned)
    # Remove leading/trailing hyphens
    return cleaned.strip('-')

def ensure_directory(directory: str) -> None:
    """Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory: Path to the directory
    """
    Path(directory).mkdir(parents=True, exist_ok=True)

def read_file(file_path: str) -> str:
    """Read content from a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        The file contents
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")

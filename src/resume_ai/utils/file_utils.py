"""Utility functions for file and directory operations."""
import os
import re
from pathlib import Path
from typing import Optional, Union, AnyStr


def ensure_extension(filename: Union[str, Path], extension: str = '.docx') -> str:
    """Ensure the filename has the specified extension.
    
    Args:
        filename: The filename or path to check
        extension: The desired extension (including the dot)
        
    Returns:
        str: The filename with the correct extension
    """
    filename = str(filename)
    if not filename.lower().endswith(extension.lower()):
        return f"{filename}{extension}"
    return filename


def clean_text_for_filename(text: str) -> str:
    """Clean text to be used in a filename.
    
    Args:
        text: The text to clean
        
    Returns:
        str: Cleaned text suitable for a filename
    """
    # Remove special characters and extra spaces
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'\s+', '-', text)
    return text


def get_unique_filename(base_path: Union[str, Path], extension: str = '.docx') -> Path:
    """Generate a unique filename by appending a number if the file already exists.
    
    Args:
        base_path: The base path (without extension) or full path
        extension: The file extension to use
        
    Returns:
        Path: A Path object with a unique filename
    """
    base_path = Path(base_path)
    
    # If base_path is a file with extension, split it
    if base_path.suffix:
        base_name = base_path.stem
        extension = base_path.suffix
    else:
        base_name = base_path.name
    
    # Get the parent directory
    parent_dir = base_path.parent
    
    # Start with the base filename
    counter = 1
    filename = parent_dir / f"{base_name}{extension}"
    
    # If file exists, try with incrementing counter
    while filename.exists():
        filename = parent_dir / f"{base_name}-{counter}{extension}"
        counter += 1
        
    return filename


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure that a directory exists, creating it if necessary.
    
    Args:
        path: Path to the directory
        
    Returns:
        Path: The path to the directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_file(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
    """Read content from a file with error handling.
    
    Args:
        file_path: Path to the file to read
        encoding: File encoding (default: utf-8)
        
    Returns:
        str: The file contents
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    try:
        return file_path.read_text(encoding=encoding)
    except Exception as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")


def write_file(file_path: Union[str, Path], content: AnyStr, encoding: str = 'utf-8') -> None:
    """Write content to a file, creating parent directories if needed.
    
    Args:
        file_path: Path to the file to write
        content: Content to write (str or bytes)
        encoding: File encoding (default: utf-8)
        
    Raises:
        IOError: If there's an error writing the file
    """
    file_path = Path(file_path)
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, str):
            file_path.write_text(content, encoding=encoding)
        else:
            file_path.write_bytes(content)
    except Exception as e:
        raise IOError(f"Error writing to file {file_path}: {str(e)}")

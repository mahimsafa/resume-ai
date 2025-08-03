"""Resume AI - AI-powered resume objective generator."""

__version__ = "0.1.0"

# Import key components for easier access
from .app import ResumeAI
from .services.ai_service import AIService
from .services.document_service import DocumentService

__all__ = [
    'ResumeAI',
    'AIService',
    'DocumentService',
]

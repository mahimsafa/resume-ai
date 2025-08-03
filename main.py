from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate
#!/usr/bin/env python3
"""
Resume AI - AI-powered resume objective generator

This script generates a tailored career objective based on your resume and a job description,
then updates a DOCX resume with the new objective.
"""
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from resume_ai.app import ResumeAI

def main():
    """Main entry point for the Resume AI application."""
    try:
        app = ResumeAI()
        app.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
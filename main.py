from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate
#!/usr/bin/env python3
"""
Resume AI - AI-powered resume objective generator

This script generates a tailored career objective based on your resume and a job description,
then updates a DOCX resume with the new objective.

Usage:
    python main.py [job_description_file]

Example:
    python main.py input/jobdescription.txt
"""
import os
import sys
import argparse
from pathlib import Path

def add_src_to_path():
    """Add the src directory to the Python path."""
    src_dir = Path(__file__).parent / 'src'
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate a tailored resume objective.')
    parser.add_argument(
        'job_description',
        nargs='?',
        default=None,
        help='Path to the job description file (default: input/jobdescription.txt)'
    )
    return parser.parse_args()

def main():
    """Main entry point for the Resume AI application."""
    try:
        # Add src to path and import after path is set
        add_src_to_path()
        from resume_ai.app import ResumeAI
        
        # Parse command line arguments
        args = parse_arguments()
        
        # Initialize and run the application
        app = ResumeAI()
        app.run(args.job_description)
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user.")
        sys.exit(1)
    except ImportError as e:
        print(f"\n❌ Error importing required modules: {e}", file=sys.stderr)
        print("   Make sure to install the required dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}", file=sys.stderr)
        print("\n💡 Try running the setup script to verify your installation:")
        print("   python setup_project.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
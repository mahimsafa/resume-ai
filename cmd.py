#!/usr/bin/env python3
"""
Resume AI - CLI Interface

This module provides the command-line interface for the Resume AI application.
"""
import argparse
import sys
from pathlib import Path
from typing import Optional

from lib.cover_letter_generator import generate_cover_letter, save_cover_letter
from lib.objective_generator import generate_career_objective
from lib.pdf_utils import update_resume_objective, create_pdf_from_docx

def get_resume_content() -> str:
    """Read the default resume content."""
    resume_path = Path("input/resume.md")
    if not resume_path.exists():
        raise FileNotFoundError("Default resume.md not found in input/ directory")
    with open(resume_path, 'r') as f:
        return f.read()

def get_resume_template() -> str:
    """Get the path to the resume template."""
    template_path = Path("input/resume.docx")
    if not template_path.exists():
        raise FileNotFoundError("resume.docx not found in input/ directory")
    return str(template_path)

def check_required_files() -> tuple[bool, str]:
    """Check if required input files exist.
    
    Returns:
        Tuple of (success, message)
    """
    input_dir = Path("input")
    required_files = {
        'resume': input_dir / 'resume.md',
        'job_description': input_dir / 'jobdescription.txt',
        'resume_template': input_dir / 'resume.docx'
    }
    
    missing = [name for name, path in required_files.items() if not path.exists()]
    if missing:
        return False, f"Missing required files: {', '.join(missing)}. Please add them to the 'input' directory."
    return True, ""

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Resume AI - AI-powered resume objective generator')
    subparsers = parser.add_subparsers(dest='command', help='Command to run', required=True)
    
    # Parser for generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a new resume with objective')
    generate_parser.add_argument('job_description', help='Path to job description file')
    generate_parser.add_argument('--cv', action='store_true', help='Generate a cover letter')
    generate_parser.add_argument('--company', default='the company', help='Company name for personalization')
    generate_parser.add_argument('--pdf', action='store_true', help='Generate PDF version of the resume')
    
    # Parser for API server
    api_parser = subparsers.add_parser('api', help='Run the API server')
    api_parser.add_argument('--host', default='0.0.0.0', help='Host to run the API server on')
    api_parser.add_argument('--port', type=int, default=8000, help='Port to run the API server on')
    
    return parser.parse_args()

def process_job_application_cli(job_description_path: str, generate_cv: bool = False, 
                             company_name: str = "the company", generate_pdf: bool = False):
    """Process a job application from the command line."""
    try:
        # Read job description
        with open(job_description_path, 'r') as f:
            job_description = f.read()
        
        # Read resume content
        resume_content = get_resume_content()
        
        # Generate objective
        print("Generating career objective...")
        objective = generate_career_objective(
            resume_content=resume_content,
            job_description=job_description
        )
        
        # Update resume
        print("Updating resume...")
        output_dir = Path("generated")
        output_path = output_dir / f"resume_{Path(job_description_path).stem}.docx"
        
        updated_resume_path = update_resume_objective(
            source_path=get_resume_template(),
            output_path=str(output_path),
            new_objective=objective
        )
        
        result = {
            "status": "success",
            "objective": objective,
            "resume_docx": str(updated_resume_path)
        }
        
        # Generate PDF if requested
        if generate_pdf:
            print("Generating PDF...")
            pdf_path = create_pdf_from_docx(updated_resume_path, str(output_dir))
            result["resume_pdf"] = pdf_path
        
        # Generate cover letter if requested
        if generate_cv:
            print("Generating cover letter...")
            cover_letter = generate_cover_letter(
                resume_content=resume_content,
                job_description=job_description,
                company_name=company_name
            )
            
            # Save cover letter
            cover_letter_path = output_dir / f"cover_letter_{Path(job_description_path).stem}.txt"
            save_cover_letter(cover_letter, str(cover_letter_path))
            
            result["cover_letter"] = cover_letter
            result["cover_letter_path"] = str(cover_letter_path)
        
        print("\nJob application processed successfully!")
        print(f"Updated resume: {result['resume_docx']}")
        if 'resume_pdf' in result:
            print(f"PDF version: {result['resume_pdf']}")
        if 'cover_letter_path' in result:
            print(f"Cover letter: {result['cover_letter_path']}")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main entry point for the CLI interface."""
    try:
        args = parse_arguments()
        
        if args.command == 'generate':
            process_job_application_cli(
                job_description_path=args.job_description,
                generate_cv=args.cv,
                company_name=args.company,
                generate_pdf=args.pdf
            )
        elif args.command == 'api':
            # Import here to avoid circular imports
            from main import run_api
            print(f"Starting API server at http://{args.host}:{args.port}")
            print(f"API documentation available at http://{args.host}:{args.port}/docs")
            run_api(host=args.host, port=args.port)
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Resume AI - AI-powered resume objective generator

This script provides both a CLI and API interface for generating tailored
career objectives, cover letters, and updating resumes.

API Endpoints:
    POST /generate-objective/ - Generate a career objective
    POST /generate-cover-letter/ - Generate a cover letter
    POST /queue/ - Process a job application (objective + resume update + optional cover letter)

CLI Usage:
    python main.py [command] [options]

Examples:
    python main.py api  # Start the API server
    python main.py generate job_description.txt  # Generate a resume with objective
    python main.py update resume.docx  # Update an existing resume
"""
from importlib import reload
import os
import sys
import argparse
import re
import uvicorn
import uuid
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Local imports
from lib.objective_generator import generate_career_objective
from lib.cover_letter_generator import generate_cover_letter, save_cover_letter
from lib.pdf_utils import update_resume_objective, create_pdf_from_docx
from utils import (
    ensure_extension,
    get_unique_filename,
    clean_text_for_filename,
    ensure_directory,
    read_file as read_file_util
)

# Initialize FastAPI app
app = FastAPI(
    title="Resume AI API",
    description="API for generating tailored career objectives and cover letters",
    version="1.0.0"
)

# Request models
class ObjectiveRequest(BaseModel):
    resume_content: str
    job_description: str
    objective_length: Optional[str] = "medium"
    tone: Optional[str] = "professional"

class CoverLetterRequest(BaseModel):
    resume_content: str
    job_description: str
    company_name: Optional[str] = "the company"
    tone: Optional[str] = "professional"

class QueueRequest(BaseModel):
    job_description: str
    generate_cv: Optional[bool] = False
    company_name: Optional[str] = "the company"
    tone: Optional[str] = "professional"

# Utility functions
def get_resume_content() -> str:
    """Read the default resume content."""
    resume_path = Path("input/resume.md")
    if not resume_path.exists():
        raise FileNotFoundError("Default resume.md not found in input/ directory")
    return read_file_util(str(resume_path))

def get_resume_template() -> str:
    """Get the path to the resume template."""
    template_path = Path("input/resume.docx")
    if not template_path.exists():
        raise FileNotFoundError("resume.docx not found in input/ directory")
    return str(template_path)

# API Endpoints
@app.post("/generate-objective/")
async def generate_objective_endpoint(request: ObjectiveRequest):
    """
    Generate a career objective based on resume and job description.
    
    - **resume_content**: Content of the resume
    - **job_description**: Job description to tailor the objective to
    - **objective_length**: Length of the objective ('short', 'medium', or 'long')
    - **tone**: Tone of the objective ('professional', 'enthusiastic', 'formal')
    """
    try:
        objective = generate_career_objective(
            resume_content=request.resume_content,
            job_description=request.job_description,
            objective_length=request.objective_length,
            tone=request.tone
        )
        return {"objective": objective}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-cover-letter/")
async def generate_cover_letter_endpoint(request: CoverLetterRequest):
    """
    Generate a cover letter based on resume and job description.
    
    - **resume_content**: Content of the resume
    - **job_description**: Job description to tailor the cover letter to
    - **company_name**: Name of the company (for personalization)
    - **tone**: Tone of the cover letter ('professional', 'enthusiastic', 'formal')
    """
    try:
        cover_letter = generate_cover_letter(
            resume_content=request.resume_content,
            job_description=request.job_description,
            company_name=request.company_name,
            tone=request.tone
        )
        return {"cover_letter": cover_letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/queue/")
async def process_job_application(
    request: QueueRequest,
    generate_cv: bool = Query(False, description="Whether to generate a cover letter")
):
    """
    Process a job application by generating an objective, updating the resume,
    and optionally generating a cover letter.
    
    - **job_description**: The job description to tailor the application to
    - **generate_cv**: Whether to generate a cover letter (default: False)
    - **company_name**: Name of the company (for personalization)
    - **tone**: Tone of the generated content ('professional', 'enthusiastic', 'formal')
    """
    try:
        # Ensure output directory exists
        output_dir = Path("generated")
        output_dir.mkdir(exist_ok=True)
        
        # Get resume content and template
        resume_content = get_resume_content()
        template_path = get_resume_template()
        
        # Generate objective
        objective, file_name = generate_career_objective(
            resume_content=resume_content,
            job_description=request.job_description,
            tone=request.tone
        )

        print(file_name)
        print(objective)
        print('-'*50)
        
        # Update resume with new objective
        # output_filename = f"resume_{uuid.uuid4().hex[:8]}.docx"
        output_filename = f"{file_name}.docx"
        output_path = output_dir / output_filename
        
        updated_resume_path = update_resume_objective(
            source_path=template_path,
            output_path=str(output_path),
            new_objective=objective
        )
        
        # Generate PDF version
        pdf_path = create_pdf_from_docx(updated_resume_path, str(output_dir))
        
        result = {
            "status": "success",
            "objective": objective,
            "resume_docx": str(updated_resume_path),
            "resume_pdf": pdf_path
        }
        
        # Generate cover letter if requested
        if generate_cv or request.generate_cv:
            cover_letter = generate_cover_letter(
                resume_content=resume_content,
                job_description=request.job_description,
                company_name=request.company_name,
                tone=request.tone
            )
            
            # Save cover letter
            cover_letter_path = output_dir / f"{file_name}.txt"
            save_cover_letter(cover_letter, str(cover_letter_path))
            
            result["cover_letter"] = cover_letter
            result["cover_letter_path"] = str(cover_letter_path)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to Resume AI API",
        "endpoints": [
            "POST /generate-objective/ - Generate a career objective",
            "POST /generate-cover-letter/ - Generate a cover letter",
            "POST /queue/?generate_cv=true - Process a job application (resume + optional cover letter)"
        ]
    }

def run_api(host: str = "0.0.0.0", port: int = 8000):
    """Run the FastAPI server."""
    uvicorn.run("main:app", host=host, port=port, reload=True)

# Ensure required directories exist
ensure_directory(Path("input"))
ensure_directory(Path("generated"))

def check_required_files() -> Tuple[bool, str]:
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
    """Main entry point for the Resume AI application."""
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
            # Run the API server
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
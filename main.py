#!/usr/bin/env python3
"""
Resume AI - AI-powered resume objective generator (API Server)

This module provides a FastAPI interface for generating tailored
career objectives, cover letters, and updating resumes.

API Endpoints:
    GET / - Welcome message and available endpoints
    POST /queue/ - Process a job application (objective + resume update + optional cover letter)
"""
import uvicorn
import uuid
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Local imports
from lib.objective_generator import generate_career_objective
from lib.cover_letter_generator import generate_cover_letter, save_cover_letter
from lib.pdf_utils import update_resume_objective, create_pdf_from_docx
from utils import read_file as read_file_util, ensure_directory

# Initialize FastAPI app
app = FastAPI(
    title="Resume AI API",
    description="API for generating tailored career objectives and cover letters",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

        # if any files in the output directory with the same prefix as the file_name, then append a number to the file_name
        if output_dir.glob(f"{file_name}.*"):
            file_name = f"{file_name}_{uuid.uuid4().hex[:8]}"
        
        
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

# This file is meant to be run with uvicorn directly or imported as a module
# To run the API server: uvicorn main:app --reload
# For production: uvicorn main:app --host 0.0.0.0 --port 8000

if __name__ == "__main__":
    # For backward compatibility, run the API server directly
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
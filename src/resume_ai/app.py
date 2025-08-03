"""Main application class for Resume AI."""
import os
from pathlib import Path
from typing import Optional

from .services.ai_service import AIService
from .services.document_service import DocumentService
from .utils.file_utils import ensure_extension, get_unique_filename

class ResumeAI:
    """Main application class for Resume AI."""
    
    def __init__(self, base_dir: Optional[str] = None):
        """Initialize the Resume AI application."""
        self.base_dir = base_dir or os.getcwd()
        self.ai_service = AIService()
        self.document_service = DocumentService()
    
    def run(self, job_description_path: str = 'jobdescription.txt'):
        """Run the Resume AI application."""
        print("Welcome to Resume Objective Generator!")
        print(f"Reading job description from {job_description_path}...\n")
        
        try:
            # Read job description
            job_description = self._read_job_description(job_description_path)
            
            # Generate objective and filename
            print("Generating tailored objective...\n")
            resume_content = self._read_resume()
            objective, filename = self.ai_service.generate_objective_and_filename(
                resume_content=resume_content,
                job_description=job_description,
                base_name="mahim"
            )
            
            print(objective)
            
            # Update the DOCX file
            output_file = self.document_service.update_docx_objective(
                source_path=os.path.join(self.base_dir, 'resume.docx'),
                output_path=filename,
                new_objective=objective
            )
            
            print(f"\nYour updated resume has been saved as: {os.path.basename(output_file)}")
            
        except FileNotFoundError as e:
            print(f"Error: {e}")
            if 'jobdescription.txt' in str(e):
                print("Please create a jobdescription.txt file with the job description.")
            elif 'resume.docx' in str(e):
                print("Please ensure resume.docx exists in the current directory.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
    def _read_resume(self) -> str:
        """Read the resume content."""
        resume_path = os.path.join(self.base_dir, 'resume.md')
        if not os.path.exists(resume_path):
            raise FileNotFoundError("resume.md not found in the current directory.")
        return self.document_service.read_file(resume_path)
    
    def _read_job_description(self, path: str) -> str:
        """Read the job description content."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found.")
            
        content = self.document_service.read_file(path).strip()
        if not content:
            raise ValueError("Job description file is empty")
            
        return content

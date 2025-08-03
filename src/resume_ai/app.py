"""Main application class for Resume AI."""
import os
from pathlib import Path
from typing import Optional, Tuple

from .services.ai_service import AIService
from .services.document_service import DocumentService
from .utils.file_utils import ensure_extension, get_unique_filename, ensure_directory

class ResumeAI:
    """Main application class for Resume AI."""
    
    def __init__(self, base_dir: Optional[str] = None):
        """Initialize the Resume AI application.
        
        Args:
            base_dir: Base directory for the application (defaults to current directory)
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.input_dir = self.base_dir / 'input'
        self.output_dir = self.base_dir / 'generated'
        self.ai_service = AIService()
        self.document_service = DocumentService()
        
        # Ensure required directories exist
        self._setup_directories()
    
    def _setup_directories(self) -> None:
        """Ensure required directories exist."""
        self.input_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def _check_required_files(self) -> Tuple[bool, str]:
        """Check if required input files exist.
        
        Returns:
            Tuple of (success, message)
        """
        required_files = {
            'resume': self.input_dir / 'resume.md',
            'job_description': self.input_dir / 'jobdescription.txt',
            'resume_template': self.input_dir / 'resume.docx'
        }
        
        missing = [name for name, path in required_files.items() if not path.exists()]
        if missing:
            return False, f"Missing required files: {', '.join(missing)}. Please add them to the 'input' directory."
        return True, ""
    
    def run(self, job_description_path: Optional[str] = None):
        """Run the Resume AI application.
        
        Args:
            job_description_path: Optional path to job description file (relative to input dir)
        """
        print("Welcome to Resume Objective Generator!")
        
        # Check for required files
        success, message = self._check_required_files()
        if not success:
            print(f"Error: {message}")
            return
            
        job_description_path = job_description_path or 'jobdescription.txt'
        job_description_path = self.input_dir / job_description_path
        
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
            source_docx = self.input_dir / 'resume.docx'
            output_file = self.document_service.update_docx_objective(
                source_path=str(source_docx),
                output_path=str(self.output_dir / filename),
                new_objective=objective
            )
            
            print(f"\nYour updated resume has been saved to: {output_file}")
            
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
        resume_path = self.input_dir / 'resume.md'
        return self.document_service.read_file(str(resume_path))
    
    def _read_job_description(self, path: Path) -> str:
        """Read the job description content.
        
        Args:
            path: Path to the job description file
            
        Returns:
            str: Content of the job description
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is empty
        """
        if not path.exists():
            raise FileNotFoundError(f"Job description file not found: {path}")
            
        content = self.document_service.read_file(str(path)).strip()
        if not content:
            raise ValueError(f"Job description file is empty: {path}")
            
        return content

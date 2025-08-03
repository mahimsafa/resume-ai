"""Service for handling document operations."""
from pathlib import Path
from typing import Optional, Tuple

from docx import Document
from docx.shared import Pt

from resume_ai.utils.file_utils import ensure_extension, get_unique_filename

class DocumentService:
    """Service for handling document operations."""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """Read content from a file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    @classmethod
    def update_docx_objective(
        cls,
        source_path: str,
        output_path: str,
        new_objective: str,
        placeholder: str = '<objective_here>',
        font_name: str = 'Spectral',
        font_size: int = 10
    ) -> str:
        """
        Update the objective section in a DOCX file.
        
        Args:
            source_path: Path to the source DOCX file
            output_path: Path where to save the updated file
            new_objective: The objective text to insert
            placeholder: The placeholder text to replace
            font_name: Font name for the objective text
            font_size: Font size in points
            
        Returns:
            str: Path to the saved file
        """
        # Ensure output path has .docx extension and is unique
        output_path = ensure_extension(output_path, '.docx')
        output_path = get_unique_filename(output_path.rsplit('.', 1)[0], '.docx')
        
        doc = Document(source_path)
        placeholder_found = False
        
        # Try to find and replace the placeholder
        for para in doc.paragraphs:
            if placeholder in para.text:
                para.clear()
                # Add 'OBJECTIVE' in bold
                title_run = para.add_run('OBJECTIVE\n')
                title_run.bold = True
                title_run.font.name = font_name
                title_run.font.size = Pt(font_size)
                # Add objective text with normal weight
                obj_run = para.add_run(new_objective)
                obj_run.font.name = font_name
                obj_run.font.size = Pt(font_size)
                placeholder_found = True
                break
        
        # If placeholder not found, add a new section at the beginning
        if not placeholder_found:
            para = doc.add_paragraph()
            # Add 'OBJECTIVE' in bold with specified font
            title_run = para.add_run('OBJECTIVE\n')
            title_run.bold = True
            title_run.font.name = font_name
            title_run.font.size = Pt(font_size)
            # Add objective text with normal weight
            obj_run = para.add_run(new_objective)
            obj_run.font.name = font_name
            obj_run.font.size = Pt(font_size)
        
        # Save the document
        doc.save(output_path)
        return output_path

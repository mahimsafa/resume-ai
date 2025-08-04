import subprocess
import re
import sys
import os
from pathlib import Path
from typing import Optional


def convert_to_pdf_libreoffice(source_path: str, output_dir: str, pdf_name: str) -> str:
    """Convert a document to PDF using LibreOffice.
    
    Args:
        source_path: Path to the source document
        output_dir: Directory where the PDF will be saved
        
    Returns:
        Path to the generated PDF file
        
    Raises:
        FileNotFoundError: If LibreOffice is not found
        subprocess.CalledProcessError: If the conversion fails
    """
    print('source_path', source_path)
    print('output_dir', output_dir)
    print('pdf_name', pdf_name)
    
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file not found: {source_path}")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    libreoffice_bin = libreoffice_exec()
    
    args = [
        libreoffice_bin,
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', output_dir,
        source_path
    ]
    
    try:
        process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        
        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode,
                args,
                process.stdout,
                process.stderr
            )
        
        # Extract the output filename from the stdout
        match = re.search(r'-> (.*?)\.pdf', process.stdout)
        if match:
            return f"{match.group(1)}.pdf"
        else:
            # If pattern matching fails, construct the expected output path
            base_name = Path(source_path).stem
            return os.path.join(output_dir, f"{base_name}.pdf")
            
    except subprocess.TimeoutExpired:
        raise TimeoutError("PDF conversion timed out")


def libreoffice_exec() -> str:
    """Get the path to the LibreOffice executable.
    
    Returns:
        Path to the LibreOffice executable
        
    Raises:
        FileNotFoundError: If LibreOffice is not found
    """
    if sys.platform == 'darwin':
        paths = [
            '/Applications/LibreOffice.app/Contents/MacOS/soffice',
            '/Applications/LibreOffice.app/Contents/MacOS/soffice.bin',
            '/Applications/LibreOffice.app/Contents/MacOS/soffice.exe'
        ]
    else:
        paths = ['libreoffice', 'soffice', 'libreoffice7.6']
    
    for path in paths:
        try:
            subprocess.run([path, '--version'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE,
                         check=True)
            return path
        except (subprocess.SubprocessError, FileNotFoundError):
            continue
    
    raise FileNotFoundError(
        "LibreOffice not found. Please install LibreOffice or add it to your PATH. "
        "On macOS, you can install it with 'brew install --cask libreoffice'"
    )

if __name__ == "__main__":
    convert_to_pdf_libreoffice("/Users/mahim/Desktop/resume-ai/generated/senior-software-engineer-backend-at-ifarmer.docx", "/Users/mahim/Desktop/resume-ai/generated/")
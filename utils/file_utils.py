from pathlib import Path

def get_resume_template() -> str:
    """Get the path to the resume template."""
    template_path = Path("input/resume.docx")
    if not template_path.exists():
        raise FileNotFoundError("resume.docx not found in input/ directory")
    return str(template_path)
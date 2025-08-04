# tasks.py
from celery_app import celery
import uuid
from pathlib import Path
from lib.objective_generator import generate_career_objective
from lib.pdf_utils import create_pdf_from_docx, update_resume_objective
from lib.cover_letter_generator import generate_cover_letter
from utils.file_utils import get_resume_template

@celery.task(bind=True)
def process_application(
    self,
    resume_content: str,
    job_description: str,
    tone: str,
    company_name: str | None = None,
    generate_cv_flag: bool = False,
):
    """
    Background job: generate objective, update resume, optional cover letter.
    All serializers must work via JSON or pickle-safe objects.
    """
    # Ideally you move the logic from your synchronous route into here:
    objective, file_name = generate_career_objective(
        resume_content=resume_content,
        job_description=job_description,
        tone=tone,
    )

    print(objective)
    print('-' * 50)

    # Ensure unique filename
    output_dir = Path("generated")
    output_dir.mkdir(exist_ok=True)
    if list(output_dir.glob(f"{file_name}.*")):
        file_name = f"{file_name}_{uuid.uuid4().hex[:8]}"

    docx_path = update_resume_objective(
        source_path=get_resume_template(),
        output_path=str(output_dir / f"{file_name}.docx"),
        new_objective=objective,
    )

    pdf_path = create_pdf_from_docx(docx_path, str(output_dir))

    result = {
        "objective": objective,
        "resume_docx": str(docx_path),
        "resume_pdf": pdf_path,
    }

    if generate_cv_flag:
        cover_letter = generate_cover_letter(
            resume_content=resume_content,
            job_description=job_description,
            company_name=company_name,
            tone=tone,
        )
        letter_path = output_dir / f"{file_name}.txt"
        save_cover_letter(cover_letter, str(letter_path))
        result["cover_letter"] = cover_letter
        result["cover_letter_path"] = str(letter_path)

    return result

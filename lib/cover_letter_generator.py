from typing import Optional
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate
from pathlib import Path

def generate_cover_letter(
    resume_content: str,
    job_description: str,
    company_name: str = "the company",
    tone: str = "professional"
) -> str:
    """
    Generate a tailored cover letter based on resume and job description.
    
    Args:
        resume_content: The content of the resume
        job_description: The job description
        company_name: Name of the company (for personalization)
        tone: Tone of the cover letter ('professional', 'enthusiastic', 'formal')
        
    Returns:
        Generated cover letter text
    """
    llm = ChatVertexAI(model="gemini-2.5-flash", temperature=0.7)
    
    prompt_template = """
    Write a {tone} cover letter for a job application at {company_name}.
    Use the following resume and job description to create a personalized cover letter.
    
    Resume:
    {resume}
    
    Job Description:
    {job_description}
    
    Note:

    1. Make sure to provide the cover letter in the format of a professional cover letter.
    2. Do not use any formatting. Use plain text
    3. Include a subject for the cover letter.
    4. Make it short and to the point.
    5. Make it under 2-3 paragraph max. But try to keep it under 2 paragraph.
    6. Most of the time try to use the resume content to generate the cover letter.
    7. Do not include any skills or experiences that is not included in the resume.
    8. Do not include any skills or experiences that is not included in the job description.
    9. Try to make the 2nd paragraph in bullet points that are related to the job description and why I am a good fit for the job.
    """
    
    prompt = PromptTemplate.from_template(prompt_template)
    formatted_prompt = prompt.format(
        resume=resume_content,
        job_description=job_description,
        company_name=company_name,
        tone=tone
    )
    
    response = llm.invoke(formatted_prompt)
    return response.content.strip()

def save_cover_letter(content: str, output_path: str) -> str:
    """
    Save the cover letter to a text file.
    
    Args:
        content: The cover letter content
        output_path: Path where to save the cover letter
        
    Returns:
        Path to the saved cover letter file
    """
    output_path = str(Path(output_path).with_suffix('.txt'))
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return output_path

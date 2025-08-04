from typing import Optional
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate
import re
from utils import clean_text_for_filename

def generate_career_objective(
    resume_content: str,
    job_description: str,
    objective_length: str = 'short',
    tone: str = 'professional',

) -> str:
    """
    Generate a tailored career objective based on resume and job description.
    
    Args:
        resume_content: The content of the resume
        job_description: The job description to tailor the objective to
        objective_length: Length of the objective ('short', 'medium', or 'long')
        tone: Tone of the objective ('professional', 'enthusiastic', 'formal')
        
    Returns:
        Generated career objective string
    """
    # Initialize the language model
    llm = ChatVertexAI(model="gemini-2.5-flash", temperature=0.7)
    
    # Define the prompt template
    prompt_template = """
    Based on the following resume and job description, generate a {tone} career objective that is {length} in length. The objective should highlight the most relevant skills and experiences from the resume that match the job requirements. Also generate a suggested filename based on the job description that includes the job role and company name in the format: [role]-at-[company].
    
    Resume:
    {resume}
    
    Job Description:
    {job_description}
    
    Output Format:

    CAREER OBJECTIVE:
    [Your career objective here]
    
    FILENAME:
    [suggested-filename]
    """
    
    # Map length to descriptive terms
    length_map = {
        'short': '2-3 sentences',
        'medium': '3-4 sentences',
        'long': '4-5 sentences'
    }
    
    # Format the prompt
    prompt = PromptTemplate.from_template(prompt_template)
    formatted_prompt = prompt.format(
        resume=resume_content,
        job_description=job_description,
        tone=tone,
        length=length_map.get(objective_length.lower(), '3-4 sentences')
    )
    
    # Generate the objective
    response = llm.invoke(formatted_prompt)
    
    # Parse the response
    try:
        objective = re.search(r'CAREER OBJECTIVE:(.*?)(?=FILENAME:|$)', response.content, re.DOTALL)
        filename = re.search(r'FILENAME:(.*?)$', response.content, re.DOTALL)
        
        if not objective or not filename:
            raise ValueError("Could not parse AI response")
        
        objective = objective.group(1).strip()
        filename = filename.group(1).strip()
        
        # Clean and validate the filename
        filename = clean_text_for_filename(filename)
        if not filename:
            filename = f"resume-generated"
        
        return objective, filename
        
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        # Fallback to a default filename if parsing fails
        return "A highly motivated professional with relevant experience.", "resume-generated"
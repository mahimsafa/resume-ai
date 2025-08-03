"""Service for AI-related operations."""
from typing import Dict, Tuple

from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate
from resume_ai.utils.file_utils import clean_text_for_filename

class AIService:
    """Service for handling AI-related operations."""
    
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.7):
        """Initialize the AI service with a specific model."""
        self.llm = ChatVertexAI(model=model_name, temperature=temperature)
        
    def generate_objective_and_filename(
        self,
        resume_content: str,
        job_description: str,
        base_name: str = "resume"
    ) -> Tuple[str, str]:
        """
        Generate a tailored objective and filename based on resume and job description.
        
        Args:
            resume_content: The content of the resume
            job_description: The job description
            base_name: Base name to use for the filename
            
        Returns:
            Tuple containing (objective, filename)
        """
        # Create a combined prompt template
        prompt_template = """
        Based on the following resume and job description:
        
        RESUME:
        {resume}
        
        JOB DESCRIPTION:
        {job_description}
        
        Please provide:
        1. A tailored career objective (2-3 sentences) that highlights the most relevant skills and experiences.
        2. A suggested filename that includes the job role and company name in the format: [role]-at-[company]
        
        Return the result in this exact format:
        
        OBJECTIVE:
        [Your tailored objective here]
        
        FILENAME:
        [role]-at-[company]
        
        Notes:
        - The objective should be concise and focused on the role's requirements.
        - Do not add any extra skills that are not present in the resume.
        - The filename should be in lowercase with words separated by hyphens.
        - Keep the filename under 50 characters total.
        - If company name is not clear, use 'company' as placeholder.
        """
        
        # Create and run the chain
        prompt = PromptTemplate(
            input_variables=["resume", "job_description"],
            template=prompt_template
        )
        
        chain = prompt | self.llm
        response = chain.invoke({
            "resume": resume_content[:2000],  # Limit content length
            "job_description": job_description[:2000]
        })
        
        # Parse the response
        objective, filename = self._parse_ai_response(response.content, base_name)
        return objective, filename
    
    def _parse_ai_response(self, response_content: str, base_name: str) -> Tuple[str, str]:
        """Parse the AI response into objective and filename."""
        objective = ""
        filename = f"{base_name.lower()}-resume"
        
        try:
            # Split the response into lines and process
            lines = response_content.split('\n')
            in_objective = False
            in_filename = False
            
            for line in lines:
                line = line.strip()
                if line.upper() == 'OBJECTIVE:':
                    in_objective = True
                    in_filename = False
                elif line.upper() == 'FILENAME:':
                    in_objective = False
                    in_filename = True
                elif in_objective and line:
                    if objective:  # Add space between lines
                        objective += ' '
                    objective += line
                elif in_filename and line and not line.startswith('['):
                    # Clean up the filename
                    clean_line = clean_text_for_filename(line)
                    filename = f"{base_name.lower()}-{clean_line}"
                    filename = filename[:100]  # Ensure reasonable length
                    break  # Only process the first filename line
            
            # If we couldn't parse the response, use fallback
            if not objective:
                objective = response_content.strip()
                
            return objective, filename
            
        except Exception:
            # Fallback if parsing fails
            return response_content.strip(), f"{base_name.lower()}-resume"

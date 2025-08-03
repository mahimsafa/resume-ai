from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate
from docx import Document
from docx.shared import Pt, RGBColor
import re
import os

def read_resume():
    with open('resume.md', 'r', encoding='utf-8') as file:
        return file.read()
        
def read_job_description():
    with open('jobdescription.txt', 'r', encoding='utf-8') as file:
        return file.read()

def generate_objective(job_description):
    # Read the resume
    resume_content = read_resume()
    
    # Initialize the LLM
    llm = ChatVertexAI(model="gemini-2.5-flash", temperature=0.7)
    
    # Create a prompt template
    prompt_template = """
    Based on the following resume and job description, generate a compelling and tailored career objective.
    The objective should be concise (2-3 sentences) and highlight the most relevant skills and experiences.
    There shouldn't be any extra text or markdown formatting. Just the objective in plain text so that I can copy and paste to my resume or LinkedIn profile.
    
    Resume:
    {resume}
    
    Job Description:
    {job_description}
    
    Tailored Objective:
    """
    
    prompt = PromptTemplate(
        input_variables=["resume", "job_description"],
        template=prompt_template
    )
    
    # Create and run the chain
    chain = prompt | llm
    result = chain.invoke({
        "resume": resume_content,
        "job_description": job_description
    })
    
    return result.content.strip()

def get_next_available_filename(base_path):
    """Generate the next available filename in the sequence (resume-1.docx, resume-2.docx, etc.)"""
    base_dir = os.path.dirname(base_path)
    base_name, ext = os.path.splitext(os.path.basename(base_path))
    counter = 1
    
    while True:
        if counter == 1:
            new_path = os.path.join(base_dir, f"{base_name}{ext}")
            if not os.path.exists(new_path):
                return new_path
        
        new_path = os.path.join(base_dir, f"{base_name}-{counter}{ext}")
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def update_docx_objective(new_objective, docx_path='resume.docx'):
    """
    Update the objective section in the DOCX file by replacing <objective_here>
    with the generated objective text, preserving formatting.
    Saves the file with an incremental filename (resume-1.docx, resume-2.docx, etc.)
    Returns the path to the saved file.
    """
    try:
        # Generate the output filename
        output_path = get_next_available_filename(docx_path)
        
        # Load the document
        doc = Document(docx_path)
        
        # Track if we found and replaced the placeholder
        placeholder_found = False
        
        # First, try to find and replace the <objective_here> placeholder
        for para in doc.paragraphs:
            if '<objective_here>' in para.text:
                # Clear the paragraph and add the new objective
                para.clear()
                
                # Split the new objective into multiple paragraphs if needed
                paragraphs = new_objective.split('\n\n')
                
                # Add the first part to the current paragraph with Spectral font and size 10
                if paragraphs:
                    run = para.add_run(paragraphs[0])
                    run.font.name = 'Spectral'
                    run.font.size = Pt(10)
                
                # Add remaining paragraphs as new paragraphs after with same styling
                for i in range(1, len(paragraphs)):
                    new_para = doc.add_paragraph()
                    new_run = new_para.add_run(paragraphs[i])
                    new_run.font.name = 'Spectral'
                    new_run.font.size = Pt(10)
                    para._p.addnext(new_para._p)
                
                placeholder_found = True
                break
        
        # If placeholder not found, look for an OBJECTIVE section
        if not placeholder_found:
            for para in doc.paragraphs:
                if 'OBJECTIVE' in para.text.upper():
                    # Clear the paragraph and add the new objective with styling
                    para.clear()
                    # Add 'OBJECTIVE' in bold
                    title_run = para.add_run('OBJECTIVE\n')
                    title_run.bold = True
                    title_run.font.name = 'Spectral'
                    title_run.font.size = Pt(10)
                    # Add objective text with normal weight
                    obj_run = para.add_run(new_objective)
                    obj_run.font.name = 'Spectral'
                    obj_run.font.size = Pt(10)
                    placeholder_found = True
                    break
        
        # If still not found, add a new section at the beginning
        if not placeholder_found:
            print("Warning: '<objective_here>' placeholder not found. Adding objective at the beginning.")
            para = doc.add_paragraph()
            # Add 'OBJECTIVE' in bold with Spectral font
            title_run = para.add_run('OBJECTIVE\n')
            title_run.bold = True
            title_run.font.name = 'Spectral'
            title_run.font.size = Pt(10)
            # Add objective text with normal weight
            obj_run = para.add_run(new_objective)
            obj_run.font.name = 'Spectral'
            obj_run.font.size = Pt(10)
            doc.paragraphs[0]._p.addprevious(para._p)
        
        # Save the document to the new filename
        doc.save(output_path)
        print(f"\nSuccessfully saved updated resume as: {os.path.basename(output_path)}")
        return output_path
        
    except Exception as e:
        print(f"Error updating DOCX file: {str(e)}")
        raise

if __name__ == "__main__":
    print("Welcome to Resume Objective Generator!")
    print("Reading job description from jobdescription.txt...")
    
    try:
        job_description = read_job_description()
        if not job_description.strip():
            raise ValueError("Job description file is empty")
            
        print("\nGenerating tailored objective...\n")
        objective = generate_objective(job_description)
        print(objective)
        
        # Update the DOCX file with the new objective
        output_file = update_docx_objective(objective)
        print(f"\nYour updated resume has been saved as: {output_file}")
    except FileNotFoundError:
        print("Error: jobdescription.txt file not found. Please create it with the job description.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
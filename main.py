from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain.prompts import PromptTemplate

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

if __name__ == "__main__":
    print("Welcome to Resume Objective Generator!")
    print("Reading job description from jobdescription.txt...")
    
    try:
        job_description = read_job_description()
        if not job_description.strip():
            raise ValueError("Job description file is empty")
            
        print("\nGenerating tailored objective...\n")
        objective = generate_objective(job_description)
        # print("\n=== TAILORED OBJECTIVE ===")
        print(objective)
        # print("\nYou can copy this objective to your resume or LinkedIn profile!")
    except FileNotFoundError:
        print("Error: jobdescription.txt file not found. Please create it with the job description.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
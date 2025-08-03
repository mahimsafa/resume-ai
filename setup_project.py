#!/usr/bin/env python3
"""
Setup script for Resume AI project.
This script helps set up the project structure and verifies the installation.
"""
import os
import shutil
from pathlib import Path

def setup_project():
    """Set up the project structure and verify installation."""
    print("🚀 Setting up Resume AI project...")
    
    # Define paths
    base_dir = Path(__file__).parent
    input_dir = base_dir / "input"
    generated_dir = base_dir / "generated"
    
    # Create directories if they don't exist
    input_dir.mkdir(exist_ok=True)
    generated_dir.mkdir(exist_ok=True)
    
    # Check for required files
    required_files = {
        'resume.md': "Markdown version of your resume",
        'resume.docx': "Word document with <objective_here> placeholder",
        'jobdescription.txt': "Job description for generating the objective"
    }
    
    print("\n📁 Project structure:")
    print(f"   • {base_dir}/")
    print(f"     ├── input/           # Input files (resume.md, resume.docx, jobdescription.txt)")
    print(f"     ├── generated/       # Generated resume files will be saved here")
    print(f"     ├── src/             # Source code")
    print(f"     └── .env             # Environment variables")
    
    print("\n🔍 Checking for required files in input/ directory:")
    all_files_exist = True
    for file, description in required_files.items():
        file_path = input_dir / file
        exists = file_path.exists()
        status = "✅" if exists else "❌"
        print(f"   {status} {file}: {description}")
        if not exists:
            all_files_exist = False
    
    if not all_files_exist:
        print("\n❌ Some required files are missing. Please add them to the input/ directory.")
        print("   You can copy your files like this:")
        print(f"   cp /path/to/your/resume.md {input_dir}/")
        print(f"   cp /path/to/your/resume.docx {input_dir}/")
        print(f"   echo 'Job description here' > {input_dir}/jobdescription.txt")
    else:
        print("\n✅ All required files are present!")
    
    # Check for .env file
    env_file = base_dir / ".env"
    if not env_file.exists():
        print("\n🔧 Creating .env file from .env.example")
        example_env = base_dir / ".env.example"
        if example_env.exists():
            shutil.copy(example_env, env_file)
            print(f"   Created {env_file}")
            print("   Please update it with your Google Cloud credentials")
        else:
            print("❌ .env.example not found. Please create a .env file manually.")
    else:
        print("\n✅ .env file exists")
    
    # Check Python dependencies
    print("\n🔍 Checking Python dependencies...")
    try:
        import langchain_google_vertexai
        import python_dotenv
        import python_docx
        print("✅ All required Python packages are installed")
    except ImportError as e:
        print(f"❌ Missing Python package: {e.name}")
        print("   Install dependencies with: pip install -r requirements.txt")
    
    print("\n🎉 Setup complete!")
    if all_files_exist:
        print("\nTo generate a resume objective, run:")
        print("   python -m resume_ai")
    else:
        print("\nPlease add the missing files and run this script again.")

if __name__ == "__main__":
    setup_project()

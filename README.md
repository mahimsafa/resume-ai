# Resume AI

An AI-powered tool that generates tailored career objectives for your resume based on job descriptions.

## Features

- Generates personalized career objectives using AI
- Updates your DOCX resume with the new objective
- Creates descriptive filenames based on job role and company
- Preserves formatting and styling of your resume
- Easy to use command-line interface

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mahimsafa/resume-ai.git
   cd resume-ai
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install in development mode:
   ```bash
   pip install -e .
   ```

3. Set up your environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your Google Cloud credentials.

## Usage

1. Prepare your files:
   - Place your resume in `resume.md` (markdown format)
   - Create a `resume.docx` with a placeholder `<objective_here>` where you want the objective to be inserted
   - Add the job description to `jobdescription.txt`

2. Run the tool:
   ```bash
   python -m resume_ai
   ```
   Or if installed with pip:
   ```bash
   resume-ai
   ```

3. The tool will:
   - Read your resume and the job description
   - Generate a tailored objective
   - Update your resume with the new objective
   - Save it with a descriptive filename

## Project Structure

```
resume-ai/
├── src/
│   └── resume_ai/
│       ├── __init__.py
│       ├── app.py              # Main application
│       ├── services/           # Service classes
│       │   ├── __init__.py
│       │   ├── ai_service.py   # AI-related functionality
│       │   └── document_service.py  # Document handling
│       └── utils/              # Utility functions
│           ├── __init__.py
│           └── file_utils.py   # File operations
├── .env.example               # Example environment variables
├── README.md                  # This file
├── requirements.txt           # Python dependencies
└── setup.py                   # Package configuration
```

## Requirements

- Python 3.8+
- Google Cloud credentials (for Vertex AI)
- A DOCX resume with a placeholder `<objective_here>`
- A markdown version of your resume

## License

MIT

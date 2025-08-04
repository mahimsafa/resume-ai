# Resume AI

An AI-powered tool that generates tailored career objectives and cover letters for your resume based on job descriptions using Google's Gemini AI model. The project provides both a Command Line Interface (CLI) and a REST API.

## ✨ Features

- **Dual Interface**: Choose between CLI or REST API based on your needs
- **AI-Powered Generation**: Creates personalized career objectives and cover letters using Google's Gemini AI
- **Seamless DOCX Integration**: Updates your Word resume while preserving all formatting and styles
- **Smart Filenames**: Automatically generates descriptive filenames based on job role and company
- **Modern API**: Built with FastAPI for high performance and automatic documentation
- **Error Handling**: Comprehensive error handling and user feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Cloud Account with Vertex AI enabled
- A DOCX resume with a placeholder `<objective_here>`

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mahimsafa/resume-ai.git
   cd resume-ai
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud credentials**:
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account key file
   - Or use `gcloud auth application-default login` if you have the Google Cloud SDK installed

## 🛠️ Usage

### Command Line Interface (CLI)

1. **Prepare your files**:
   - Create an `input` directory if it doesn't exist
   - Place your resume in `input/resume.md`
   - Place your job description in `input/jobdescription.txt`
   - Place your resume template (with `<objective_here>` placeholder) in `input/resume.docx`

2. **Run the CLI tool**:
   ```bash
   # Generate a resume with objective
   python cmd.py generate input/jobdescription.txt
   
   # Generate with cover letter
   python cmd.py generate input/jobdescription.txt --cv --company "Company Name"
   
   # Generate PDF version
   python cmd.py generate input/jobdescription.txt --pdf
   ```

3. **Find your updated files** in the `generated/` directory with descriptive filenames.

### REST API

1. **Start the API server**:
   ```bash
   # Development (auto-reload on changes)
   uvicorn main:app --reload
   
   # Production
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **API Endpoints**:

   - **GET /** - Welcome message and API documentation
   - **POST /queue/** - Process a job application
     
     Example request:
     ```bash
     curl -X POST "http://localhost:8000/queue/?generate_cv=true" \
          -H "Content-Type: application/json" \
          -d '{
                "job_description": "Job description here...",
                "company_name": "Tech Corp",
                "tone": "professional"
              }'
     ```

3. **Interactive API documentation** available at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### File Structure
```
input/
├── resume.md          # Your resume in markdown format
├── resume.docx        # Your resume with <objective_here> placeholder
└── jobdescription.txt # The job description
generated/             # Output directory for generated files
```

## 🏗️ Project Structure

```
resume-ai/
├── input/                  # Input files (manually added)
│   ├── resume.md
│   ├── resume.docx
│   └── jobdescription.txt
├── generated/             # Generated files (auto-created)
├── lib/                   # Core functionality modules
│   ├── objective_generator.py  # AI-powered objective generation
│   ├── cover_letter_generator.py  # Cover letter generation
│   └── pdf_utils.py       # PDF and DOCX manipulation
├── main.py                # FastAPI application
├── cmd.py                 # Command Line Interface
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:

```ini
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_PROJECT=your-project-id

# API Configuration (optional)
API_HOST=0.0.0.0
API_PORT=8000
```

### Customizing Prompts
You can customize the AI prompts in the respective generator modules:
- `lib/objective_generator.py` - For career objective generation
- `lib/cover_letter_generator.py` - For cover letter generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Powered by [Google Gemini AI](https://ai.google/)
- Built with [python-docx](https://python-docx.readthedocs.io/)
- Project structure inspired by [Python Packaging Authority](https://packaging.python.org/)

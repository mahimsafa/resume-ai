# Resume AI

An AI-powered tool that generates tailored career objectives for your resume based on job descriptions using Google's Gemini AI model.

## ✨ Features

- **AI-Powered Objective Generation**: Creates personalized career objectives using Google's Gemini AI
- **Seamless DOCX Integration**: Updates your Word resume while preserving all formatting and styles
- **Smart Filenames**: Automatically generates descriptive filenames based on job role and company
- **Modular Architecture**: Clean separation of concerns with dedicated service modules
- **Error Handling**: Comprehensive error handling and user feedback
- **Configurable**: Customize fonts, styles, and file locations

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
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Google Cloud project details.

## 🛠️ Usage

### Basic Usage

1. **Prepare your files** in the `input/` directory:
   ```
   input/
   ├── resume.md          # Your resume in markdown format
   ├── resume.docx        # Your resume with <objective_here> placeholder
   └── jobdescription.txt # The job description
   ```

2. **Run the tool**:
   ```bash
   python main.py
   ```
   Or for a specific job description:
   ```bash
   python main.py input/jobdescription.txt
   ```

3. **Find your updated resume** in the `generated/` directory with a descriptive filename.

### Advanced Usage

#### Customize Output Directory
```bash
python main.py --output custom-output/
```

#### Specify Custom Input Files
```bash
python main.py --resume input/my-resume.md --docx input/my-resume.docx --job input/job-posting.txt
```

## 🏗️ Project Structure

```
resume-ai/
├── input/                  # Input files (manually added)
│   ├── resume.md
│   ├── resume.docx
│   └── jobdescription.txt
├── generated/             # Generated resumes (auto-created)
├── src/
│   └── resume_ai/
│       ├── __init__.py
│       ├── app.py              # Main application class
│       ├── services/           # Service layer
│       │   ├── __init__.py
│       │   ├── ai_service.py   # AI integration with Gemini
│       │   └── document_service.py  # DOCX manipulation
│       └── utils/              # Helper functions
│           ├── __init__.py
│           └── file_utils.py   # File operations
├── .env.example           # Environment variables template
├── .gitignore
├── README.md
├── requirements.txt       # Python dependencies
├── setup.py              # Package configuration
└── setup_project.py      # Project setup helper
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```ini
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_PROJECT=your-project-id
```

### Customizing the Prompt
Edit the prompt template in `src/resume_ai/services/ai_service.py` to adjust how the AI generates objectives.

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

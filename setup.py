from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="resume-ai",
    version="0.1.0",
    author="Mahim",
    author_email="your.email@example.com",
    description="AI-powered resume objective generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/resume-ai",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "langchain-google-vertexai>=0.1.0",
        "python-docx>=0.8.11",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        "console_scripts": [
            "resume-ai=resume_ai.app:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

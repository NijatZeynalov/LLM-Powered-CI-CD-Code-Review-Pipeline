# LLM Powered CI/CD Code Review Pipeline

An automated code review system powered by LLaMA (via Groq) that provides intelligent feedback on pull requests. This tool automatically analyzes code changes, performs security checks, validates style guidelines, and provides AI-powered suggestions for improvement.

## Features

- **Automated Code Analysis**: Uses LLaMA to analyze code quality and suggest improvements
- **Security Scanning**: Identifies potential security vulnerabilities
- **Style Guide Enforcement**: Ensures code follows Python best practices
- **Documentation Validation**: Checks for proper documentation
- **Automated PR Feedback**: Posts review comments directly on pull requests

## Technology Stack

- GitHub Actions
- Python 3.10+
- Groq API (LLaMA)
- LangChain
- Bandit (Security Scanner)
- Pylint (Style Checker)
- Black (Code Formatter)

## Prerequisites

- GitHub repository with Python code
- Groq API account and key
- GitHub Actions enabled on your repository

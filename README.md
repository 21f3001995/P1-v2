# LLM Code Deployment

> Automated web application generation, deployment, and iteration powered by Large Language Models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

LLM Code Deployment is an intelligent automation pipeline that transforms structured application briefs into fully deployed web applications. The system leverages large language models to generate, iterate, and deploy production-ready code while maintaining professional development workflows.

### Key Capabilities

- **Automated Code Generation**: Convert structured briefs and requirements into complete HTML/CSS/JavaScript applications
- **Iterative Development**: Support multiple rounds of updates, enhancements, and refactoring without losing previous work
- **Intelligent Repository Management**: Automatic GitHub repository creation, updates, and version control
- **Live Deployment**: One-click deployment to GitHub Pages with automated configuration
- **Evaluation Integration**: Built-in notification system for automated code review and quality assessment
- **Professional Documentation**: Auto-generated README files, MIT licensing, and organized project structure


## Features

### 1. Intelligent Code Generation
- Processes structured application briefs with requirements and constraints
- Handles multiple attachment formats (CSV, JSON, Markdown)
- Generates clean, maintainable HTML/CSS/JavaScript code
- Supports iterative improvements and feature additions

### 2. Automated Repository Workflow
- Creates dedicated GitHub repositories for each project
- Organizes attachments in isolated `/attachments` directory
- Generates comprehensive documentation automatically
- Includes MIT License for open-source compliance

### 3. Seamless Deployment
- Automatic GitHub Pages configuration and activation
- Asynchronous monitoring of deployment status
- Live URL generation and verification
- Rollback support for failed deployments

### 4. Evaluation & Monitoring
- RESTful API integration for automated evaluation
- Retry mechanism with exponential backoff
- Detailed logging of all operations
- Commit SHA tracking for version control

### 5. Developer Experience
- Clean, modular codebase architecture
- Comprehensive error handling and logging
- Support for local testing with mock endpoints
- Extensible plugin system for custom workflows

## How It Works

### Workflow Overview

1. **Request Reception**: System receives a structured application brief via HTTP POST with requirements, attachments, and specifications

2. **LLM Processing**: The brief is processed by a large language model that generates complete, production-ready web application code

3. **Repository Creation**: A dedicated GitHub repository is automatically created with proper structure and documentation

4. **Deployment**: GitHub Pages is configured and activated, making the application immediately accessible via a live URL

5. **Evaluation Notification**: Metadata including repository URL, commit SHA, and deployment link is sent to evaluation services

### Example Workflow

A typical request includes:
- **Task ID**: Unique identifier for the project
- **Brief**: Detailed description of the application requirements
- **Attachments**: Supporting files (CSV data, specifications, mockups)
- **Round Number**: Enables iterative updates and refinements

The system then autonomously handles code generation, git operations, deployment, and notification - delivering a fully functional web application in minutes.


## Acknowledgments

Built with modern LLM capabilities and professional development practices to enable rapid, iterative web application development.

---

# Resume Builder

A function to apply different resume formats to a standardized resume using LaTex and Jinja2 templates.

## Current Status
- **Phase:** MVP Development
- **Progress:** Initial templating complete, working on resume formatting and tracking, and end to end testing
- **Target:** End-to-end workflow by May 1, 2026

## Components
- ✅ **YAML Resume Structure** - Structured resume data 
- ✅ **LaTeX Template System** - PDF generation via Jinja2
- 🔄 **Resume Versioning** - Structured resume data  (in progress)
- 🔄 **End to End testing** - Validate resume and template compatibility (in progress)
- ⏳ **Template Versioning** - Structured resume data  (in progress)
- ⏳ **Additional Templates** - Structured resume data  (planned)
- ⏳ **API Endpoints** - Automated job posting collection (planned)
- ⏳ **CLI Endpoints** - Automated job posting collection (planned)
- ⏳ **AI Optimization** - Standardized resume formats for AI optimization (future)

## Quick Start
```bash
# Generate resume PDF
python resume_builder.py resume/resume_v0_0_0.json

# View current resume structure
cat resume/resume_v0_0_0.json | jq '.contact_info'
```

## Architecture
- **Data:** YAML resume structure with metadata and versioning
- **Templates:** LaTeX templates with Jinja2 for customization
- **Output:** PDF resumes via LaTeX compilation

## Recent Changes
- Designed standardized resume.json structure
- Implemented resume_builder python function
- Created a templated LaTeX file for 

## Recent Changes
- Updating to YAML structure
- Researching application tracking system design

## Links
- **Resume Data:** [resume/resume.json](resume/resume.json)
- **Main Builder:** [resume_builder.py](resume_builder.py)
- **Templates:** [templates/](templates/)
- **Tests:** [tests/](tests/)
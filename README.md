# Resume Builder
Using a standardized resume format to enable flexible resume updates and generation with LaTex and Jinja2 templates.

## ;TLDR
Creating a good resume with good content AND an aesthetically pleasing layout is difficult. This project attempts to simplify 
this work needed by separating resume content and resume design. Using a standardized resume format (YAML)
we can focus on resume content without worrying about resume design. After finalizing content we can choose a resume from the
template library to see what existing design most fits job or personal requirements. Because templates are written in latex
they can be easily modified and added to the resume library for future uses. 

## Current Status
- **Phase:** Application testing
- **Progress:** Initial templating, resume generation, and end-to-end testing complete. Shared online and working on integration with my application process
- **Target:** Project usage feedback by July 1st

## Components
- ✅ **YAML Resume Structure** - Structured resume data 
- ✅ **LaTeX Template System** - PDF generation via Jinja2
- ✅ **End to End testing** - Validate resume and template compatibility (in progress)
- ✅ **Resume Versioning** - Structured resume data  (in progress)
- ✅ **Template Versioning** - Structured resume data  (in progress)
- ✅ **Additional Templates** - Structured resume data  (planned)
- ⏳ **API Endpoints** - Automated job posting collection (planned)
- ⏳ **CLI Endpoints** - Automated job posting collection (planned)
- ⏳ **AI Optimization** - Standardized resume formats for AI optimization (future)
- ⏳ **Cloud hosted** - Host a version in the cloud for api usage (future)

## Quick Start
```bash
# Generate resume PDF from a resume.yaml file choosing the classic.tex template
resume-builder --resume resume.yaml --template classic.tex --output resume.tex --pdf resume_pdf/
```

## Architecture
- **Data:** YAML resume structure with metadata and versioning
- **Templates:** LaTeX templates with Jinja2 for customization
- **Output:** PDF resumes via LaTeX compilation

## Links
- **Resume Data:** [resume/resume.json](resume/resume.json)
- **Main Builder:** [resume_builder.py](resume_builder/resume_builder.py)
- **Templates:** [templates/](resume_builder/templates/)
- **Tests:** [tests/](tests/)
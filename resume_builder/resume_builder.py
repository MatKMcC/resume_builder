#!/usr/bin/env python3
"""
Resume Builder with Jinja2 Templates

This script generates LaTeX resumes using Jinja2 templating for clean, maintainable templates.
It reads structured JSON data and renders it through LaTeX templates with advanced logic.
"""

import json
import yaml
import sys
import subprocess
import argparse
from pathlib import Path
import logging
from typing import Dict, Any

from jinja2 import Environment, FileSystemLoader, TemplateError
from pylatex import utils as plutils

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Jinja2ResumeBuilder:
    def __init__(self):
        # Set up Jinja2 environment with LaTeX-compatible delimiters

        package_dir = Path(__file__).parent
        templates_dirs = [str(package_dir / 'templates')]

        self.jinja_env = Environment(
            loader=FileSystemLoader(templates_dirs),
            # LaTeX uses { } heavily, so we use different delimiters
            variable_start_string='<<',
            variable_end_string='>>',
            block_start_string='<%',
            block_end_string='%>',
            comment_start_string='<#',
            comment_end_string='#>',
            # Important: don't strip whitespace automatically in LaTeX
            trim_blocks=False,
            lstrip_blocks=False
        )
        
        # Register custom filters for LaTeX processing
        self.jinja_env.filters['latex_escape'] = self.latex_escape
        
        self.resume_data = None
        
    def latex_escape(self, text):
        """Escape special LaTeX characters"""
        return plutils.escape_latex(text)
    
    def load_resume_data(self, file_path: Path) -> Dict[str, Any]:
        """
        Load resume data from JSON or YAML file.

        Args:
            file_path: Path to resume file

        Returns:
            Resume data dictionary
        """

        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                self.resume_data = yaml.safe_load(f)
            except yaml.YAMLError:
                self.resume_data = json.load(f)

        return self.resume_data
    
    def generate_latex(self, template_name):
        """Generate LaTeX content using Jinja2 template"""
        if not self.resume_data:
            logger.error("✗ No resume data loaded")
            return None
        
        try:
            template = self.jinja_env.get_template(template_name)
            
            # Render template
            latex_content = template.render(**self.resume_data)
            logger.info("✅ Template rendered successfully")
            return latex_content
            
        except TemplateError as e:
            logger.error(f"✗ Template error: {e}")
            return None
        except Exception as e:
            logger.error(f"✗ Error generating LaTeX: {e}")
            return None
    
    def save_latex(self, content, output_path):
        """Save generated LaTeX content to file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ LaTeX saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"✗ Error saving LaTeX: {e}")
            return False
    
    def compile_pdf(self, tex_file, pdf_file):
        """Compile LaTeX to PDF using pdflatex"""
        try:
            logger.info(f"📄 Compiling PDF: {pdf_file}")
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', f'-output-directory={pdf_file}', tex_file],
                capture_output=True, 
                text=True, 
                timeout=60
            )
            
            if result.returncode == 0:
                logger.info(f"✅ PDF generated successfully: {pdf_file}")
                return True
            else:
                logger.warning("⚠️ LaTeX compilation had warnings/errors")
                logger.debug(f"LaTeX output:\n{result.stdout}")
                # Check if PDF was still created
                if Path(pdf_file).exists():
                    logger.info(f"✅ PDF was created despite warnings: {pdf_file}")
                    return True
                else:
                    logger.error("✗ PDF was not created")
                    return False
                    
        except FileNotFoundError:
            logger.warning("⚠️ pdflatex not found. Install LaTeX to compile PDF automatically.")
            logger.info(f"📝 You can manually compile with: pdflatex {tex_file}")
            return False
        except subprocess.TimeoutExpired:
            logger.error("✗ LaTeX compilation timed out")
            return False
        except Exception as e:
            logger.error(f"✗ PDF compilation error: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Generate resume PDF using Jinja2 LaTeX templates')
    parser.add_argument('--template', default='green_side_bar.tex', help='Template file to use')
    parser.add_argument('--resume', help='Resume file')
    parser.add_argument('--output', help='Output LaTeX file')
    parser.add_argument('--pdf', help='Output PDF Directory')
    parser.add_argument('--no-compile', action='store_true', help='Skip PDF compilation')
    
    args = parser.parse_args()
    
    # Check if input files exist
    if not Path(args.resume).exists():
        logger.error(f"✗ Resume JSON not found: {args.resume}")
        sys.exit(1)

    # TODO: This should be updated to not check paths but jinja templates
    # if not Path('templates', args.template).exists():
    #     logger.error(f"✗ Template not found: {args.template}")
    #     sys.exit(1)
    
    # Initialize builder
    builder = Jinja2ResumeBuilder()
    
    # Load resume data
    logger.info(f"📖 Reading resume data: {args.resume}")
    if not builder.load_resume_data(args.resume):
        sys.exit(1)
    
    # Generate LaTeX
    logger.info(f"📄 Rendering template: {args.template}")
    latex_content = builder.generate_latex(args.template)
    
    if not latex_content:
        logger.error("✗ Failed to generate LaTeX content")
        sys.exit(1)
    
    # Save LaTeX file
    logger.info(f"💾 Saving LaTeX: {args.output}")
    if not builder.save_latex(latex_content, args.output):
        sys.exit(1)
    
    # Compile PDF (optional)
    if not args.no_compile:
        success = builder.compile_pdf(args.output, args.pdf)
        if success:
            logger.info("🎉 Resume generation complete!")
            logger.info(f"📄 Generated files:")
            logger.info(f"   - {args.output} (LaTeX source)")
            logger.info(f"   - {args.pdf} (PDF output)")
        else:
            logger.info(f"⚠️ PDF compilation failed, but LaTeX was created: {args.output}")
    else:
        logger.info("🎉 LaTeX generation complete!")
        logger.info(f"📄 Generated: {args.output}")
        logger.info(f"💡 Compile manually with: pdflatex {args.output}")


if __name__ == "__main__":
    main()

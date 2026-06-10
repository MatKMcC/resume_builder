"""
End-to-end integration tests for the resume builder.

These tests validate the complete workflow:
1. Load resume JSON data
2. Generate LaTeX output via templates
3. Validate output against expected results
4. Ensure the complete pipeline works correctly
"""

import pytest
import json
from pathlib import Path
import tempfile
import shutil
import difflib
import sys

# Add project root to path so we can import the resume builder
sys.path.insert(0, str(Path(__file__).parent.parent))

from resume_builder import Jinja2ResumeBuilder


@pytest.mark.integration
class TestEndToEndResumeGeneration:
    """End-to-end tests for complete resume generation workflow."""
    
    @pytest.fixture
    def resume_builder(self):
        """Create a resume builder instance for testing."""
        return Jinja2ResumeBuilder()
    
    @pytest.fixture
    def test_resume_data(self, resume_builder):
        """Load the test resume data (v0.0.0 format)."""
        # We'll use the existing test data, but you mentioned schema file
        # Let's use the actual resume data instead
        test_resume_path = Path(__file__).parent / "fixtures" / "resume_v0_0_0.json"
        
        if not test_resume_path.exists():
            pytest.skip(f"Test resume data not found at {test_resume_path}")

        return resume_builder.load_resume_data(test_resume_path)
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary directory for test outputs."""
        temp_dir = Path(tempfile.mkdtemp(prefix="resume_e2e_test_"))
        yield temp_dir
        # Cleanup after test
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def expected_output_path(self):
        """Path to expected LaTeX output file."""
        return Path(__file__).parent / "expected_outputs" / "green_side_bar.tex"
    
    def test_compare_latex_outputs_integration(self, resume_builder, test_resume_data, temp_output_dir, expected_output_path):
        """
        Integration test that compares generated LaTeX with expected output.
        
        This test validates that our LaTeX generation produces consistent results.
        """
        # Generate LaTeX using resume builder
        resume_builder.resume_data = test_resume_data
        generated_output = resume_builder.generate_latex("green_side_bar.tex")
        assert generated_output is not None, "Failed to generate LaTeX output"

        # Step 4: Save the generated output for comparison
        generated_output_path = temp_output_dir / "generated_resume_output.tex"
        with open(generated_output_path, 'w', encoding='utf-8') as f:
            f.write(generated_output)

        # Load expected output files
        if not expected_output_path.exists():
            pytest.fail(f"Expected output file missing: {expected_output_path}. "
                       f"Run 'python tests/test_resume_builder.py' to generate it first.")
        with open(expected_output_path, 'r', encoding='utf-8') as f:
            expected_output = f.read()

        # Compare created LaTeX file with the expected output
        # Normalize whitespace for comparison (LaTeX is sensitive but we can be flexible)
        generated_lines = [line.strip() for line in generated_output.split('\n') if line.strip()]
        expected_lines = [line.strip() for line in expected_output.split('\n') if line.strip()]

        # Create detailed diff if there are differences
        if expected_lines != generated_lines:
            diff = difflib.unified_diff(
                expected_lines,
                generated_lines,
                lineterm=''
            )
            diff_text = '\n'.join(diff)

            # Show a helpful error message
            pytest.fail(
                f"Generated LaTeX does not match expected output!\n"
                f"Expected file: {expected_output_path}\n"
                f"Generated file: {generated_output_path}\n\n"
                f"Differences:\n{diff_text}"
            )
    
    def test_latex_document_structure(self, resume_builder, test_resume_data):
        """
        Test that generated LaTeX has proper document structure.
        
        This is a more granular test that validates specific aspects.
        """
        resume_builder.resume_data = test_resume_data
        latex_output = resume_builder.generate_latex("green_side_bar.tex")
        
        assert latex_output is not None, "LaTeX generation failed"
        
        # Test basic LaTeX document structure
        assert "\\documentclass" in latex_output, "Missing document class"
        assert "\\begin{document}" in latex_output, "Missing document begin"
        assert "\\end{document}" in latex_output, "Missing document end"
        
        # Test that contact information appears in output
        contact_info = test_resume_data.get('contact_info', {})
        if contact_info.get('name'):
            assert contact_info['name'] in latex_output, f"Name '{contact_info['name']}' not found in output"
        if contact_info.get('email'):
            assert contact_info['email'] in latex_output, f"Email '{contact_info['email']}' not found in output"
    
    def test_template_variable_substitution(self, resume_builder, test_resume_data):
        """
        Test that template variables are properly substituted.
        
        This test validates that our Jinja2 templating is working correctly.
        """
        resume_builder.resume_data = test_resume_data
        latex_output = resume_builder.generate_latex("green_side_bar.tex")
        
        assert latex_output is not None, "LaTeX generation failed"
        
        # Ensure no template variables remain unsubstituted
        # These are the Jinja2 delimiters we defined in resume_builder.py
        assert "<<" not in latex_output, "Unsubstituted template variables found (<<)"
        assert ">>" not in latex_output, "Unsubstituted template variables found (>>)"
        assert "<%=" not in latex_output, "Unsubstituted template expressions found"
        assert "%>" not in latex_output, "Unsubstituted template blocks found"
    
    @pytest.mark.slow
    def test_pdf_compilation_works(self, resume_builder, test_resume_data, temp_output_dir):
        """
        Test that generated LaTeX can actually be compiled to PDF.
        
        This is marked as 'slow' because PDF compilation takes time.
        """
        import subprocess
        import shutil
        
        # Check if pdflatex is available
        if not shutil.which("pdflatex"):
            pytest.skip("pdflatex not available - cannot test PDF compilation")
        
        resume_builder.resume_data = test_resume_data
        latex_output = resume_builder.generate_latex("green_side_bar.tex")
        
        assert latex_output is not None, "LaTeX generation failed"
        
        # Save LaTeX to temporary file
        tex_file = temp_output_dir / "test_resume.tex"
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_output)
        
        # Try to compile to PDF
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', f'-output-directory={temp_output_dir}', str(tex_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check that PDF was created
            pdf_file = temp_output_dir / "test_resume.pdf"
            assert pdf_file.exists(), f"PDF compilation failed. Output: {result.stdout}\nErrors: {result.stderr}"
            
            # Check PDF file size is reasonable (not empty)
            assert pdf_file.stat().st_size > 1000, "Generated PDF seems too small"
            
        except subprocess.TimeoutExpired:
            pytest.fail("PDF compilation timed out - possibly infinite loop in LaTeX")
        except Exception as e:
            pytest.fail(f"PDF compilation failed with error: {e}")


# Helper function for creating expected output
def create_expected_output_helper():
    """
    Helper function to generate expected output file.
    
    Run this separately to create the 'golden' output file that we'll compare against.
    This is not a test - it's a utility for test setup.
    """
    # This function shows you how to create the expected output
    builder = Jinja2ResumeBuilder()
    
    test_resume_path = Path(__file__).parent / "fixtures" / "resume_v0_0_0.json"
    with open(test_resume_path, 'r') as f:
        builder.resume_data = json.load(f)
    
    latex_output = builder.generate_latex("green_side_bar.tex")
    
    expected_output_dir = Path(__file__).parent / "expected_outputs"
    expected_output_dir.mkdir(exist_ok=True)
    
    expected_output_path = expected_output_dir / "green_side_bar.tex"
    with open(expected_output_path, 'w', encoding='utf-8') as f:
        f.write(latex_output)
    
    print(f"Created expected output at: {expected_output_path}")


if __name__ == "__main__":
    # If you run this file directly, it will create the expected output
    create_expected_output_helper()

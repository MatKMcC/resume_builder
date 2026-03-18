"""
Test template rendering across versions and template types.

Tests ensure that:
1. Templates render correctly for each resume version
2. Template-specific features work properly
3. LaTeX output is valid and consistent
4. Template version compatibility is maintained
"""

import pytest
from pathlib import Path
from typing import Optional
import tempfile
import re

# -------------- Conf Test Files

#
#
# @pytest.fixture
# def temp_output_dir():
#     """Create temporary directory for test outputs."""
#     temp_dir = tempfile.mkdtemp(prefix="resume_test_")
#     yield Path(temp_dir)
#     # Cleanup after test
#     shutil.rmtree(temp_dir)
#
#
# @pytest.fixture
# def expected_output(resume_version, template_type, test_data_dir):
#     """Load expected output for version/template combination."""
#     expected_file = (EXPECTED_OUTPUT_DIR /
#                     f"resume_v{resume_version.replace('.', '_')}_{template_type}.tex")
#
#     if not expected_file.exists():
#         return None  # Skip comparison if no expected output
#
#     with open(expected_file, 'r') as f:
#         return f.read()
#
#
# @pytest.fixture(scope="session")
# def resume_builder():
#     """Import and return the ResumeBuilder class."""
#     import sys
#     from pathlib import Path
#
#     # Add project root to path
#     project_root = Path(__file__).parent.parent
#     sys.path.insert(0, str(project_root))
#
#     from resume_builder import Jinja2ResumeBuilder
#     return Jinja2ResumeBuilder
#
#
# class ResumeTestHelper:
#     """Helper class for common resume testing operations."""
#

#
#     @staticmethod
#     def compare_template_outputs(output1: str, output2: str, tolerance: float = 0.9) -> bool:
#         """Compare template outputs with some tolerance for minor differences."""
#         if not output1 or not output2:
#             return False
#
#         # Simple similarity check - can be enhanced
#         lines1 = set(line.strip() for line in output1.split('\n') if line.strip())
#         lines2 = set(line.strip() for line in output2.split('\n') if line.strip())
#
#         if not lines1 or not lines2:
#             return output1.strip() == output2.strip()
#
#         intersection = len(lines1.intersection(lines2))
#         union = len(lines1.union(lines2))
#
#         similarity = intersection / union if union > 0 else 0
#         return similarity >= tolerance
#
#
# @pytest.fixture
# def resume_helper():
#     """Provide ResumeTestHelper instance."""
#     return ResumeTestHelper()




@pytest.fixture(params=TEMPLATE_VERSIONS)
def template_type(request):
    """Parametrized fixture that provides each template type."""
    return request.param


# -------------- Template Test Files
@pytest.mark.template
class TestTemplateRendering:
    """Test template rendering functionality."""

    def test_template_renders_without_error(self, resume_builder, resume_data, template_type, temp_output_dir):
        """Test that templates render without errors for each resume version."""
        builder = resume_builder()
        builder.load_resume_data_from_dict(resume_data)
        
        try:
            # Attempt to render template
            latex_output = builder.render_template(template_type)
            assert latex_output is not None
            assert len(latex_output) > 0
            
            # Save output for inspection
            output_file = temp_output_dir / f"test_{template_type}_{resume_data['metadata']['version']}.tex"
            with open(output_file, 'w') as f:
                f.write(latex_output)
                
        except Exception as e:
            pytest.fail(f"Template {template_type} failed to render: {e}")

    def test_required_latex_structure(self, resume_builder, resume_data, template_type):
        """Test that rendered LaTeX has required document structure."""
        builder = resume_builder()
        builder.load_resume_data_from_dict(resume_data)
        
        latex_output = builder.render_template(template_type)
        
        # Check for required LaTeX document structure
        required_elements = [
            r'\\documentclass',
            r'\\begin{document}',
            r'\\end{document}'
        ]
        
        for element in required_elements:
            assert re.search(element, latex_output), f"Missing {element} in {template_type} template"

    def test_contact_info_rendered(self, resume_builder, resume_data, template_type):
        """Test that contact information is properly rendered in templates."""
        builder = resume_builder()
        builder.load_resume_data_from_dict(resume_data)
        
        latex_output = builder.render_template(template_type)
        contact = resume_data['contact_info']
        
        # Check that contact info appears in output
        assert contact['name'] in latex_output, f"Name missing from {template_type} output"
        assert contact['email'] in latex_output, f"Email missing from {template_type} output"

    def test_latex_escaping(self, resume_builder, template_type):
        """Test that special LaTeX characters are properly escaped."""
        # Create resume with special characters that need escaping
        test_resume = {
            "metadata": {"version": "1.0.0"},
            "contact_info": {
                "name": "Test & User",  # & needs escaping
                "email": "test@example.com",
                "phone": "$100K+ earner",  # $ needs escaping
                "location": "Test City, ST"
            },
            "professional_summary": {
                "content": "Expert in C++ & Python with 100% success rate"  # &, % need escaping
            },
            "companies": [],
            "achievements": [],
            "education": [],
            "skills": {"technical": {"programming": []}}
        }
        
        builder = resume_builder()
        builder.load_resume_data_from_dict(test_resume)
        
        latex_output = builder.render_template(template_type)
        
        # Check that special characters are escaped
        assert '\\&' in latex_output or 'Test \\& User' in latex_output
        assert '\\$' in latex_output or not '$100K+' in latex_output
        assert '\\%' in latex_output or not '100% success' in latex_output

    @pytest.mark.parametrize("section", ['companies', 'achievements', 'education'])
    def test_section_rendering(self, resume_builder, resume_data, template_type, section):
        """Test that each resume section renders properly."""
        if not resume_data[section]:  # Skip if section is empty
            pytest.skip(f"No {section} data to test")
            
        builder = resume_builder()
        builder.load_resume_data_from_dict(resume_data)
        
        latex_output = builder.render_template(template_type)
        
        # Check that section content appears
        section_data = resume_data[section]
        if isinstance(section_data, list) and section_data:
            # For list sections, check first item
            first_item = section_data[0]
            if isinstance(first_item, dict):
                # Look for any field from the first item
                for key, value in first_item.items():
                    if isinstance(value, str) and value:
                        assert value in latex_output, f"{section} content missing from {template_type}"
                        break

    def test_template_version_consistency(self, resume_builder, template_type):
        """Test that template works consistently across resume versions."""
        versions_tested = []
        outputs = []
        
        # Test with different version formats
        test_versions = [
            {"version": "1.0.0", "schema_version": "1.0"},
            {"version": "2.0.0", "schema_version": "2.0", "created": "2026-01-01"}
        ]
        
        base_resume = {
            "contact_info": {
                "name": "Test User",
                "email": "test@example.com"
            },
            "professional_summary": {"content": "Test summary"},
            "companies": [],
            "achievements": [],
            "education": [],
            "skills": {"technical": {"programming": ["Python"]}}
        }
        
        for version_meta in test_versions:
            test_resume = base_resume.copy()
            test_resume["metadata"] = version_meta
            
            builder = resume_builder()
            builder.load_resume_data_from_dict(test_resume)
            
            try:
                output = builder.render_template(template_type)
                outputs.append(output)
                versions_tested.append(version_meta["version"])
            except Exception as e:
                pytest.fail(f"Template {template_type} failed for version {version_meta['version']}: {e}")
        
        # All versions should produce valid output
        assert len(outputs) == len(test_versions)
        assert all(len(output) > 0 for output in outputs)


@pytest.mark.template
class TestTemplateSpecificFeatures:
    """Test features specific to each template type."""

    def test_classic_template_features(self, resume_builder, mock_resume_minimal):
        """Test classic template specific features."""
        if not self._template_exists("classic"):
            pytest.skip("Classic template not found")
            
        builder = resume_builder()
        builder.load_resume_data_from_dict(mock_resume_minimal)
        
        latex_output = builder.render_template("classic")
        
        # Classic template should be simple and clean
        # Add specific assertions for classic template features
        assert latex_output is not None

    def test_modern_template_features(self, resume_builder, mock_resume_minimal):
        """Test modern template specific features."""
        if not self._template_exists("modern"):
            pytest.skip("Modern template not found")
            
        builder = resume_builder()
        builder.load_resume_data_from_dict(mock_resume_minimal)
        
        latex_output = builder.render_template("modern")
        
        # Modern template might have more styling
        assert latex_output is not None

    def test_tech_focused_template_features(self, resume_builder, mock_resume_minimal):
        """Test tech-focused template specific features."""
        if not self._template_exists("tech-focused"):
            pytest.skip("Tech-focused template not found")
            
        builder = resume_builder()
        builder.load_resume_data_from_dict(mock_resume_minimal)
        
        latex_output = builder.render_template("tech-focused")
        
        # Tech template might emphasize technical skills differently
        assert latex_output is not None

    @staticmethod
    def _template_exists(template_name: str) -> bool:
        """Check if template file exists."""
        template_dir = Path(__file__).parent.parent / "templates"
        template_file = template_dir / f"{template_name}.tex"
        return template_file.exists()


@pytest.mark.template
@pytest.mark.slow
class TestTemplateOutput:
    """Test template output quality and consistency."""

    def test_output_consistency(self, resume_builder, resume_data, template_type):
        """Test that template produces consistent output for same input."""
        builder = resume_builder()
        builder.load_resume_data_from_dict(resume_data)
        
        # Generate output multiple times
        outputs = []
        for _ in range(3):
            output = builder.render_template(template_type)
            outputs.append(output)
        
        # All outputs should be identical
        assert all(output == outputs[0] for output in outputs), \
            f"Template {template_type} produces inconsistent output"

    def test_output_size_reasonable(self, resume_builder, resume_data, template_type):
        """Test that template output size is reasonable."""
        builder = resume_builder()
        builder.load_resume_data_from_dict(resume_data)
        
        latex_output = builder.render_template(template_type)
        
        # Output should be reasonable size (not empty, not huge)
        output_size = len(latex_output)
        assert 100 < output_size < 50000, \
            f"Template {template_type} output size unreasonable: {output_size} chars"

    def test_expected_output_comparison(self, resume_builder, resume_data, template_type, expected_output, resume_helper):
        """Test output against expected output if available."""
        if expected_output is None:
            pytest.skip(f"No expected output for {template_type}")
            
        builder = resume_builder()
        builder.load_resume_data_from_dict(resume_data)
        
        actual_output = builder.render_template(template_type)
        
        # Compare with expected output (with some tolerance for minor changes)
        similarity = resume_helper.compare_template_outputs(actual_output, expected_output)
        assert similarity, f"Template {template_type} output differs significantly from expected"


# Helper functions
def count_latex_commands(latex_text: str, command: str) -> int:
    """Count occurrences of a LaTeX command."""
    pattern = rf'\\{re.escape(command)}'
    return len(re.findall(pattern, latex_text))


def extract_section_content(latex_text: str, section_marker: str) -> Optional[str]:
    """Extract content from a specific section in LaTeX output."""
    pattern = rf'{re.escape(section_marker)}(.*?)(?=\\[a-zA-Z]+{{|\\end{{|$)'
    match = re.search(pattern, latex_text, re.DOTALL)
    return match.group(1).strip() if match else None







# @pytest.mark.version
# class TestVersionMigration:
#     """Test version migration and upgrade paths."""
#
#     def test_v1_to_v2_migration(self, test_data_dir):
#         """Test migration from v1.0.0 to v2.0.0."""
#         # Load v1 data
#         v1_file = test_data_dir / "resume_v0_0_0.json"
#         if not v1_file.exists():
#             pytest.skip("V1 test data not available")
#
#         with open(v1_file, 'r') as f:
#             v1_data = json.load(f)
#
#         # Perform migration (implement this in your resume_builder)
#         # migrated_data = migrate_resume_v1_to_v2(v1_data)
#
#         # For now, just test that v1 data has expected structure
#         assert 'contact_info' in v1_data
#         assert 'professional_summary' in v1_data
#
#     def test_version_detection(self, resume_data):
#         """Test that version can be detected from resume data."""
#         version = resume_data.get('metadata', {}).get('version', '1.0.0')
#         assert version in ['1.0.0', '1.1.0', '2.0.0'], f"Unknown version: {version}"
#
#     def test_backward_compatibility(self, resume_builder):
#         """Test that newer versions can still handle older resume formats."""
#         # Create minimal v1.0.0 format resume
#         v1_resume = {
#             "contact_info": {
#                 "name": "Test User",
#                 "email": "test@example.com"
#             },
#             "professional_summary": {
#                 "content": "Test summary"
#             },
#             "companies": [],
#             "achievements": [],
#             "education": [],
#             "skills": {"technical": {"programming": []}}
#         }
#
#         # Should be able to process without errors
#         builder = resume_builder()
#         try:
#             # Test that builder can handle v1 format
#             builder.load_resume_data_from_dict(v1_resume)
#         except Exception as e:
#             pytest.fail(f"Failed to handle v1.0.0 format: {e}")
#
#
# @pytest.mark.version
# @pytest.mark.slow
# class TestVersionPerformance:
#     """Test performance across different resume versions."""
#
#     def test_loading_performance(self, resume_data, resume_version):
#         """Test that resume loading is performant across versions."""
#         import time
#
#         start_time = time.time()
#         # Simulate multiple loads
#         for _ in range(10):
#             data = json.loads(json.dumps(resume_data))
#         end_time = time.time()
#
#         load_time = (end_time - start_time) / 10
#         assert load_time < 0.1, f"Loading too slow for version {resume_version}: {load_time}s"
#
#     def test_memory_usage(self, resume_data, resume_version):
#         """Test memory usage is reasonable across versions."""
#         import sys
#
#         memory_size = sys.getsizeof(json.dumps(resume_data))
#         max_size = 100 * 1024  # 100KB max
#
#         assert memory_size < max_size, f"Resume too large for version {resume_version}: {memory_size} bytes"
"""
Test resume structure across resume versions

Tests ensure that:
1. Resumes load
2. Resumes follow expected structure and have expected fields
3. Resume versions are valid and follow version expectations
"""

import pytest
import jsonschema
import re


@pytest.mark.resume_schema
class TestResumeSchema:
    """Test resume version handling and compatibility."""

    def test_schema_validation(self, resume, resume_schema):
        """Test that resume data validates against its schema."""
        try:
            jsonschema.validate(resume, resume_schema)
        except jsonschema.ValidationError as e:
            pytest.fail(f"Schema validation failed: {e.message}")


@pytest.mark.resume_structure
class TestResumeStructure:
    """Test the Resume structure rendering for resume fixtures"""

    def test_resume_load(self, resume, resume_version):
        """Test that resume data loads successfully for each version."""
        assert resume is not None
        assert isinstance(resume, dict)


    @pytest.mark.parametrize("section", [
          'contact_info'
        , 'professional_summary'
        , 'companies'
        , 'achievements'
        , 'education'
        , 'skills'
    ])
    def test_section_structure(self, resume, section, resume_version):
        """Test that each section has the expected structure."""
        assert section in resume, f"Missing {section} in version {resume_version}"


    def test_contact_info_format(self, resume, resume_version):
        """Test contact info format is consistent across versions."""
        contact = resume.get('contact_info', {})

        # Core fields should always be present
        required_fields = ['name', 'email', 'phone']
        for field in required_fields:
            assert field in contact, f"Missing {field} in version {resume_version}"
            assert contact[field], f"Empty {field} in version {resume_version}"

        # Email format validation
        email = contact['email']
        assert '@' in email and '.' in email, f"Invalid email format in version {resume_version}"

        # phone format validation
        phone = contact['phone']
        phone = "".join(char for char in phone if char.isdigit())
        assert len(phone) == 10, f"There are not 10 phone number digits in version {resume_version}"


@pytest.mark.resume_metadata
class TestResumeMetadata:
    """Test the version structure rendering for resume fixtures"""

    def test_resume_version_format(self, resume, resume_version):
        """Validate semantic version format."""
        pattern = r'^\d+\.\d+\.\d+$'
        assert bool(re.match(pattern, resume['metadata']['version']))

    @pytest.mark.parametrize("metadata", [
        'version'
        , 'resume_id'
        , 'variant'
        , 'created'
        , 'job_id'
        , 'commit_id'
    ])
    def test_metadata_structure(self, resume, metadata, resume_version):
        """Test that each section has the expected structure."""
        assert metadata in resume['metadata'], f"Missing {metadata} in version {resume_version} metadata"

    def test_resume_version(self, resume, resume_version):
        """Test that the resume version is correctly stated"""
        assert resume['metadata']['version'] == resume_version, f"Resume version {resume_version} does not match"



#!/usr/bin/env python3
"""
Tests for the Resume Imploder Module
"""

import pytest

from resume_builder.resume_imploder import ResumeImploder


class TestResumeImploder:
    """Test suite for the ResumeImploder class."""
    
    @pytest.fixture
    def imploder(self, resume_dir, manifest_pth, test_data_dir):
        """Create a ResumeExploder instance for testing."""
        return ResumeImploder(resume_dir, manifest_pth, test_data_dir)

    def manifest(self):
        pass

    def test_implode_resume(self, imploder, resume):

        # load the resume
        imploded_resume = imploder.implode()
        assert imploded_resume == resume




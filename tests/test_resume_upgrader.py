#!/usr/bin/env python3
"""
Tests for the Resume Upgrader Module
"""

import pytest

from resume_builder.resume_upgrader import ResumeUpgrader


class TestResumeUpgrader:
    """Test suite for the ResumeUpgrader class."""
    
    @pytest.fixture
    def upgrader(self):
        """Create a ResumeUpgrader instance for testing."""
        return ResumeUpgrader()

    def test_upgrade_resume(self, upgrader, resume_pth):

        # load the resume
        resume = upgrader.load_resume_data(resume_pth)

        # skip the first version
        if resume['metadata']['version'] == '0.0.0':
            assert True
        else:

            # reverse the resume chain
            reverse_chain = {v:k for k, v in upgrader.upgrade_chain.items()}
            prior_version = reverse_chain[resume['metadata']['version']]

            # load the prior resume in the test folder
            prior_pth = str(resume_pth).replace(resume['metadata']['version'], prior_version)
            prior_resume = upgrader.load_resume_data(prior_pth)

            # check that the upgrader works
            assert resume == upgrader.upgrade_resume(prior_resume, target_version=resume['metadata']['version'])

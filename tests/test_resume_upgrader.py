#!/usr/bin/env python3
"""
Tests for the Resume Upgrader Module
"""

import json
from unittest.mock import patch
import pytest
from pathlib import Path

from resume_upgrader import ResumeUpgrader

def load_resume(resume_version):
    """Load JSON schema for specified resume version."""
    schema_file = Path(__file__).parent / "fixtures" / f"resume_v{resume_version.replace('.', '_')}.json"
    with open(schema_file, 'r') as f:
        return json.load(f)


class TestResumeUpgrader:
    """Test suite for the ResumeUpgrader class."""
    
    @pytest.fixture
    def upgrader(self):
        """Create a ResumeUpgrader instance for testing."""
        return ResumeUpgrader()

    def test_upgrade_resume(self, upgrader, resume):

        # skip the first version
        if resume['metadata']['version'] == '0.0.0':
            assert True
        else:
            # reverse the resume chain
            reverse_chain = {v:k for k, v in upgrader.upgrade_chain.items()}
            prior_version = reverse_chain[resume['metadata']['version']]

            # check the upgrader by loading the resume and the prior resume
            prior_resume = load_resume(prior_version)

            # check that the upgrader works
            assert resume == upgrader.upgrade_resume(prior_resume)

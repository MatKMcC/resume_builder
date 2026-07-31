#!/usr/bin/env python3
"""
Tests for the Resume Exploder Module
"""

import pytest

from resume_builder.resume_exploder import ResumeExploder
from tests.conftest import test_data_dir

import filecmp
from pathlib import Path


def assert_dirs_equal(dir1, dir2):
    """Recursively checks if two directories are identical."""
    # 1. Compare the immediate files and subdirectories
    comparison = filecmp.dircmp(dir1, dir2)

    # 2. Check for structural mismatches
    assert not comparison.left_only, f"Files only in {dir1}: {comparison.left_only}"
    assert not comparison.right_only, f"Files only in {dir2}: {comparison.right_only}"
    assert not comparison.diff_files, f"Mismatched file contents: {comparison.diff_files}"
    assert not comparison.funny_files, f"Uncomparable files found: {comparison.funny_files}"

    # 3. Recursively check all common subdirectories
    for subdir in comparison.common_dirs:
        assert_dirs_equal(Path(dir1) / subdir, Path(dir2) / subdir)


class TestResumeExploder:
    """Test suite for the ResumeExploder class."""

    @pytest.fixture
    def exploder(self, resume_version, resume_pth, tmp_path):
        """Create a ResumeExploder instance for testing."""
        if resume_version < "1.1.0":
            pytest.skip("Resume version 1.1.0 is required to explode a resume")
        return ResumeExploder(resume_pth, tmp_path)

    def test_manifest_creation(self, manifest, exploder):
        assert manifest == exploder.manifest

    def test_exploded_resume(self, resume_dir, exploder):
        # load the resume
        exploder.explode()
        assert_dirs_equal(resume_dir, exploder.output_dir)


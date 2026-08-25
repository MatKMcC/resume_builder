"""
Pytest configuration and fixtures for resume builder testing.

This module provides fixtures for:
- Resume version test data
- Template rendering test setup
- Schema validation fixtures
- Mock data generation
"""

import pytest
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
import tempfile
import shutil

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "fixtures"
SCHEMA_DIR = Path(__file__).parent / "schemas"
EXPECTED_OUTPUT_DIR = TEST_DATA_DIR / "expected_outputs"

# Resume versions to test against
RESUME_VERSIONS = ["1.2.0"]
TEMPLATE_VERSIONS = ["green_side_bar"]

# Markers for different test categories
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "resume_version: mark test as version compatibility test")
    config.addinivalue_line("markers", "resume_schema: mark test as template rendering test")
    config.addinivalue_line("markers", "resume_metadata: mark test as template rendering test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "json: Tests JSON structure requirements")

@pytest.fixture
def test_data_dir():
    """Path to test data directory."""
    return TEST_DATA_DIR

@pytest.fixture
def schema_dir():
    """Path to JSON schema directory."""
    return SCHEMA_DIR

@pytest.fixture(params=RESUME_VERSIONS)
def resume_version(request):
    """Parametrized fixture that provides each resume version."""
    return request.param

@pytest.fixture
def resume_schema(resume_version, schema_dir):
    """Load JSON schema for specified resume version."""

    if resume_version < "1.0.0":
        schema_file = schema_dir / f"resume_v{resume_version.replace('.', '_')}.json"
    else:
        schema_file = schema_dir / f"resume_v{resume_version.replace('.', '_')}.yaml"

    if not schema_file.exists():
        pytest.skip(f"Schema for version {resume_version} not found")

    if resume_version < "1.0.0":
        with open(schema_file, 'r') as f:
            return json.load(f)
    else:
        with open(schema_file, 'r') as f:
            return yaml.safe_load(f)

@pytest.fixture
def resume_pth(test_data_dir, resume_version):
    """Load resume test data for a specified version."""
    if resume_version < "1.0.0":
        resume_version = resume_version.replace('.', '_')
        resume_pth = test_data_dir / f"resume_v{resume_version}.json"
    else:
        resume_version = resume_version.replace('.', '_')
        resume_pth = test_data_dir / f"resume_v{resume_version}.yaml"
    if not resume_pth.exists():
        pytest.skip(f"Resume data for version {resume_pth} not found")
    return resume_pth

@pytest.fixture
def resume(resume_pth):
    """Load resume test data for a specified version."""
    with open(resume_pth, 'r', encoding='utf-8') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError:
            return json.load(f)

@pytest.fixture
def resume_dir(test_data_dir, resume_version):
    """Load resume test data for a specified version."""
    resume_version = resume_version.replace('.', '_')
    resume_dir = test_data_dir / f"resume_v{resume_version}_dir" / 'resume'

    if not resume_dir.exists():
        pytest.skip(f"Resume directory for version {resume_dir} not found")

    return resume_dir

@pytest.fixture
def manifest_pth(resume_dir):
    """Load resume test data for a specified version."""
    manifest_pth = resume_dir / ".." / f"manifest.yaml"

    if not manifest_pth.exists():
        pytest.skip(f"Manifest data for version {manifest_pth} not found")

    return manifest_pth

@pytest.fixture
def manifest(manifest_pth):
    """Load resume test data for a specified version."""
    with open(manifest_pth, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)



# Custom reporting hooks for better test organization
from collections import defaultdict
test_results_by_class = defaultdict(list)

def pytest_runtest_logreport(report):
    """Collect test results organized by class for custom summary."""
    # Parse nodeid to get class information
    nodeid_parts = report.nodeid.split("::")

    if (report.outcome == "skipped" and report.when == "setup") or (report.when == "call"):
        if len(nodeid_parts) >= 3:
            file_name = nodeid_parts[0].replace("tests/", "")
            class_name = nodeid_parts[1]
            test_name = nodeid_parts[2]
        else:
            file_name = nodeid_parts[0].replace("tests/", "")
            class_name = "Standalone"
            test_name = nodeid_parts[1] if len(nodeid_parts) > 1 else "unknown"

        test_results_by_class[f"{file_name}::{class_name}"].append({
            "name": test_name,
            "outcome": report.outcome,
            "duration": report.duration,
            "nodeid": report.nodeid,
            "report": report
        })

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Custom terminal summary organized by test classes."""
    if config.getoption("--tb") != "no":
        tr = terminalreporter
        tr.write_sep("=", "TEST SUMMARY BY CLASS", bold=True)
        
        total_passed = total_failed = total_skipped = 0

        for class_key, results in sorted(test_results_by_class.items()):
            passed = [r for r in results if r["outcome"] == "passed"]
            failed = [r for r in results if r["outcome"] == "failed"]
            skipped = [r for r in results if r["outcome"] == "skipped"]
            tr.write_sep(class_key)
            
            total_passed += len(passed)
            total_failed += len(failed) 
            total_skipped += len(skipped)
            
            # Write class header with color
            tr.write_line("")
            if failed:
                tr.write_line(f"❌ {class_key}", red=True)
            else:
                tr.write_line(f"✅ {class_key}", green=True)
                
            tr.write_line("─" * (len(class_key) + 4))
            
            # Summary stats
            total = len(results)
            stats_line = f"   📊 {total} tests: "
            if passed:
                stats_line += f"✅ {len(passed)} passed, "
            if failed:
                stats_line += f"❌ {len(failed)} failed, "
            if skipped:
                stats_line += f"⏭️  {len(skipped)} skipped"
                
            tr.write_line(stats_line)
            
            # Show failed tests prominently
            if failed:
                tr.write_line("   🚨 Failed:")
                for test in failed:
                    tr.write_line(f"      • {test['name']}", red=True)
            
            # Show timing for slow tests (>0.5s)
            slow_tests = [r for r in results if r["duration"] > 0.5]
            if slow_tests:
                tr.write_line("   🐌 Slow tests:")
                for test in sorted(slow_tests, key=lambda x: x["duration"], reverse=True):
                    tr.write_line(f"      • {test['name']} ({test['duration']:.2f}s)")
        
        # Overall summary
        tr.write_sep("=", "OVERALL SUMMARY", bold=True)
        tr.write_line(f"📈 Total: {total_passed + total_failed + total_skipped} tests")
        if total_passed:
            tr.write_line(f"✅ Passed: {total_passed}", green=True)
        if total_failed:
            tr.write_line(f"❌ Failed: {total_failed}", red=True)
        if total_skipped:
            tr.write_line(f"⏭️  Skipped: {total_skipped}", yellow=True)

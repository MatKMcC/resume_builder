#!/usr/bin/env python3
"""
Resume Upgrader Module

This module provides functions to upgrade resume data between different schema versions.
It ensures backward compatibility and smooth migration paths for resume formats.
"""

import argparse
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Any
import copy

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResumeUpgrader:
    """Handles upgrading resume data between different schema versions."""

    def __init__(self):
        self.supported_versions = ['0.0.0', '0.1.0', '1.0.0', '1.1.0']
        self.upgrade_functions = {
            '0.0.0': self.upgrade_from_0_0_0_to_0_1_0,
            '0.1.0': self.upgrade_from_0_1_0_to_1_0_0
        }

    def get_resume_version(self, resume_data: Dict[str, Any]) -> str:
        """
        Extract version from resume data.

        Args:
            resume_data: The resume data dictionary

        Returns:
            Version string, defaults to '0.0.0' if not found
        """
        return resume_data.get('metadata', {}).get('version', '0.0.0')

    def set_resume_version(self, resume_data: Dict[str, Any], version: str) -> Dict[str, Any]:
        """
        Set version in resume data metadata.

        Args:
            resume_data: The resume data dictionary
            version: Version string to set

        Returns:
            Updated resume data with version set
        """
        if 'metadata' not in resume_data:
            resume_data['metadata'] = {}

        resume_data['metadata']['version'] = version
        return resume_data

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
                return yaml.safe_load(f)
            except yaml.YAMLError:
                return json.load(f)

    def save_resume_data(self, resume_data: Dict[str, Any], file_path: Path) -> None:
        """
        Save resume data to JSON or YAML file based on extension.

        Args:
            resume_data: Resume data to save
            file_path: Output file path
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            if resume_data['metadata']['version'] >= '1.0.0':
                yaml.dump(resume_data, f,
                          default_flow_style=False,
                          allow_unicode=True,
                          sort_keys=False,
                          indent=2)
            else:
                json.dump(resume_data, f, indent=4, ensure_ascii=False)

    def upgrade_from_0_0_0_to_0_1_0(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upgrade resume from version 0.0.0 to 0.1.0.

        Changes in 0.1.0:
        - Remove 'highlights' arrays from achievements to improve readability

        Args:
            resume_data: Resume data in version 0.0.0 format

        Returns:
            Resume data upgraded to version 0.1.0 format
        """
        logger.info("Upgrading resume from version 0.0.0 to 0.1.0")

        # Create a deep copy to avoid modifying the original
        upgraded_data = copy.deepcopy(resume_data)

        # Process achievements section
        if 'achievements' in upgraded_data:
            for achievement in upgraded_data['achievements']:
                # Remove highlights array if it exists
                if 'highlights' in achievement:
                    logger.debug(
                        f"Removing highlights from achievement: {achievement.get('content', 'Unknown')[:50]}...")
                    del achievement['highlights']

            logger.info(f"Processed {len(upgraded_data['achievements'])} achievements")

        # Update version metadata
        upgraded_data = self.set_resume_version(upgraded_data, '0.1.0')
        upgraded_data['metadata']['variant'] = 'removed highlights from job achievements'
        upgraded_data['metadata']['created'] = '2026-06-09'

        logger.info(f"Successfully upgraded resume to version {upgraded_data['metadata']['version']} -- {upgraded_data['metadata']['variant']}")
        return upgraded_data

    def upgrade_from_0_1_0_to_1_0_0(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upgrade resume from version 0.1.0 to 1.0.0.

        Changes in 1.0.0:
        - Convert to YAML format

        Args:
            resume_data: Resume data in version 0.1.0 format

        Returns:
            Resume data upgraded to version 1.0.0 format
        """
        logger.info("Upgrading resume from version 0.1.0 to 1.0.0 (YAML format)")

        # Create a deep copy to avoid modifying the original
        upgraded_data = copy.deepcopy(resume_data)

        # Update version metadata to 1.0.0
        upgraded_data = self.set_resume_version(upgraded_data, '1.0.0')
        upgraded_data['metadata']['format'] = 'yaml'
        upgraded_data['metadata']['variant'] = 'stable YAML format'
        upgraded_data['metadata']['created'] = '2026-06-09'

        logger.info(f"Successfully upgraded resume to version {upgraded_data['metadata']['version']} -- {upgraded_data['metadata']['variant']}")
        return upgraded_data

    def upgrade_from_1_0_0_to_1_1_0(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upgrade resume from version 1.0.0 to 1.1.0.

        Changes in 1.1.0:
        -

        Args:
            resume_data: Resume data in version 1.0.0 format

        Returns:
            Resume data upgraded to version 1.1.0 format
        """
        logger.info("Upgrading resume from version 0.1.0 to 1.0.0 (YAML format)")

        # Create a deep copy to avoid modifying the original
        upgraded_data = copy.deepcopy(resume_data)

        # Update version metadata to 1.0.0
        upgraded_data = self.set_resume_version(upgraded_data, '1.0.0')
        upgraded_data['metadata']['format'] = 'yaml'
        upgraded_data['metadata']['variant'] = 'stable YAML format'
        upgraded_data['metadata']['created'] = '2026-06-09'

        logger.info(f"Successfully upgraded resume to version {upgraded_data['metadata']['version']} -- {upgraded_data['metadata']['variant']}")
        return upgraded_data

    def upgrade_from_1_1_0_to_1_2_0(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upgrade resume from version 0.1.0 to 1.0.0.

        Changes in 1.0.0:
        - Convert to YAML format

        Args:
            resume_data: Resume data in version 0.1.0 format

        Returns:
            Resume data upgraded to version 1.0.0 format
        """
        logger.info("Upgrading resume from version 0.1.0 to 1.0.0 (YAML format)")

        # Create a deep copy to avoid modifying the original
        upgraded_data = copy.deepcopy(resume_data)

        # Update version metadata to 1.0.0
        upgraded_data = self.set_resume_version(upgraded_data, '1.0.0')
        upgraded_data['metadata']['format'] = 'yaml'
        upgraded_data['metadata']['variant'] = 'stable YAML format'
        upgraded_data['metadata']['created'] = '2026-06-09'

        logger.info(f"Successfully upgraded resume to version {upgraded_data['metadata']['version']} -- {upgraded_data['metadata']['variant']}")
        return upgraded_data

    def upgrade_resume(self, resume_data: Dict[str, Any], target_version: str = None) -> Dict[str, Any]:
        """
        Upgrade resume data to the target version or latest supported version.

        Args:
            resume_data: The resume data to upgrade
            target_version: Target version to upgrade to (defaults to latest)

        Returns:
            Upgraded resume data

        Raises:
            ValueError: If upgrade path is not supported
        """
        current_version = self.get_resume_version(resume_data)
        target_version = target_version or max(self.supported_versions)

        logger.info(f"Upgrading resume from version {current_version} to {target_version}")

        if current_version == target_version:
            logger.info("Resume is already at target version")
            return resume_data

        if current_version not in self.supported_versions:
            raise ValueError(f"Unsupported source version: {current_version}")

        if target_version not in self.supported_versions:
            raise ValueError(f"Unsupported target version: {target_version}")

        # upgrade the resume to the target version
        prior_version = current_version
        while current_version != target_version:
            upgrade_function = self.upgrade_functions.get(current_version)
            if not upgrade_function:
                raise ValueError(f"No upgrade path from {current_version}")

            resume_data = upgrade_function(resume_data)
            current_version = resume_data['metadata']['version']

            if current_version is None or current_version == prior_version:
                raise ValueError(f"No upgrade path from {current_version} to {target_version}")
            prior_version = current_version

        return resume_data

    def upgrade_resume_file(self, input_path: Path, output_path: Path = None, target_version: str = None) -> Path:
        """
        Upgrade a resume file and save the result.

        Args:
            input_path: Path to input resume file
            output_path: Path for output file (auto-determined if None)
            target_version: Target version (defaults to latest)

        Returns:
            Path to the upgraded resume file
        """
        input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Resume file not found: {input_path}")

        # Load resume data (supports both JSON and YAML)
        resume_data = self.load_resume_data(input_path)

        # Upgrade the data
        upgraded_data = self.upgrade_resume(resume_data, target_version)

        # Save upgraded resume (format determined by file extension)
        self.save_resume_data(upgraded_data, output_path)

        logger.info(f"Upgraded resume saved to: {output_path}")
        return output_path

def main():
    # add arguments
    parser = argparse.ArgumentParser(description='Upgrade resume files to newer schema versions')
    parser.add_argument('input_file', help='Path to input resume file (JSON or YAML)')
    parser.add_argument('-o', '--output', help='Path to output file (auto-determined if not provided)')
    parser.add_argument('-v', '--target-version', help='Target version (defaults to latest: 1.0.0)')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        upgrader = ResumeUpgrader()
        output_path = upgrader.upgrade_resume_file(
            input_path=args.input_file,
            output_path=args.output,
            target_version=args.target_version
        )
        print(f"Successfully upgraded resume: {output_path}")

    except Exception as e:
        logger.error(f"Failed to upgrade resume: {e}")

if __name__ == '__main__':
    main()

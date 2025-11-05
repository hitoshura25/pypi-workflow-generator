#!/usr/bin/env python3
"""
CLI for PyPI Workflow Generator.

This module provides the command-line interface for generating
GitHub Actions workflows.
"""

import argparse
import sys
from .generator import generate_workflows

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="""
Generate GitHub Actions workflows for automated PyPI publishing.

Generates 3 workflow files:
  - _reusable-build-publish.yml (shared build/test/publish logic)
  - release.yml (manual releases via GitHub UI)
  - test-pr.yml (PR testing to TestPyPI)

Benefits:
  - No PAT or GitHub App tokens required
  - Test/build before pushing tags (safe failure handling)
  - DRY: shared logic for build/test/publish
  - Simple per-repository setup (only PyPI Trusted Publisher needed)

Example:
  pypi-workflow-generator --package-name mypackage

This creates:
  .github/workflows/_reusable-build-publish.yml
  .github/workflows/release.yml
  .github/workflows/test-pr.yml
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--python-version',
        default='3.11',
        help='Python version to use in workflows (default: 3.11)'
    )
    parser.add_argument(
        '--test-path',
        default='.',
        help='Path to tests directory (default: .)'
    )
    parser.add_argument(
        '--verbose-publish',
        action='store_true',
        help='Enable verbose mode for PyPI publishing actions'
    )
    parser.add_argument(
        '--package-name',
        required=True,
        help='Name of the Python package (required for validation)'
    )

    args = parser.parse_args()

    try:
        result = generate_workflows(
            python_version=args.python_version,
            test_path=args.test_path,
            verbose_publish=args.verbose_publish
        )
        print(result['message'])
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nHint: Run 'pypi-workflow-generator-init' to initialize your project first.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())

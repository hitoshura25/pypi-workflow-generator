import os
from pypi_workflow_generator.generator import generate_workflows

def test_generate_workflows_default_arguments(tmp_path):
    """Test workflow generation with default arguments."""
    # Create dummy project files required for validation
    (tmp_path / 'pyproject.toml').write_text('[build-system]')
    (tmp_path / 'setup.py').write_text('from setuptools import setup\nsetup()')

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        output_dir = tmp_path / ".github" / "workflows"
        result = generate_workflows(
            python_version='3.11',
            test_path='.',
            base_output_dir=output_dir,
            verbose_publish=False
        )

        assert result['success']
        assert 'files_created' in result
        assert 'message' in result
        assert len(result['files_created']) == 3

        # Verify all 3 files exist
        reusable_file = output_dir / '_reusable-build-publish.yml'
        release_file = output_dir / 'release.yml'
        test_pr_file = output_dir / 'test-pr.yml'

        assert reusable_file.exists()
        assert release_file.exists()
        assert test_pr_file.exists()

        # Check reusable workflow content
        with open(reusable_file, 'r') as f:
            content = f.read()

        assert "python-version: '3.11'" in content or "python_version" in content
        assert "pytest" in content

    finally:
        os.chdir(original_cwd)


def test_generate_workflows_custom_arguments(tmp_path):
    """Test workflow generation with custom arguments."""
    # Create dummy project files required for validation
    (tmp_path / 'pyproject.toml').write_text('[build-system]')
    (tmp_path / 'setup.py').write_text('from setuptools import setup\nsetup()')

    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        output_dir = tmp_path / ".github" / "workflows"
        result = generate_workflows(
            python_version='3.9',
            test_path='tests',
            base_output_dir=output_dir,
            verbose_publish=True
        )

        assert result['success']
        assert 'files_created' in result
        assert 'message' in result
        assert len(result['files_created']) == 3

        # Verify all 3 files exist
        reusable_file = output_dir / '_reusable-build-publish.yml'
        release_file = output_dir / 'release.yml'
        test_pr_file = output_dir / 'test-pr.yml'

        assert reusable_file.exists()
        assert release_file.exists()
        assert test_pr_file.exists()

        # Check custom Python version
        with open(reusable_file, 'r') as f:
            content = f.read()

        assert "3.9" in content
        assert "verbose: true" in content or "verbose_publish" in content

    finally:
        os.chdir(original_cwd)
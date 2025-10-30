import os
import pytest
from pypi_workflow_generator.main import generate_workflow


def test_generate_workflow_default_arguments(tmp_path):
    """Test workflow generation with default arguments."""
    output_dir = tmp_path / ".github" / "workflows"
    generate_workflow(python_version='3.11', output_filename='pypi-publish.yml', release_on_main_push=False, base_output_dir=output_dir)

    output_file = output_dir / 'pypi-publish.yml'
    assert output_file.exists()

    with open(output_file, 'r') as f:
        content = f.read()

    assert "python-version: '3.11'" in content
    assert """tags:
      - 'v*.*.*'""" in content
    assert "startsWith(github.ref, 'refs/tags')" in content
    assert "github.ref == 'refs/heads/main'" not in content

def test_generate_workflow_custom_arguments(tmp_path):
    """Test workflow generation with custom arguments."""
    output_dir = tmp_path / ".github" / "workflows"
    generate_workflow(python_version='3.9', output_filename='custom-pypi-publish.yml', release_on_main_push=True, base_output_dir=output_dir)

    output_file = output_dir / 'custom-pypi-publish.yml'
    assert output_file.exists()

    with open(output_file, 'r') as f:
        content = f.read()

    assert "python-version: '3.9'" in content
    assert "branches: [ main ]" in content
    assert "github.ref == 'refs/heads/main'" in content
    assert """tags:
      - 'v*.*.*'""" not in content
    assert "startsWith(github.ref, 'refs/tags')" not in content

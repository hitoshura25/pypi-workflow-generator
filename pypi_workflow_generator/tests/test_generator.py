import os
import pytest
from pypi_workflow_generator.main import generate_workflow


def test_generate_workflow_default_arguments(tmp_path):
    """Test workflow generation with default arguments."""
    output_dir = tmp_path / ".github" / "workflows"
    generate_workflow(python_version='3.11', output_filename='pypi-publish.yml', release_on_main_push=False, base_output_dir=output_dir, verbose_publish=False)

    output_file = output_dir / 'pypi-publish.yml'
    assert output_file.exists()

    with open(output_file, 'r') as f:
        content = f.read()

    assert "python-version: '3.11'" in content
    assert """tags:
      - 'v*.*.*'""" in content
    expected_if_condition = "if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags')"
    # Extract the 'if:' line for the 'Publish release to PyPI' step and compare after stripping whitespace
    publish_pypi_block_start = content.find("- name: Publish release to PyPI")
    publish_pypi_block_end = content.find("- name: Publish pre-release to TestPyPI", publish_pypi_block_start) # Find next step
    if publish_pypi_block_end == -1:
        publish_pypi_block_end = len(content) # If no next step, go to end of content
    publish_pypi_block = content[publish_pypi_block_start:publish_pypi_block_end]

    if_line = next(line for line in publish_pypi_block.splitlines() if line.strip().startswith("if:"))
    assert "".join(expected_if_condition.split()) == "".join(if_line.split())
    assert "- name: Set pre--release version for TestPyPI" in content
    assert 'LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null) || LATEST_TAG="0.0.0"' in content
    assert 'echo "SETUPTOOLS_SCM_PRETEND_VERSION=${LATEST_TAG}.dev{{ github.run_id }}" >> $GITHUB_ENV' in content

def test_generate_workflow_custom_arguments(tmp_path):
    """Test workflow generation with custom arguments."""
    output_dir = tmp_path / ".github" / "workflows"
    generate_workflow(python_version='3.9', output_filename='custom-pypi-publish.yml', release_on_main_push=True, base_output_dir=output_dir, verbose_publish=True)

    output_file = output_dir / 'custom-pypi-publish.yml'
    assert output_file.exists()

    with open(output_file, 'r') as f:
        content = f.read()

    assert "python-version: '3.9'" in content
    assert "branches: [ main ]" in content
    expected_if_condition = "if: github.event_name == 'push' && github.ref == 'refs/heads/main'"
    publish_pypi_block_start = content.find("- name: Publish release to PyPI")
    publish_pypi_block_end = content.find("- name: Publish pre-release to TestPyPI", publish_pypi_block_start) # Find next step
    if publish_pypi_block_end == -1:
        publish_pypi_block_end = len(content) # If no next step, go to end of content
    publish_pypi_block = content[publish_pypi_block_start:publish_pypi_block_end]

    if_line = next(line for line in publish_pypi_block.splitlines() if line.strip().startswith("if:"))
    assert "".join(expected_if_condition.split()) == "".join(if_line.split())
    assert """tags:
      - 'v*.*.*'""" not in content
    assert "startsWith(github.ref, 'refs/tags')" not in "".join(content.split())
    assert "verbose: true" in content
    assert "- name: Set pre--release version for TestPyPI" in content
    assert 'LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null) || LATEST_TAG="0.0.0"' in content
    assert 'echo "SETUPTOOLS_SCM_PRETEND_VERSION=${LATEST_TAG}.dev{{ github.run_id }}" >> $GITHUB_ENV' in content

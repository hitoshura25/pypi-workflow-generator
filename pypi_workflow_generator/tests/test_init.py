import os
import pytest
from pypi_workflow_generator.init import init_project


def test_init_project(tmp_path):
    """Test project initialization."""
    # Change the current working directory to the temporary directory
    os.chdir(tmp_path)

    # Run the init_project function
    init_project()

    # Assert that the files have been created
    assert os.path.exists('pyproject.toml')
    assert os.path.exists('setup.py')

    # Assert that the contents of the files are correct
    with open('pyproject.toml', 'r') as f:
        pyproject_content = f.read()
    assert "[build-system]" in pyproject_content
    assert "requires = [\"setuptools>=61.0\", \"setuptools_scm[toml]>=6.2\"]" in pyproject_content
    assert "build-backend = \"setuptools.build_meta\"" in pyproject_content
    assert "[tool.setuptools_scm]" in pyproject_content
    assert "version_scheme = \"post-release\"" in pyproject_content

    with open('setup.py', 'r') as f:
        setup_content = f.read()
    assert "from setuptools import setup, find_packages" in setup_content
    assert "import os" in setup_content
    assert "def local_scheme(version):" in setup_content
    assert "if os.environ.get(\"IS_PULL_REQUEST\")" in setup_content
    assert "return f\".dev{os.environ['GITHUB_RUN_ID']}\"" in setup_content
    assert "else:" in setup_content
    assert "return \"\"" in setup_content
    assert "with open(\"README.md\", \"r\", encoding=\"utf-8\") as fh:" in setup_content
    assert "long_description = fh.read()" in setup_content
    assert "name='your-package-name'," in setup_content
    assert "use_scm_version={\"local_scheme\": local_scheme}," in setup_content
    assert "long_description=long_description," in setup_content
    assert "long_description_content_type='text/markdown'," in setup_content
    assert "packages=find_packages()," in setup_content
    assert "include_package_data=True," in setup_content
    assert "install_requires=[" in setup_content
    assert "'Jinja2'," in setup_content
    assert "entry_points={"
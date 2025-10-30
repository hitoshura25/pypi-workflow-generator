# `pypi_workflow_generator` Package

This package provides the core logic for generating a GitHub Actions workflow for Python packages.

## `main.py`

This script is the primary entry point for generating the `pypi-publish.yml` workflow file.

### Usage (CLI Mode)

```bash
python -m pypi_workflow_generator.main --python-version <version> --output-filename <filename> [--release-on-main-push]
```

**Arguments:**
*   `--python-version`: The version of Python to use in the workflow (default: `3.11`).
*   `--output-filename`: The name for the generated workflow file (default: `pypi-publish.yml`).
*   `--release-on-main-push`: A flag to initiate the release on every push to the `main` branch (default: `False`).

### Usage (MCP Mode)

For AI agents, the script supports an `--mcp-input` flag that accepts a JSON payload:

```bash
python -m pypi_workflow_generator.main --mcp-input '{"python_version": "3.10", "output_filename": "custom-workflow.yml", "release_on_main_push": true}'
```

## `create_release.py`

This helper script facilitates the creation of version tags for releases.

### Usage

```bash
python -m pypi_workflow_generator.create_release <version_tag>
```

**Arguments:**
*   `<version_tag>`: The version string to tag (e.g., `v1.0.0`). This will execute `git tag <version_tag>` and `git push origin <version_tag>`.

## `pypi_publish.yml.j2`

This is a Jinja2 template file used by `main.py` to render the GitHub Actions workflow. It defines the structure and logic of the CI/CD pipeline for building, testing, and publishing Python packages.

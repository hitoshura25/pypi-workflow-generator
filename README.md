# pypi-workflow-generator

A dual-mode tool (MCP server + CLI) for generating GitHub Actions workflows for Python package publishing to PyPI.

## Features

- ✅ **Dual-Mode Operation**: Works as MCP server for AI agents OR traditional CLI for developers
- ✅ **PyPI Trusted Publishers**: Secure publishing without API tokens
- ✅ **Automated Versioning**: Uses setuptools_scm for git-based versioning
- ✅ **Pre-release Testing**: Automatic TestPyPI publishing on pull requests
- ✅ **Production Publishing**: Automatic PyPI publishing on version tags
- ✅ **Complete Project Initialization**: Generates pyproject.toml and setup.py
- ✅ **Release Management**: Simple git tag creation for triggering releases

## Installation

```bash
pip install pypi-workflow-generator
```

## Usage

This package can be used in three ways:

### 1. MCP Mode (For AI Agents)

For AI agents with MCP support (Claude Code, Continue.dev, Cline):

**Add to `claude_desktop_config.json` or `claude_config.json`**:
```json
{
  "mcpServers": {
    "pypi-workflow-generator": {
      "command": "mcp-pypi-workflow-generator"
    }
  }
}
```

The agent can now use these tools:
- `generate_workflow` - Generate GitHub Actions workflow
- `initialize_project` - Create pyproject.toml and setup.py
- `create_release` - Create and push git release tags

**Example conversation**:
```
You: "Please set up a PyPI publishing workflow for my Python project"

Claude: I'll help you set up a complete PyPI publishing workflow.

[Calls initialize_project and generate_workflow tools]

✅ Created:
  - pyproject.toml
  - setup.py
  - .github/workflows/pypi-publish.yml

Next steps:
1. Configure Trusted Publishers on PyPI
2. Create a release: pypi-release patch
```

### 2. CLI Mode (For Developers)

**Initialize a new project**:
```bash
pypi-workflow-generator-init \
  --package-name my-awesome-package \
  --author "Your Name" \
  --author-email "your.email@example.com" \
  --description "My awesome Python package" \
  --url "https://github.com/username/my-awesome-package" \
  --command-name my-command
```

**Generate workflow**:
```bash
pypi-workflow-generator --python-version 3.11
```

**Create a release**:
```bash
pypi-release patch  # or 'minor' or 'major'
```

### 3. Programmatic Use

```python
from pypi_workflow_generator import generate_workflow, initialize_project

# Initialize project
initialize_project(
    package_name="my-package",
    author="Your Name",
    author_email="your@email.com",
    description="My package",
    url="https://github.com/user/repo",
    command_name="my-cmd"
)

# Generate workflow
generate_workflow(
    python_version="3.11",
    release_on_main_push=False
)
```

## Generated Workflow Features

The generated `pypi-publish.yml` workflow includes:

- **Automated Testing**: Runs pytest on every PR and release
- **Pre-release Publishing**: TestPyPI publishing on PRs with version like `1.0.0.dev123`
- **Production Publishing**: PyPI publishing on version tags
- **Trusted Publishers**: No API tokens needed (OIDC authentication)
- **setuptools_scm**: Automatic versioning from git tags

## Setting Up Trusted Publishers

The generated GitHub Actions workflow (`pypi-publish.yml`) utilizes [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/) for secure package publishing. This method enhances security by allowing your GitHub Actions workflow to authenticate with PyPI using OpenID Connect (OIDC) instead of requiring you to store sensitive API tokens as GitHub secrets.

**Why Trusted Publishers?**
- **Enhanced Security:** Eliminates the need to store PyPI API tokens, reducing the risk of token compromise.
- **Best Practice:** Recommended by PyPI for publishing from automated environments like GitHub Actions.

**How to Set Up Trusted Publishers for Your Project:**

Before your workflow can successfully publish to PyPI or TestPyPI, you must configure Trusted Publishers for your project on the respective PyPI instance.

1. **Log in to PyPI/TestPyPI:**
   - For TestPyPI: Go to `https://test.pypi.org/` and log in.
   - For official PyPI: Go to `https://pypi.org/` and log in.

2. **Navigate to Your Project's Publishing Settings:**
   - Go to your project's management page. The URL will typically look like:
     `https://[test.]pypi.org/manage/project/<your-package-name>/settings/publishing/`
   - Replace `<your-package-name>` with the actual name of your Python package (e.g., `pypi-workflow-generator`).

3. **Add a New Trusted Publisher:**
   - Click on the "Add a new publisher" button.
   - Select "GitHub Actions" as the publisher type.
   - Provide the following details:
     - **Owner:** The GitHub username or organization that owns your repository (e.g., `hitoshura25`).
     - **Repository:** The name of your GitHub repository (e.g., `pypi-workflow-generator`).
     - **Workflow Name:** The name of your workflow file (e.g., `pypi-publish.yml`).
     - **Environment (Optional):** If your GitHub Actions workflow uses a specific environment, specify its name here. Otherwise, leave it blank.

4. **Save the Publisher:** Confirm and save the new publisher.

Once configured, your GitHub Actions workflow will be able to publish packages without needing `PYPI_API_TOKEN` or `TEST_PYPI_API_TOKEN` secrets.

## CLI Options

### `pypi-workflow-generator`

Generate GitHub Actions workflow for PyPI publishing.

```
Options:
  --python-version VERSION    Python version (default: 3.11)
  --output-filename NAME      Workflow filename (default: pypi-publish.yml)
  --release-on-main-push      Trigger release on main branch push
  --test-path PATH            Path to tests (default: .)
  --verbose-publish           Enable verbose publishing
```

### `pypi-workflow-generator-init`

Initialize a new Python project with PyPI configuration.

```
Options:
  --package-name NAME         Package name (required)
  --author NAME               Author name (required)
  --author-email EMAIL        Author email (required)
  --description TEXT          Package description (required)
  --url URL                   Project URL (required)
  --command-name NAME         CLI command name (required)
```

### `pypi-release`

Create and push a git release tag.

```
Usage:
  pypi-release {major,minor,patch} [--overwrite]

Arguments:
  {major,minor,patch}  The type of release (major, minor, or patch)

Options:
  --overwrite          Overwrite an existing tag
```

**Note**: The CLI uses semantic versioning (major/minor/patch) for convenience. The MCP tool `create_release` accepts explicit version strings (e.g., "v1.0.0") for flexibility. See [Interface Differences](#interface-differences) below.

## MCP Server Details

The MCP server runs via stdio transport and provides three tools:

**Tool: `generate_workflow`**
- Generates GitHub Actions workflow file
- Parameters: python_version, output_filename, release_on_main_push, test_path, verbose_publish

**Tool: `initialize_project`**
- Creates pyproject.toml and setup.py
- Parameters: package_name, author, author_email, description, url, command_name

**Tool: `create_release`**
- Creates and pushes git tag
- Parameters: version

See [MCP-USAGE.md](./MCP-USAGE.md) for detailed MCP configuration and usage.

## Interface Differences

The package provides two interfaces with slightly different APIs for different use cases:

### CLI vs MCP: Release Creation

**CLI Mode** (`pypi-release`):
- Uses semantic versioning keywords: `major`, `minor`, `patch`
- Automatically increments version from latest git tag
- Convenience for developers who want simple versioning

```bash
pypi-release patch      # Creates v1.0.1 (if current is v1.0.0)
pypi-release minor      # Creates v1.1.0
pypi-release major      # Creates v2.0.0
```

**MCP Mode** (`create_release` tool):
- Accepts explicit version strings: `v1.0.0`, `v2.5.3`, etc.
- Direct control over version numbers
- Flexibility for AI agents to determine versions programmatically

```json
{
  "version": "v1.0.0"
}
```

**Why the difference?** The CLI optimizes for human convenience (automatic incrementing), while MCP optimizes for programmatic control (explicit versions).

### Entry Point Naming Convention

The MCP server uses the `mcp-` prefix (industry standard for MCP tools):
- `mcp-pypi-workflow-generator` - Follows MCP ecosystem naming
- Makes it discoverable when searching for MCP servers
- Clearly distinguishes server mode from CLI mode

All other commands use the `pypi-` prefix for CLI operations:
- `pypi-workflow-generator`
- `pypi-workflow-generator-init`
- `pypi-release`

## Architecture

```
User/AI Agent
      │
      ├─── MCP Mode ────────> server.py (MCP protocol)
      │                           │
      ├─── CLI Mode ────────> main.py / init.py / create_release.py
      │                           │
      └─── Programmatic ────> __init__.py
                                  │
                    All modes use shared core:
                                  ▼
                            generator.py
                      (Business logic)
```

## Dogfooding

This project uses itself to generate its own GitHub Actions workflow! The workflow file at `.github/workflows/pypi-publish.yml` was created by running:

```bash
pypi-workflow-generator \
  --python-version 3.11 \
  --test-path pypi_workflow_generator/ \
  --verbose-publish
```

This ensures:
- ✅ The tool actually works (we use it ourselves)
- ✅ The template stays consistent with real-world usage
- ✅ We practice what we preach
- ✅ Users can see a real example of the generated output

Check the workflow file header to see the exact command used.

## Development

```bash
# Clone repository
git clone https://github.com/hitoshura25/pypi-workflow-generator.git
cd pypi-workflow-generator

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Build package
python -m build
```

## Contributing

Contributions welcome! Please open an issue or PR.

## License

Apache-2.0

## Links

- **Repository**: https://github.com/hitoshura25/pypi-workflow-generator
- **Issues**: https://github.com/hitoshura25/pypi-workflow-generator/issues
- **PyPI**: https://pypi.org/project/pypi-workflow-generator/

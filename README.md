# pypi-workflow-generator

A dual-mode tool (MCP server + CLI) for generating GitHub Actions workflows for Python package publishing to PyPI.

## Features

- ✅ **Dual-Mode Operation**: Works as MCP server for AI agents OR traditional CLI for developers
- ✅ **PyPI Trusted Publishers**: Secure publishing without API tokens
- ✅ **No PAT Required**: Uses default GitHub token - zero additional setup
- ✅ **Safe Tag Creation**: Tags only pushed after tests/build succeed
- ✅ **Automated Versioning**: Uses setuptools_scm for git-based versioning
- ✅ **Pre-release Testing**: Automatic TestPyPI publishing on pull requests
- ✅ **Production Publishing**: Manual releases via GitHub Actions UI
- ✅ **Complete Project Initialization**: Generates pyproject.toml and setup.py
- ✅ **DRY Architecture**: Reusable workflows for shared logic

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
- `generate_workflows` - Generate all 3 GitHub Actions workflows (no PAT required!)
- `initialize_project` - Create pyproject.toml and setup.py
- `create_release` - Create and push git release tags

**Example conversation**:
```
You: "Please set up a PyPI publishing workflow for my Python project"

Claude: I'll help you set up a complete PyPI publishing workflow.

[Calls initialize_project and generate_workflows tools]

✅ Created:
  - pyproject.toml
  - setup.py
  - .github/workflows/_reusable-build-publish.yml
  - .github/workflows/release.yml
  - .github/workflows/test-pr.yml

Next steps:
1. Configure Trusted Publishers on PyPI and TestPyPI
2. Create release via GitHub UI: Actions → "Release to PyPI"
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

**Generate workflows**:
```bash
pypi-workflow-generator --package-name my-awesome-package
```

This creates 3 workflow files:
- `_reusable-build-publish.yml` - Shared build/test/publish logic
- `release.yml` - Manual releases via GitHub UI
- `test-pr.yml` - PR testing to TestPyPI

**Create a release**:
```bash
# Via GitHub UI (recommended):
# 1. Go to Actions → "Release to PyPI"
# 2. Click "Run workflow"
# 3. Select version bump type (patch/minor/major)
# 4. Click "Run workflow"
```

### 3. Programmatic Use

```python
from pypi_workflow_generator.generator import generate_workflows, initialize_project

# Initialize project
initialize_project(
    package_name="my-package",
    author="Your Name",
    author_email="your@email.com",
    description="My package",
    url="https://github.com/user/repo",
    command_name="my-cmd"
)

# Generate workflows
generate_workflows(
    python_version="3.11",
    test_path="tests/",
    verbose_publish=True
)
```

## Generated Workflows

This tool generates **THREE** GitHub Actions workflows:

### 1. Release Workflow (`release.yml`)

Manual release workflow triggered via GitHub UI:

- **Version Calculation**: Automatically calculates next version (patch/minor/major)
- **Safe Tag Creation**: Creates tag locally first, tests/builds, then pushes only if successful
- **Automated Testing**: Runs pytest before publishing
- **Package Building**: Builds distribution packages
- **PyPI Publishing**: Publishes to production PyPI via Trusted Publishers
- **GitHub Release**: Creates GitHub Release with auto-generated notes
- **No PAT Required**: Uses default `GITHUB_TOKEN`
- **setuptools_scm**: Automatic versioning from git tags

### 2. PR Testing Workflow (`test-pr.yml`)

Automatically tests pull requests:

- **Triggered on PRs**: Runs automatically when PRs are opened/updated
- **Automated Testing**: Runs pytest on PR code
- **Package Building**: Builds distribution to verify it's buildable
- **TestPyPI Publishing**: Publishes pre-release to TestPyPI for testing
- **Uses Reusable Workflow**: Calls `_reusable-build-publish.yml` for DRY

### 3. Reusable Test and Build Workflow (`_reusable-test-build.yml`)

Shared logic called by other workflows:

- **Parameterized**: Accepts Python version, test path, and git ref
- **Test Pipeline**: Checkout → setup → test → build
- **Artifact Export**: Uploads built packages for use by caller workflows
- **Reusable**: Single source of truth for test/build logic
- **Note**: Does NOT publish (publishing done by caller workflows for PyPI Trusted Publishing compatibility)

## Creating Releases

**Via GitHub Actions UI** (only method):

1. Go to **Actions** tab in your repository
2. Select **Release to PyPI** workflow
3. Click **Run workflow**
4. Choose release type:
   - **patch**: Bug fixes (0.1.0 → 0.1.1)
   - **minor**: New features (0.1.1 → 0.2.0)
   - **major**: Breaking changes (0.2.0 → 1.0.0)
5. Click **Run workflow**

The workflow will:
1. ✅ Calculate the next version number
2. ✅ Check if tag already exists
3. ✅ Create tag locally (not pushed yet)
4. ✅ Run tests
5. ✅ Build package
6. ✅ Publish to PyPI
7. ✅ Push tag to repository (only if all above succeed)
8. ✅ Create GitHub Release with auto-generated notes

**Key Benefit**: Tags are only pushed if tests and build succeed, preventing orphaned tags for failed releases.

## Setting Up Trusted Publishers

The generated GitHub Actions workflows utilize [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/) for secure package publishing. This method enhances security by allowing your GitHub Actions workflow to authenticate with PyPI using OpenID Connect (OIDC) instead of requiring you to store sensitive API tokens as GitHub secrets.

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

3. **Add Trusted Publishers:**
   - You need to add **two** publishers (one for production, one for testing)
   - Click on the "Add a new publisher" button.
   - Select "GitHub Actions" as the publisher type.
   - For **PyPI** (production releases):
     - **Owner:** Your GitHub username or organization (e.g., `your-username`)
     - **Repository:** Your repository name (e.g., `my-awesome-package`)
     - **Workflow Name:** `release.yml`
     - **Environment (Optional):** Leave blank
   - For **TestPyPI** (PR testing):
     - **Owner:** Same as above
     - **Repository:** Same as above
     - **Workflow Name:** `test-pr.yml`
     - **Environment (Optional):** Leave blank

   **Important:** Do NOT use `_reusable-test-build.yml` as the workflow name. PyPI Trusted Publishing does not support reusable workflows. The workflow name must be the file that contains the publish step (`test-pr.yml` or `release.yml`).

4. **Save the Publishers:** Confirm and save both publishers.

Once configured, your GitHub Actions workflows will be able to publish packages without needing any API tokens. **No PAT or GitHub App setup required!**

## That's It!

With Trusted Publishers configured, you're ready to go. The workflows use GitHub's default `GITHUB_TOKEN` for all operations - no additional authentication setup needed.

## CLI Options

### `pypi-workflow-generator`

Generate all 3 GitHub Actions workflows for PyPI publishing.

```
Usage:
  pypi-workflow-generator --package-name PACKAGE [options]

Required:
  --package-name NAME         Package name (required for validation)

Options:
  --python-version VERSION    Python version (default: 3.11)
  --test-path PATH            Path to tests (default: .)
  --verbose-publish           Enable verbose publishing

Generates:
  .github/workflows/_reusable-build-publish.yml
  .github/workflows/release.yml
  .github/workflows/test-pr.yml
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

## MCP Server Details

The MCP server runs via stdio transport and provides three tools:

**Tool: `generate_workflows`**
- Generates all 3 GitHub Actions workflow files at once
- Creates: _reusable-build-publish.yml, release.yml, and test-pr.yml
- Parameters: python_version, test_path, verbose_publish

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

This project uses itself to generate its own GitHub Actions workflows! The workflow files at:
- `.github/workflows/_reusable-test-build.yml`
- `.github/workflows/release.yml`
- `.github/workflows/test-pr.yml`

Were all created by running:

```bash
pypi-workflow-generator \
  --package-name pypi-workflow-generator \
  --python-version 3.11 \
  --test-path pypi_workflow_generator/ \
  --verbose-publish
```

This ensures:
- ✅ The tool actually works (we use it ourselves)
- ✅ All 3 workflows are tested in production
- ✅ The templates stay consistent with real-world usage
- ✅ We practice what we preach
- ✅ Users can see real examples of the generated output

Check the workflow file headers to see the exact command used. Try creating a release using the GitHub Actions UI!

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

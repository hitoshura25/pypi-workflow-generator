# MCP Usage Guide

Complete guide for using pypi-workflow-generator as an MCP server.

## What is MCP?

Model Context Protocol (MCP) is a standard protocol that allows AI agents to interact with external tools. This package implements an MCP server that AI agents can use to generate PyPI publishing workflows.

## Supported AI Agents

- ✅ Claude Code (Anthropic)
- ✅ Continue.dev
- ✅ Cline
- ⚠️ Cursor, Aider, Windsurf (use CLI mode instead)

## Configuration

### Claude Code

Add to your project's `claude_config.json` or user-level `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pypi-workflow-generator": {
      "command": "mcp-pypi-workflow-generator"
    }
  }
}
```

### Continue.dev

Add to `~/.continue/config.json`:

```json
{
  "mcpServers": [
    {
      "name": "pypi-workflow-generator",
      "command": "mcp-pypi-workflow-generator"
    }
  ]
}
```

### Cline

Add to Cline's MCP settings:

```json
{
  "mcpServers": {
    "pypi-workflow-generator": {
      "command": "mcp-pypi-workflow-generator"
    }
  }
}
```

## Available Tools

### 1. generate_workflow

Generate GitHub Actions workflow for PyPI publishing.

**Parameters**:
- `python_version` (string, optional): Python version, default "3.11"
- `output_filename` (string, optional): Workflow filename, default "pypi-publish.yml"
- `release_on_main_push` (boolean, optional): Trigger on main push, default false
- `test_path` (string, optional): Tests directory, default "."
- `verbose_publish` (boolean, optional): Verbose publishing, default false

**Example**:
```json
{
  "python_version": "3.11",
  "output_filename": "pypi-publish.yml",
  "release_on_main_push": false,
  "test_path": "tests",
  "verbose_publish": true
}
```

**Returns**:
- Success message with file path
- Error message if project not initialized

### 2. initialize_project

Initialize new Python project with PyPI configuration.

**Parameters** (all required):
- `package_name` (string): Package name
- `author` (string): Author name
- `author_email` (string): Author email
- `description` (string): Package description
- `url` (string): Project URL
- `command_name` (string): CLI command name

**Example**:
```json
{
  "package_name": "my-package",
  "author": "Jane Doe",
  "author_email": "jane@example.com",
  "description": "My awesome package",
  "url": "https://github.com/janedoe/my-package",
  "command_name": "my-cli"
}
```

**Returns**:
- Success message with list of created files
- Error message if parameters missing

### 3. create_release

Create and push git release tag.

**Parameters**:
- `version` (string, required): Version tag (e.g., "v1.0.0")

**Example**:
```json
{
  "version": "v1.0.0"
}
```

**Returns**:
- Success message with version tag
- Error message if git operations fail

## Example Workflows

### Complete Project Setup

```
You: "Set up my Python project for PyPI publishing"

Agent: I'll set up your Python project with a complete PyPI publishing workflow.

[Agent calls initialize_project]
Created pyproject.toml and setup.py

[Agent calls generate_workflow]
Generated .github/workflows/pypi-publish.yml

Your project is now configured for PyPI publishing with:
- Automated versioning via setuptools_scm
- TestPyPI publishing on pull requests
- PyPI publishing on version tags
- Trusted Publishers (no API tokens needed)

Next steps:
1. Configure Trusted Publishers on PyPI
2. Create your first release with: pypi-release patch
```

### Just Generate Workflow

```
You: "Generate a PyPI workflow using Python 3.12"

Agent: [Calls generate_workflow with python_version="3.12"]

Generated .github/workflows/pypi-publish.yml with Python 3.12
```

### Create Release

```
You: "Create a v2.0.0 release"

Agent: [Calls create_release with version="v2.0.0"]

Created and pushed tag v2.0.0
GitHub Actions will now build and publish to PyPI
```

## Troubleshooting

### Agent Can't Find MCP Server

**Issue**: Agent reports "mcp-pypi-workflow-generator not found"

**Solution**:
```bash
# Verify installation
pip list | grep pypi-workflow-generator

# Verify command exists
which mcp-pypi-workflow-generator

# Reinstall if needed
pip install --force-reinstall pypi-workflow-generator
```

### Tool Execution Fails

**Issue**: Tool returns error

**Check**:
1. For `generate_workflow`: Project must have `pyproject.toml` and `setup.py`
   - Run `initialize_project` first
2. For `create_release`: Git repository must be initialized
   - Run `git init` if needed
3. For `initialize_project`: All required parameters must be provided
   - Verify all 6 parameters are present

### Non-MCP Agents

**Issue**: Your AI agent doesn't support MCP

**Solution**: Use CLI mode instead:
```bash
pypi-workflow-generator-init --package-name my-pkg --author "Name" --author-email "email@example.com" --description "My package" --url "https://github.com/user/repo" --command-name my-cmd
pypi-workflow-generator --python-version 3.11
pypi-release patch
```

## Protocol Details

The MCP server uses:
- **Transport**: stdio (JSON-RPC over stdin/stdout)
- **Protocol Version**: MCP 1.0
- **Capabilities**: tools
- **Request Format**: JSON-RPC 2.0

## Development

Testing the MCP server:

```bash
# Start server
mcp-pypi-workflow-generator

# Send request (in another terminal)
echo '{"id":1,"method":"tools/list","params":{}}' | mcp-pypi-workflow-generator

# Expected response:
{"id": 1, "tools": [...]}
```

### Manual Testing

Test each tool individually:

**List Tools**:
```bash
echo '{"id":1,"method":"tools/list","params":{}}' | mcp-pypi-workflow-generator 2>/dev/null
```

**Initialize Project**:
```bash
cd /tmp/test-project
echo '{
  "id":2,
  "method":"tools/call",
  "params":{
    "name":"initialize_project",
    "arguments":{
      "package_name":"test-pkg",
      "author":"Test",
      "author_email":"test@example.com",
      "description":"Test package",
      "url":"https://github.com/test/test-pkg",
      "command_name":"test-cmd"
    }
  }
}' | mcp-pypi-workflow-generator 2>/dev/null
```

**Generate Workflow**:
```bash
cd /tmp/test-project
echo '{
  "id":3,
  "method":"tools/call",
  "params":{
    "name":"generate_workflow",
    "arguments":{
      "python_version":"3.11"
    }
  }
}' | mcp-pypi-workflow-generator 2>/dev/null
```

## Best Practices

1. **Always initialize first**: Run `initialize_project` before `generate_workflow`
2. **Use semantic versioning**: Tags should follow `v{major}.{minor}.{patch}` format
3. **Test locally**: Verify workflows work before pushing to production
4. **Configure Trusted Publishers**: Set up PyPI authentication before first release

## FAQ

**Q: Can I use this without MCP support?**
A: Yes! Use the CLI commands: `pypi-workflow-generator-init`, `pypi-workflow-generator`, and `pypi-release`.

**Q: Does this work with TestPyPI?**
A: Yes! The generated workflow automatically publishes to TestPyPI on pull requests.

**Q: How do I update the generated workflow?**
A: Re-run `generate_workflow` with desired parameters. The file will be overwritten.

**Q: Can I customize the generated files?**
A: Yes! All generated files can be edited after creation. They're standard Python project files.

**Q: What happens if I create a release without configuring Trusted Publishers?**
A: The GitHub Actions workflow will fail at the publishing step. Configure Trusted Publishers on PyPI first.

## Support

- **Repository**: https://github.com/hitoshura25/pypi-workflow-generator
- **Issues**: https://github.com/hitoshura25/pypi-workflow-generator/issues
- **Documentation**: See main [README.md](./README.md)

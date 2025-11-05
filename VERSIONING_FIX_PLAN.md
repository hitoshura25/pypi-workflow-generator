# PLAN: Fix Versioning in Reusable Build Workflow

**Date:** 2025-11-05

**Issue:** The git tag created in the `create-tag` job of `release.yml` is not available in the separate runner environment of the `test-and-build` job, which uses a reusable workflow. This prevents `setuptools_scm` from correctly determining the package version during the build step.

---

## Proposed Solution

The most direct and safest solution is to explicitly pass the calculated version string to the reusable workflow and use the `SETUPTOOLS_SCM_PRETEND_VERSION` environment variable. This tells `setuptools_scm` what version to use, bypassing its need to discover the version from a git tag.

This approach has two key advantages:
1.  **Preserves "Safe Tagging":** The git tag is still only pushed to the remote repository *after* the build and publish steps succeed. No tags for failed releases will pollute the git history.
2.  **Maintains DRY Principle:** The build and test logic remains in the reusable workflow, avoiding code duplication.

---

## Implementation Steps

### Step 1: Modify `_reusable_test_build.yml.j2` Template

The reusable workflow needs to be updated to accept the version string and use it.

**File:** `pypi_workflow_generator/_reusable_test_build.yml.j2`

**Changes:**
1.  **Add a `version` input:** A new optional input will be added to the `workflow_call` trigger.
2.  **Set environment variable for build step:** The `Build package` step will be modified to include an `env` block that sets `SETUPTOOLS_SCM_PRETEND_VERSION`.

**New `_reusable_test_build.yml.j2` content:**

```yaml
name: Reusable Test and Build

on:
  workflow_call:
    inputs:
      python_version:
        description: 'Python version to use'
        required: false
        type: string
        default: '{{ python_version }}'
      test_path:
        description: 'Path to tests'
        required: false
        type: string
        default: '{{ test_path }}'
      ref:
        description: 'Git ref to checkout (tag, branch, or commit)'
        required: false
        type: string
        default: ''
      version:
        description: 'Version to build the package with (e.g., v1.2.3)'
        required: false
        type: string
        default: ''

jobs:
  test-and-build:
    runs-on: ubuntu-latest
    permissions:
      contents: read

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          ref: {% raw %}${{ inputs.ref || github.ref }}{% endraw %}
          fetch-depth: 0  # For setuptools_scm
          fetch-tags: true

      - name: Set up Python {% raw %}${{ inputs.python_version }}{% endraw %}
        uses: actions/setup-python@v4
        with:
          python-version: {% raw %}${{ inputs.python_version }}{% endraw %}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests with pytest
        run: python -m pytest {% raw %}${{ inputs.test_path }}{% endraw %}

      - name: Build package
        run: python -m build
        env:
          SETUPTOOLS_SCM_PRETEND_VERSION: {% raw %}${{ inputs.version }}{% endraw %}

      - name: Store the distribution packages
        uses: actions/upload-artifact@v4
        with:
          name: python-package-distributions
          path: dist/
```

### Step 2: Modify `release.yml.j2` Template

The main release workflow needs to be updated to pass the calculated version to the reusable workflow.

**File:** `pypi_workflow_generator/release.yml.j2`

**Change:**
1.  **Update `test-and-build` job:** In the `test-and-build` job, the `ref` input will be changed to `github.sha` to ensure the correct commit is checked out. The `version` input will be added to pass the new version string to the reusable workflow.

**New `test-and-build` job in `release.yml.j2`:**

```yaml
  test-and-build:
    needs: [create-tag]
    uses: ./.github/workflows/_reusable-test-build.yml
    with:
      python_version: '{{ python_version }}'
      test_path: '{{ test_path }}'
      ref: {% raw %}${{ github.sha }}{% endraw %}
      version: {% raw %}${{ needs.create-tag.outputs.new_version }}{% endraw %}
```

This change ensures the `test-and-build` job checks out the exact commit the workflow was triggered on and then uses the version string calculated in the `create-tag` job to build the package. This solves the problem of the tag not being available in the reusable workflow.

### Step 3: Regenerate Workflows

After modifying the templates, the `pypi-workflow-generator` tool must be run to apply these changes to the actual workflow files located in the `.github/workflows/` directory.

```bash
# Install the local package to make the script available
pip install -e .

# Run the generator
pypi-workflow-generator
```

This will update `.github/workflows/_reusable-test-build.yml` and `.github/workflows/release.yml` with the new logic.

---

This plan addresses the versioning issue while preserving the existing project structure and safety features.

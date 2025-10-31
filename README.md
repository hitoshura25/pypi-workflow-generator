# pypi-workflow-generator
 A command-line tool that generates a best-practice GitHub Actions workflow for testing and publishing Python packages to PyPI.

## Publishing to PyPI with Trusted Publishers

The generated GitHub Actions workflow (`pypi-publish.yml`) utilizes [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/) for secure package publishing. This method enhances security by allowing your GitHub Actions workflow to authenticate with PyPI using OpenID Connect (OIDC) instead of requiring you to store sensitive API tokens as GitHub secrets.

**Why Trusted Publishers?**
*   **Enhanced Security:** Eliminates the need to store PyPI API tokens, reducing the risk of token compromise.
*   **Best Practice:** Recommended by PyPI for publishing from automated environments like GitHub Actions.

**How to Set Up Trusted Publishers for Your Project:**

Before your workflow can successfully publish to PyPI or TestPyPI, you must configure Trusted Publishers for your project on the respective PyPI instance.

1.  **Log in to PyPI/TestPyPI:**
    *   For TestPyPI: Go to `https://test.pypi.org/` and log in.
    *   For official PyPI: Go to `https://pypi.org/` and log in.

2.  **Navigate to Your Project's Publishing Settings:**
    *   Go to your project's management page. The URL will typically look like:
        `https://[test.]pypi.org/manage/project/<your-package-name>/settings/publishing/`
    *   Replace `<your-package-name>` with the actual name of your Python package (e.g., `pypi-workflow-generator`).

3.  **Add a New Trusted Publisher:**
    *   Click on the "Add a new publisher" button.
    *   Select "GitHub Actions" as the publisher type.
    *   Provide the following details:
        *   **Owner:** The GitHub username or organization that owns your repository (e.g., `hitoshura25`).
        *   **Repository:** The name of your GitHub repository (e.g., `pypi-workflow-generator`).
        *   **Workflow Name:** The name of your workflow file (e.g., `pypi-publish.yml`).
        *   **Environment (Optional):** If your GitHub Actions workflow uses a specific environment, specify its name here. Otherwise, leave it blank.

4.  **Save the Publisher:** Confirm and save the new publisher.

Once configured, your GitHub Actions workflow will be able to publish packages without needing `PYPI_API_TOKEN` or `TEST_PYPI_API_TOKEN` secrets.

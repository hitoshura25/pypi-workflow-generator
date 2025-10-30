
import argparse
import json
import os
from jinja2 import Environment, FileSystemLoader

def generate_workflow(python_version, output_filename, release_on_main_push):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(script_dir))
    template = env.get_template('pypi_publish.yml.j2')

    # Render the template with the provided Python version
    workflow_content = template.render(python_version=python_version, release_on_main_push=release_on_main_push)

    # Construct the full output path
    output_dir = os.path.join(os.getcwd(), '.github', 'workflows')
    os.makedirs(output_dir, exist_ok=True) # Create directories if they don't exist
    full_output_path = os.path.join(output_dir, output_filename)

    # Write the rendered content to the output file
    with open(full_output_path, 'w') as f:
        f.write(workflow_content)

    print(f"Successfully generated {full_output_path}")

def main():
    parser = argparse.ArgumentParser(description='Generate a GitHub Actions workflow for Python packages.')

    # CLI mode arguments
    parser.add_argument('--python-version', default='3.11', help='The version of Python to use in the workflow.')
    parser.add_argument('--output-filename', default='pypi-publish.yml', help='The name for the generated workflow file.')
    parser.add_argument('--release-on-main-push', action='store_true', help='Initiate the release on every main branch push.')

    # MCP mode argument
    parser.add_argument('--mcp-input', help='A JSON string containing the input parameters for MCP mode.')

    args = parser.parse_args()

    if args.mcp_input:
        # MCP mode
        try:
            mcp_params = json.loads(args.mcp_input)
            python_version = mcp_params.get('python_version', '3.11')
            output_filename = mcp_params.get('output_filename', 'pypi-publish.yml')
            release_on_main_push = mcp_params.get('release_on_main_push', False)
        except json.JSONDecodeError:
            print("Error: Invalid JSON string provided for --mcp-input.")
            return
    else:
        # CLI mode
        python_version = args.python_version
        output_filename = args.output_filename
        release_on_main_push = args.release_on_main_push

    generate_workflow(python_version, output_filename, release_on_main_push)

if __name__ == "__main__":
    main()

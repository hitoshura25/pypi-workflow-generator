import os
import argparse
from jinja2 import Environment, FileSystemLoader

def init_project(package_name, author, author_email, description, url, command_name):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(script_dir))

    # Render the pyproject.toml template
    pyproject_template = env.get_template('pyproject.toml.j2')
    pyproject_content = pyproject_template.render()

    # Render the setup.py template
    setup_template = env.get_template('setup.py.j2')
    setup_content = setup_template.render(package_name=package_name, author=author, author_email=author_email, description=description, url=url, command_name=command_name)

    # Write the rendered content to the output files
    with open('pyproject.toml', 'w') as f:
        f.write(pyproject_content)

    with open('setup.py', 'w') as f:
        f.write(setup_content)

    print("Successfully initialized the project with pyproject.toml and setup.py")

def main():
    parser = argparse.ArgumentParser(description='Initialize a new Python project with a PyPI publishing workflow.')
    parser.add_argument('--package-name', required=True, help='The name of the package.')
    parser.add_argument('--author', required=True, help='The name of the author.')
    parser.add_argument('--author-email', required=True, help='The email of the author.')
    parser.add_argument('--description', required=True, help='A short description of the package.')
    parser.add_argument('--url', required=True, help='The URL of the project.')
    parser.add_argument('--command-name', required=True, help='The name of the command-line entry point.')
    args = parser.parse_args()

    init_project(args.package_name, args.author, args.author_email, args.description, args.url, args.command_name)

if __name__ == "__main__":
    main()

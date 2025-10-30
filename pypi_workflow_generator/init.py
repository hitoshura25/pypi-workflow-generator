import os
from jinja2 import Environment, FileSystemLoader

def init_project():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader(script_dir))

    # Render the pyproject.toml template
    pyproject_template = env.get_template('pyproject.toml.j2')
    pyproject_content = pyproject_template.render()

    # Render the setup.py template
    setup_template = env.get_template('setup.py.j2')
    setup_content = setup_template.render()

    # Write the rendered content to the output files
    with open('pyproject.toml', 'w') as f:
        f.write(pyproject_content)

    with open('setup.py', 'w') as f:
        f.write(setup_content)

    print("Successfully initialized the project with pyproject.toml and setup.py")

def main():
    init_project()

if __name__ == "__main__":
    main()

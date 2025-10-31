
from setuptools import setup, find_packages
import os

def local_scheme(version):
    if os.environ.get("IS_PULL_REQUEST"):
        return f".dev{os.environ['GITHUB_RUN_ID']}"
    else:
        return ""

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = ""

setup(
    name='pypi-workflow-generator',
    author='Your Name',
    author_email='your.email@example.com',
    description='A tool to generate GitHub Actions workflows for Python packages.',
    url='https://github.com/your-username/pypi-workflow-generator',
    use_scm_version={"local_scheme": local_scheme},
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Jinja2>=3.0',
    ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pypi-workflow-generator=pypi_workflow_generator.main:main',
            'pypi-workflow-generator-init=pypi_workflow_generator.init:main',
            'pypi-release=pypi_workflow_generator.create_release:main',
        ],
    },
)

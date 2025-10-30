
from setuptools import setup, find_packages
import os

def local_scheme(version):
    if os.environ.get("IS_PULL_REQUEST"):
        return f".dev{os.environ['GITHUB_RUN_ID']}"
    else:
        return ""

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pypi-workflow-generator',
    use_scm_version={"local_scheme": local_scheme},
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Jinja2',
    ],
    entry_points={
        'console_scripts': [
            'pypi-workflow-generator=pypi_workflow_generator.main:main',
            'pypi-release=pypi_workflow_generator.create_release:main',
        ],
    },
)

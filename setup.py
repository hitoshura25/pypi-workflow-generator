
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pypi-workflow-generator',
    version='0.1.0',
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


from setuptools import setup, find_packages

setup(
    name='pypi-workflow-generator',
    version='0.1.0',
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

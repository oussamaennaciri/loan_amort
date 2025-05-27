# setup.py
from setuptools import setup, find_packages

setup(
    name="loan_amort",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "python-dateutil",
        "mplcursors",
    ],
    entry_points={
        "console_scripts": [
            "loan_amort=loan_amort.cli:main",
        ],
    },
)

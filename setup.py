from setuptools import setup, find_packages

setup(
    name="loan_amort",
    version="0.1.0",
    description="Python toolkit & CLI for loan amortization schedules, metrics, and charts",
    author="Oussama Ennaciri",
    author_email="oussamaennaciri@gmail.com",
    packages=find_packages(exclude=["tests*", ".github*"]),
    install_requires=[
        "pandas>=2.0",
        "click>=8.0",
        "matplotlib>=3.0",
    ],
    entry_points={
        "console_scripts": [
            "loan-amortize=cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)

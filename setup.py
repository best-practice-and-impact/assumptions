from os import path
import re
from setuptools import setup

with open("README.md") as readme:
    long_description = readme.read()

setup(
    name="assumptions",
    version="0.0.1",
    description="Generating Markdown assumptions logs from code comments",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="David Foster",
    author_email="foster.dev999@gmail.com",
    packages=["assumptions"],
    include_package_data=True,
    license="MIT",
    python_requires=">=3.6",
    extras_require={
        "testing": [
            "coverage",
            "pytest>=3.6,<4",
            "pytest-cov",
            "pytest-regressions",
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing",
    ],
    entry_points = {
        'console_scripts': ['assumptions=assumptions.cli:cli'],
    }
)

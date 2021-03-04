from pathlib import Path

from setuptools import setup

# Get version from package __init__
text = Path("./assumptions/__init__.py").read_text(encoding="utf8")
for line in text.split("\n"):
    if "__version__" in line:
        break
version = line.split("= ")[-1].strip('"')

path_doc_reqs = Path(__file__).parent.joinpath("docs", "requirements.txt")
testing_reqs = [
    "coverage",
    "pytest>=3.6,<4",
    "pytest-cov",
    "pytest-regressions",
]


def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()


setup(
    name="assumptions",
    version=version,
    description="Generating Markdown assumptions logs from code comments.",
    long_description=Path("./README.rst").read_text(encoding="utf8"),
    long_description_content_type="text/x-rst",
    author="David Foster",
    author_email="foster.dev999@gmail.com",
    packages=["assumptions"],
    include_package_data=True,
    license="MIT",
    python_requires=">=3.6",
    extras_require={
        "testing": testing_reqs,
        "docs": read_requirements(path_doc_reqs),
        "dev": ["bump2version"] + testing_reqs,
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
    entry_points={
        "console_scripts": ["assumptions=assumptions.cli:cli"],
    },
)

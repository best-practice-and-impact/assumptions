# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
from assumptions import __version__

# -- Project information -----------------------------------------------------

project = "assumptions"
copyright = "2021, David Foster"
author = "David Foster"

# The full version, including alpha/beta/rc tags
version = __version__
# The full version, including alpha/beta/rc tags.
release = __version__


# -- General configuration ---------------------------------------------------
language = "en"
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",  # For using numpydocs style docstings
    "jupyter_sphinx",  # For showing code outputs
    "myst_parser",  # For including .md files
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

exclude_patterns = ["build"]

# -- Options for HTML output -------------------------------------------------

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "github_url": "https://github.com/foster999/assumptions",
    "use_edit_page_button": True,
    "external_links": [
        {
            "name": "Quality Assurance of Code Guidance",
            "url": "https://best-practice-and-impact.github.io/qa-of-code-guidance/intro.html",
        },
    ],
}

html_logo = "_static/assumptions.png"

html_context = {
    "github_user": "foster999",
    "github_repo": "assumptions",
    "github_version": "main",
    "doc_path": "docs",
}

html_static_path = ["_static"]

html_css_files = [
    "custom.css",
]


def pre_build_handler(app, config):
    """
    Run assumptions to generate example log outputs.
    """
    import subprocess

    subprocess.run(
        [
            "assumptions",
            "-e",
            ".py",
            "-o",
            f"{app.srcdir}/example/assumptions_caveats_log.md",
        ],
    )
    subprocess.run(
        [
            "assumptions",
            "-e",
            ".py",
            "-o",
            f"{app.srcdir}/example/todo_list.md",
            "-l",
            "todo_list",
        ],
    )


def setup(app):
    app.connect("config-inited", pre_build_handler)

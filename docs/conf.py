# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import importlib.metadata
import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

project = 'ptcx'
# noinspection PyShadowingBuiltins
date = datetime.date.today().year
copyright = '{date}, Aurin Aegerter (aka Steve, kaliiiiiiiiii)'
author = 'Aurin Aegerter (aka Steve, kaliiiiiiiiii)'
release =importlib.metadata.version('ptcx')

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    "sphinx_autodoc_typehints",
    #"sphinx.ext.viewcode",
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path=["_static"]
html_css_files = [
    'css/dark.css',
]


# -- autodoc options --

autodoc_member_order = 'bysource'
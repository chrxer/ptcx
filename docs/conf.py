# Configuration file for the Sphinx documentation builder.  # pylint: disable=missing-module-docstring
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
from pathlib import Path
ROOT=Path(__file__).parent.parent.absolute()
sys.path.append(str(ROOT))

import toml # pylint: disable=wrong-import-position, wrong-import-order
import datetime # pylint: disable=wrong-import-position, wrong-import-order



TOML=toml.load(ROOT.joinpath("pyproject.toml"))

project = TOML['project']['name']
# noinspection PyShadowingBuiltins
date = datetime.date.today().year

author = "" # pylint: disable=invalid-name
for _author in TOML['project']["authors"]:
    author += f"{_author['name']};"
author = author[:-1]

copyright = f'{date}, {author}' # pylint: disable=invalid-name, redefined-builtin
release = TOML["project"]["version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',

    #"sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_github_style",
    "sphinx_autodoc_typehints",
    "sphinx_new_tab_link"
]

new_tab_link_show_external_link_icon = True # pylint: disable=invalid-name

always_document_param_types=True # pylint: disable=invalid-name

linkcode_url="https://github.com/chrxer/ptcx" # pylint: disable=invalid-name

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo' # pylint: disable=invalid-name
html_static_path=["_static"]
html_css_files = [
    'css/dark.css',
]

intersphinx_mapping = {
        'python': ('https://docs.python.org/3', None),
        'tree_sitter':('https://tree-sitter.github.io/py-tree-sitter/', None)
    }


# -- autodoc options --

autodoc_member_order = 'bysource' # pylint: disable=invalid-name

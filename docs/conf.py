# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

import sphinx.ext.viewcode

sys.path.insert(0, os.path.abspath('..'))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'dpest'
copyright = '2025, Luis Vargas-Rojas'
author = 'Luis Vargas-Rojas'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon','sphinx.ext.githubpages','sphinx.ext.autosummary']


autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_mock_imports = ["flopy", "pyemu"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'pydata_sphinx_theme'

html_theme = 'alabaster'
#html_static_path = ['_static']

# import sphinx_rtd_theme
# html_theme = "sphinx_rtd_theme"
# #html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


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

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.doctest'
]
autosummary_generate = True
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autodoc_mock_imports = ["flopy", "pyemu"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'

html_show_sourcelink = True

# html_sidebars = {
#     "**": ["sidebar-nav-bs"]
# }

html_sidebars = {
    '**': [
        'globaltoc.html',
        'relations.html',  # optional: previous/next links
        'searchbox.html',
    ]
}

html_theme_options = {
    "github_url": "https://github.com/DS4Ag/dpest/",  # Replace with your GitHub repo URL
    "use_repository_button": True,
    "use_source_button": True,
    "show_nav_level": 2,  # Ensure navigation is visible up to depth 2
    "navigation_with_keys": True,  # Enable keyboard navigation
}
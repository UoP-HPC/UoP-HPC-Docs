# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Lovelace - University of Plymouth HPC'
copyright = '2025, University of Plymouth & Collaborators'
author = 'University of Plymouth & Collaborators'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

#extensions = []
extensions = [
        'sphinx_rtd_theme',
        'sphinx.ext.autosectionlabel',
        'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['asciinema-player.css']
html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "UoP-HPC", # Username
    "github_repo": "UoP-HPC-Docs", # Repo name
    "github_version": "main", # Version
    "conf_py_path": "/source/", # Path in the checkout to the docs root
}

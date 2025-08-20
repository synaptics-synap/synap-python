# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SyNAP Python API'
copyright = '2025, Synaptics Incorporated'
author = 'Synaptics Incorporated'

version = '0.1.0'
release = 'stable'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'autoapi.extension',
    'sphinx.ext.autodoc', 
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints'
]

autoapi_dirs = ['../../src']
autoapi_file_patterns = ['*.pyi']
autoapi_options = ['members', 'inherited-members', 'imported-members', 'undoc-members']
autoapi_add_toctree_entry = False
autoapi_template_dir = '_templates/autoapi'
autodoc_typehints = 'description'
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


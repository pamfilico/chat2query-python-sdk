"""Sphinx configuration for Chat2Query Python SDK documentation."""

from __future__ import annotations

import os
import sys
from datetime import datetime

try:
    from importlib.metadata import version as get_version
except ImportError:  # Python <3.8 fallback
    from importlib_metadata import version as get_version  # type: ignore


# -- Path setup --------------------------------------------------------------

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PACKAGE_DIR = os.path.join(ROOT_DIR, "chat2query")

if PACKAGE_DIR not in sys.path:
    sys.path.insert(0, PACKAGE_DIR)


# -- Project information -----------------------------------------------------

project = "Chat2Query Python SDK"
author = "Chat2Query"
copyright = f"{datetime.now():%Y}, {author}"

try:
    release = get_version("chat2query-python-sdk")
except Exception:
    release = "0.0.0"


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

autosummary_generate = False
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

html_theme = "press"
html_static_path = ["_static"]

# SEO Configuration
html_title = "Chat2Query Python SDK - Natural Language to SQL"
html_short_title = "Chat2Query SDK"

html_meta = {
    'description': 'Official Python SDK for Chat2Query API. Convert natural language to SQL queries with AI-powered database interactions.',
    'keywords': 'chat2query, python sdk, natural language to sql, sql generation, database api, ai sql, langchain, openai',
    'author': 'Chat2Query',
    'og:title': 'Chat2Query Python SDK',
    'og:description': 'Convert natural language to SQL with Python',
    'og:type': 'website',
    'og:url': 'https://pamfilico.github.io/chat2query-python-sdk/',
    'og:site_name': 'Chat2Query Documentation',
    'twitter:card': 'summary',
    'twitter:title': 'Chat2Query Python SDK',
    'twitter:description': 'Convert natural language to SQL with Python',
}

# GitHub Pages configuration
html_baseurl = "https://pamfilico.github.io/chat2query-python-sdk/"
html_extra_path = []

# Press theme options with external links
html_theme_options = {
    "external_links": [
        ("GitHub", "https://github.com/pamfilico/chat2query-python-sdk"),
        ("Chat2Query", "https://chat2query.com"),
    ],
}

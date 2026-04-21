# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Melissae'
copyright = '2025, h3ik0 & Cie.'
author = 'h3ik0'

release = '2.0'
version = '2.0.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_book_theme'

html_logo = 'logo.png'
html_favicon = 'logo.png'

html_theme_options = {
    "default_mode": "dark",
    "logo": {
        "text": "Melissae",
        "image_light": "logo.png",
        "image_dark": "logo.png",
    },
}

# -- Options for EPUB output
epub_show_urls = 'footnote'

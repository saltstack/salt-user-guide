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
import datetime
import os

from docutils import nodes
from docutils.nodes import Element
from sphinx.writers.html import HTMLTranslator


# Force all external links to open as new tabs,
# without breaking internal links. This causes
# external links to work by default on HTML
# generated sites, while natively working in PDF
# output, also.
#
# Overwrites visit_reference() Sphinx method found
# in HTMLTranslator class of sphinx/sphinx/writers/html.py
# Solution Source: https://stackoverflow.com/a/61669375/5340149
class PatchedHTMLTranslator(HTMLTranslator):
    def visit_reference(self, node: Element) -> None:
        atts = {"class": "reference"}
        if node.get("internal") or "refuri" not in node:
            atts["class"] += " internal"
        else:
            atts["class"] += " external"
            # Customize behavior (open in new tab, secure linking site)
            atts["target"] = "_blank"
            atts["rel"] = "noopener noreferrer"
        if "refuri" in node:
            atts["href"] = node["refuri"] or "#"
            if self.settings.cloak_email_addresses and atts["href"].startswith(
                "mailto:"
            ):
                atts["href"] = self.cloak_mailto(atts["href"])
                self.in_mailto = True
        else:
            assert (
                "refid" in node
            ), 'References must have "refuri" or "refid" attribute.'
            atts["href"] = "#" + node["refid"]
        if not isinstance(node.parent, nodes.TextElement):
            assert len(node) == 1 and isinstance(node[0], nodes.image)
            atts["class"] += " image-reference"
        if "reftitle" in node:
            atts["title"] = node["reftitle"]
        if "target" in node:
            atts["target"] = node["target"]
        self.body.append(self.starttag(node, "a", "", **atts))

        if node.get("secnumber"):
            self.body.append(
                ("%s" + self.secnumber_suffix) % ".".join(map(str, node["secnumber"]))
            )


# Run above custom function against links
def setup(app):
    app.set_translator("html", PatchedHTMLTranslator)


this_year = datetime.datetime.today().year
if this_year == 2021:
    copyright_year = 2021
else:
    copyright_year = f"2021 - {this_year}"

# -- Project information -----------------------------------------------------

project = "Salt user guide"
copyright = f"{copyright_year}, VMware, Inc."
author = "VMware, Inc."

# Variables to pass into the docs from sitevars.txt for rst substitution
with open("sitevars.rst") as site_vars_file:
    site_vars = site_vars_file.read().splitlines()

rst_prolog = """
{}
""".format(
    "\n".join(site_vars[:])
)

# Pull release from "release" in sitevars.rst
release = [s for s in site_vars if "|release|" in s][0].split(":: ")[1]
version = release

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx.ext.todo",
    "sphinx-prompt", # Required by sphinx_substitution_extensions
    "sphinx_inline_tabs",
    "sphinx_substitution_extensions"
]

source_suffix = ".rst"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "sitevars.rst",
]


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

# Base Material Theme requirements
html_show_sourcelink = True  # False on private repos; True on public repos
html_theme = 'furo'
html_title = project

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://example.com)
html_css_files = [
    'css/import-all-salt-docs.css',
    'css/local-testing.css'
]

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/img/SaltProject_altlogo_teal.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large. Favicons can be up to at least 228x228. PNG
# format is supported as well, not just .ico'
html_favicon = "_static/img/SaltProject_Logomark_teal.png"

###
# PDF Generation / LaTeX configuration
###
# If generating PDFs in the future, should ensure external logo is copied local
# https://gitlab.com/saltstack/open/salt-branding-guide/-/raw/master/logos/SaltProject_altlogo_teal.png?inline=true
#latex_logo = "docs/_static/img/SaltProject_verticallogo_black.png"

# Linux Biolinum, Linux Libertine: https://en.wikipedia.org/wiki/Linux_Libertine
# Source Code Pro: https://github.com/adobe-fonts/source-code-pro/releases
latex_elements = {
    "inputenc": "",
    "utf8extra": "",
    "preamble": r"""
    \usepackage{fontspec}
    \setsansfont{Linux Biolinum O}
    \setromanfont{Linux Libertine O}
    \setmonofont{Source Code Pro}
""",
}

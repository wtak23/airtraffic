# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# General information about the project.
project = u'US Airtraffic Analysis'
author = u'Takanori Watanabe'

# -- General configuration ------------------------------------------------
numpydoc_class_members_toctree = False
numpydoc_show_class_members = False
extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',
    'numpydoc', # used to parse numpy-style docstrings for autodoc    
]

# The master toctree document.
master_doc = 'index'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
version = u'' # The short X.Y version.
release = u'' # The full version, including alpha/beta/rc tags.

language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
# 'test3.rst',
#'templates',
]



# -- Options for HTML output ----------------------------------------------
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

source_suffix = '.rst'

# choose between "Read the doc" or "Bootstrap" theme (i'm not set on which one to use...)
theme = 'rtd'

if theme == 'rtd':
    html_theme = 'sphinx_rtd_theme'
    html_theme_options = {
        'collapse_navigation': False, #<- set to false when publishing
        # 'sticky_navigation': True,  # Set to False to disable the sticky nav while scrolling.
        # 'navigation_depth': 4,
    }
elif theme == 'bootstrap':
    #=========================================================================#
    # config for bootstrap repos
    #
    # Credit: styling inspired (ie, taken) from Seaborn 
    #         http://seaborn.pydata.org/index.html
    #=========================================================================#
    import sphinx_bootstrap_theme
    html_theme = 'bootstrap'
    html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

    html_theme = 'bootstrap'
    html_theme_options = {
        # Navigation bar title. (Default: ``project`` value)
        #'navbar_title': "Demo",

        # Tab name for entire site. (Default: "Site")
        'navbar_site_name': "TOC",

        # A list of tuples containing pages or urls to link to.
        # Valid tuples should be in the following forms:
        #    (name, page)                 # a link to a page
        #    (name, "/aa/bb", 1)          # a link to an arbitrary relative url
        #    (name, "http://example.com", True) # arbitrary absolute url
        # Note the "1" or "True" value above as the third argument to indicate
        # an arbitrary url.
        'navbar_links': [
            ('<i class="fa fa-home" aria-hidden="true"></i>&nbsp; takwatanabe.me', "http://takwatanabe.me", True),
            ('<i class="fa fa-github" aria-hidden="true"></i>&nbsp; Github', "https://github.com/wtak23/airtraffic", True),
            # ("Link", "http://example.com", True),
        ],

        # Render the next and previous page links in navbar. (Default: true)
        'navbar_sidebarrel': False,

        #-------------------------------------------------------------------------#
        # Render the current pages TOC in the navbar. (Default: true)
        'navbar_pagenav': True,

        # Tab name for the current pages TOC. (Default: "Page")
        'navbar_pagenav_name': "page",
        #-------------------------------------------------------------------------#

        # Global TOC depth for "site" navbar tab. (Default: 1)
        # Switching to -1 shows all levels.
        'globaltoc_depth': -1,

        # Include hidden TOCs in Site navbar?
        #
        # Note: If this is "false", you cannot have mixed ``:hidden:`` and
        # non-hidden ``toctree`` directives in the same page, or else the build
        # will break.
        #
        # Values: "true" (default) or "false"
        'globaltoc_includehidden': "true",

        # HTML navbar class (Default: "navbar") to attach to <div> element.
        # For black navbar, do "navbar navbar-inverse"
        # 'navbar_class': "navbar navbar-inverse",

        # Fix navigation bar to top of page?
        # Values: "true" (default) or "false"
        'navbar_fixed_top': "true",

        # Location of link to source.
        # Options are "nav" (default), "footer" or anything else to exclude.
        'source_link_position': "footer",

        'bootswatch_theme': "flatly",
        'bootstrap_version': "3",
    }

# The name for this set of Sphinx documents.
# "<project> v<release> documentation" by default.
#
# html_title = u'PROJECT_NAME v1'
html_title = ''

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (relative to this directory) to use as a favicon
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#
# html_extra_path = []

# If not None, a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
# The empty string is equivalent to '%b %d, %Y'.
# html_last_updated_fmt = None
html_last_updated_fmt = ''

html_show_sphinx = False
html_show_copyright = False

# Output file base name for HTML help builder.
# htmlhelp_basename = 'PROJECT_NAME'
htmlhelp_basename = project

def setup(app):
    # to hide/show the prompt in code examples:
    app.add_javascript('copybutton.js')
    app.add_stylesheet('style.css') # <- from seaborn doc

html_secnumber_suffix = ' '
html_add_permalinks = None 
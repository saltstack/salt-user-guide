.. _writing-salt-docs:

======================================
Writing Salt documentation (rST guide)
======================================

Version 1.1 - last updated February 2022

Introduction
============
Welcome to the Salt documentation guide. All of the Salt Project documentation
is written in reStructured Text (rST), a flavor of Markdown that is specifically
designed to work with Python-based projects. This guide will explain how to
format your rST in the Salt Project documentation.

This guide:

* Links out to a general guide for basic rST formatting guidelines.
* Lists the specific rST formatting guidelines that we want to highlight for use
  in Salt documentation projects.

For additional help, see:

* :ref:`style-guide` - For general guidance about using Salt Project terms and
  other style or formatting conventions.
* :ref:`contributing` - For more information about contributing to this
  repository specifically, including setting up your environment.


.. Tip::
    Want to see how this page looks in raw rST? Click **Show Source** at the
    bottom of the page. The link is in the footer.


General reStructured text (rST) guides
======================================
To learn about how to format rST in general, see the official
`reStructuredText Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_.

However, an even better guide is the
`TYPO3 reStructured Text & Sphinx <https://docs.typo3.org/m/typo3/docs-how-to-document/master/en-us/WritingReST/Index.html>`_ guide, especially the
`reST & Sphinx cheat sheet <https://docs.typo3.org/m/typo3/docs-how-to-document/master/en-us/WritingReST/CheatSheet.html>`_.

These two guides explain some aspects of rST that are not covered in the rest of
this rST guide such as:

* Formatting text as **bold** or *italicized*
* Formatting ``in-line commands or code examples``
* Other general information about rST

The rest of this guide highlights how we want you to format various rST elements
in Salt documentation.


Headings
========
In general, Salt only uses three levels of headings:

* Heading 1 (h1) for topic or page titles, which uses ``=`` with both overlining
  and underlining
* Heading 2 (h2) for section headings, which uses ``=`` underlining only
* Heading 3 (h3) for subsection headings, which uses ``-`` underlining only

.. warning::
    Do not use a heading level lower than h3.

The following callout shows how to format the three heading levels::

   =============================
   Heading 1 - Topic/page titles
   =============================

   Heading 2 - Section titles
   ==========================

   Heading 3 - Subsection titles
   -----------------------------


Line endings
============
To make it easier to review rST files in merge requests, insert a hard return at
80 characters and start a new line, per
`Google's docstring guidelines <https://google.github.io/styleguide/pyguide.html#381-docstrings>`_.

To make life easier, consider setting your code editor to display the 80
character preferred line length.


Code blocks
===========
Inline code, commands, file paths, and file names should be formatted using
double backticks (``````). For longer code snippets, use a full code block.

The syntax to include a code block is::

  .. code-block:: bash

      Your code example goes here

In the previous example, the part that follows the double-colon (``::``)
indicates the type of code highlighting that should be applied. The code
highlighting we use most commonly in Salt documentation includes:

* **yaml** for YAML configuration files
* **bash** for CLI commands
* **sls** for Salt states
* **text** for generic examples

Many different code highlighters are available for rST. See TYPO3's guide to
`Code blocks with syntax highlighting <https://docs.typo3.org/m/typo3/docs-how-to-document/master/en-us/WritingReST/Codeblocks.html>`_
for more information, along with
`Pygments list of available lexers <https://pygments.org/docs/lexers/>`_.

When you're writing YAML code examples, we require you to include the file path
for the configuration file in the Salt Project. Use the ``:caption:`` element to
show the file path. For example::

  .. code-block:: yaml
     :caption: /etc/salt/master.d/grains.conf

     autosign_grains_dir: /etc/salt/autosign_grains

This renders as:

.. code-block:: yaml
   :caption: /etc/salt/master.d/grains.conf

   autosign_grains_dir: /etc/salt/autosign_grains

If your code block contains an executed command, remove any command prompts such
as ``$``.


Tabbed content
==============
In some cases, you might want to provide examples of how to run the same command
in different operating systems or languages. The best way to represent
alternative command syntax is to use tabbed content.

For example, you might want to show the syntax to run a script running in
yum-based operating systems (such as RHEL) or in apt-based operating systems
(such as Debian/Ubuntu).

In this case, you can use tabbed content to show the same script with different
syntax. For example::

  .. tabs::

     .. tab:: RHEL

        .. code-block:: bash

            yum check-update

     .. tab:: Debian/Ubuntu

        .. code-block:: bash

            apt update
            apt-get update


This renders as:

.. tabs::

   .. tab:: RHEL

      .. code-block:: bash

          yum check-update

   .. tab:: Debian/Ubuntu

      .. code-block:: bash

          apt update
          apt-get update



Be aware that getting the indentation and spacing right on tabs can sometimes
prove difficult. As always, it's a good idea to preview your changes locally
before opening a merge request. See :ref:`contributing` for more information.

.. Warning::
    The core Salt docs do not yet support tabs. Currently you can only use them
    in the ``salt-user-guide`` and ``salt-install-guide`` repositories.



Admonitions (tips, note boxes, warnings)
========================================
Admonitions help draw readers' attention to important notes or warnings. The
following admonitions are the most commonly used in Salt documentation:

* Note
* Tip
* Danger
* Warning

The typical format for an admonition is::

  .. Note::
      Your admonition goes here

In the previous example, you could swap out ``Note`` for one of the other
admonition types.

These admonitions render as follows:

.. Note::
    This is a note admonition.

.. Tip::
    This is a tip admonition.

.. Danger::
    This is a danger admonition.

.. Warning::
    This is a warning admonition.

If you want to create custom text for the admonition title, use the following
syntax::

  .. Admonition:: Your custom admonition title

     The admonition text goes here.

This admonition renders as:

.. Admonition:: Your custom admonition title

   The admonition text goes here.


Links
=====
For links to an external website, use this syntax::

  `Page title <url>`_

For relative links to topics within the same documentation set, you first need
to add a label to the topic or section you want to link to. The syntax for the
section or topic label is::

  .. _section-label:

After inserting this label, you can link to it from another topic using this
syntax::

  :ref:`section-label`


For links to sections within the same page, be aware that the section title must
match the actual section title verbatim. The syntax for linking to a section
title is::

  `Section title`_


Lists
=====
For unordered lists (bullet lists), use asterisks (\*). For example::

  * Unordered list item 1
  * Unordered list item 2
  * Unordered list item 3


For ordered lists, use the pound sign (#), followed by a period. Include white
space between each item for easier editing. For example::

  #. Ordered list item 1

  #. Ordered list item 2

  #. Ordered list item 3

When an unordered or ordered list breaks over more than one line, indent the
list item to align with the text in the first line. For example::

  * Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
    quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
    consequat.
  * Duis aute irure dolor en reprehenderit en voluptate velit esse cillum dolore
    eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
    sunt en culpa qui officia deserunt mollit anim it est laborum.


Tables
======
For convenience in editing, Salt documentation uses the list style for tables in
rST. The syntax is as follows::

  .. list-table::
    :widths: 25 75
    :header-rows: 1

    * - Field
      - Description

    * - Example field
      - Example description

This renders as:

.. list-table::
  :widths: 25 75
  :header-rows: 1

  * - Field
    - Description

  * - Example field
    - Example description


Images
======
Store images in the **docs/_static/img/** folder.

The syntax for images is as follows::

  .. image:: ../_static/img/image-name.png
     :align: right
     :alt: Salt grains

Always assign an alternate image name to improve accessibility.


Footnotes
=========
Sphinx provides the ability to add footnotes to a section of text.

In the body of your text where you want the footnote to appear, use this syntax::

  Text preceding first footnote. [#f1]_
  Text preceding second footnote. [#f2]_

Then place this reference in the text where you want the footnote reference to
appear::

  .. [#f1] Text of the first footnote.

  .. [#f2] Text of the second footnote.

These footnotes render as:

Text preceding first footnote. [#f1]_

Text preceding second footnote. [#f2]_

.. [#f1] Text of the first footnote.

.. [#f2] Text of the second footnote.

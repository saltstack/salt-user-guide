.. _style-guide:

======================================
Salt Project documentation style guide
======================================

Version 1.1 - last updated February 2022

Introduction
============
Welcome to the Salt Project documentation style guide. This style guide is
intended for use by project contributors, not necessarily end-users. It provides
general guidance to anyone who contributes to the Salt project's documentation
about:

* How to use and refer to Salt Project terms and other aspects of word choice.
* Grammar and formatting conventions such as capitalization, person, voice,
  formatting example code and IP addresses, and other stylistic conventions.

For additional help, see:

* :ref:`writing-salt-docs` - For information about the conventions we want you
  to use when formatting reStructured Text (rST).
* :ref:`contributing` - For more information about contributing to the Salt User
  Guide repository specifically, including setting up your environment.


.. Note::
    Not all the documentation you read at Salt will be perfect in following
    these guidelines. Treat this document as the guidelines we aspire to follow,
    not as a direct promise to perfectly comply with this guide in all Salt
    documentation.

    If you notice a style guide inconsistency, you are always welcome and
    encouraged to open a new issue explaining the problem. Better yet: we
    empower you to fix the issue yourself and open a merge or pull request.


Intended audience and scope
===========================
This style guide is intended for use by any contributors that are writing
documentation for the Salt project, including software engineers. This guide
can help project contributors to communicate clearly and consistently in the
Salt documentation.


Our preferred style guides: Google
==================================
We have adopted the Google's style guides as our preferred style guides for both
documentation and for formatting docstrings in Python.


Google style Python docstrings
------------------------------
We use the `Google Python Style Guide <https://google.github.io/styleguide/pyguide.html>`_
for formatting docstrings in our module documentation.

For the specific docstrings guidelines, see `Comments and docstrings <https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings>`_.

See also the `Sphinx Docs - Example Google style Python docstrings <https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html>`_.


Google developer documentation style
------------------------------------
We have adopted the `Google developer documentation style guide
<https://developers.google.com/style>`_ for Salt documentation. When writing
documentation for our project, align with the Google style guide's voice and
tone.

For a quick summary, see the `Google style guide highlights
<https://developers.google.com/style/highlights>`_. The rest of this document
describes our project-specific customizations to Google's guide.



Highlights from Google developer docs style guide
=================================================
We don't expect you to read the entire style guide, but we strongly recommend
checking out the `Style guide highlights
<https://developers.google.com/style/highlights>`_.

In addition to those highlights, the key elements from Google's style guide
that we want to ensure that you follow when writing Salt docs are highlighted
in the following sections.


Samples - Code, commands, and IP addresses
------------------------------------------
When documenting IP addresses and other URLs, apply the following guidelines:

* Inline code samples should be wrapped in backticks. For example:

  .. code-block:: bash

      ``name=testjob.``

* When referencing IP addresses, use the IP addresses that are specifically
  designated for examples. These are:

  * ``192.0.2.1``
  * ``198.51.100.1``
  * ``203.0.113.1``

* To reference filename placeholders in Linux commands, nest in the ``{{ }}``
  symbols, all lowercase, separated by hyphens. Example: ``{{file-name}}.zip.``


See Google's `Example domains and names
<https://developers.google.com/style/examples?hl=en>`_ for more information.


Use sentence case capitalization in headings
--------------------------------------------
In document titles and headings, use sentence case. That is, capitalize only the
first word in the title, the first word in a subheading after a colon, and any
proper nouns or other terms that are always capitalized a certain way.

See Google's `Capitalization in titles and headings
<https://developers.google.com/style/capitalization?hl=en#capitalization-in-titles-and-headings>`_
article for more information.


Use the second person
---------------------
Feel free to refer to our readers as "you." Using the second person is the
industry standard for technical writing. See Google's `Second person and first
person <https://developers.google.com/style/person>`_ article for more
information.


Glossary of preferred terms
===========================
The Salt Project is represented as "the Salt Project" or "Salt." The term "Salt"
is always capitalized, whether used as a noun or as an adjective.

The table provides guidelines about the terms you should and should not use for
consistency, listed in alphabetical order:

.. list-table::
  :widths: 20 40 40
  :header-rows: 1

  * - Word or phrase
    - Usage
    - Examples

  * - master, masters, Salt master, Salt masters, master service
    - * The term "master" should never be capitalized unless it is at the
        beginning of a heading.

      * In general, the first instance of this term in a topic should use the
        formal version of "Salt master." All other instances should use the
        shortened version of "master."

      * When referring to the Salt master service (such as starting or stopping
        the service), use "master service."
    - **Salty style:** The Salt master is a server that is running the master
      service. The master issues commands to one or more Salt  minions.

  * - minion, minions, Salt minion, Salt minions, minion service
    - * The term "minion" should never be capitalized unless it is at the
        beginning of a heading.

      * In general, the first instance of this term in a topic should use the
        formal version of "Salt minion." All other instances should use the
        shortened version of "minion."

      * When referring to the Salt minion service (such as starting or stopping
        the service), use "minion service."
    - **Salty style:** The Salt minions are servers that are running the
      minion service. The minions receive commands from the master.


General writing tips
====================
The following as some general guidelines recommended at Salt:

* **Point-of-view** - Use the second person, imperative tense where possible.
  For example: "Use ``test.ping`` to check if a minion is online."
* **Active voice** - Use active voice and present-tense. Avoid filler words.
* **Serial Commas** - When writing a list that includes three or more items, use
  the serial comma (or "Oxford comma"). For example: "France, Italy, and Spain."

For some additional general tips about improving writing and communication see:

* `Write the Docs - Style Guides <https://www.writethedocs.org/guide/writing/style-guides/#writing-style>`_
* `18F Content Guide <https://content-guide.18f.gov/>`_


Accessible writing
==================
Documentation should be written in a way that supports people with disabilities
and users with various input methods and devices. Improving accessibility also
helps make documentation clearer and more useful for everyone.

For resources on making your writing more accessible, see:

* `Writing accessible documentation - Google developer documentation style guide <https://developers.google.com/style/accessibility>`_
* `Accessibility guidelines and requirements - Microsoft Writing Style Guide <https://docs.microsoft.com/en-us/style-guide/accessibility/accessibility-guidelines-requirements>`_
* `Writing for Accessibility - Mailchimp Content Style Guide <https://styleguide.mailchimp.com/writing-for-accessibility/>`_


Inclusive and bias-free writing
===============================
When contributing to this project, you should strive to write documentation with
inclusivity and diversity in mind. Inclusive language recognizes diversity and
strives to communicate respectfully to all people. This kind of language is
sensitive to differences and seeks to promote equal opportunities.

For resources on making your writing more inclusive, see:

* `Inclusive documentation - Google developer documentation style guide <https://developers.google.com/style/inclusive-documentation>`_
* `The Conscious Style Guide - a collection of resources
  <https://consciousstyleguide.com/>`_
* `Bias-free communication - Microsoft Writing Style Guide <https://docs.microsoft.com/en-us/style-guide/bias-free-communication>`_
* `Guidelines for Inclusive Language - Linguistic Society of America <https://www.linguisticsociety.org/resource/guidelines-inclusive-language>`_

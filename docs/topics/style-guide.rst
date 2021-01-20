.. _style-guide:

================
Salt style guide
================

Version 1.0 - last updated January 2021

Introduction
============
Welcome to the Salt Project style guide! This style guide is intended for use by
project contributors, not necessarily end-users. It provides general guidance to
anyone who contributes to the Salt project's documentation.

Intended audience and scope
===========================
This style guide is intended for use by any contributors that are writing
documentation for the Salt project, including software engineers. This guide
can help project contributors to communicate clearly and consistently in the
Salt documentation.

Our preferred style guide
=========================
We have adopted the `Google developer documentation style guide
<https://developers.google.com/style>`_ for Salt documentation. For a quick
summary, see the `Google style guide highlights
<https://developers.google.com/style/highlights>`_.

The rest of this document describes our project-specific customizations to
Google's guide.

Our project uses standard American spelling and our preferred dictionary is the
`American Heritage Dictionary
<https://ahdictionary.com/>`_.

When writing documentation for our project, align with the Google style guide's
voice and tone.

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
    - The term "master" should never be capitalized unless it is at the
      beginning of a heading.

      In general, the first instance of this term in a topic should use the
      formal version of "Salt master." All other instances should use the
      shortened version of "master."

      When referring to the Salt master service (such as starting or stopping
      the service), use "master service."
    - **Salty style:** The Salt master is a server that is running the master
      service. The master issues commands to one or more Salt  minions.

  * - minion, minions, Salt minion, Salt minions, minion service
    - The term "minion" should never be capitalized unless it is at the
      beginning of a heading.

      In general, the first instance of this term in a topic should use the
      formal version of "Salt minion." All other instances should use the
      shortened version of "minion."

      When referring to the Salt minion service (such as starting or stopping
      the service), use "minion service."
    - **Salty style:** The Salt minions are servers that are running the
      minion service. The minions receive commands from the master.


.. Using linters
.. =============
.. This project uses the {our preferred linter.}

.. {Provide instructions or policies related to the linter here.}


General writing tips
====================
The following as some general guidelines recommended at Salt:

* **Point-of-view** - Use the second person, imperative tense where possible.
  For example: "Use ``test.ping`` to check if a minion is online."
* **Active voice** - Use active voice and present-tense. Avoid filler words.
* **Capitalization** - The Google Developer's Style Guide recommends using
  sentence case capitalization for titles and headings.
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

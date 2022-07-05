===============
Salt User Guide
===============

.. image:: https://img.shields.io/badge/slack-@saltstackcommunity-blue.svg?logo=slack
   :target: https://join.slack.com/t/saltstackcommunity/shared_invite/zt-3av8jjyf-oBQ2M0vhXOhJpNpRkPWBvg

.. image:: https://img.shields.io/twitch/status/saltprojectoss
   :target: https://www.twitch.tv/saltprojectoss

.. image:: https://img.shields.io/reddit/subreddit-subscribers/saltstack?style=social
   :target: https://www.reddit.com/r/saltstack/

.. image:: https://img.shields.io/twitter/follow/Salt_Project_OS?style=social&logo=twitter
   :target: https://twitter.com/intent/follow?screen_name=Salt_Project_OS

.. image:: https://img.shields.io/badge/stackoverflow-saltstack-orange.svg
   :target: https://stackoverflow.com/questions/tagged/salt-stack+or+salt-cloud+or+salt-creation+or+salt-contrib?sort=Newest

If you're looking to learn about Salt, you've come to the right place.

- `View the Sphinx-built documentation here <https://docs.saltproject.io/salt/user-guide/en/latest/index.html>`__
- `View the source repo here <https://gitlab.com/saltstack/open/docs/salt-user-guide>`__

About the Salt User Guide
=========================

The Salt User Guide supplements and extends the core documentation for the
`Salt Project <https://github.com/saltstack/salt>`__. This guide is intended to
help Salt users learn about Salt's core concepts and features. It was originally
authored by Alan Cugler and reviewed as a cross-collaborative effort between
many Salt experts.

Contributions from anyone inside the Salt project community are always welcome.
Please read the `Contributing to Salt documentation <CONTRIBUTING.md>`__ for
more information.


Related links
=============
Check out the following links related to the Salt User Guide:

* `Salt Project <https://github.com/saltstack/salt>`__: The repository for the
  Salt Project.
* `Salt Project Home Page <https://saltproject.io/>`__: The web portal for
  Salt community events and resources.
* `Contributing Guide <https://docs.saltproject.io/salt/user-guide/en/latest/topics/contributing.html>`__:
  For information about contributing to the Salt User Guide and other Salt
  documentation projects, including how to set up your environment and other
  policies around submitting merge requests or issues.
* `Salt Style Guide <https://docs.saltproject.io/salt/user-guide/en/latest/topics/style-guide.html>`__:
  For general guidance about using Salt Project terms and other style or
  formatting conventions.
* `Writing Salt documentation (rST guide) <https://docs.saltproject.io/salt/user-guide/en/latest/topics/writing-salt-docs.html>`__:
  For conventions and guidelines about formatting reStructured Text (rST) in
  Salt documentation.



Other Salt documentation
------------------------
The following documentation is part of the Salt Project documentation:

* `Salt Install Guide <https://docs.saltproject.io/salt/install-guide/en/latest/>`__:
  This guide provides instructions for installing Salt on Salt supported operating
  systems. It also explains how to configure Salt, start Salt services, and verify
  your installation.
* `Salt Project documentation <https://docs.saltproject.io/en/latest/contents.html>`__:
  Includes the full documentation for the Salt Project.
* `Module documentation <https://docs.saltproject.io/en/latest/py-modindex.html>`__:
  The Salt modules and state modules explain the use cases and arguments needed
  to execute the Salt modules.


Overview of the toolchain
=========================
This repository uses the following tools:

* The Salt User Guide documentation is composed in
  `reStructured text (rST) <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__,
  which is a version of Markdown that is generally used in Python-based projects.
* The rST is then run through `Sphinx <https://www.sphinx-doc.org/en/master/>`__,
  a static site generator that converts the rST into HTML for publication on the
  web.
* Sphinx applies the
  `Furo Theme for Sphinx <https://github.com/pradyunsg/furo>`__
  to render the site.
* The guide is also accessible directly on GitLab using the
  `GitLab pages <https://docs.gitlab.com/ee/user/project/pages/>`__ feature.
* GitLab handles the
  `CI/CD pipeline <https://gitlab.com/saltstack/open/docs/salt-user-guide/-/pipelines>`__
  for the project.
* Successful pipelines on the ``master`` branch get published to the ``docs.saltproject.io`` domain

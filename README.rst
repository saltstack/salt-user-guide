===============
Salt User Guide
===============

.. image:: https://img.shields.io/badge/slack-@saltstackcommunity-blue.svg?logo=slack
   :target: https://saltstackcommunity.herokuapp.com/

.. image:: https://img.shields.io/twitch/status/saltstackinc
   :target: https://www.twitch.tv/saltstackinc

.. image:: https://img.shields.io/reddit/subreddit-subscribers/saltstack?style=social
   :target: https://www.reddit.com/r/saltstack/

.. image:: https://img.shields.io/twitter/follow/saltstack?style=social&logo=twitter
   :target: https://twitter.com/intent/follow?screen_name=saltstack

.. image:: https://img.shields.io/badge/stackoverflow-saltstack-orange.svg
   :target: https://stackoverflow.com/questions/tagged/salt-stack+or+salt-cloud+or+salt-creation+or+salt-contrib?sort=Newest

If you're looking to learn about Salt, you've come to the right place!

- `View the Sphinx-built documentation here <https://saltstack.gitlab.io/open/docs/salt-user-guide>`__
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

* `Salt Style Guide <https://saltstack.gitlab.io/open/docs/salt-user-guide/topics/style-guide.html>`__
* `Salt Project <https://github.com/saltstack/salt>`__


Other Salt documentation
------------------------

The following documentation is part of the Salt Project documentation:

* `Salt Project documentation <https://docs.saltproject.io/en/latest/contents.html>`__:
  Includes the full documentation for the Salt Project.
* `Module documentation <https://docs.saltproject.io/en/latest/py-modindex.html>`__:
  The Salt modules and state modules explain the use cases and arguments needed
  to execute the Salt modules.


Overview of the toolchain
=========================

* The Salt User Guide documentation is composed in
  `reStructured text (rST) <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__,
  which is a version of Markdown that is generally used in Python-based projects.
* The rST is then run through `Sphinx <https://www.sphinx-doc.org/en/master/>`__,
  a static site generator that converts the rST into HTML for publication on the
  web.
* Sphinx applies the
  `SaltStack Material Theme for Sphinx <https://gitlab.com/saltstack/open/docs/sphinx-material-saltstack>`__
  to render the site.
* The guide is hosted directly on GitLab using the
  `GitLab pages <https://docs.gitlab.com/ee/user/project/pages/>`__ feature.
* GitLab handles the
  `CI/CD pipeline <https://gitlab.com/saltstack/open/docs/salt-user-guide/-/pipelines>`__
  for the project.

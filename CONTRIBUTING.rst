.. _contributing:

==================
Contributing guide
==================

Ways to contribute
==================

Here at the Salt Project, we value all contributions, not just contributions to
the code. In addition to contributing to the code, you can help the Salt Project
by:

* Writing, reviewing, and revising Salt documentation, modules, and tutorials
* Opening issues (documentation issues can be opened in this repository)
* Helping with user-to-user support questions
* Spreading the word about how great Salt is

The rest of this guide will explain our toolchain and how to set up your
environment to contribute to the Salt User Guide.


Related links
=============

For information about how to refer to Salt-specific terms and other
documentation-related conventions, check out the
`Salt Style Guide <https://gitlab.com/saltstack/open/salt-branding-guide>`__.

This project also makes use of the following in the toolchain:

* `reStructuredText Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__
* `Sphinx <https://www.sphinx-doc.org/en/master/>`__
* `GitLab Pages <https://docs.gitlab.com/ee/user/project/pages/>`__ for hosting
* `GitLab CI <https://docs.gitlab.com/ee/ci/>`__


Overview of how to contribute to this repository
================================================

To contribute to this repository, you first need to set up your repository for
the first time, you need to:

* `Fork, clone, and branch the repo`_
* `Set up your local preview environment`_

After this initial setup, you then need to:

* `Sync local master branch with upstream master`_
* Edit the documentation in reStructured Text
* `Preview HTML changes locally`_
* Open a merge request in Gitlab
* After a merge request gets approved, it can be merged!

At any time, you can ask a member of the documentation team for assistance.


Prerequisites
=============

For local development, the following prerequisites are needed:

* `git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`__
* `Python 3.6+ <https://realpython.com/installing-python/>`__
* `Ability to create python venv <https://realpython.com/python-virtual-environments-a-primer/>`__


Fork, clone, and branch the repo
================================

The Salt Project uses the fork and branch Git workflow. For an overview of this method,
see
`Using the Fork-and-Branch Git Workflow <https://blog.scottlowe.org/2015/01/27/using-fork-branch-git-workflow/>`__.

First,
`create a new fork <https://gitlab.com/saltstack/open/docs/salt-user-guide/-/forks/new>`__.
Fork the repository into your personal GitLab user workspace.

Then, clone the forked repo to your local machine:

.. code-block:: bash

    # SSH
    git clone git@gitlab.com:<forked-repo-path>/salt-user-guide.git

    # or HTTPS
    git clone https://gitlab.com/<forked-repo-path>/salt-user-guide.git

Configure the remotes for your main upstream repository:

.. code-block:: bash

    # Move into cloned repo
    cd salt-user-guide

    ## Choose SSH or HTTPS upstream endpoint
    # SSH
    git remote add upstream git@gitlab.com:saltstack/open/docs/salt-user-guide.git
    # or HTTPS
    git remote add upstream https://gitlab.com/saltstack/open/docs/salt-user-guide.git

Create new branch for changes to submit:

.. code-block:: bash

    git checkout -b my-new-feature

Set up your local preview environment
=====================================

If you are not on a Linux machine, you need to set up a virtual environment to
preview your local changes and ensure the `prerequisites`_ are met for a Python
virtual environment.

From within your local copy of the forked repo:

.. code-block:: bash

    # Setup venv
    python3 -m venv .venv
    # If Python 3.6+ is in path as 'python', use the following instead:
    # python -m venv .venv

    # Activate venv
    source .venv/bin/activate

    # Install required python packages to venv
    pip install -U pip setuptools wheel
    # The requirements-dev.txt file includes pre-commit and nox
    pip install -r requirements-dev.txt

    # Setup pre-commit
    pre-commit install

All required files should now be in place.

``pre-commit`` and ``nox`` Setup
--------------------------------

Here at Salt we use `pre-commit <https://pre-commit.com/>`__ and
`nox <https://nox.thea.codes/en/stable/>`__ to make it easier for
contributors to get quick feedback, for quality control, and to increase
the chance that your merge request will get reviewed and merged.

``nox`` handles Sphinx requirements and plugins for you, always ensuring your
local packages are the needed versions when building docs. You can think of it
as Make with superpowers.


What is pre-commit?
-------------------

``pre-commit`` is a tool that will automatically run
local tests when you attempt to make a git commit. To view what tests are run,
you can view the ``.pre-commit-config.yaml`` file at the root of the
repository.

One big benefit of pre-commit is that *auto-corrective measures* can be done
to files that have been updated. This includes Python formatting best
practices, proper file line-endings (which can be a problem with repository
contributors using differing operating systems), and more.

If an error is found that cannot be automatically fixed, error output will help
point you to where an issue may exist.

.. warning::

    Currently there is an issue with the pip-tools-compile pre-commit hook on Windows.
    The details around this issue are included here:
    https://github.com/saltstack/salt/issues/56642.
    Please ensure you export ``SKIP=pip-tools-compile`` to skip pip-tools-compile.


Sync local master branch with upstream master
=============================================

If needing to sync feature branch with changes from upstream master, do the
following:

.. note::

    This will need to be done in case merge conflicts need to be resolved
    locally before a merge to master in the upstream repo.

.. code-block:: bash

    git checkout master
    git fetch upstream
    git pull upstream master
    git push origin master
    git checkout my-new-feature
    git merge master


Preview HTML changes locally
============================

To ensure that the changes you are implementing are formatted correctly, you
should preview a local build of your changes first. To preview the changes:

.. code-block:: bash

    # Activate venv
    source .venv/bin/activate

    # Generate HTML documentation with nox
    nox -e 'docs-html(clean=False)'

    # Sphinx website documentation is dumped to docs/_build/html/*
    # You can view this locally
    # firefox example
    firefox docs/_build/html/index.html

.. note::

    If you encounter an error, you might need to re-install the requirements
    file. See the instructions in
    `Set up your local preview environment`_.


Preview changes in Gitlab Pages
===============================

After you submit a merge request to this repo, the documentation generated by
Sphinx in this repository is published via GitLab Pages. This feature allows
you to share a preview of your changes with the merge approvers.

Each forked repository has their own GitLab Pages deployed website! Example
format of your Gitlab pages preview URL:

* `<https://scriptautomate.gitlab.io/salt-user-guide/>`__

To preview a GitLab Pages deployment for the main repository or a fork, do the
following:

.. code-block:: text

    # Example URL of forked repository
    # GitLab Repository
    https://gitlab.com/<username>/salt-user-guide

    # Change the beginning of the URL, ending with this format
    # GitLab Pages
    https://<username>.gitlab.io/salt-user-guide

Notice that ``https://gitlab.io/<username>`` changed to
``https://<username>.gitlab.io``.


Single-branch deployment warning
--------------------------------

**GitLab Pages** will always deploy the **latest branch** of a repository. Keep
this in mind when it comes to forks or the upstream repo, as the latest branch
to be pushed to the repository will be what GitLab Pages deploys. It is not
possible to have multiple branches viewable in GitLab Pages at the same time for
a repository.

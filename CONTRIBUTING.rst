.. _contributing:

==================================
Contributing to Salt documentation
==================================

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

For additional help, see:

* :ref:`style-guide` - For general guidance about using Salt Project terms
  and other style or formatting conventions.
* :ref:`writing-salt-docs` - For information about the conventions we want you
  to use when formatting reStructured Text (rST).


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
  `SaltStack Material Theme for Sphinx <https://gitlab.com/saltstack/open/docs/sphinx-material-saltstack>`__
  to render the site.
* The guide is hosted directly on GitLab using the
  `GitLab pages <https://docs.gitlab.com/ee/user/project/pages/>`__ feature.
* GitLab handles the
  `CI/CD pipeline <https://gitlab.com/saltstack/open/docs/salt-user-guide/-/pipelines>`__
  for the project.
* `EditorConfig <https://editorconfig.org/>`__ is an optional tool you can use
  with your preferred editor to ensure that you follow the Salt Project coding
  guidelines.


Overview of how to contribute to the Salt User Guide repository
===============================================================
To contribute to this repository, you first need to set up your own local repository:

* `Fork, clone, and branch the repo`_
* `Set up your local preview environment`_

After this initial setup, you then need to:

* `Sync local master branch with upstream master`_
* Edit the documentation in reStructured Text
* `Preview HTML changes locally`_
* Open a merge request in Gitlab

Once a merge request gets approved, it can be merged.
At any time, you can ask a member of the documentation team for assistance.


Prerequisites
=============
Contributing to Salt requires an account on `GitLab.com <https://about.gitlab.com/>`__.
If you do not already have one, create a free account on the `GitLab sign-up page <https://gitlab.com/users/sign_up/>`__.

For local development, the following prerequisites are needed:

* `git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`__
* `Python 3.7+ <https://realpython.com/installing-python/>`__
* `Ability to create python venv <https://realpython.com/python-virtual-environments-a-primer/>`__
* `vale <https://docs.errata.ai/vale/install>`__
* `vendir <https://carvel.dev/#install>`__


Linux/macOS users
-----------------
We recommend installing `Homebrew <https://brew.sh/>`__, as it allows easy installation of
`vale <https://docs.errata.ai/vale/install>`__ and `vendir <https://carvel.dev/#install>`__.

To install Homebrew:

.. code-block:: bash

   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


You can then proceed with installing prerequisites:

.. code-block:: bash

   # Update Homebrew
   brew update

   # vale
   brew install vale

   # vendir
   brew tap vmware-tanzu/carvel
   brew install vendir


Windows users
-------------
For the best experience, when contributing from a Windows OS to projects using
Python-based tools like ``pre-commit``, we recommend setting up `Windows Subsystem
for Linux (WSL) <https://docs.microsoft.com/en-us/windows/wsl/>`__, with the
latest version being WSLv2.

The following gists on GitHub have been consulted with success for several
contributors:

* `Official Microsoft docs on installing WSL <https://docs.microsoft.com/en-us/windows/wsl/install-win10>`__

* Alternatively, you can download and install it from the Microsoft store, which
  you can access by typing ``store`` in the Start menu search.

Some additional helpful resources:

* Some Windows users enjoy using Windows Terminal to access the WSL command
  line. See `Windows Terminal installation <https://docs.microsoft.com/en-us/windows/terminal/install>`_.

* If you're using Windows Terminal and Ubuntu, see `How to add Ubuntu Tab to Windows 10’s New Terminal <https://rkstrdee.medium.com/how-to-add-ubuntu-tab-to-windows-10s-new-terminal-271eb6dfd8ee>`_.

* You might also want to install the Magic Monty Git Bash Prompt utility, which
  provides some nice Git highlighting features for quality of life. See
  `Installing Git Bash Prompt via a Git clone <https://github.com/magicmonty/bash-git-prompt#via-git-clone>`_.

* A list of PowerShell commands in a gist to `Enable WSL and Install Ubuntu 20.04
  <https://gist.github.com/ScriptAutomate/f94cd44dacd0f420fae65414e717212d>`__.

* Ensure you also read the comment thread below the main content for additional
  guidance about using Python on the WSL instance.

We recommend `Installing Chocolatey on Windows 10 via PowerShell w/ Some Starter
Packages <https://gist.github.com/ScriptAutomate/02e0cf33786f869740ee963ed6a913c1>`__.
This installs ``git``, ``microsoft-windows-terminal``, and other helpful tools
via the awesome Windows package management tool, `Chocolatey <https://chocolatey.org/why-chocolatey>`__.

``choco install git`` easily installs ``git`` for a good Windows-dev experience.
From the ``git`` package page on Chocolatey:

* Git BASH
* Git GUI
* Shell Integration

If you're using WSL, proceed with installing requirements from `Linux/macOS users`_ above.

Otherwise, you can then proceed with installing prerequisites:

.. code-block:: bash

   # vale
   choco install vale

   # vendir
   choco install vendir


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

.. note::

    Before cloning your forked repo, you need to create an SSH
    key so that your local Git repository can authenticate to the GitLab remote
    server. See `GitLab and SSH keys <https://docs.gitlab.com/ee/ssh/README.html>`__
    for instructions.

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


Configure your editor (optional)
================================
`EditorConfig <https://editorconfig.org/>`__ is an optional tool you can use
with your preferred code/text editor to ensure that you follow the Salt Project
coding and style guidelines. To enable EditorConfig, check the compatibility
and configuration settings for your preferred code/text editor.

Using EditorConfig is optional for contributing to this repository, but
recommended.


Set up your local preview environment
=====================================
If you are not on a Linux machine, you need to set up a virtual environment to
preview your local changes and ensure the `prerequisites`_ are met for a Python
virtual environment.

From within your local copy of the forked repo:

.. code-block:: bash

    # Setup venv
    python3 -m venv .venv
    # If Python 3.7+ is in path as 'python', use the following instead:
    # python -m venv .venv

    # Activate venv
    source .venv/bin/activate
    # On Windows, use instead:
    # .venv/Scripts/activate

    # Install required python packages to venv
    pip install -U pip setuptools wheel
    # The requirements-dev.txt file includes pre-commit and nox
    pip install -r requirements-dev.txt

    # Setup pre-commit
    pre-commit install

    # If you want to use Vale's in-editor style checking immediately
    # (Will be pulled down automatically at first commit)
    pre-commit run vendir


All required files should now be in place.


``pre-commit``, ``nox``, and ``vale`` setup
-------------------------------------------
Here at Salt we use `pre-commit <https://pre-commit.com/>`__,
`nox <https://nox.thea.codes/en/stable/>`__, and `vale <https://docs.errata.ai/vale/about>`__
to make it easier for contributors to get quick feedback, for quality control,
and to increase the chance that your merge request will get reviewed and merged.

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

If pre-commit fails, try running it a second time. Sometimes on the first
pass, pre-commit automatically fixes any errors (such as line ending
characters that are weirdly added by Windows operating systems). If you
run pre-commit a second time, it should pass. If it doesn't pass again,
that means you have a genuine error that you need to fix. Use the error
codes and messages to troubleshoot.

.. warning::

    Currently there is an issue with the pip-tools-compile pre-commit hook on
    Windows. The details around this issue are included here:
    https://github.com/saltstack/salt/issues/56642.
    Please ensure you export ``SKIP=pip-tools-compile`` to skip pip-tools-compile.


What is Vale?
-------------
``vale`` is a tool that will automatically run from ``pre-commit`` to enforce the
:ref:`style-guide` and suggest general writing guidelines
when you attempt to make a git commit.

Vale can check your writing in real-time (or near-realtime) in a wide variety of
editors, including plugins for:

* `Atom <https://atom.io/packages/atomic-vale>`__
* `Vim <https://github.com/lgalke/vim-compiler-vale>`__
* `Sublime Text <https://packagecontrol.io/packages/SublimeLinter-contrib-vale>`__
* `Visual Studio Code <https://github.com/errata-ai/vale-vscode>`__

This permits you to view errors immediately rather than having to wait until
pre-commit is run when your changes are checked in. While the command-line version
of vale won't automatically make corrections for you, there is also a reasonably priced
commercial version called `Vale Server <https://errata.ai/vale-server/>`__ which does
permit auto-correction (along with other features).


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
should preview a local build of your changes first.

For simplified workflow, a live-reload version of the documentation can run in
the background while writing docs. To build and serve the Sphinx HTML
documentation, with live-reloading on all file changes (for every save):

.. code-block:: bash

    # Activate venv
    source .venv/bin/activate
    # On Windows, use instead:
    # .venv/Scripts/activate

    # Generate live-reload of documentation in web browser
    # Use CTRL+C in the terminal when done, to close the session
    nox -e docs

To preview how the CI tooling generates the HTML for usage, without live-reloading:

.. code-block:: bash

    # Activate venv
    source .venv/bin/activate
    # On Windows, use instead:
    # .venv/Scripts/activate

    # Generate HTML documentation with nox
    nox -e 'docs-html(clean=False)'

    # Sphinx website documentation is dumped to docs/_build/html/*
    # You can view this locally
    # firefox example
    firefox docs/_build/html/index.html

The above two approaches view the same docs output, just one is live-reloading.

.. note::

    If you encounter an error, you might need to re-install the requirements
    file. See the instructions in
    `Set up your local preview environment`_.


Preview changes in GitLab Pages
===============================
After you submit a merge request to this repo, the documentation generated by
Sphinx in this repository is published via GitLab Pages. This feature allows
you to share a preview of your changes with the merge approvers.

Each forked repository has their own GitLab Pages deployed website. Example
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

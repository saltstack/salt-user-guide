"""
noxfile
~~~~~~~

Nox configuration script

Modified from original source found in the Salt project:
- https://github.com/saltstack/salt
"""

import datetime
import os
import sys

# fmt: off
if __name__ == "__main__":
    sys.stderr.write(
        "Do not execute this file directly. Use nox instead, it will know how to handle this file\n"
    )
    sys.stderr.flush()
    exit(1)
# fmt: on

import nox  # isort:skip
from nox.command import CommandFailed  # isort:skip

# Global Path Definitions
REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
# Python versions to run against
_PYTHON_VERSIONS = ("3", "3.6", "3.7", "3.8", "3.9")

# Nox options
#  Reuse existing virtualenvs
nox.options.reuse_existing_virtualenvs = True
#  Don't fail on missing interpreters
nox.options.error_on_missing_interpreters = False

# Change current directory to REPO_ROOT
os.chdir(REPO_ROOT)

RUNTESTS_LOGFILE = os.path.join(
    "artifacts",
    "logs",
    "runtests-{}.log".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f")),
)

# Prevent Python from writing bytecode
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


def _get_session_python_version_info(session):
    try:
        version_info = session._runner._real_python_version_info
    except AttributeError:
        old_install_only_value = session._runner.global_config.install_only
        try:
            # Force install only to be false for the following chunk of code
            # For additional information as to why see:
            #   https://github.com/theacodes/nox/pull/181
            session._runner.global_config.install_only = False
            session_py_version = session.run(
                "python",
                "-c"
                'import sys; sys.stdout.write("{}.{}.{}".format(*sys.version_info))',
                silent=True,
                log=False,
            )
            version_info = tuple(
                int(part) for part in session_py_version.split(".") if part.isdigit()
            )
            session._runner._real_python_version_info = version_info
        finally:
            session._runner.global_config.install_only = old_install_only_value
    return version_info


def _get_pydir(session):
    version_info = _get_session_python_version_info(session)
    if version_info < (3, 5):
        session.error("Only Python >= 3.6 is supported")
    return "py{}.{}".format(*version_info)


def _install_requirements(session, transport):
    # Latest pip, setuptools, and wheel
    install_command = ["--progress-bar=off", "-U", "pip", "setuptools", "wheel"]
    session.install(*install_command, silent=True)

    # Install requirements
    requirements_file = os.path.join("docs/requirements.txt")
    install_command = ["--progress-bar=off", "-r", requirements_file]
    session.install(*install_command, silent=True)


@nox.session(name="docs-html", python="3")
@nox.parametrize("clean", [False, True])
def docs_html(session, clean):
    """
    Build Sphinx HTML Documentation
    """
    pydir = _get_pydir(session)

    # Latest pip, setuptools, and wheel
    install_command = ["--progress-bar=off", "-U", "pip", "setuptools", "wheel"]
    session.install(*install_command, silent=True)

    # Install requirements
    requirements_file = os.path.join("docs/requirements.txt")
    install_command = ["--progress-bar=off", "-r", requirements_file]
    session.install(*install_command, silent=True)
    os.chdir("docs/")
    if clean:
        session.run("make", "clean", external=True)
    session.run("make", "html", "SPHINXOPTS=-Wn", external=True)

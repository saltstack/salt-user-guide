.. _troubleshooting:

===============
Troubleshooting
===============

Generally speaking, troubleshooting anything requires finesse, but here are
some common patterns for you to keep in mind. For more tips, see this Salt `Troubleshooting
<https://docs.saltproject.io/en/master/topics/troubleshooting/>`__ guide.

Checking process status
=======================
The Salt master, minion, and proxies are run as system processes in the
``systemd`` service, and managed by ``systemctl``.

Check the status to see if the process is running or if it has encountered an error:

.. code-block:: shell

    systemctl status salt-minion

Alternately, bypass ``systemd`` and run the process in the foreground.
For example, with log level debugging:

.. code-block:: shell

    salt-master -l debug

.. code-block:: shell

    salt-minion -l debug

Viewing log files
=================
The log file locations for the master, minion, and proxy processes are configured
via the configuration files. Their default location is ``/var/log/salt``.
It may be helpful to view the log files with ``tail``:

.. code-block:: shell

    tail -f /var/log/salt/master

.. code-block:: shell

    tail -f /var/log/salt/minion

.. code-block:: shell

    tail -f /var/log/salt/proxy

Log levels
----------
The following log levels are available in Salt:

.. list-table::
  :widths: 20 20 60
  :header-rows: 1

  * - Level
    - Numeric Value
    - Description

  * - quiet
    - 1000
    - Nothing logged

  * - critical
    - 50
    - Critical errors

  * - error
    - 40
    - Errors

  * - warning
    - 30
    - Warnings

  * - info
    - 20
    - Normal log information

  * - profile
    - 15
    - Profiling information on salt performance

  * - debug
    - 10
    - Information useful for debugging

  * - trace
    - 5
    - Even more debugging information

  * - all
    - 0
    - Everything

You can change the log level via the configuration file:

.. code-block:: yaml
   :caption: /etc/salt/minion.d/logs.conf

    log_file: /var/log/salt/minion  # default
    log_level: debug

You must restart the process for the configuration changes to take effect:

.. code-block:: shell

    systemctl restart salt-minion

Viewing Salt events
===================
Salt achieves remote execution by having the master publish “events”, while the
minions listening to this event bus execute the commands in which they are targeted.
The master's event bus can be viewed in real time with ``salt-run``:

.. code-block:: shell

    salt-run state.event pretty=True

Opening ports
=============
Salt master and minions require two open ports for communication.
By default, port ``4505`` is for publishing or subscribing to the master’s event bus,
and port ``4506`` is for returning data. These can be configured via the
master / minion configuration files:

In the master configuration file:

.. code-block:: yaml

    publish_port: 4505
    ret_port: 4506

In the minion configuration file:

.. code-block:: yaml

    publish_port: 4505
    master_port: 4506

.. Tip::
    Make sure your firewall is not blocking these ports, if applicable.

Salt keys
=============
``salt-key`` is a valuable utility for managing key acceptance.
However, it may be beneficial to understand how Salt stores this
information in the file system.

The accepted and rejected minion keys are stored on the master’s file system
``/etc/salt/pki/master/``

In this directory you will find the master’s public and private key and several
other directories for storing the incoming minion key according to its state.
Once the keys are accepted, they will be stored in
``/etc/salt/pki/master/minions/<minion-id>``
``<minion-id>`` is the id of the minion in question.

On the minion, the keys are stored in ``/etc/salt/pki/minion/``.
Here you will find the minion’s private and public keys as well as the public key
for it’s master (in a file named ``minion_master.pub``)

.. Tip::
    If the master or minion’s key has changed, Salt will have to accept the new key.
    If a previous key had been accepted (on the master / minion) this file may
    need to be deleted (manually or with ``salt-key``),
    and the master / minion processes restarted.

Troubleshooting states
======================
The following steps typically occur when a state is executed:

#.  Render template (such as Jinja)
#.  Compile YAML to “high-data”
#.  Compile “high data” to “low data”
#.  Execute each low chunk until complete

To diagnose problems, try performing single steps along this execution.
For example, we can render the Jinja with the following:

.. code-block:: shell

    salt <tgt> slsutil.renderer <my_custom_state> default_renderer=jinja

Jinja and YAML (in order) are rendered by default.

.. code-block:: shell

    salt <tgt> slsutil.renderer <my_custom_state>

The above commands are for rendering the file from a Jinja / YAML perspective.
The rendered SLS is similar since the state system will render Jinja / YAML.
However, this command includes keys added during the state system render phase:

.. code-block:: shell

    salt <tgt> state.show_sls <my_custom_state>

This can be a useful command especially when passing pillars from the command line:

.. code-block:: shell

    salt <tgt> state.show_sls <my_custom_state> pillar='{"foo": "bar"}'

Salt states can be executed in test mode, by setting the flag :code:`test=True`:

.. code-block:: shell

    salt <tgt> state.apply <my_custom_state> test=True

Here the state is rendered and evaluated as much as possible,
yet changes are not applied to the remote device.

Adding logging to custom modules
================================
After creating a custom module, add logging in the normal python way:

.. code-block:: python
   :caption: /srv/salt/_modules/my_custom_module.py

   import logging

   log = logging.getLogger(__name__)


   def hello():
       log.debug("hello is running...")
       return "hello"

In the above example, set the log level to ``debug`` or lower.

Debugging reactor states
========================
The best way to debug Reactor States is to use multiple views into the
Salt master and then fire some specific events:

* Monitor the Salt master log file: ``/var/log/salt/master``.
  This will help to debug Jinja / YAML errors in the Reactor SLS file.
* Monitor the Event Bus: ``salt-run state.event pretty=True``.
  Watch for the triggering event as well as the Reactor events.
* Fire events manually to trigger the Reactor.

Problems with sync/cache
========================
Salt stores all modules and other files in the minions cache, typically
located under ``/var/cache/salt``. If custom modules aren’t behaving
the way you think they should, it's possible that the cache is not up to date.
All custom modules must be synced to the minions:

.. code-block:: shell

    salt \* saltutil.sync_all

But if a file is deleted, you must also clear the cache and re-sync:

.. code-block:: shell

    salt \* saltutil.clear_cache
    salt \* saltutil.sync_all

When in doubt, it may be helpful to restart the minion process:

.. code-block:: shell

    systemctl restart salt-minion

Troubleshoot rendering
======================

Render json file
----------------
Loads json data from an absolute path:

.. code-block:: shell

    salt \* jinja.import_JSON /srv/salt/foo.json

Render YAML file
----------------
Loads YAML data from an absolute path:

.. code-block:: shell

    salt \* jinja.import_yaml /srv/salt/foo.yaml

Render a map file
-----------------
Assuming the map is loaded in your formula SLS as follows:

.. code-block:: sls

    {% from "foo/map.jinja" import bar with context %}

Then the following syntax can be used to render the map variable ``bar``:

.. code-block:: shell

    $ salt \* jinja.load_map /srv/salt/foo/map.jinja bar

.. _salt-grains:

===========
Salt grains
===========

.. _salt-grains-use-case:

Use case
========

Salt comes with an interface to derive information about the underlying
system. This is called the grains interface, because it presents Salt
with grains of information. Grains are collected for the operating
system, domain name, IP address, kernel, OS type, memory, and many other
system properties.

The grains interface is made available to Salt modules and components so
that the right Salt minion commands are automatically available on the
right systems.

Grain data is relatively static. However, if system information changes
(such as network settings), or if a new value is assigned to a custom
grain, grain data is refreshed.

.. note::

   Grains resolve to lowercase letters. For example, ``FOO`` and ``foo``
   target the same grain.

.. _salt-grains-key-concepts:

Grains of Salt: Key concepts          
----------------------------

.. image:: ../_static/img/grains.jpeg
   :align: right
   :alt: Salt grains

*  Grains comprise system properties or other custom attributes.
*  Though grains can be defined in several ways, they are always derived
   or defined on the minion.
*  Grains cover data such as: ``os``, ``kernel``, ``ip_interfaces``, and
   ``minion`` id.
*  Grains are generally used to determine things like which package
   manager should be used or if the init system is powered by systemctl.
*  The grains interface is available to Salt modules and components so
   that the right Salt minion commands are automatically available on
   the right systems.

.. _salt-grains-commands:

Grains terminal commands
========================

.. _salt-grains-commands-listing:

Listing grains
--------------

Available grains can be listed by using the ``grains.ls``  module:

.. code-block:: bash

   salt '*' grains.ls

Grains data can be listed by using the ``grains.items`` module:

.. code-block:: bash

   salt '*' grains.items

.. _salt-grains-commands-targeting:

Targeting with grains
---------------------

Grain data can be used when targeting minions.

For example, the following command matches all CentOS minions:

.. code-block:: bash

   salt -G 'os:CentOS' test.version

This command matches all minions with 64-bit CPUs, and return number of
CPU cores for each matching minion:

.. code-block:: bash

   salt -G 'cpuarch:x86_64' grains.item num_cpus

Additionally, globs can be used in grain matches, and grains that are
nested in a dictionary can be matched by adding a colon for each level
that is traversed. For example, the following command will match hosts
that have a grain called ``ec2_tags``, which itself is a dictionary with a
key named environment and which has a value that contains the word
production:

.. code-block:: bash

   salt -G 'ec2_tags:environment:*production*'

.. _salt-grains-config-settings:

Configuration settings          
======================

To automatically accept minions based on certain characteristics, such
as the uuid, you can specify certain grain values on the Salt master.
Minions with matching grains will have their keys automatically
accepted.

#. Configure the ``autosign_grains_dir`` in the Salt master config file:

   .. code-block:: yaml
      :caption: /etc/salt/master.d/grains.conf
      :name: /etc/salt/master.d/grains.conf

      autosign_grains_dir: /etc/salt/autosign_grains

#. Configure the grain values to be accepted:

   Place a file named like the grain in the ``autosign_grains_dir`` and write
   the values that should be accepted automatically inside that file. For
   example, to automatically accept minions based on their uuid, create a
   file named:

   .. code-block:: text
      :caption: /etc/salt/autosign_grains/uuid
      :name: /etc/salt/autosign_grains/uuid

      8f7d68e2-30c5-40c6-b84a-df7e978a03ee
      1d3c5473-1fbc-479e-b0c7-877705a0730f

The Salt master is now set up to accept minions with either of the two
specified uuids. Multiple values must always be written into separate
lines. Lines starting with a # are ignored.

#. Configure the Salt minion, to send the specific grains to the Salt master,
   in the ``minion`` config file:

   .. code-block:: yaml
      :caption: /etc/salt/minion
      :name: /etc/salt/minion

      autosign_grains:
        - uuid

Now you should be able to start ``salt-minion`` and run ``salt-call
state.apply`` or any other Salt commands that require Salt master
authentication.

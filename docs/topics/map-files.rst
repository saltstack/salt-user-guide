.. _map-files:

=========
Map files
=========

Use case
========

Map files are crucial for leveraging large clusters that are experiencing performance issues.

* Map files provide a place to add in central data not needing pillar encryption.
* Map files allow advanced variable mapping, with Jinja logic, to be abstracted away from the Salt states.
* Instead of the default Jinja rendering to YAML, you can also set map files to use other renderers such as Python or JSON.

Jinja logic abstraction
=======================

Map files allow Jinja logic to be isolated from the Salt states, keeping the Salt states straightforward and organized.

Static lookup data
==================

Instead of adding data dictionaries as Jinja in the Salt states, you can separate the data that a state uses from the state itself. This increases the flexibility and reusability of a state.  Some examples are:

* Platform-specific package names and file system paths
* Defaults for an application
* Common settings within a company or organization

Organizing the state data as a dictionary (such as a hash map, lookup table, or associative array) often provides lightweight namespacing and allows for simple lookups.
Using a dictionary also allows for easier merging, and for overriding static values within a lookup table that has dynamic values fetched from pillar.

The convention in Salt formulas is to place platform-specific data, such as package names and file system paths, into a file named ``map.jinja`` that is placed alongside the state files.

The syntax for referencing a value is a normal dictionary lookup in Jinja, such as ``{{ mysql['service'] }}`` or the shorthand ``{{ mysql.service }}``.

.. code-block:: sls
	:caption: /srv/salt/mysql/map.jinja

	{% set mysql = salt['grains.filter_by']({
		'Debian': {
			'server': 'mysql-server',
			'client': 'mysql-client',
			'service': 'mysql',
			'config': '/etc/mysql/my.cnf',
			'python': 'python-mysqldb',
		},
		'RedHat': {
			'server': 'mysql-server',
			'client': 'mysql',
			'service': 'mysqld',
			'config': '/etc/my.cnf',
			'python': 'MySQL-python',
		},
		'Gentoo': {
			'server': 'dev-db/mysql',
			'client': 'dev-db/mysql',
			'service': 'mysql',
			'config': '/etc/mysql/my.cnf',
			'python': 'dev-python/mysql-python',
		},
	}, merge=salt['pillar.get']('mysql:lookup')) %}


Values defined in the map file can be fetched for the current platform in any state file using the following syntax:

.. code-block:: sls
    :caption: /srv/salt/mysql/init.sls

    {% from "mysql/map.jinja" import mysql with context %}

    mysql-server:
      pkg.installed:
        - name: {{ mysql.server }}
      service.running:
        - name: {{ mysql.service }}

Organizing pillar data
----------------------

It is considered best practice to make formulas expect all formula-related parameters be placed under a second-level lookup key, within a main namespace designated for holding data for a particular service or software. This is managed by the formula:

.. code-block:: yaml

    mysql:
      lookup:
        version: 5.8.11

Alternate map rendering
=======================

One possible use is to allow writing map files, commonly seen in Salt formulas, but without tying the renderer of the map file to the renderer used in the other SLS files.
In other words, a map file could use the Python renderer and still be included and used by an SLS file that uses the default ``jinja|yaml`` renderer.

For example, the two following map files produce identical results, but one is written using the normal ``jinja|yaml`` and the other is using ``py``:

.. code-block:: sls

    #!jinja|yaml
    {% set apache = salt.grains.filter_by({
        ...normal jinja map file here...
    }, merge=salt.pillar.get('apache:lookup')) %}
    {{ apache | yaml() }}

.. code-block:: sls

    #!py
    def run():
        apache = __salt__.grains.filter_by({
            ...normal map here but as a python dict...
        }, merge=__salt__.pillar.get('apache:lookup'))
        return apache


Regardless of which of the above map files is used, it can be accessed from any other SLS file by calling this function. The following is a usage example in Jinja:

.. code-block:: sls

    {% set apache = salt.slsutil.renderer('map.sls') %}

Troubleshoot rendering
======================

The Jinja rendering module has functions for rendering JSON, YAML, and general map files.

Render JSON file
----------------

Loads JSON data from the absolute path:

.. code-block:: bash

    salt \* jinja.import_JSON /srv/salt/foo.json

Render YAML file
----------------

Loads YAML data from the absolute path:

.. code-block:: bash

    salt \* jinja.import_yaml /srv/salt/foo.yaml

Render a map file
-----------------

If the map is loaded in your Salt state file as follows:

.. code-block:: bash

    {% from "foo/map.jinja" import bar with context %}

Then the following syntax can be used to render the map variable ``bar``:

.. code-block:: bash

    salt \* jinja.load_map /srv/salt/foo/map.jinja bar

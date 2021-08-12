.. _pillar:

======
Pillar
======

Pillar use case
===============
Salt pillar brings data into the cluster from the opposite direction as grains. While grains data is generated from the minion, the pillar is data generated from the master.

Pillars are organized similarly to states in a Pillar state tree, where ``top.sls`` acts to coordinate pillar data to environments and minions with access to the data.

**Highly sensitive data**:

*  Information transferred via pillar has a dictionary generated for the targeted minion and encrypted with that minion’s key for secure data transfer. This makes pillar suitable for managing security information, such as cryptographic keys and passwords.
*  Configuration data for applications can be stored in pillar, and the data is passed to execution modules to determine how to configure the application.
*  Pillar data is encrypted on a per-minion basis. This encryption makes it useful for storing sensitive data specific to a particular minion.

**Minion configuration**:

*  Minion modules such as the execution modules, states, and returners can often be configured via data stored in pillar.
*  Pillar data is targeted to minions using a pillar top file.

.. note::
  By default, the contents of the master configuration file are not loaded into pillar for all minions, but this behavior is configured with the ``pillar_opts: False`` option in the master configuration.
  If enabled, this allows the master configuration file to be used for global configuration of minions.


Basics
======
Pillar SLS files can contain any type of YAML structure:

.. code-block:: sls
   :caption: /srv/pillar/top.sls

    base:
      '*':
        - example

.. code-block:: sls
   :caption: /srv/pillar/example.sls

    pillar1: value
    pillar2:
      - value
      - value
    pillar3:
      sub_key:
        - value
        - value

A few things to note about pillar structures:

*  Pillars can be defined in pillar state files.
*  Pillar data must be serialized data structures such as strings, lists, and dictionaries.
*  Pillar data is typically defined and represented in YAML.


Rendering pillar
================
To view pillar data, use the pillar execution module. This module includes several functions, each with their own use. These functions include:

.. list-table::
  :widths: 20 80
  :header-rows: 0

  * - :code:`pillar.item`
    - Retrieves the value of one or more keys from the in-memory pillar data.

  * - :code:`pillar.items`
    - Compiles and returns a fresh pillar dictionary, leaving the in-memory pillar data untouched. If pillar keys are passed to this function however, this function acts like pillar.item and returns their values from the in-memory pillar data.

  * - :code:`pillar.raw`
    - Like pillar.items, it returns the entire pillar dictionary, but from the in-memory pillar data instead of compiling fresh pillar data.

  * - :code:`pillar.get`
    - Described in detail below.

The ``pillar.get`` function works much in the same way as the ``get`` method in a Python dictionary, with the addional feature that nested dictionaries can be traversed using a colon as a delimiter.

If a structure like this is in pillar:

.. code-block:: yaml

    foo:
      bar:
        baz: qux

Extracting it from the raw pillar in an SLS formula or file template is done this way:

.. code-block:: sls

    {{ pillar['foo']['bar']['baz'] }}


Now, with the new ``pillar.get`` function the data can be safely gathered and a default can be set, allowing the template to fall back if the value is not available. This makes handling nested structures much easier.

.. code-block:: sls

    {{ salt['pillar.get']('foo:bar:baz', 'fallback value') }}

.. note::

   On ``pillar.get()`` vs ``salt['pillar.get']()``:

   Note that within templating, the pillar variable is just a dictionary. This means that calling ``pillar.get()`` inside of a template will just use the default dictionary ``.get()`` function which does not include the extra colon delimiter functionality. It must be called using the above syntax ``(salt['pillar.get']('foo:bar:baz', 'qux'))`` to get the Salt function, instead of the default dictionary behavior.


Configuration settings
======================
The configuration for the ``pillar_roots`` in the master configuration is identical in behavior and function as the ``file_roots`` configuration:

.. code-block:: yaml
   :caption: /etc/salt/master.d/pillar.conf

    pillar_roots:
      base:
        - /srv/pillar

This example configuration declares that the base environment will be located in the ``/srv/pillar`` directory.

A few things to note about the pillar environment:

*  The Salt Master server maintains a ``pillar_roots`` setup that matches the structure of the ``file_roots`` used in the Salt file server.
*  Similar to the Salt file server, the ``pillar_roots`` option in the master configuration is based on environments mapping to directories.
*  The pillar data is then mapped to minions based on matchers in a top file which is laid out in the same way as the state top file.
*  Salt pillars can use the same matcher types as the standard top file, except matching on pillar.


In-memory vs. on-demand data
============================
Since compiling pillar data is computationally expensive, the minion will maintain a copy of the pillar data in memory. This avoids needing to ask the master to recompile and send the minion a copy of the pillar data each time it is requested. This in-memory pillar data is what is returned by the ``pillar.item``, ``pillar.get``, and ``pillar.raw`` functions.

Also, for those writing custom execution modules, or contributing to Salt's existing execution modules, the in-memory pillar data is available as the ``__pillar__`` dunder dictionary.

The in-memory pillar data is generated on minion start, and can be refreshed using the ``saltutil.refresh_pillar`` function:

.. code-block:: shell

    salt \* saltutil.refresh_pillar

This function triggers the minion to asynchronously refresh the in-memory pillar data and will always return ``None``.

In contrast to in-memory pillar data, certain actions trigger pillar data to be compiled to ensure that the most up-to-date pillar data is available. These actions include:

*  Running states
*  Running ``pillar.items``

Performing these actions will not refresh the in-memory pillar data. So, if pillar data is modified, and then states are run, the states will see the updated pillar data. However, ``pillar.item``, ``pillar.get``, and ``pillar.raw`` will not see this data unless refreshed using ``saltutil.refresh_pillar``.


External pillar
===============
Salt provides a mechanism for generating pillar data by calling external services for compatible data.

Salt will load any external pillar modules in the specified ``extension_modules`` directory as well as the modules installed with Salt by default.

With the directory set and code loaded for external pillar, the final step for implementation is to configure the master.

Set ``ext_pillar` in ``/etc/salt/master.d/ext_pillar.conf``:

.. code-block:: yaml

    ext_pillar:
      - example_a: some argument
      - example_b:
        - argumentA
        - argumentB
      - example_c:
          keyA: valueA
          keyB: valueB


Pillar namespace
================
The separate pillar SLS files all merge down into a single dictionary of ``key:value`` pairs. Pillar files are applied in the order they are listed in the top file, so when there are conflicting keys, earlier ones will be overwritten. In the previous scenario, conflicting key values in services will overwrite those in packages because the service values are at the bottom of the list.

.. code-block:: yaml
   :caption: /srv/salt/pillar/top.sls

    base:
      '*':
        - packages
        - services

.. code-block:: yaml
   :caption: /srv/salt/pillar/packages.sls

    bind: bind9

.. code-block:: yaml
   :caption: /srv/salt/pillar/services.sls

    bind: named

In this scenario, a request for the bind pillar key will only return ``named`` The ``bind9`` value will be lost, because ``services.sls`` was evaluated later.

When working with extensive pillar data, structuring your pillar files with more hierarchy can avoid namespace collisions and more effectively map variables to jinja variables in the states. For example, you can rework a pillar file to nest any ``key:value`` to be unique:

.. code-block:: yaml
   :caption: /srv/salt/pillar/packages.sls

    packages:
      bind: bind9

This now makes ``packages:bind`` key unique since it is nested, and won’t conflict with the ``services:bind`` key.


Pillar data merge
=================
If the same pillar key is defined in multiple pillar SLS files, and the keys in both files refer to nested dictionaries, then the content from these dictionaries will be recursively merged.

To demonstrating this, take the ``top.sls`` pillar structure and change the ``packages.sls`` and ``services.sls`` dictionary structure to have no nested ``key:value`` conflicts:

.. code-block:: yaml
   :caption: /srv/salt/pillar/top.sls

    base:
      '*':
        - packages
        - services

.. code-block:: yaml
   :caption: /srv/salt/pillar/packages.sls

    bind:
      package-name: bind9
      version: 9.9.5

.. code-block:: yaml
   :caption: /srv/salt/pillar/services.sls

    bind:
      port: 53
      listen-on: any

The resulting pillar dictionary from the ``services.sls`` and ``packages.sls`` pillar union will be:

.. code-block:: shell

   salt-call pillar.get bind


.. code-block:: text

   local:
    ----------
    listen-on:
        any
    package-name:
        bind9
    port:
        53
    version:
        9.9.5

Since both pillar SLS files contained a ``bind`` key which contained a nested dictionary, the pillar dictionary's ``bind`` key contains the combined contents of both SLS files' ``bind`` keys.

Include pillar
==============
Pillar SLS files may include other pillar files, similarly to state files. There are two syntax types to choose from: *simple* and *full*.

A *simple* ``include`` adds the additional pillar as if it were part of the same file:

.. code-block:: yaml

   include:
     - users

A *full* ``include`` allows two additional options:

*  Passing default values to the templating engine for the included pillar file.
*  Adding an optional key under which to nest the results of the included pillar.

.. code-block:: yaml

   include:
     - users:
         defaults:
           sudo: ['bob', 'paul']
         key: users

With this form, ``users.sls`` will be nested within the ``users`` key of the compiled pillar. Additionally, the ``sudo`` value will be available as a template variable to ``users.sls``.


Pillar cache
=============
If there is an unacceptable delay in job publishing because of pillar render time, we can enable master side caching for pillar.

This option reduces job time, but will introduce disadvantages that need to be considered.

Master caching
--------------
If the pillar rendering time is too slow, we can set ``pillar_cache: True``. This creates a cache, either in memory or on the disk, to pull pillar data from, removing time for pillar render for each minion on every request:

.. code-block:: yaml
   :caption: /etc/salt/master.d/pillar.conf

   pillar_cache: True

Cache expiring
--------------
The cache TTL controls the amount of time, in seconds, before the cache expires and pillar is recompiled in to a new cache:

.. code-block:: yaml
   :caption: /etc/salt/master.d/pillar.conf

   pillar_cache_ttl: 3600

Memory or disk
--------------
When electing to use the cache, you can either set for disk or RAM memory storage:

.. code-block:: yaml
   :caption: /etc/salt/master.d/pillar.conf

    # Value can be "disk" or "memory"
    # This example uses "disk"
    pillar_cache_backend: disk

``disk``:

*  The default storage backend.
*  Rendered pillars are serialized and deserialized as msgpack structures for speed.

.. warning::

    This may represent a substantial security risk. Pillars are stored UNENCRYPTED. Ensure that the master cache has permissions set appropriately (sane defaults are provided).

``memory``:

*  Uses an in-memory Python data structure for maximal performance.
*  Each master worker contains its own in-memory cache
*  No guarantee of cache consistency between minion requests.
*  This works best in situations where the pillar rarely if ever changes.

.. warning::

    This may represent a substantial security risk. These unencrypted pillars will be accessible to any process which can examine the memory of the ``salt-master``.


Pillar environment
==================
When multiple pillar environments are used, the default behavior is for the pillar data from all environments to be merged together. The pillar dictionary will therefore contain keys from all configured environments.

The ``pillarenv`` minion config option can be used to force the minion to only consider pillar configuration from a single environment. This can be useful in cases where one needs to run states with alternate pillar data, either in a testing or QA environment, or to test changes to the pillar data before pushing them live.

For example, assume that the following is set in the minion config file:

.. code-block:: yaml

    pillarenv: base

This would cause that minion to ignore all other pillar environments besides ``base`` when compiling the in-memory pillar data. Then, when running states, the ``pillarenv`` CLI argument can be used to override the minion's ``pillarenv`` config value:

.. code-block:: shell

    salt \* state.apply mystates pillarenv=testing

The above command will run the states with pillar data sourced exclusively from the ``testing`` environment, without modifying the in-memory pillar data.

.. note::

    When running states, the ``pillarenv`` CLI option does not require a ``pillarenv`` option to be set in the minion config file. When ``pillarenv`` is left unset, as mentioned above, all configured environments will be combined. Running states with ``pillarenv=testing`` in this case would still restrict the states' pillar data to just that of the testing pillar environment.

It is possible to pin the pillarenv to the effective saltenv, using the ``pillarenv_from_saltenv`` minion config option. When this is set to ``True``, if a specific saltenv is specified when running states, the ``pillarenv`` will be the same. This essentially makes the following two commands equivalent:

.. code-block:: shell

   salt \* state.apply mystates saltenv=dev

.. code-block:: shell

    salt \* state.apply mystates saltenv=dev pillarenv=dev

However, if a ``pillarenv`` is specified, it will override this behavior. So, the following command will use the ``qa`` pillar environment but source the SLS files from the ``dev`` saltenv:

.. code-block:: shell

    salt \* state.apply mystates saltenv=dev pillarenv=qa

So, if a ``pillarenv`` is set in the minion config file, ``pillarenv_from_saltenv`` will be ignored, and passing a ``pillarenv`` on the CLI will temporarily override ``pillarenv_from_saltenv``.


Jinja in pillar
===============
A simple example is to set up a mapping of package names in pillar for separate Linux distributions:

.. code-block:: sls
   :caption: /srv/pillar/pkg/init.sls

    pkgs:
      {% if grains['os_family'] == 'RedHat' %}
      apache: httpd
      vim: vim-enhanced
      {% elif grains['os_family'] == 'Debian' %}
      apache: apache2
      vim: vim
      {% elif grains['os'] == 'Arch' %}
      apache: apache
      vim: vim
      {% endif %}


States with pillar
==================
Consequently this data can be used from within modules, renderers, and State SLS files via the shared pillar dictionary:

.. code-block:: sls

    apache:
      pkg.installed:
        - name: {{ pillar['apache'] }}

.. code-block:: sls

    git:
      pkg.installed:
        - name: {{ pillar['git'] }}

Finally, the above states can use the values provided to them via pillar. All pillar values targeted to a minion are available via the ``pillar`` dictionary. As seen in the above example, Jinja substitutions can then be utilized to access the keys and values in the pillar dictionary.

Note that you cannot just list key/value-information in ``top.sls``. Instead, target a minion to a pillar file and then list the keys and values in the pillar:

.. code-block:: sls
   :caption: /srv/pillar/top.sls

    base:
      '*':
        - updates
      'load-balancer-minion':
        - ibm-cloud-keys

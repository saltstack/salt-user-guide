.. _states:

===========
Salt states
===========

Overview of Salt states
=======================

Salt states are used to deploy and manage infrastructure with easy to read and write yaml files. Using states allows automation of recursive and predictable tasks that can be queued into a job for salt to implement without user input.

These states can be as simplified or complex as needed with:

* Multi-language renderers
* Requisite derivative state options
* Multiple data types for variable manipulation

State structure compared to terminal
====================================

Every state created should be translatable into terminal commands with salt execution modules. These states are then grouped together in salt state files. These state files should be viewed as a series of terminal configuration commands batched together to achieve an infrastructure’s intended state.

Technically you can have the execution modules terminal commands bash scripted to achieve the same task. However there are several drawbacks. For example, to install a system as a working DNS server, you may run the following in a shell script:

.. code-block:: bash

    #!/bin/bash

    # Install latest dns package
    salt \* pkg.latest bind

    # Lay down a new configuration file
    salt \* cp.get_file salt://dns/files/dns.conf /etc/named.conf

    # Start dns service
    salt \* service.start named

What is missing here is conditional statements.

* What if the package is already installed or needs to be upgraded?
* What if the service is already started? Does it need to be restarted?
* How about setting permissions and ownership on the file in addition to copying it from the Salt Master to the target location? Would that require additional calls - restart a service?

Most logic to match this kind of forethought is already in state modules.

State language variations
=========================

YAML is a fast to type, human readable language used by default for creating salt states, with jinja2 as a templating language to remove redundancy in states and state files.

However, there are scenarios for using other languages and templating languages. For example:

* **Python** states sometimes allow complicated logic to be stateful that otherwise cant be created in YAML.
* **JSON** states are faster for computers to translate in comparison to YAML, but are less human readable.

.. Admonition:: Reference

    https://docs.saltstack.com/en/latest/ref/renderers/all/index.html#all-salt-renderers

Salt State files are rendered on the ``salt-minion`` in a decentralized computational model. This removes bottleneck possibilities from rendering and module execution on the ``salt-master``.

.. image:: ../_static/img/states.png
   :align: right
   :alt: Illustration of a state file on a master which stores them. Minions communicate with the master such that the master sends state to the minions which the minions - or state system - process and return the results to the master.

State modules
=============

When creating individual states a ``module.function`` is specified from the state modules. These state modules call their execution module counterparts and add or restrict options from the execution module for stateful operations.

If this separation between state module and execution module is not well understood, frustration is inevitable. For example, state modules don’t have “status check” options for us to see logs and such. Instead, you call for action that Salt uses to determine the status and act accordingly.

So if I wanted to check and install the ``tree`` package in the terminal...

.. code-block:: bash

    $ tree

.. code-block::

    # tree command output

    Command 'tree' not found, but can be installed with:
    sudo apt install tree

.. code-block:: bash

    $ sudo apt install tree

.. code-block::

    # sudo apt install tree command output

    Reading package lists... Done
    Building dependency tree
    Reading state information... Done
    The following NEW packages will be installed:
      tree
    [installed successfully]...

However, doing the same with a salt state requires no check state, since the install state is implicitly checking for the package from the system's package manager.

.. code-block:: sls
    :caption: /srv/salt/tree.sls

    install_tree_now:
      pkg.installed:
        - pkgs:
        - tree

.. code-block:: bash

    $ salt rebel_01 state.sls tree

.. code-block:: yaml

    # salt rebel_01 state.sls tree command output

    rebel_01:
    ----------
              ID: install_tree_now
        Function: pkg.installed
          Result: True
         Comment: The following packages were installed/updated: tree
         Started: 18:44:21.733166
        Duration: 7498.878 ms
         Changes:
                  ----------
                  tree:
                      ----------
                      new:
                          1.7.0-5
                      old:

    Summary for rebel_01
    ------------
    Succeeded: 1 (changed=1)
    Failed:    0
    ------------
    Total states run:     1
    Total run time:   7.499 s

The State SLS data structure
____________________________

A state definition in a state file will have the following components:

* **Identifier** The identifier declaration for the state section.
* **State** Module The name of the State module to find the function in, such as pkg

  * **Function** The function to call in the named module, such as installed

* **Name** The name of the state call, this is usually the name of the file to be managed or the name of the package to be installed
* **Arguments** The state function will accept a number of arguments.
* **Requisites/Declarations** These will be discussed in a later chapter

Here is a generic single state layout in yaml using the names of the high data components:

.. code-block:: sls
    :caption: /srv/salt/example.sls

    identifier:
      module.function:
        - name: name_value
        - function_arg: arg_value
        - function_arg: arg_value
        - function_arg: arg_value

Layers of data abstraction
__________________________

Another important quality of life salt feature is a lot of the package differences between operating systems (OS) have been abstracted away and normalized.

An easy example is whether an OS uses yum or apt, salt will use the correct package manager automatically when evaluating the states. Therefore, this removes code developers would have to write, and making it easier to write code compatible with a diverse infrastructure.

Organizing states
=================

An engineer that writes salt states for a state tree should write them in such a way that another engineer can quickly ascertain the salt state’s purpose and see the workflow of the entire state tree.

The states (and overall the state tree) should generally be shallow in complexity if possible. Reflecting the infrastructure deployment in the simplest states of incremental change towards the desired infrastructure. Often, overly “clever” code in salt states, and in code development in general, will lead to problems and confusion down the line as a project/code matures.

.. code-block::

    /srv/salt
    ├── core.sls
    ├── httpd
    │ ├── files
    │ │ ├── apache2.conf
    │ │ └── httpd.conf
    │ └── init.sls
    ├── dns
    │ ├── files
    │ │ ├── bind.conf
    │ │ └── named.conf
    │ └── init.sls
    ├── ntp
    │ ├── files
    │ │ └── ntp.conf
    │ ├── init.sls
    │ ├── ntp-client.sls
    │ └── ntp-server.sls
    ├── redis
    │ ├── files
    │ │ └── redis.conf
    │ ├── init.sls
    │ └── map.jinja
    ├── ssh
    │ ├── files
    │ │ ├── ssh_config
    │ │ └── sshd_config
    │ ├── init.sls
    │ └── map.jinja
    └── top.sls

This example state tree may look confusing because of multiple features being utilised. However, the important takeaway from this tree is noticing it is moderately developed and feature extensive, but the directory children only go three deep for this state tree. So you can still have a sophisticated state tree for infrastructure management without nesting files to a point of navigational difficulty.

The Salt state tree "file roots"
________________________________

On the ``salt-master`` you can configure the ``file_roots`` option for where the state tree starts. By default this is ``/srv/salt`` directory. The state tree directory is where all state files are found, along with any files related to the salt states such as application configuration files.

The top file
____________

It is not practical to run each state individually targeting the applicable minion(s) each time. Some environments have hundreds of state files targeting thousands of minions. Salt offers two features to help with this scaling problem.

* ``top.sls`` file, to map salt states to the authorized minion(s)
* ``highstate`` execution, to run all salt states outlined in ``top.sls`` in a single salt job.

The top file creates a few general abstractions.

* Maps what nodes should pull from which environments.
* Defines which states should be run from those environments.

The contents of the files and the way they are laid out is intended to be as simple as possible while allowing for maximum flexibility:

.. code-block:: sls
    :caption: /srv/salt/top.sls

    base:
    '*':
      - core
    '^(app|web).(qa|prod).loc$':
      - match: pcre
      - httpd
      - nagios.web
    'os:Ubuntu':
      - match: grain
      - repos.ubuntu
    'os_family:RedHat':
      - match: grain
      - repos.epel
    'nagios* or G@role:monitoring':
      - match: compound
      - nagios.server

* ``base`` is the default environment to use as the ``file_roots``
* Targeting parameter is defined next

  * If a match type is anything other than minion ID globbing, then a **match** type must be defined

* One or more state files are added as list items under the target

Top file targeting types
________________________

Targeting in the top file can use the same matching types as the salt command-line by declaring the match option.

The default match type is a compound matcher. A single glob, when passed through the compound matcher, acts the same way as matching by glob, so in most cases the two are indistinguishable.

.. list-table::
    :widths: 40 25 150
    :header-rows: 1

    * - Type
      - ??
      - Description

    * - glob
      - n/a
      - A glob match on minion ID

    * - pcre
      - E
      - A minion ID match using PCRE

    * - grain
      - ?
      - A match on grain data

    * - grain_pcre
      - P
      - A grain match using PCRE

    * - list
      - ?
      - A list of minion ID's (must be complete minion ID's)

    * - pillar
      - I
      - A match on pillar data

    * - pillar_pcre
      - ?
      - A pillar match using PCRE

    * - compound
      - n/a
      - A compound match of multiple match types

    * - ipcidr
      - ?
      - A match for expression in CIDR notation

    * - nodegroup
      - N
      - A match for pre-defined compound expressions

Running highstate using top files
_________________________________

When managing from the master it is wise to manually run the command when the state tree is updated, or to execute from the master with a  cron job.

Simply use the salt command to execute the state.highstate function:

.. code-block:: bash

    $ salt \* state.highstate

The entire highstate high data can be viewed by running:

.. code-block:: bash

    $ salt \* state.show_highstate

The output is similar to using ``state.show_sls`` for individual states.

Batching large jobs
___________________

While salt can easily handle thousands of simultaneous state runs it may be desirable to have the master throttle the output in batches. With a large salt cluster it can be beneficial to run salt states in batches.

This will run salt in such a way that only 10% of all the minions will be running ``state.highstate`` at once and work through all of the minions.

.. code-block:: bash

    $ salt \* state.highstate --batch 10%

This will run salt in such a way that only 10 minions will be running ``state.highstate`` at once and work through all of the minions.

.. code-block:: bash

    $ salt \* state.highstate --batch 10

.. Note::

    If the minion population being targeted is larger than the percentage or count being batched, the currently targeted minions will constitute a sliding window the batched amount.


Managing multiple environments
==============================

Multiple state trees can be created by defining multiple environments.

Multiple environments are declared by:

* Defining multiple environments in the master configuration
* Creating a top file configuration for each environment or a common top file accessible to all environments which contains sections defining each environment
* Minions must be configured to make requests from the Salt master to a single environment or be overridden on the command line.

Multiple environments structure on the Salt master
__________________________________________________

Multiple State Trees are defined by declaring more environments within the Salt Master configuration. Each State Tree may have multiple paths defined. This allows for a different State Tree for Production, Development, and QA.

If multiple environments are needed, separate ``file_roots`` can be created to serve more than just one State Tree:

.. code-block:: sls
    :caption: /etc/salt/master.d/file_roots.conf

    file_roots:
      base:
        - /srv/salt/base
      dev:
        - /srv/salt/dev1
        - /srv/salt/dev2
      qa:
        - /srv/salt/qa1
        - /srv/salt/qa2
      prod:
        - /srv/salt/prod

Multiple environments top file structure
________________________________________

The top file maps states from multiple environments to applicable minions in the salt cluster.
Each state tree environment may have a top.sls file.

* Each state tree environment may have a top.sls file.

  * The ``top.sls`` file must contain a reference to the environment being served

* A ``top.sls`` file may span multiple environments, however, this is not common

A ``top.sls`` file that spans multiple environments and is accessible to each environment might look like:

.. code-block:: sls

    base:
      '*':
        - core
    dev:
      'webserver*dev*':
        - webserver
      'db*dev*':
        - db
    qa:
      'webserver*qa*':
        - webserver
      'db*qa*':
        - db
    prod:
      'webserver*prod*':
        - webserver
      'db*prod*':
        - db

This ``top.sls`` file example would either need to be made available to each environment's ``file_roots`` as defined in the Salt master configuration. This example could also be broken into four separate ``top.sls`` files - one in each environment's ``file_roots``.

Minion environment configuration
________________________________

A minion can be configured to only pull states from a specific environment using the following Salt minion configuration:

.. code-block:: sls
    :caption: /etc/salt/minion.d/environment.conf

    environment: prod

With this setting, the Salt minion would be limited to only viewing the ``file_roots`` path defined by the Salt master for the ``prod`` environment.

Multiple environment example
____________________________

This example shows how all state tree components collectively generate a highstate.


The steps include:

#. Defining the ``file_roots``
    #. Use a ``base`` environment as the default - not used in this scenario
    #. Create a ``prod`` environment for production states
    #. Create a ``dev`` environment for further state development
#. Creating the Salt states
    #. Disable USB storage on all systems from prod
    #. Provide an SSH configuration files for both prod and dev
    #. Provide an Apache configuration for dev and prod with a different name
#. Add resources for state runs
#. Create top file

Defining the file_roots
_______________________

The ``file_roots`` configuration:

.. code-block:: sls
    :caption: /etc/salt/master.d/file_roots.conf

    file_roots:
      base: # Not used in this example, but must be defined
        - /srv/salt/base
      dev:  # Not used in this example
        - /srv/salt/dev
      prod:
        - /srv/salt/prod

Create a disable USB storage state
__________________________________

The Disable USB Storage State in the ``base`` environment will look like:

.. code-block:: sls
    :caption: /srv/salt/prod/security/disable-usb.sls

    disable_usb:
      file.managed:
        - name: /etc/modprobe.d/blacklist-usbstorage
        - contents: |
            # Blacklist USB storage
            blacklist usb-storage

Create the SSH state
____________________

The SSH State file will look like:

.. code-block:: sls

    install_openssh:
      pkg.installed:
        - name: openssh

    push_ssh_conf:
      file.managed:
        - name: /etc/ssh/ssh_config
        - source: salt://ssh/ssh_config

    push_sshd_conf:
      file.managed:
        - name: /etc/ssh/sshd_config
        - source: salt://ssh/sshd_config

    start_sshd:
      service.running:
        - name: sshd
        - enable: True

Create the Apache state
_______________________

The Apache State file will look like:

.. code-block:: sls
    :caption: /srv/salt/dev/apache/init.sls

    implement_httpd:
      pkg.installed:
        - name: httpd

    http_conf:
      file.managed:
        - name: /etc/httpd/conf/httpd.conf
        - source: salt://apache/httpd.conf

    start_httpd:
      service.running:
        - name: httpd
        - enable: True

Create a firewalld state
________________________

.. code-block:: sls
    :caption: /srv/salt/dev/firewalld/init.sls

    install_firewalld:
      pkg.installed:
          - name: firewalld

    firewalld_open_web:
      firewalld.present:
          - name: public
          - masquerade: False
          - ports:
              - 80/tcp
              - 443/tcp

Production build-out
____________________

We will make a copy of all states in the Development State Tree ``/srv/salt/dev`` to the Production State Tree in :file:`/srv/salt/prod`.

Also, just to show that we have two environments the ``apache/init.sls`` state is renamed to ``apache-prod/init.sls`` in the Production environment for this example.

Create the default top file
___________________________

The state ``top.sls`` will target all systems for ``ssh`` and only web servers will get the apache state.

It will be copied by to both ``dev`` and ``prod`` State Tree paths.

.. code-block:: sls
    :caption: /etc/salt/master.d/file_roots.conf

    dev:
      '*':
        - ssh
      'G@role:web':
        - match: grain
        - apache
        - firewalld

    prod:
      '*':
        - ssh
        - security.disable-usb
      'G@role:web':
        - match: grain
        - apache-prod
        - firewalld

Test setup
__________

We can see the different state trees using the ``saltenv`` kwarg to override the minion's configured environment.

The following is the ``dev`` environment (all ``web`` minions have a ``role`` grain):

.. code-block:: bash

    $ salt \* cp.list_states saltenv=dev

.. code-block:: sls

    # salt \* cp.list_states saltenv=dev command output

    ns01:
      - ssh
      - top
    web01:
      - apache
      - firewalld
      - ssh
      - top

Here is the ``prod`` environment (all ``web`` minions have a ``role`` grain):

.. code-block:: bash

    $ salt \* cp.list_states saltenv=dev

.. code-block:: sls

    # salt \* cp.list_states saltenv=prod

    ns01:
      - security.disable-usb
      - ssh
      - top
    web01:
      - apache-prod
      - firewalld
      - security.disable-usb
      - ssh
      - top

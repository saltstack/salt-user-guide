.. _requisites:

=================================
State requisites and declarations
=================================

ID vs. name
===========
Technically speaking, the component of the high data that determines the name
argument that is passed to the state function is not called name in the high
data, it is called ``ID``.

The ID is copied into the name argument unless the name argument is explicitly
declared by specifying a ``name`` value (or ``names`` values).
The following example shows the declaration of both an ID and name:

.. code-block:: yaml
   :caption: /srv/salt/dns/init.sls

   push_dns_conf:                  # The ID which identifies the state
     file.managed:
       - name: /etc/named.conf     # The name passed to file.managed function
       - source: salt://dns/files/named.conf

Taking into account that the ID could be copied into the name argument, the
example could also be written to only use ID:

.. code-block:: yaml
   :caption: /srv/salt/dns/init.sls

   /etc/named.conf:
     file.managed:
       - source: salt://dns/files/named.conf

ID must be unique across the entire state tree. If the same ID declaration is
used twice, only the first one matched will be used. All subsequent ID
declarations with the same name will be ignored.

.. note::

   Salt `Best Practices
   <https://docs.saltproject.io/en/latest/topics/best_practices.html>`_
   recommend always using a unique, descriptive value for the state ID

One ID to many names
--------------------
The ``names`` argument allows for one ID to become many names.


.. code-block:: yaml
   :caption: /srv/salt/py3.sls

   python-pkgs:
     pkg.installed:
       - names:
         - python
         - pypy
         - python-mako

Another example using directories:

.. code-block:: yaml
   :caption: /srv/salt/deploy_code.sls

   deploy_dirs:
     file.directory:
       - makedirs: True
       - names:
         - /opt/code/docs
         - /opt/code/config
         - /opt/code/images

State execution order
=====================
The following sections of this chapter outline declarations that will set the
order of execution as high data is processed and compiled into low data.

Tools exist in Salt to modify state ordering. These tools consist of requisite
declarations and order options. When Salt States are executed, they are first
ordered in a list (called low data), and then the list is iterated over.

*  This differs from other configuration management tools which execute
   everything within an event loop or execute raw code.
*  The approach of setting up a finite list of executions means that the code
   can be defined in a truly declarative way, and still execute in a completely
   predictable manner.

Implicit ordering
-----------------
States will always execute in the order that they are defined in your SLS
files.

.. code-block:: yaml

    dns_install:
      pkg.installed:
        - name: bind

    dns_service:
      service.running:
        - name: named
        - enable: True

    dns_conf:
      file.managed:
        - name: /etc/named.conf
        - source: salt://dns/files/named.conf

What would be the outcome of executing this state based on implicit ordering?

The order declaration
---------------------
The ``order`` option is used by adding an order number to a state:

.. code-block:: yaml

   install_app:
     pkg.installed:
       - name: app

   prestage_application_data:
     file.recurse:
       - name: /app/production
       - source: salt://app/source
       - order: 1

By setting the ``order`` option to 1 this ensures that the ``/app/production``
directory will be populated before any other states that are executed.

Any state declared without an ``order`` option will be executed after all
states with the ``order`` option are executed in the order they are present
in the State File. This construct can only handle ordering states from the
beginning. Sometimes you may want to send a state to the end of the execution -
to do this, set ``order: last``

.. code-block:: yaml

    update_status:
      module.function:
       - name: http.query
       - args:
         - 'https://example.org/update-status'
       - kwargs:
         - method: POST
       - params: 'keyA=valA&keyB=valB'
       - order: last

    install_app:
      pkg.installed:
        - name: app

    prestage_application_data:
      file.recurse:
        - name: /app/production
        - source: salt://app/source
        - order: 1

Before using the ``order`` option, remember that the majority of state ordering
should be done using other Requisite Declarations. A requisite declaration
will override an ``order`` option so a state with an ``order`` option defined
should not require or be required by other states.

Requisite declarations
======================
Often when setting up states any single action will require or depend on
another action. Salt allows you to build relationships between states with
requisite declarations.

A requisite declaration ensures that the named state is evaluated before the
state requiring it. Failures can also be accounted for when completing the
states defined in the SLS file.

Referencing state declarations
------------------------------
Requisites can match either the ID declaration or the name parameter.
A requisite references another part of a state file (SLS) in the form of:
``state_module: [id | name]``

For example, consider the previous example:

.. code-block:: yaml

   dns_install:
     pkg.installed:
       - name: bind

   dns_service:
     service.running:
       - name: named
       - enable: True

   dns_conf:
     file.managed:
       - name: /etc/named.conf
       - source: salt://dns/files/named.conf

A reference to the package installation would be:
``pkg: dns_install`` (by ID) or ``pkg: bind`` (by name)

A reference to the service running would be:
``service: dns_service`` (by ID) or ``service: named`` (by name)

It is recommended as a Salt best practice to **always** refer to the state ID
when adding requisites.

State failure behavior
----------------------
The default behavior when a state fails is to continue to execute the
remainder of the defined states. This is called a soft fail, meaning that
execution of the state continues after a failure.

The situation may exist where you would want all state execution to stop if a
single state execution fails. This can be done in states with requisite
definitions. The capability to do this is called failing hard. A hard failure
can be implemented in two ways:

*  Defined in a state declaration
*  Defined globally in the minion configuration

The ``failhard`` option defined within a state declaration:

.. code-block:: yaml

   dns_install:
     pkg.installed:
       - name: bind
       - failhard: True

If the state fails to install the package, then no other states will be
executed. Globally, this can be set in the minion configuration:

.. code-block:: yaml
   :caption: /etc/salt/minion.d/failhard.conf

   failhard: True

Standard requisites
-------------------
A requisite statement ensures that the named state is evaluated before the
state requiring it. There are several direct requisite statements that can be
used in Salt that inherently implement failing hard behavior:

*  ``require``
*  ``watch``
*  ``onfail``
*  ``onchanges``
*  ``use``
*  ``prereq``

The two most common types of requisites in Salt are ``require`` and ``watch``

The require requisite
---------------------
The requisite system works by finding the states that are required, and
executing them before the state that requires them. Then the required states
can be evaluated to see if they have executed correctly.

The foundation of the requisite system is the require requisite declaration.

*  The require requisite ensures that the required states are executed before
   the state declaring the require
*  The state declaring the require will only be executed if the required state
   returns True

.. code-block:: yaml

   dns_install:
     pkg.installed:
       - name: bind

   dns_service:
     service.running:
       - name: named
       - enable: True

   dns_conf:
     file.managed:
       - name: /etc/named.conf
       - source: salt://dns/files/named.conf
       - require:
         - pkg: dns_install

In the previous example, we use a ``require`` to make sure the ``bind`` package is
successfully installed before attempting to copy the configuration file to the
minion. We'll deal with the service when we describe the ``watch`` requisite.

Circular references
-------------------
Salt will detect circular references and not allow them. If a circular
reference is detected Salt will return an error such as:

.. code-block:: shell

   Data failed to compile:
   ----------
   A recursive requisite was found, SLS "named" ID "dns_install" ID "dns_conf"

In this example, ``dns_install`` required ``dns_conf`` and ``dns_conf``
required ``dns_install``, thus creating a circular reference. Salt must be able
to evaluate which state to test first to decide order and if execution is
needed based on the requirements.

The watch requisite
-------------------
The ``watch`` requisite is more advanced than the ``require`` requisite. The
``watch`` requisite executes the same logic as ``require``:

*  If a state is being watched, it does not need to also be required. This
   logic is built into ``watch`` to evaluate the watched states as True
*  The ``watch`` requisite also checks if the watched states have returned
   any changes

If the watched states returned changes, and the watched states execute
successfully, then the state declaring the ``watch`` will execute a function
that reacts to the changes in the watched states:

.. code-block:: yaml
   :caption: /srv/salt/dns/init.sls

   dns_install:
     pkg.installed:
       - name: bind

   dns_service:
     service.running:
       - name: named
       - enable: True
       - watch:
         - file: dns_conf

   dns_conf:
     file.managed:
       - name: /etc/named.conf
       - source: salt://dns/files/named.conf
       - require:
         - pkg: dns_install

Running the previous state file execution will produce the following output if
the ``/etc/named.conf`` is updated:

.. code-block:: shell

   rebel_01:
   ----------
             ID: /etc/named.conf
       Function: file.managed
         Result: True
        Comment: File /etc/named.conf updated
        Started: 22:40:34.126006
       Duration: 34.006 ms
        Changes:
                  ----------
                 diff:
                      ---
                     +++
                     @@ -10,38 +10,37 @@
                      -     listen-on port 53 { 127.0.0.1; };
                     +     listen-on port 53 { 0.0.0.0; };
                     +zone "my.domain" IN {
                     +       type master;
                     +       file "master/master.my.domain";
                     +       // enable slaves only
                     +       allow-transfer {192.0.2.1;192.0.2.2;);
                     +};
   ----------
             ID: start_dns
       Function: service.running
           Name: named
         Result: True
        Comment: Started Service named
        Started: 23:10:36.318223
       Duration: 400.123 ms
        Changes:
                  ----------
                 named:
                     True
   Summary for rebel_01
   ------------
   Succeeded: 1 (changed=1)
   Failed:    0
   ------------
   Total states run:     1
   Total run time:  34.006 ms

In this example the named service will be started (or restarted) since the
file ``/etc/named.conf`` is changed (new or updated). The ``watch`` requisite
is based on the ``mod_watch`` function. Salt Python state modules can include a
function called ``mod_watch`` which is then called if the ``watch`` call is
invoked.

*  In the case of the service state the underlying service is restarted.
*  In the case of the cmd state the command is executed.

The ``watch`` requisite only works if the state that is watching has a
``mod_watch`` function written. If the watching state where the ``watch`` is
set does not have a ``mod_watch`` function (like pkg), then the listed states
will behave only as if they were under a ``require`` statement.

Multiple requisites
-------------------
The requisite declaration is passed as a list, allowing for the easy addition
of multiple requisites. Multiple requisite types can also be separately
declared:

.. code-block:: yaml

   dns_install:
     pkg.installed:
       - name: bind

   create_user:
     user.present:
       - name: bind
       - require:
       - pkg: dns_install

   create_group:
    group.present:
      - name: bind
      - require:
      - pkg: dns_install

   dns_service:
     service.running:
       - name: named
       - enable: True
       - require:
         - pkg: dns_install     # Technically not needed since "watch" is on dns_conf
         - user: create_user    # dns_conf has a "require" defined for dns_install
         - group: create_group  # Cascading require as "watch" is also a require
       - watch:
         - file: dns_conf

   dns_conf:
     file.managed:
       - name: /etc/named.conf
       - source: salt://dns/files/named.conf
       - require:
         - pkg: dns_install

It is important to understand the flow of the state file execution.

The onfail declaration
----------------------
The ``onfail`` requisite allows for reactions to happen strictly as a response
to the failure of another state.

This can be used in a number of ways, such as executing a second attempt to
set up a service or begin to execute a separate thread of states because of a
failure. The ``onfail`` requisite is applied in the same way as require as watch:

.. code-block:: yaml

   httpd_service:
     service.running:
       - name: httpd

   report_failure:
     module.run:
       - name: slack_notify.call_hook
       - kwargs:
           message: Apache failed to start
       - onfail:
         - service: httpd_service

The onchanges declaration
-------------------------
The ``onchanges`` requisite makes a state only apply if the required states
generate changes, and if the watched state's result is ``True``.

Unlike ``watch``, the ``onchange`` requisite does not execute if there are no
detected changes, where a ``watch`` does. For example, in a ``watch``:

.. code-block:: yaml

   dns_service:
     service.running:
       - name: named
       - enable: True
       - watch:
         - file: dns_conf

   dns_conf:
     file.managed:
       - name: /etc/named.conf
       - source: salt://dns/files/named.conf

In the case of using a ``watch``, even if there are no changes in the
``watch`` file, the Salt state system will execute this function to put the
service in a running state, or at least check to see if it is running.

When using the ``onchanges`` the behavior changes:

.. code-block:: yaml

   dns_service:
     service.running:
       - name: named
       - enable: True
       - onchanges:
         - file: dns_conf

   dns_conf:
     file.managed:
       - name: /etc/named.conf
       - source: salt://dns/files/named.conf

If an ``onchanges`` is declared instead of a ``watch``, and if there are no
changes, the service is not set to run if currently stopped. The logic is that
the service will not be started if it is currently not running and there are
no changes to the file.

This can be a useful way to execute a post hook after changing aspects of a
system. An example of using an ``onchanges`` is if you only want salt-cloud
updated if there is a new bootstrap script available:

.. code-block:: yaml

   deploy_bootstrap:
     file.managed:
       - name: /etc/salt/cloud.deploy.d/bootstrap-salt.sh
       - source: salt://conf/boostrap-salt.sh

   install_salt_cloud:
     pkg.latest:
       - name: salt-cloud
       - onchanges:
         - file: deploy_bootstrap

The use requisite
-----------------
The ``use`` requisite declarations allow for the transparent duplication of
data between states.

When a state "uses" another state, it copies the other state's arguments as
defaults. A simple example of the ``use`` declaration:

.. code-block:: yaml

   manage_eth0:
     network.managed:
       - name: eth0
       - enabled: True
       - type: eth
       - proto: static
       - ipaddr: 192.0.2.7
       - netmask: 255.255.255.0
       - gateway: 192.0.2.1
       - enable_ipv6: true
       - ipv6proto: static
       - ipv6ipaddrs:
         - 2001:db8:dead:beef::3/64
         - 2001:db8:dead:beef::7/64
       - ipv6gateway: 2001:db8:dead:beef::1
       - ipv6netmask: 64
       - dns:
         - 198.51.100.8
         - 203.0.113.4

   manage_eth1:
     network.managed:
       - name: eth1
       - ipaddr: 203.0.113.120
       - gateway: 203.0.113.1
       - ipv6ipaddr: 2001:db8:dead:c0::3
       - ipv6gateway: 2001:db8:dead:c0::1
       - use:
         - network: manage_eth0

The ``use`` statement was developed primarily for the networking states but
can be used on any states in Salt. This makes sense for the network state
because it can define a long list of options that need to be applied to
multiple network interfaces.

The prereq requisite
--------------------
The ``prereq`` requisite allows for actions to be taken based on the expected
results of a state that has not yet been executed.

The state containing the ``prereq`` requisite is defined as the pre-requiring
state. When a ``prereq`` requisite is evaluated, the pre-required state
reports if it expects to have any changes. It does this by running the
pre-required single state as a test-run by enabling ``test=True``.

The best way to define how ``prereq`` operates is displayed in the following
practical example:

.. code-block:: yaml

   gracefulRestart:
     module.run:
       - name: service.restart
       - m_names:
         - httpd
       - prereq:
         - file: site-code

   siteCode:
     file.recurse:
       - name: /opt/site_code
       - source: salt://site/code

When the ``apache`` service should be shut down because underlying code is going
to change, the service should be off-line while the update occurs. In this
example, ``gracefulRestart`` is the pre-requiring state and ``siteCode`` is the
pre-required state.

Including other SLS files
=========================
The ``include`` declaration is a top level declaration that defines a list of
SLS files to bring into the current SLS file.

An ``include`` can be used to bring in data from another SLS file for many
reasons.

*  If you want to combine many states into one.
*  If the SLS file needs to require or watch components found in another SLS
   file.
*  If components of another SLS file need to be extended, or if a shortcut SLS
   file needs to be made.
*  If another SLS file needs to be read-only in another environment, but
   allowed to be included, used, or extended

This example includes all core states for the infrastructure:

.. code-block:: yaml
   :caption: /srv/salt/core.sls

   include:
     - ssh
     - sudo
     - edit.vim
     - edit.emacs
     - ntp

Included state files are relative to the ``file_roots``.

Including for requisites
------------------------
Require ``kvm`` before starting ``libvirt``. Here is the basic ``kvm`` state file:

.. code-block:: yaml
   :caption: /srv/salt/kvm/init.sls

   install_qemu:
     pkg.installed:
       - name: qemu-kvm

   load_kvm:
     kmod.present:
       - name: kvm_intel

Here is the ``libvirt`` state file including the ``kvm`` state requiring it:

.. code-block:: yaml
   :caption: /srv/salt/libvirt/init.sls

   include:
     - kvm

   install_libvirt:
     - pkg.installed:
       - name: libvirt

   start_libvirt:
     - service.running:
       - name: libvirt
       - require:
         - kmod: load_kvm
         - pkg: install_qemu

Extending external SLS data
===========================
Sometimes a state defined in one SLS file will need to be modified from a
separate SLS file.

A good example of this is when an argument needs to be overwritten or when a
service needs to watch an additional state.

The extend declaration
----------------------
The ``extend`` declaration is a top level declaration like ``include`` and
encapsulates ID declaration data included from other SLS files.


Using the following Salt State file as a starting point:

.. code-block:: yaml
   :caption: /srv/salt/ssh/init.sls

   install_ssh:
     pkg.latest:
       - name: openssh

   ssh_server:
     service.running:
       - name: sshd
       - enable: True
       - watch:
         - pkg: install_ssh
       - file: sshd_conf

   sshd_conf:
     file.managed:
       - name: /etc/ssh/sshd_config
       - source: salt://ssh/files/sshd_config

We can use the ``ssh`` state file as a base, and then build upon it to suit
specific needs:

.. code-block:: yaml
   :caption: /srv/salt/ssh/dmz.sls

   include:
     - ssh

   extend:
     sshd_conf:
       file:
         - name: /etc/ssh/sshd_config
         - source: salt://ssh/files/dmz_sshd_config

     ssh_server:
       service:
         - watch:
           - file: add_banner

   add_banner:
     file.managed:
       - name: /etc/ssh/banner
       - source: salt:/ssh/files/banner

A few critical things happened here. First off, the SLS files that are going
to be extended are included, then the ``extend`` declaration is defined. Under
the ``extend`` declaration, two ids are extended: the ``ssh_conf`` file state
is overwritten with a new name and source, then ``ssh_server`` is extended to
watch the banner file in addition to anything it is already watching.

Extend rules and regulation
---------------------------
The ``extend`` declaration is a **top-level declaration**. This means that
``extend`` can only be called once in an SLS file. If it is declared more
than once, then only the second ``extend`` block will be used.

The following example is **wrong**:

.. code-block:: yaml

   include:
     - http
     - ssh

   extend:
     apache:
       file:
         - name: /etc/httpd/conf/httpd.conf
         - source: salt://http/httpd2.conf

   # Second overwrites first
   extend:
     ssh-server:
       service:
         - watch:
           - file: /etc/ssh/banner

.. note::

   If the second ``extend`` is removed or commented, then the state file will
   work as intended.

Things to remember when extending states:

*  Always include the SLS files being extended with an ``include``
   declaration
*  Requisites ``watch`` and ``require`` are appended to, everything else is
   overwritten
*  ``extend`` is a **top level declaration**. Like the state ID, it cannot be
   declared more than once in a single SLS
*  Many state IDs can be extended using the ``extend`` declaration

The requisite _in declarations
==============================
Each requisite also has a corresponding _in counterpart:

*  ``require_in``
*  ``watch_in``
*  ``prereq_in``
*  ``use_in``
*  ``onchanges_in``
*  ``onfail_in``

The corresponding _in requisites basically allow the logic of rendering to do
the reverse of the declaration.

An example using ``require_in`` and ``watch_in`` could look like this:

.. code-block:: yaml

   install_ssh:
     pkg.latest:
       - name: openssh
       - watch_in:
         - service: ssh_server
       - require_in:
         - file: sshd_conf

   ssh_server:
     service.running:
       - name: sshd
       - enable: True

   sshd_conf:
     file.managed:
       - name: /etc/ssh/sshd_config
       - source: salt://ssh/files/sshd_config
       - watch_in:
         - service: ssh_server

An alternate way to extend a state declaration:

.. code-block:: yaml

   include:
     - ssh

   add_banner:
     file.managed:
       - name: /etc/ssh/banner
       - source: salt:/ssh/files/banner
       - watch_in:
         - service: ssh_server

Here's our networking example with the ``use_in`` declaration taken a bit
further:

.. code-block:: yaml

   manage_eth0:
     network.managed:
       - name: eth0
       - enabled: True
       - type: eth
       - proto: static
       - ipaddr: 192.0.2.7
       - netmask: 255.255.255.0
       - gateway: 192.0.2.1
       - enable_ipv6: true
       - ipv6proto: static
       - ipv6ipaddrs:
         - 2001:db8:dead:beef::3/64
         - 2001:db8:dead:beef::7/64
       - ipv6gateway: 2001:db8:dead:beef::1
       - ipv6netmask: 64
       - dns:
         - 198.51.100.8
         - 203.0.113.4
       - use_in:
         - network: manage_eth1
         - network: manage_eth2

   manage_eth1:
     network.managed:
       - name: eth1
       - ipaddr: 203.0.113.120
       - gateway: 203.0.113.1
       - ipv6ipaddr: 2001:db8:dead:c0::3
       - ipv6gateway: 2001:db8:dead:c0::1

   manage_eth2:
     network.managed:
       - name: eth2
       - ipaddr: 203.0.113.121
       - gateway: 203.0.113.1
       - ipv6ipaddr: 2001:db8:dead:c0::4
       - ipv6gateway: 2001:db8:dead:c0::1

Altering states
===============
The state altering system is used to make sure that states are evaluated
exactly as the user expects. It can be used to double check that a state
performed exactly how it was expected to, or to make 100% sure that a state
only runs under certain conditions.

The use of ``unless`` or ``onlyif`` options help make states even more
stateful.

.. note::

   Under the hood, these altering states declarations call ``cmd.retcode`` with
   ``python_shell=True``. This means the commands referenced by these
   declarations will be parsed by a shell. So be aware of side-effects as this
   shell will be run with the same privileges as the Salt Minion.

The onlyif requisite
--------------------
The ``onlyif`` requisite is used if all of the commands defined return True.
Then the state will be run.

If any of the specified commands return False, the state will not run. This
example creates a new MySQL database user only if the ``projectDB`` database
exists.

.. code-block:: yaml

   create_db_user:
     mysql_user.present:
       - name: jdoe
       - host: localhost
       - password: p@ssw0rd
       - onlyif:
         - mysql -u ro_user -e 'use projectDB'

The unless requisite
--------------------
The ``unless`` requisite specifies that a state should only run when any of the
specified commands return False.

The ``unless`` requisite operates as NAND where it produces a value of True,
if, and only if, at least one of the propositions is False. It is useful in
giving more granular control over when a state should execute. In the example
below, the state will only run if either the ``vim-enhanced`` package is not
installed (returns False) or if ``/usr/bin/vim`` does not exist (returns
False). The state will run if both commands return False.

However, the state will not run if both commands return True.

.. code-block:: yaml

   install_vim:
     pkg.installed:
       - name: vim
       - unless:
         - rpm -q vim-enhanced
         - ls /usr/bin/vim

The ``unless`` requisite checks are resolved for each name to which they are
associated.

The check_cmd requisite
-----------------------
Check Command is used for determining that a state did or did not run as
expected.

* This will attempt to do a replace on all ``enabled=0`` in the .repo file, and
  replace them with ``enabled=1``.

.. code-block:: yaml

   comment-repo:
     file.replace:
       - name: /etc/yum.repos.d/fedora.repo
       - pattern: ^enabled=0
       - repl: enabled=1
       - check_cmd:
         - grep '^enabled=1' /etc/yum.repos.d/fedora.repo
         # or
         - grep '^enabled=0' /etc/yum.repos.d/fedora.repo && return 1 || return 0

The ``check_cmd`` is just a bash command.

*  It will do a grep for ``enabled=0`` in the file, and if it finds any, it
   will return a 0, which will prompt the ``&&`` portion of the command to
   return a 1, causing ``check_cmd`` to set the state as failed.
*  If it returns a 1, meaning it didn't find any ``enabled=0`` it will hit the
   ``||`` portion of the command, returning a 0, and declaring the function
   succeeded.

The listen requisite
--------------------
``listen`` and its counterpart ``listen_in`` trigger ``mod_watch`` functions
for states when those states succeed and result in changes, similar to how
``watch`` and its counterpart ``watch_in``. Unlike ``watch`` and ``watch_in``,
``listen``, and ``listen_in`` will **not** modify the order of states and can
be used to ensure your states are executed in the order they are defined. All
``listen``/``listen_in`` actions will occur at the end of a state run, after
all states have completed.

.. code-block:: yaml
   :caption: /srv/salt/httpd/restart_last.sls

   restart_apache2:
     service.running:
       - name: apache2
       - listen:
         - file: /etc/apache2/apache2.conf

   configure_apache2:
     file.managed:
       - name: /etc/apache2/apache2.conf
       - source: salt://apache2/apache2.conf

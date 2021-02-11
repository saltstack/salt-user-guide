.. _salt-overview:

=======================
Chapter 1 Salt Overview
=======================

Features of Salt
=================
The Salt system is a Python-based open-source remote execution framework for
configuration management, automation, provisioning, and orchestration.

.. image:: ../_static/img/features-of-salt.png
   :align: right
   :alt: Features of Salt

Salt delivers a dynamic communication bus for infrastructure to leverage in:

* Remote execution.
* Configuration management.
* Automation and orchestration.

Salt supports the *Infrastructure as Code* approach to deployment and datacenter
management.

**Remote management**

Running commands on remote systems is the core function of Salt. Salt can execute
multiple commands across thousands of systems in seconds with a single execution.

**Configuration management**

The Salt configuration management system is based on storing all configuration
or "state" data inside an easily understood data structure. The concept behind
the State system is:

* **Simple** - easy to administer and manage.
* **Extensible** - easy to add custom modules, or extend existing states.
* **Deterministic** - executes in the same way every time.
* **Layerable** - provides layers of data abstraction (such as states call execution modules).

**Automation and orchestration**
Executing remote management and configuration on a minion is perfect when you
want to ensure that the minion is configured and running the way you want.
Sometimes, however, you want to configure a set of minions all at once.
For example, if you want to set up a load balancer in front of a cluster of
web servers, you can ensure the load balancer is set up first. You can then
apply the same matching configuration consistently across the whole cluster,
which is known as orchestration.

**Salt management concepts**
-----------------------------

A basic Salt implementation consists of a Salt Master managing one or more Salt Minions.

* A Salt Master is a server running the ```salt-master ``` service that provides
  management to many systems.
* A Salt Minion is any system/device managed by Salt. A Salt Minion can
  run the ```salt-minion``` service or can be agentless using ```salt-ssh```
  or ```salt-proxy```.
* A Salt Proxy process can behave as a salt-minion, which in turn connects
  to an underlying device to execute commands or states.  Salt Proxy
  connections are typically achieved via SSH or RESTful API calls.
* Systems managed via SSH with the ```salt-ssh``` model are also considered
  agentless minions under the managed systems model.
* A newer system in development is ```salt-bin```, which will.

.. image:: ../_static/img/salt-architecture.png
   :align: right
   :alt: Salt architecture


**Salt master**

A server running the ```salt-master``` service is a Salt Master. The Salt Master
provides a cohesive platform for orchestration and automation between managed systems.

**Salt minion**

A system under control of the master is considered a Salt Minion.
However, minions do not require a master to be managed but can run in a stand-alone
mode.

* The ```salt-minion``` service runs as a management agent on a system.
* The ```salt-minion``` service can run pretty much anywhere you can have a
      Python interpreter.

**Salt proxy**

Proxy minions are a feature that enables controlling devices that,
for whatever reason, cannot run a standard salt-minion.  A proxy minion process
is used to establish a connection to an underlying device, using methods native
to that device (SSH, Rest, etc).

**Salt SSH**

The Salt SSH system was added to Salt as an alternative means to communicate
with minions. The Salt SSH system can be used in tandem with or as an alternative
to the standard Salt system. The Salt SSH system does not require that a Salt
Minion be present on the target system. Only SSH needs to be running and port
22 open. We introduce this capability of Salt so you can appreciate the full
capability of Salt but will not be using it in this class.

**SaltStack Config**

SaltStack Congif provides an intuitive user interface to perform complex functions
like configuration management and orchestration. Jobs in SaltStack Config can be
built, stored, and scheduled so you spend less time and fewer resources executing
routine functions. It also allows distributing the work to other skill-level
employees and teams while securing your system and guarding the environment
from the misuse of powerful tools.

SaltStack Config features include:

* A web-based user interface
* Role-based access control
* Multi-master support
* Central job and event cache
* LDAP, SAML, OIDC, & Active Directory integration
* Security policies with industry-standard compliance profiles, such as CIS and
  DISA STIGS
* Reporting
* An enterprise API (eAPI)

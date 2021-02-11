.. _execution-framework:

========================
Salt execution framework
========================

Types of executions
===================

Salt commands can be executed in different ways:

* Remote execution - using the ``salt`` command from the Salt master
* Master execution - using ``salt-run``
* Local execution - using ``salt-call`` initiated on the Salt minion

.. image:: ../_static/img/salt-execution-types.jpg
   :align: right
   :alt: Illustration

Each command is just a wrapper around an API client interface. The command to run determines where you are executing the command (master or minion) and where you want the command to run (master or minion).

Calling modules locally on a minion
===================================

Salt modules can be called locally on the minion, bypassing the master's initial publish of the command on the event bus using the ``salt-call`` command.

* The salt ``module.functions`` make up a rich API for system management.
* These ``module.functions`` are all available for execution directly on the minion.

Salt-call is an effective tool for both accessing the Salt functions without needing to *initially* run through the master, but to also debug operations on a minion. Some complex operations, like configuration management can be more easily debugged if run locally with ``salt-call``.

Using salt-call
_______________

Using ``salt-call`` is simple. It is used the same way as the ``salt`` command but does not require a target (because it is running the ``module.function`` on the local minion).

To view network interfaces using ``salt-call``:

.. code-block:: bash

    $ salt-call network.interfaces

The documentation is also available using ``salt-call``:

.. code-block:: bash

    $ salt-call sys.doc pkg.install

A ``module.function`` alias exists for viewing documentation using ``salt-call``:

.. code-block:: bash

    $ salt-call -d service

Viewing local grains
____________________

Grains data can be viewed locally on the minion using ``salt-call`` in two different ways:

.. code-block:: bash

    $ salt-call grains.items

Alternatively:

.. code-block:: bash

    $ salt-call -g

You may also view specific grain items the same way:

.. code-block:: bash

    $ salt-call grains.get os_familiy

The Salt command line execution
===============================

Salt executes jobs in the remote execution framework in an asynchronous fashion. However, the command line works in synchronous mode so that output is more easily viewed at the completion of a job.

If a command times out or if your shell gets disconnected, the command still runs because it has been published on port 4505.

When a job takes longer than the default 5 seconds or a specific time, the **LocalClient** will publish another request that goes through the same process to check on the job.

In other words, this is the amount of time before the master will check active jobs on the minions or give up and report a time-out for the missing minion return data. As long as the minion responds to the *check job status* request, the time will reset for another duration.

Command line execution options
______________________________

Salt can execute jobs asynchronously using the ``--async`` command line option:

.. code-block:: bash

    $ salt -G 'os_family:RedHat' pkg.upgrade --async

.. code-block:: bash

    # salt -G 'os_family:RedHat' pkg.upgrade --async command output

    Executed command with job ID: 20190220150112550868

This option will immediately return to the command prompt and print out the assigned **Job ID**.

In addition to running jobs asynchronously, a job may be submitted synchronously (default mode) but still show the assigned **Job ID**:

.. code-block:: bash

    $ salt -G 'os_family:RedHat' pkg.upgrade -v

.. code-block:: bash

    # salt -G 'os_family:RedHat' pkg.upgrade -v command output

    Executed command with job ID: 20190220170719865801
    --------------------------------------------------

This command will operate in the default *synchronous* manner, but the **Job ID** will be printed in the terminal.

All Salt commands (``salt``, ``salt-call``, and ``salt-run``) can be issued with a logging flag in order to see more detailed output in the terminal:

.. code-block:: bash

    $ salt -l debug \*ubuntu status.meminfo

.. code-block::

    # salt -l debug \*ubuntu status.meminfo command output

    [DEBUG   ] Reading configuration from /etc/salt/master
    [DEBUG   ] Including configuration from '/etc/salt/master.d/reactor.conf'
    [DEBUG   ] Reading configuration from /etc/salt/master.d/reactor.conf
    [DEBUG   ] Using cached minion ID from /etc/salt/minion_id: 20190218-sosfubuntu
    [DEBUG   ] Configuration file path: /etc/salt/master
    [DEBUG   ] MasterEvent PUB socket URI: /var/run/salt/master/master_event_pub.ipc
    [DEBUG   ] MasterEvent PULL socket URI: /var/run/salt/master/master_event_pull.ipc
    [DEBUG   ] Initializing new AsyncZeroMQReqChannel for (u'/etc/salt/pki/master', u'20190218-sosf-master_master', u'tcp://127.0.0.1:4506', u'clear')
    [DEBUG   ] Connecting the Minion to the Master URI (for the return server): tcp://127.0.0.1:4506
    [DEBUG   ] Trying to connect to: tcp://127.0.0.1:4506
    [DEBUG   ] Initializing new IPCClient for path:
    /var/run/salt/master/master_event_pub.ipc
    [DEBUG   ] LazyLoaded local_cache.get_load
    [DEBUG   ] Reading minion list from
    /var/cache/salt/master/jobs/3f/9c26a4b94e2bec13fe333149fe26839b0d9168de78ff6378
    76d8108e8b39bb/.minions.p
    [DEBUG   ] get_iter_returns for jid 20190220172435508684 sent to set(['20190218-sosf-ubuntu']) will timeout at 17:24:40.515091
    [DEBUG   ] jid 20190220172435508684 return from 20190218-sosf-master
    [DEBUG   ] return event: {u'20190218-sosf-ubuntu': {u'jid': u'20190220172435508684', u'retcode': 0, ...

Salt job management
===================

Salt job management begins by understanding:

* Job IDs
* Job Cache

Job IDs
_______

Every Salt job is assigned a unique Job ID. The Job ID is used to track the individual executions.

Job IDs are represented as a **jid** and are created on the master for each job and sent down with the command.

The Job IDs are timestamps of when the jobs are started.

A job id looks like this:

.. code-block::

    20190220172435508684

This Job ID is for a job started: Feb 20, 2019, at 17:24:35 and 508684 microseconds:

.. code-block::

    Year: 2019
    Month: 02
    Day: 20
    Hour: 17
    Minute: 24
    Second: 35
    Microsecond: 508684

Job cache
_________

The job cache is the storage system for all executed jobs.

* The job cache is located in the cachedir under the directory named jobs.

.. code-block::

    File: /var/cache/salt/master/jobs

* This directory is cleaned by the master on a regular basis.

The number of hours that old jobs are kept defaults to 24, but it is configured via the ``keep_jobs`` option in the master configuration file.

.. code-block::

    Keep_jobs: 24

It is recommended to store job data in an **external job cache** (discussed in a later chapter) if a requirement to keep this data is more than 5 days. This figure is dependent on several factors including:

* Number of jobs needing to be executed in that time span
* Number of minions being targeted
* Master resources (disk space)

Running jobs on the master and managing jobs
============================================

The ``salt`` command is typed on the master, but Salt sends jobs for remote execution on minions. The ``salt-run`` command sends jobs to Salt to run on the master. Jobs that are to be run on the salt master by ``salt-run`` are called *runners*.

Runners are a specific type of Salt module intended to execute in the environment of the Salt master. Runners will be discussed in greater detail later in the course, but for now, we will discuss job management which employs the Salt Runner module: **jobs**. The **jobs** runner module allows for viewing the Salt master’s job cache.

View running jobs
_________________

Currently running jobs can be viewed via the ``jobs.active`` runner ``module.function``:

.. code-block:: bash

    $ salt-run jobs.active

.. code-block:: bash

    # salt-run jobs.active command output

    20190220150112550868:
    ----------
    Arguments:
    Function:
        pkg.upgrade
    Returned:
    Running:
        |_
        ----------
        20190218-sosf-redhat:
            10733
        |_
        ----------
        20190218-sosf-master:
            24081
    StartTime:
        2019, Feb 20 15:01:12.550868
    Target:
        2019, Feb 20 15:01:12.550868
    Target:
        os_family:RedHat
    Target:
        os_family:RedHat
    Target-type:
        grain
    User:
        root

View previously run jobs
________________________

Jobs that have been executed in the past ``keep_jobs`` window can be easily looked up using the jobs runner. ``jobs.list_jobs`` will list information about all previously executed jobs in the ``keep_jobs`` window:

.. code-block:: bash

    $ salt-run jobs.list_jobs

.. code-block:: bash

    # salt-run jobs.list_jobs command output

    '20190220104253056848':
	Arguments: []
	Function: test.ping
	Start Time: 2019, Feb 20 10:42:53.056848
	Target: '*'
	Target-type: glob
    '20190220104301355086':
	Arguments:
        - [dmesg]
	Function: cmd.run
	Start Time: 2019, Feb 20 10:43:01.355086
	Target: '*ubuntu'
	Target-type: glob

With this data, the details of a specific job can be pulled up using the Job ID:

.. code-block:: bash

    $ salt-run jobs.lookup_jid 20190220104253056848

To see the status of a currently active job, add the **display_progress=True** option:

.. code-block:: bash

    $ salt-run jobs.lookup_jid 20190220150112550868 display_progress=True

.. code-block:: bash

     # salt-run jobs.lookup_jid 20190220150112550868 display_progress=True command output

    event:
    ----------
    message:
        Querying returner: local_cache
    suffix:
        progress
    event:
        ----------
    message:
        20190218sosf-redhat
    ...

Kill and term jobs
__________________

The **saltutil** execution module contains Salt functions to terminate Salt jobs:

``saltutil.term_job`` will send a termination signal to a job (SIGTERM 15)

.. code-block:: bash

    $ salt 201190218-sosf-redhat saltutil.term)job 20190220150112550868

``saltutil.kill_job`` will send a kill signal to a job (SIGKILL 9)

.. code-block:: bash

    $ salt 20190218-sosf-redhat saltutil.kill_job 20190220150112550868

The event system
================

Salt maintains an event system that fires local publications on a local UNIX socket.

* Events are fired for a number of situations on the Master.
* The event system is made available on the minion and master.
* The same system user that the minion or master is running as can fire events using the salt event API.

Types of Salt events
____________________

The Salt master has the following types of events:

* authentication
* start
* key
* job
* presence
* cloud
* run

Event components
________________

The event system sends two pieces of information. The **tag** and the **data** items.

* The **tag** is a "/" separated string representing a simple data structure.
* The **data** will be serialized by Salt into a MessagePack string.

Viewing Salt events
___________________

One of the best ways to see exactly what events are fired and what data is available in each event is to use the ``state.event`` runner:

.. code-block:: bash

    $ salt-run state.event pretty=True

.. code-block:: bash

    # salt-run state.event pretty=True command output

    salt/job/20190220181913504496/new {
    "_stamp": "2019-02-20T18:19:13.506890",
    "arg": [],
    "fun": "test.ping",
    "jid": "20190220181913504496",
    "minions": [
        "20190218-sosf-centos",
        "20190218-sosf-master",
        "20190218-sosf-redhat",
        "20190218-sosf-ubuntu",
        "20190218-sosf-windows"
    ],
    "missing": [],
    "tgt": [
        "*"
    ],
    "tgt_type": "glob",
    "user": "root"
    }
    salt/job/20190220181913504496/ret/20190218-sosf-ubuntu 	{
        "_stamp": "2019-02-20T18:19:08.490451",
        "cmd": "_return",
        "fun": "test.ping",
        "fun_args": [],
        "id": "20190218-sosf-ubuntu"
        "jid": "20190220181913504496",
        "retcode": 0,
        "retcode": 0,
        "return": true,
        "success": true
    }
    ...

Minions firing events to master
_______________________________

The minions can fire off events on the master via the **event** execution module.
An event can be sent to the Salt master by using the **event.send** function:

.. code-block:: bash

    $ salt-call event.send 'mycustom/app/tag' '{"app": "mycustom", "build_num": "3.1", "result": "true"}' with_grains=True

The function ``event.fire_master`` can be used to send events to master as well (without the ability to append grains data):

.. code-block:: bash

    $ salt-call event.fire_master '{"app": "mycustom", "build_num": "3.1", "result": "true"}' 'mycustom/app/tag'

Here is some sample output from ``state.event`` of an event using ``event.send`` and ``with_grains=True`` from the Salt minion:

.. code-block:: Python

    mycustom/app/tag 	{
    "_stamp": "2019-02-20T18:36:00.182479",
    "cmd": "_minion_event",
    "data": {
        "__pub_fun": "event.send",
        "__pub_jid": "20190220113600174263",
        "__pub_pid": 12819,
        "__pub_tgt": "salt-call",
        "app": "mycustom",
        "build_num": "3.1",
        "grains": {
            "SSDs": [
            "nvme0n1"
            ],
        "biosreleasedate": "07/18/2018",
        "biosversion": "1.8.0",
        ...
    "id": "20190218-sosf-centos",
    "tag": "mycustom/app/tag"

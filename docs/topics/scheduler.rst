.. _scheduler:

=========
Scheduler
=========

Scheduling jobs
===============

Salt’s scheduling system allows incremental executions on minions or the master.
The schedule system exposes the execution of any execution function on minions,
or any runner on the master.

Scheduling can be enabled by multiple methods:

* ``schedule`` option in either the master or minion configuration files. These require the master or minion application to be restarted for the schedule to be implemented.
* Minion pillar data. Schedule is implemented by refreshing the minion’s pillar data, for example by using ``saltutil.refresh_pillar``.
* The schedule state or schedule module. A scheduled run has no output on the minion unless the configuration is set to info level or higher. Refer to ``minion-logging-settings``.

States are executed on the minion. You can pass positional arguments and provide a YAML dictionary of named arguments.

.. Note::

    The scheduler executes different functions on the master and minions. When running on the master,
    the functions reference runner functions. When running on the minion, the functions specify execution
    functions.

Declaring scheduled jobs
________________________

A skeleton structure of a schedule declaration is:

.. code-block:: sls

    # master or minion configuration
    schedule:
      <job1>:
        function: <module.function>
        <kwarg>: <value>
        job_args:
          - <arg1>
          - <arg2>
        kwargs:
          <kwarg1>: <value1>
    ...

Defining time in schedules
__________________________

Time for jobs can be specified with valid elements or modifiers:

Time elements:

* seconds
* minutes
* hours
* days

Scheduling elements:

* when
* cron
* once

Scheduling modifiers:

* until
* after
* range
* splay

The following keyword arguments can also be used if the ``python-dateutil`` Python module
is installed.

.. code-block:: Python

    # python-dateutil options
    # date formats can be:
    - 2017-04-21 23:46:00
    - Thu Sep 25 10:30:00 EDT 2017

    # repeat job until a specified time
    until: 'Thu Sep 25 23:30:00 EDT 2017'

    # do not run job until a specified time
    after: '2017-09-25 23:30:00'

    # run at a specific time
    when: Thu May 02 03:45:30 UTC 2017

This schedules the command ``state.sls`` to bind every 3600 seconds (one hour).

.. code-block:: sls

    schedule:
      Job1:
        function: state.sls
        seconds: 3600
        args:
          - bind

Specifying a random time
________________________

The ``splay`` kwarg can be used to set a random time within a defined window.

This schedules the command ``state.sls bind pillar='{"site": "example.com"}'``
every 300 seconds (five minutes), splaying the time between 0 and 15 seconds:

.. code-block:: sls

    schedule:
      Job1:
        function: state.sls
        seconds: 300
        args:
          - bind
        kwargs:
          pillar:
            site: example.com
        splay: 15

This schedules the command ``state.sls bind pillar='{"site": "example.com"}'``
every 300 seconds (five minutes), splaying the time between 10 and 15 seconds:

.. code-block:: sls

    schedule:
      job1:
        function: state.sls
        seconds: 300
        args:
          - bind
        kwargs:
          pillar:
            site: example.com
        splay:
          start: 10
          end: 15

Schedule by date and time
_________________________

The frequency of jobs can also be specified using date strings supported by the
Python ``dateutil`` library.

This schedules the command ``state.sls bind`` at 5:00 PM minion localtime:

.. code-block:: sls

    schedule:
      job1:
        function: state.sls
        args:
          - bind
        when: 5:00pm

This schedules the command ``state.sls bind`` at 5:00 PM on Monday, Wednesday
and Friday, and at 3:00 PM on Tuesday and Thursday.

.. code-block:: sls

    schedule:
      job1:
        function: state.sls
        args:
          - bind
        when:
          - Monday 5:00pm
          - Tuesday 3:00pm
          - Wednesday 5:00pm
          - Thursday 3:00pm
          - Friday 5:00pm

This schedules the command ``state.sls bind`` every 3600 seconds (one hour)
between the hours of 8:00 AM and 5:00 PM. The range parameter must be a dictionary with
date strings using the ``dateutil`` format.

.. code-block:: sls

    schedule:
      Job1:
        function: state.sls
        seconds: 3600
        args:
          - bind
        range:
          start: 8:00am
          end: 5:00pm


Using the invert option for range, this schedules the command ``state.sls bind``
every 3600 seconds (one hour) until the current time is between the hours of 8:00 AM and 5:00 PM.
The ``range`` parameter must be a dictionary with date strings using the ``dateutil`` format.

.. code-block:: sls

    schedule:
      Job1:
        function: state.sls
        seconds: 3600
        args:
          - bind
        range:
          invert: True
          start: 8:00am
          end: 5:00pm

This schedules the function ``pkg.install`` to be executed once at the specified time.
The ``range`` parameter must be a dictionary with date strings using the ``dateutil`` format.

.. code-block:: sls

    schedule:
      job1:
        function: pkg.install
        kwargs:
          pkgs: [{'bar': '>1.2.3'}]
          refresh: true
        once: '2016-01-07T14:30:00'

The schedule entry job1 will not be removed after the job completes, so use
``schedule.delete`` to manually remove it afterwards.

The default date format is ``ISO 8601`` but can be overridden by also specifying the ``once_fmt`` option, like this:

.. code-block:: sls

    schedule:
      job1:
        function: test.ping
        once: 2015-04-22T20:21:00
        once_fmt: '%Y-%m-%dT%H:%M:%S'

Maximum parallel jobs running
_____________________________

For jobs that are long-running and could possibly step on each other, or for jobs that could pile up
in case of infrastructure outage, the scheduler supports the option ``maxrunning``, the maximum
number of copies of the routine that can run. The default for ``maxrunning`` is 1.

.. code-block:: sls

    schedule:
      Long_running_job:
        function: big_file_transfer
        jid_include: True
        maxrunning: 1

Cron-like schedule
__________________

The scheduler also supports scheduling jobs using a cron-like format:

.. code-block::

    # cron format
    cron:  '* * * * *'
            | | | | |
            | | | | +--- day of week (0 - 6) (Sunday = 0)
            | | | +----- month (1 - 12)
            | | +------- day of month (1 - 31)
            | +--------- hour (0 - 23)
            +----------- minute (0 - 59)

.. Note::

    The ``cron`` format requires the ``python-coniter`` module.

.. code-block:: sls

    schedule:
      Job1:
        function: state.sls
        cron: '*/15 * * * *'
        args:
          - bind

Job data return
_______________

By default, data about jobs runs from the Salt scheduler is returned to the master.

Setting the ``return_job`` parameter to ``False`` will prevent the data from being
sent back to the Salt master.

.. code-block:: sls

    schedule:
      job1:
        function: scheduled_job_function
        return_job: False

Job metadata
____________

It can be useful to include specific data to differentiate a job from other jobs.
Using the ``metadata`` parameter, special values can be associated with a scheduled job.

These values are not used in the execution of the job, but can be used to search for
specific jobs later if combined with the ``return_job`` parameter.

The ``metadata`` parameter must be specified as a dictionary, otherwise it will be ignored.

.. code-block:: sls

    schedule:
      job1:
        function: scheduled_job_function
        metadata:
          foo: bar

Run on start
____________

By default, any job scheduled based on the startup time of the minion will run
the scheduled job when the minion starts up.

Sometimes this is not the desired situation. Setting the ``run_on_start`` parameter
to ``False`` will cause the scheduler to skip this first run and wait until the next scheduled run:

.. code-block:: sls

    schedule:
      job1:
        function: state.sls
        seconds: 3600
        run_on_start: False
        args:
          - bind

Until and after
________________________

Using the ``until`` argument, the Salt scheduler allows you to specify an end time for a scheduled job.
If this argument is specified, jobs will not run once the specified time has passed.
Time should be specified in a format supported by the Python ``dateutil`` library.

.. code-block:: sls

    schedule:
      job1:
        function: state.sls
        seconds: 15
        until: '12/31/2015 11:59pm'
        args:
          - bind

Using the ``after`` argument, the Salt scheduler allows you to specify a start time for a scheduled job.
If ``after`` is specified, jobs will not run until the specified time has passed.
Time should be specified in a format supported by the Python ``dateutil`` library.

.. code-block:: sls

    schedule:
      job1:
        function: state.sls
        seconds: 15
        after: '12/31/2015 11:59pm'
        args:
          - bind


Managing jobs and schedules
===========================

Managing jobs
_____________

Scheduled jobs can be managed with the following functions.

A new job can be added with the following command. This job will run every 15 minutes:

.. code-block:: bash

    salt \* schedule.add job2 function='state.sls' job_args='["setup.cloud"]' job_ ,!kwargs='{"site": "example.com"}' cron='*/15 * * * *'

The new job will be defined as:

.. code-block:: sls

    schedule:
      job2:
        args:
          - setup.cloud
        cron: '*/15 * * * *'
        enabled: true
        function: state.sls
        jid_include: true
        kwargs:
          site: example.com
        maxrunning: 1
        name: job1
        return_job: true

.. Note::

    Jobs are loaded into the Salt daemon memory space and not saved persistently to disk.
    The ``schedule.save`` function will save the file
    to ``/etc/salt/minion.d/_schedule.conf``.

The job can then be modified by running:

.. code-block:: bash

    salt \* schedule.modify job2 function='state.sls' job_args='["setup.cloud"]' job_ ,!kwargs='{"site": "example2.com"}' minutes=60

The new job will be defined as:

.. code-block:: sls

    schedule:
      job2:
        args:
          - setup.cloud
        enabled: true
        function: state.sls
        jid_include: true
        kwargs:
          site: example2.com
        maxrunning: 1
        minutes: 60
        name: job2

Scheduled jobs can be listed:

.. code-block:: sls

    salt \* schedule.list

Scheduler operations
____________________

The scheduler can be enabled on minions:

.. code-block:: sls

    salt \* schedule.enable

The scheduler can be disabled on minions:

.. code-block:: sls

    salt \* schedule.disable

A specific job can be disabled in the scheduler:

.. code-block:: sls

    salt \* schedule.disable_job job1

A specific job can be enabled in the scheduler:

.. code-block:: sls

    salt \* schedule.enable_job job1

Jobs can be reloaded from disk by running:

.. code-block:: sls

    salt \* schedule.reload

Scheduling jobs from pillar
============================

A minion schedule can be set and managed centrally on the Salt master in pillar.
A pillar file defining the schedule for a minion would be defined as:

.. code-block:: sls
    :caption: /srv/pillar/schedule.sls

    schedule:
      job10:
        args: [rollout.app1_cicd]
        enabled: true
        function: state.sls
        jid_include: true
        kwargs: {site: example.com}
        maxrunning: 1
        name: job10
        return_job: true
        seconds: 3600

This schedule would then be added to the pillar top file to target specific minions.
After a refresh of pillar data, a minion would now have the new scheduled jobs
combined with locally defined scheduled jobs.


Managing schedules in states
============================

Scheduled jobs can be managed in Salt states with the schedule state module.

This example schedules the command ``state.sls bind`` at 5pm on Monday, Wednesday, and Friday,
and at 3pm on Tuesday and Thursday.

.. Note::

    This requires that ``python-dateutil`` is installed on the minion.

.. code-block:: sls

    job1:
      schedule.present:
        - function: state.sls
        - job_args:
        - bind
        - when:
          - Monday 5:00pm
          - Tuesday 3:00pm
          - Wednesday 5:00pm
          - Thursday 3:00pm
          - Friday 5:00pm

Scheduled jobs can also be specified using the format used by cron. This example
schedules the command ``state.sls bind test=True`` to run every 5 minutes.

.. Note::

    This requires that ``python-dateutil`` is installed on the minion.

.. code-block:: sls

    job1:
      schedule.present:
        - function: state.sls
        - job_args:
          - bind
        - job_kwargs:
            test: True
        - cron: '*/5 * * * *'

This will remove job1 from the schedule:

.. code-block:: sls

    job1:
      schedule.absent: []

This will disable job1 from the schedule:

.. code-block:: sls

    disable_job1:
      schedule.disable:
        - name: job1

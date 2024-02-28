.. _stop_cics_module:


stop_cics -- Query CICS and CICSPlex SM resources and definitions
=================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Stop a CICS Region using CEMT PERFORM SHUTDOWN. The shutdown-assist transaction will be used if SDTRAN is specified in the CICS Region system initialisation parameters. The task will run until the region has successfully shutdown or the shutdown has failed.






Parameters
----------

  job_name (True, str, None)
    Identifies the name of the job that the region was started with. Job names are 1-8 characters.

    If a job name was not specified in the start-up playbook, the \ :literal:`applid`\  can be provided instead.


  mode (False, str, normal)
    Specify the type of shutdown to be executed on the CICS Region.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: "Stop CICS"
      ibm.ibm_zos_cics.stop_cics:
        job_name: ABC9ABC1

    - name: "Stop CICS immediately"
      ibm.ibm_zos_cics.stop_cics:
        job_name: STARTJOB
        mode: immediate



Return Values
-------------

changed (always, bool, )
  True if the shutdown command was executed.


failed (always, bool, )
  True if the module failed, otherwise False.


executions (always, list, )
  A list of program executions performed during the task.


  name (always, str, )
    A human-readable name for the program execution.


  rc (On shutdown execution, int, )
    The return code for the program execution.


  return (always, str, )
    The standard output returned by the program execution.






Status
------





Authors
~~~~~~~

- Kiera Bennett (@KieraBennett)


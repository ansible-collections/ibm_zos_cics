.. _stop_cics_module:


stop_cics -- Query CICS and CICSPlex SM resources and definitions
=================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Stop a CICS region by using CEMT PERFORM SHUTDOWN. You can choose to perform a NORMAL or IMMEDIATE shutdown. During a NORMAL or IMMEDIATE shutdown, a shutdown assist program should run to enable CICS to shut down in a controlled manner. By default, the CICS-supplied shutdown assist transaction, CESD is used. You can specify a custom shutdown assist program in the SDTRAN system initialization parameter. The task runs until the region has successfully shut down, or until the shutdown fails.






Parameters
----------

  job_name (True, str, None)
    Identifies the name of the job that the region was started with. Job names are 1-8 characters.

    If a job name was not specified in the Start CICS playbook, the \ :literal:`applid`\  is used for the job name of the running region.

    The Stop CICS module uses this job name to identify the CICS region to be shut down.


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
  A list of program executions performed during the Ansible task.


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


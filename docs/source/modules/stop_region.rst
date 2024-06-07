.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/main/plugins/modules/stop_region.py

.. _stop_region_module:


stop_region -- Stop a CICS region
=================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Stop a CICS region by issuing a CEMT PERFORM SHUTDOWN, or cancel the job using ZOAU's job cancelling capability.
- The job\_id, job\_name, or both can be used to shutdown a region. If mulitple jobs are running with the same name, the job\_id is required.
- You can choose the shutdown mode from NORMAL, IMMEDIATE, or CANCEL.
- During a NORMAL or IMMEDIATE shutdown, a shutdown assist transaction should run to enable CICS to shut down in a controlled manner. By default, the CICS-supplied shutdown assist transaction, CESD is used. You can specify a custom shutdown assist transaction in the SDTRAN system initialization parameter. The task runs until the region has successfully shut down, or until the shutdown fails.
- You must have a console installed in the CICS region so that the stop\_region module can communicate with CICS. To define a console, you must install a terminal with the CONSNAME attribute set to your TSO user ID. For detailed instructions, see \ `Defining TSO users as console devices <https://www.ibm.com/docs/en/cics-ts/6.1?topic=cics-defining-tso-users-as-console-devices>`__\ . Add your console definition into one of the resource lists defined on the GRPLIST system initialization parameter so that it gets installed into the CICS region. Alternatively, you can use a DFHCSDUP script to update an existing CSD. This function is provided by the csd module.
- You may specify a timeout, in seconds, to wait for the region to stop after issuing the command. If this timeout is reached, the module completes in a failed state. Default behaviour does not use a timeout, which is set using a value of -1.





Parameters
----------


     
job_id
  Identifies the job ID belonging to the running CICS region.

  The stop\_region module uses this job ID to identify the state of the CICS region and shut it down.


  | **required**: False
  | **type**: str


     
job_name
  Identifies the job name belonging to the running CICS region.

  The stop\_region module uses this job name to identify the state of the CICS region and shut it down.

  The job\_name must be unique; if multiple jobs with the same name are running, use job\_id.


  | **required**: False
  | **type**: str


     
mode
  Specify the type of shutdown to be executed on the CICS region.


  | **required**: False
  | **type**: str
  | **default**: normal
  | **choices**: normal, immediate, cancel


     
no_sdtran
  No shutdown assist transaction is to be run at CICS shutdown.


  | **required**: False
  | **type**: bool


     
sdtran
  The 4-character identifier of the shutdown assist transaction.

  The default shutdown transaction, if neither SDTRAN nor NOSDTRAN is specified, is CESD.


  | **required**: False
  | **type**: str


     
timeout
  Time to wait for region to stop, in seconds.

  Specify -1 to exclude a timeout.


  | **required**: False
  | **type**: int
  | **default**: -1




Examples
--------

.. code-block:: yaml+jinja

   
   - name: "Stop CICS region"
     ibm.ibm_zos_cics.stop_region:
       job_id: JOB12345

   - name: "Stop CICS region immediately"
     ibm.ibm_zos_cics.stop_region:
       job_id: JOB12354
       mode: immediate

   - name: "Stop CICS region with name and ID"
     ibm.ibm_zos_cics.stop_region:
       job_id: JOB12354
       job_name: MYREG01

   - name: "Stop CICS using job name"
     ibm.ibm_zos_cics.stop_region:
       job_name: ANS1234
       mode: normal

   - name: "Cancel CICS region"
     ibm.ibm_zos_cics.stop_region:
       job_name: ANS1234
       mode: cancel









Return Values
-------------


   
                              
       changed
        | True if the PERFORM SHUTDOWN or CANCEL command was executed.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       failed
        | True if the Ansible task failed, otherwise False.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       executions
        | A list of program executions performed during the Ansible task.
      
        | **returned**: always
        | **type**: list
              
   
                              
        name
          | A human-readable name for the program execution.
      
          | **returned**: always
          | **type**: str
      
      
                              
        rc
          | The return code for the program execution.
      
          | **returned**: always
          | **type**: int
      
      
                              
        return
          | The standard output returned by the program execution.
      
          | **returned**: always
          | **type**: dict
              
   
                              
         changed
            | True if the state was changed, otherwise False.
      
            | **returned**: always
            | **type**: bool
      
      
                              
         failed
            | True if the module failed, otherwise False.
      
            | **returned**: always
            | **type**: bool
      
      
                              
         jobs
            | The output information for a list of jobs matching specified criteria.
      
            | **returned**: on zos_job_query module execution
            | **type**: list
              
   
                              
          job_id
              | Unique job identifier assigned to the job by JES.
      
              | **type**: str
      
      
                              
          job_name
              | The name of the batch job.
      
              | **type**: str
      
      
                              
          owner
              | The owner who ran the job.
      
              | **type**: str
      
      
                              
          ret_code
              | Return code output collected from the job log.
      
              | **type**: dict
              
   
                              
           msg
                | Return code or abend resulting from the job submission.
      
                | **type**: str
      
      
                              
           msg_code
                | Return code extracted from the `msg` so that it can be evaluated. For example, ABEND(S0C4) yields "S0C4".
      
                | **type**: str
      
      
                              
           msg_txt
                | Returns additional information related to the job.
      
                | **type**: str
      
      
                              
           code
                | Return code converted to an integer value (when possible).
      
                | **type**: int
      
      
                              
           steps
                | Series of JCL steps that were executed and their return codes.
      
                | **type**: list
              
   
                              
            step_name
                  | Name of the step shown as "was executed" in the DD section.
      
                  | **type**: str
      
      
                              
            step_cc
                  | The CC returned for this step in the DD section.
      
                  | **type**: int
      
        
      
        
      
        
      
      
                              
         message
            | Message returned on failure.
      
            | **returned**: on zos_job_query module execution
            | **type**: str
      
      
                              
         content
            | The resulting text from the command submitted.
      
            | **returned**: on zos_operator module execution
            | **type**: list
      
      
                              
         cmd
            | The operator command that has been executed
      
            | **returned**: on zos_operator module execution
            | **type**: str
      
      
                              
         rc
            | The return code from the operator command
      
            | **returned**: on zos_operator module execution
            | **type**: int
      
      
                              
         max_rc
            | The maximum return code from the tso status command
      
            | **returned**: on zos_tso_command module execution
            | **type**: int
      
      
                              
         output
            | The output from the tso command
      
            | **returned**: on zos_tso_command module execution
            | **type**: list
              
   
                              
          command
              | The executed TSO command.
      
              | **returned**: always
              | **type**: str
      
      
                              
          rc
              | The return code from the executed TSO command.
      
              | **returned**: always
              | **type**: int
      
      
                              
          content
              | The response resulting from the execution of the TSO command.
      
              | **returned**: always
              | **type**: list
      
      
                              
          lines
              | The line number of the content.
      
              | **returned**: always
              | **type**: int
      
        
      
        
      
        
      
      
                              
       msg
        | A string containing an error message if applicable
      
        | **returned**: always
        | **type**: str
      
        

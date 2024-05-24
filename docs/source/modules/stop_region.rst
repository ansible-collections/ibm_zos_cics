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
- Stop a CICS region by using CEMT PERFORM SHUTDOWN. You can choose to perform a NORMAL or IMMEDIATE shutdown.
- During a NORMAL or IMMEDIATE shutdown, a shutdown assist program should run to enable CICS to shut down in a controlled manner. By default, the CICS-supplied shutdown assist transaction, CESD is used. You can specify a custom shutdown assist program in the SDTRAN system initialization parameter. The task runs until the region has successfully shut down, or until the shutdown fails.
- You must have a console installed in the CICS region so that the stop\_region module can communicate with CICS. To define a console, you must install a terminal with the CONSNAME attribute set to your TSO user ID. For detailed instructions, see \ `Defining TSO users as console devices <https://www.ibm.com/docs/en/cics-ts/6.1?topic=cics-defining-tso-users-as-console-devices>`__\ . Add your console definition into one of the resource lists defined on the GRPLIST system initialization parameter so that it gets installed into the CICS region. Alternatively, you can use a DFHCSDUP script to update an existing CSD. This function is provided by the csd module.





Parameters
----------


     
job_id
  Identifies the job ID belonging to the running CICS region.

  The stop\_region module uses this job ID to identify the state of the CICS region and shut it down.


  | **required**: True
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









Return Values
-------------


   
                              
       changed
        | True if the PERFORM SHUTDOWN command was executed.
      
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
      
          | **returned**: on shutdown execution
          | **type**: int
      
      
                              
        return
          | The standard output returned by the program execution.
      
          | **returned**: always
          | **type**: dict
              
   
                              
         changed
            | True if the state was changed, otherwise False.
      
            | **returned**: always
            | **type**: bool
      
      
                              
         jobs
            | The output information for a list of jobs matching specified criteria.
      
            | **returned**: success
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
      
            | **returned**: failure
            | **type**: str
      
      
                              
         content
            | The resulting text from the command submitted.
      
            | **returned**: on success of PERFORM SHUTDOWN command submission.
            | **type**: list
      
        
      
        
      
      
                              
       msg
        | A string containing an error message if applicable
      
        | **returned**: always
        | **type**: str
      
        

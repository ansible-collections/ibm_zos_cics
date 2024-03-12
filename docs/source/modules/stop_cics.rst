.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/main/plugins/modules/stop_cics.py

.. _stop_cics_module:


stop_cics -- Stop a CICS Region
===============================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Stop a CICS region by using CEMT PERFORM SHUTDOWN. You can choose to perform a NORMAL or IMMEDIATE shutdown. During a NORMAL or IMMEDIATE shutdown, a shutdown assist program should run to enable CICS to shut down in a controlled manner. By default, the CICS-supplied shutdown assist transaction, CESD is used. You can specify a custom shutdown assist program in the SDTRAN system initialization parameter. The task runs until the region has successfully shut down, or until the shutdown fails.





Parameters
----------


     
job_name
  Identifies the name of the job that the region was started with. Job names are 1-8 characters.

  If a job name was not specified in the Start CICS playbook, the \ :literal:`applid`\  is used for the job name of the running region.

  The Stop CICS module uses this job name to identify the CICS region to be shut down.


  | **required**: True
  | **type**: str


     
mode
  Specify the type of shutdown to be executed on the CICS Region.


  | **required**: False
  | **type**: str
  | **default**: normal
  | **choices**: normal, immediate, cancel




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


   
                              
       changed
        | True if the shutdown command was executed.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       failed
        | True if the module failed, otherwise False.
      
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
              | Return code output collected from job log.
      
              | **type**: dict
              
   
                              
           msg
                | Return code or abend resulting from the job submission.
      
                | **type**: str
      
      
                              
           msg_code
                | Return code extracted from the `msg` so that it can be evaluated. For example, ABEND(S0C4) would yield "S0C4".
      
                | **type**: str
      
      
                              
           msg_txt
                | Returns additional information related to the job.
      
                | **type**: str
      
      
                              
           code
                | Return code converted to integer value (when possible).
      
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
      
            | **returned**: on success of shutdown command submission.
            | **type**: list
      
        
      
        
      
        

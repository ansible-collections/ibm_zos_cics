.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/main/plugins/modules/local_request_queue.py

.. _local_request_queue_module:


local_request_queue -- Create and remove the CICS local request queue
=====================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create and remove the \ `local request queue <https://www.ibm.com/docs/en/cics-ts/latest?topic=sets-local-request-queue-data-set>`__ data set used by a CICS® region. The local request queue data set stores pending BTS requests. It ensures that, if CICS fails, no pending requests are lost.
- You can use this module when provisioning or de-provisioning a CICS region.
- Use the :literal:`state` option to specify the intended state for the local request queue. For example, use :literal:`state=initial` to create a local request queue data set if it doesn't yet exist, or empty an existing local request queue of all records.





Parameters
----------


     
region_data_sets
  The location of the region data sets to be created by using a template, for example, :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`.

  If you want to use a data set that already exists, ensure that the data set is a local request queue data set.


  | **required**: True
  | **type**: dict


     
  dfhlrq
    Overrides the templated location for the local request queue data set.


    | **required**: False
    | **type**: dict


     
    dsn
      The data set name of the local request queue to override the template.


      | **required**: False
      | **type**: str



     
  template
    The base location of the region data sets with a template.


    | **required**: False
    | **type**: str



     
space_primary
  The size of the primary space allocated to the local request queue data set. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect when the local request queue data set is being created. If the data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 4


     
space_secondary
  The size of the secondary space allocated to the local request queue data set. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect when the local request queue data set is being created. If the data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 1


     
space_type
  The unit portion of the local request queue data set size. Note that this is just the unit; the value for the primary space is specified with :literal:`space\_primary` and the value for the secondary space is specified with :literal:`space\_secondary`.

  This option takes effect only when the local request queue data set is being created. If the data set already exists, the option has no effect.

  The size can be specified in megabytes (\ :literal:`m`\ ), kilobytes (\ :literal:`k`\ ), records (\ :literal:`rec`\ ), cylinders (\ :literal:`cyl`\ ), or tracks (\ :literal:`trk`\ ).


  | **required**: False
  | **type**: str
  | **default**: m
  | **choices**: m, k, rec, cyl, trk


     
state
  The intended state for the local request queue, which the module aims to achieve.

  Specify :literal:`absent` to remove the local request queue data set entirely, if it exists.

  Specify :literal:`initial` to create the local request queue data set if it does not exist, or empty this existing local request queue of all records.

  Specify :literal:`warm` to retain an existing local request queue data set in its current state. The module checks whether the specified data set exists, and if it does, leaves the data set as is. If the data set does not exist, the operation fails.


  | **required**: True
  | **type**: str
  | **choices**: initial, absent, warm


     
volumes
  The volume(s) where the data set is created. Use a string to define a singular volume or a list of strings for multiple volumes.


  | **required**: False
  | **type**: raw




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Initialize a local request queue data set by using the templated location
     ibm.ibm_zos_cics.local_request_queue:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: "initial"

   - name: Initialize a user specified local request queue data set
     ibm.ibm_zos_cics.local_request_queue:
       region_data_sets:
         dfhlrq:
           dsn: "REGIONS.ABCD0001.DFHLRQ"
       state: "initial"

   - name: Initialize a large request queue data set by using the templated location
     ibm.ibm_zos_cics.local_request_queue:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       space_primary: 50
       space_type: "m"
       state: "initial"

   - name: Retain the existing state of a local request queue data set defined by the template
     ibm.ibm_zos_cics.local_request_queue:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: "warm"

   - name: Retain the existing state of a user specified local request queue data set
     ibm.ibm_zos_cics.local_request_queue:
       region_data_sets:
         dfhlrq:
           dsn: "REGIONS.ABCD0001.DFHLRQ"
       state: "warm"

   - name: Delete a local request queue data set defined by the template
     ibm.ibm_zos_cics.local_request_queue:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: "absent"

   - name: Delete a user specified local request queue data set
     ibm.ibm_zos_cics.local_request_queue:
       region_data_sets:
         dfhlrq:
           dsn: "REGIONS.ABCD0001.DFHLRQ"
       state: "absent"









Return Values
-------------


   
                              
       changed
        | True if the state was changed, otherwise False.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       failed
        | True if the Ansible task failed, otherwise False.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       start_state
        | The state of the local request queue data set before the Ansible task runs.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the start of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
      
                              
        exists
          | True if the specified local request queue data set exists.
      
          | **returned**: always
          | **type**: bool
      
        
      
      
                              
       end_state
        | The state of the local request queue data set at the end of the Ansible task.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the end of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
      
                              
        exists
          | True if the specified local request queue data set exists.
      
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
      
      
                              
        stdout
          | The standard output stream returned from the program execution.
      
          | **returned**: always
          | **type**: str
      
      
                              
        stderr
          | The standard error stream returned from the program execution.
      
          | **returned**: always
          | **type**: str
      
        
      
      
                              
       msg
        | A string containing an error message if applicable
      
        | **returned**: always
        | **type**: str
      
        

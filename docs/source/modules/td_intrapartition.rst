.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/main/plugins/modules/td_intrapartition.py

.. _td_intrapartition_module:


td_intrapartition -- Create and remove the CICS transient data intrapartition data set
======================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create and remove the \ `transient data intrapartition <https://www.ibm.com/docs/en/cics-ts/latest?topic=data-defining-intrapartition-set>`__ data set used by a CICS® region. This data set holds all the data for intrapartition queues.
- You can use this module when provisioning or de-provisioning a CICS region.
- Use the :literal:`state` option to specify the intended state for the transient data intrapartition data set. For example, use :literal:`state=initial` to create a transient data intrapartition data set if it doesn't exist.





Parameters
----------


     
region_data_sets
  The location of the region data sets to be created by using a template, for example, :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`.

  If you want to use a data set that already exists, ensure that the data set is a transient data intrapartition data set.


  | **required**: True
  | **type**: dict


     
  dfhintra
    Overrides the templated location for the transient data intrapartition data set.


    | **required**: False
    | **type**: dict


     
    dsn
      The data set name of the transient data intrapartition to override the template.


      | **required**: False
      | **type**: str



     
  template
    The base location of the region data sets with a template.


    | **required**: False
    | **type**: str



     
space_primary
  The size of the primary space allocated to the transient data intrapartition data set. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect only when the transient data intrapartition data set is being created. If the data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 100


     
space_secondary
  The size of the secondary space allocated to the transient data intrapartition data set. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect only when the transient data intrapartition data set is being created. If the data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 10


     
space_type
  The unit portion of the transient data intrapartition data set size. Note that this is just the unit; the value for the primary space is specified with :literal:`space\_primary` and the value for the secondary space is specified with :literal:`space\_secondary`.

  This option takes effect only when the transient data intrapartition data set is being created. If the data set already exists, the option has no effect.

  The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  | **required**: False
  | **type**: str
  | **default**: REC
  | **choices**: M, K, REC, CYL, TRK


     
state
  The intended state for the transient data intrapartition data set, which the module aims to achieve.

  Specify :literal:`absent` to remove the transient data intrapartition data set entirely, if it exists.

  Specify :literal:`initial` to create the transient data intrapartition data set if it does not exist. If the specified data set exists but is empty, the module leaves the data set as is. If the specified data set exists and has contents, the module deletes the data set and then creates a new, empty one.

  Specify :literal:`warm` to retain an existing transient data intrapartition data set in its current state. The module verifies whether the specified data set exists and whether it contains any records. If both conditions are met, the module leaves the data set as is. If the data set does not exist or if it is empty, the operation fails.


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

   
   - name: Initialize a transient data intrapartition data set by using the templated location
     ibm.ibm_zos_cics.td_intrapartition:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: "initial"

   - name: Initialize a user specified transient data intrapartition data set
     ibm.ibm_zos_cics.td_intrapartition:
       region_data_sets:
         dfhintra:
           dsn: "REGIONS.ABCD0001.DFHINTRA"
       state: "initial"

   - name: Initialize a large transient data intrapartition data set by using the templated location
     ibm.ibm_zos_cics.td_intrapartition:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       space_primary: 50
       space_type: "M"
       state: "initial"

   - name: Retain the existing state of a transient data intrapartition data set data set defined by the template
     ibm.ibm_zos_cics.td_intrapartition:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: "warm"

   - name: Retain the existing state of a user specified transient data intrapartition data set
     ibm.ibm_zos_cics.td_intrapartition:
       region_data_sets:
         dfhintra:
           dsn: "REGIONS.ABCD0001.DFHINTRA"
       state: "warm"

   - name: Delete a transient data intrapartition data set data set defined by the template
     ibm.ibm_zos_cics.td_intrapartition:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: "absent"

   - name: Delete a user specified transient data intrapartition data set
     ibm.ibm_zos_cics.td_intrapartition:
       region_data_sets:
         dfhintra:
           dsn: "REGIONS.ABCD0001.DFHINTRA"
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
        | The state of the transient data intrapartition data set before the Ansible task runs.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the start of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
      
                              
        exists
          | True if the specified transient data intrapartition data set exists.
      
          | **returned**: always
          | **type**: bool
      
        
      
      
                              
       end_state
        | The state of the transient data intrapartition data set at the end of the Ansible task.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the end of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
      
                              
        exists
          | True if the specified transient data intrapartition data set exists.
      
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
      
        

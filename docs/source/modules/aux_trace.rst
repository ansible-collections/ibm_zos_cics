.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/main/plugins/modules/aux_trace.py

.. _aux_trace_module:


aux_trace -- Allocate auxiliary trace data sets
===============================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Allocates the two \ `auxiliary trace <https://www.ibm.com/docs/en/cics-ts/latest?topic=sets-setting-up-auxiliary-trace-data>`__ data sets used by a CICS® region. When CICS auxiliary trace is activated, trace entries produced by CICS are written to the auxiliary trace data sets. These data sets can hold large amounts of trace data.
- The two data sets are referred to as auxiliary trace data set A (DFHAUXT) and auxiliary trace data set B (DFHBUXT).





Parameters
----------


     
destination
  Identify which one of the auxiliary trace data sets is the target of the operation. If the value is left blank, A is implied, but you can specify A or B.

  Specify :literal:`A` to create or delete the A data set.

  Specify :literal:`B` to create or delete the B data set. This MUST be set for the creation of the B data set.


  | **required**: False
  | **type**: str
  | **default**: A
  | **choices**: A, B


     
region_data_sets
  The location of the region data sets to be created by using a template, for example, :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`.

  If you want to use a data set that already exists, ensure that the data set is an auxiliary trace data set.


  | **required**: True
  | **type**: dict


     
  dfhauxt
    Overrides the templated location for the DFHAUXT data set.


    | **required**: False
    | **type**: dict


     
    dsn
      The data set name of DFHAUXT to override the template.


      | **required**: False
      | **type**: str



     
  dfhbuxt
    Overrides the templated location for the DFHBUXT data set.


    | **required**: False
    | **type**: dict


     
    dsn
      The data set name of DFHBUXT to override the template.


      | **required**: False
      | **type**: str



     
  template
    The base location of the region data sets with a template.


    | **required**: False
    | **type**: str



     
space_primary
  The size of the primary space allocated to the auxiliary trace data set. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect only when the auxiliary trace data set is being created. If the data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 20


     
space_secondary
  The size of the secondary space allocated to the auxiliary trace data set. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect only when the auxiliary trace data set is being created. If the data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 4


     
space_type
  The unit portion of the auxiliary trace data set size. Note that this is just the unit; the value for the primary space is specified with :literal:`space\_primary` and the value for the secondary space is specified with :literal:`space\_secondary`.

  This option takes effect only when the auxiliary trace data set is being created. If the data set already exists, the option has no effect.

  The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  | **required**: False
  | **type**: str
  | **default**: M
  | **choices**: M, K, CYL, TRK


     
state
  The intended state for the auxiliary trace data set, which the module aims to achieve.

  Specify :literal:`absent` to remove the auxiliary trace data set data set entirely, if it exists.

  Specify :literal:`initial` to create the auxiliary trace data set if it does not exist. If the specified data set exists but is empty, the module leaves the data set as is. If the specified data set exists and has contents, the module deletes the data set and then creates a new, empty one.

  Specify :literal:`warm` to retain an existing auxiliary trace data set in its current state. The module checks whether the specified data set exists, and if it does, leaves the data set as is. If the data set does not exist, the operation fails.


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

   
   - name: Allocate auxiliary trace data set A (implicit) by using the templated location
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: initial

   - name: Allocate a user specified data set as auxiliary trace data set A (implicit)
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         dfhauxt:
           dsn: "REGIONS.ABCD0001.DFHAUXT"
       state: initial

   - name: Allocate auxiliary trace data set A by using the templated location
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: initial
       destination: A

   - name: Allocate a user specified data set as auxiliary trace data set A
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         dfhauxt:
           dsn: "REGIONS.ABCD0001.DFHAUXT"
       state: initial
       destination: A

   - name: Allocate auxiliary trace data set B by using the templated location
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: initial
       destination: B

   - name: Allocate a user specified data set as auxiliary trace data set B
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         dfhbuxt:
           dsn: "REGIONS.ABCD0001.DFHBUXT"
       state: initial
       destination: B

   - name: Retain the existing state of auxiliary trace data set A (implicit) defined by the template
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: "warm"

   - name: Retain the existing state of a user specified auxiliary trace data set A (implicit)
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         dfhauxt:
           dsn: "REGIONS.ABCD0001.DFHAUXT"
       state: "warm"

   - name: Retain the existing state of auxiliary trace data set B defined by the template
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: "warm"
       destination: B

   - name: Retain the existing state of a user specified auxiliary trace data set B
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         dfhbuxt:
           dsn: "REGIONS.ABCD0001.DFHBUXT"
       state: "warm"
       destination: B

   - name: Delete auxiliary trace data set A (implicit) defined by the template
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: absent

   - name: Delete a user specified auxiliary trace data set A (implicit)
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         dfhauxt:
           dsn: "REGIONS.ABCD0001.DFHBUXT"
       state: absent

   - name: Delete auxiliary trace data set B defined by the template
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       state: absent
       destination: B

   - name: Delete a user specified auxiliary trace data set B
     ibm.ibm_zos_cics.aux_trace:
       region_data_sets:
         dfhbuxt:
           dsn: "REGIONS.ABCD0001.DFHBUXT"
       state: absent
       destination: B









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
        | The state of the auxiliary trace data set before the Ansible task runs.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the start of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: Sequential

            
      
      
                              
        exists
          | True if the specified auxiliary trace data set exists.
      
          | **returned**: always
          | **type**: bool
      
        
      
      
                              
       end_state
        | The state of the auxiliary trace data set at the end of the Ansible task.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the end of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: Sequential

            
      
      
                              
        exists
          | True if the specified auxiliary trace data set exists.
      
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
      
        

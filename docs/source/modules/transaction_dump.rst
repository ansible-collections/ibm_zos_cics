.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/main/plugins/modules/transaction_dump.py

.. _transaction_dump_module:


transaction_dump -- Allocate transaction dump data sets
=======================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Allocates the two \ `transaction dump <https://www.ibm.com/docs/en/cics-ts/6.1?topic=sets-defining-transaction-dump-data>`__\  data sets used by a CICS® region.
- They are referred to as transaction dump data set A and transaction dump data set B.





Parameters
----------


     
destination
  Identifies which one of the transaction dump data sets is the target of the operation. If the value is left blank, A is implied, but you can specify A or B.

  Specify \ :literal:`A`\  to create or delete the A transaction dump data set.

  Specify \ :literal:`B`\  to create or delete the B transaction dump data set. This MUST be set for the creation of the B data set.


  | **required**: False
  | **type**: str
  | **default**: A
  | **choices**: A, B


     
region_data_sets
  The location of the region data sets to be created by using a template, for example, \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .


  | **required**: True
  | **type**: dict


     
  dfhdmpa
    Overrides the templated location for the DFHDMPA data set.


    | **required**: False
    | **type**: dict


     
    dsn
      The data set name of DFHDMPA to override the template.


      | **required**: False
      | **type**: str



     
  dfhdmpb
    Overrides the templated location for the DFHDMPB data set.


    | **required**: False
    | **type**: dict


     
    dsn
      The data set name of DFHDMPB to override the template.


      | **required**: False
      | **type**: str



     
  template
    The base location of the region data sets with a template.


    | **required**: False
    | **type**: str



     
space_primary
  The size of the primary space allocated to the transaction dump data set. Note that this is just the value; the unit is specified with \ :literal:`space\_type`\ .

  This option takes effect only when the transaction dump data set is being created. If the data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 20


     
space_secondary
  The size of the secondary space allocated to the transaction dump data set. Note that this is just the value; the unit is specified with \ :literal:`space\_type`\ .

  This option takes effect only when the transaction dump data set is being created. If the data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 4


     
space_type
  The unit portion of the transaction dump data set size. Note that this is just the unit; the value for the primary space is specified with \ :literal:`space\_primary`\  and the value for the secondary space is specified with \ :literal:`space\_secondary`\ .

  This option takes effect only when the transaction dump data set is being created. If the data set already exists, the option has no effect.

  The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  | **required**: False
  | **type**: str
  | **default**: M
  | **choices**: M, K, REC, CYL, TRK


     
state
  The intended state for the transaction dump data set, which the module aims to achieve.

  Specify \ :literal:`absent`\  to remove the transaction dump data set data set entirely, if it already exists.

  Specify \ :literal:`initial`\  to create the transaction dump data set if it does not exist.

  Specify \ :literal:`warm`\  to retain an existing transaction dump data set in its current state. The module verifies whether the specified data set exists and whether it contains any records. If both conditions are met, the module leaves the data set as is. If the data set does not exist or if it is empty, the operation fails.


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

   
   - name: Allocate transaction dump data set A (implicit)
     ibm.ibm_zos_cics.transaction_dump:
       state: initial

   - name: Allocate transaction dump data set A
     ibm.ibm_zos_cics.transaction_dump:
       state: initial
       destination: A

   - name: Allocate transaction dump data set B
     ibm.ibm_zos_cics.transaction_dump:
       state: initial
       destination: B

   - name: Delete transaction dump data set A (implicit)
     ibm.ibm_zos_cics.transaction_dump:
       state: absent

   - name: Delete transaction dump data set B
     ibm.ibm_zos_cics.transaction_dump:
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
        | The state of the transaction dump data set before the Ansible task runs.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the start of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: Sequential

            
      
      
                              
        exists
          | True if the specified transaction dump data set exists.
      
          | **returned**: always
          | **type**: bool
      
        
      
      
                              
       end_state
        | The state of the transaction dump data set at the end of the Ansible task.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the end of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: Sequential

            
      
      
                              
        exists
          | True if the specified transaction dump data set exists.
      
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
      
        
      
        

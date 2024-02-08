.. _transaction_dump_module:


transaction_dump -- Allocate transaction dump data sets
=======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Allocates the two \ `transaction dump <https://www.ibm.com/docs/en/cics-ts/6.1?topic=sets-defining-transaction-dump-data>`__\  data sets used by a CICS® region.






Parameters
----------

  space_primary (False, int, 20)
    The size of the primary space allocated to the transaction dump data set. Note that this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option takes effect only when the transaction dump data set is being created. If the data set already exists, the option has no effect.

    The size value of the secondary space allocation for the transaction dump data set is 10; the unit is specified with \ :literal:`space\_type`\ .


  space_type (False, str, M)
    The unit portion of the transaction dump data set size. Note that this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option takes effect only when the transaction dump data set is being created. If the data set already exists, the option has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region data sets to be created using a template, for example, \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .


    template (False, str, None)
      The base location of the region data sets with a template.


    dfhdmpa (False, dict, None)
      Overrides the templated location for the DFHDMPA data set.


      dsn (False, str, None)
        The data set name of DFHDMPA to override the template.



    dfhdmpb (False, dict, None)
      Overrides the templated location for the DFHDMPB data set.


      dsn (False, str, None)
        The data set name of DFHDMPB to override the template.




  cics_data_sets (False, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  library of the CICS installation, for example, \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .


    template (False, str, None)
      The templated location of the \ :literal:`SDFHLOAD`\  library.


    sdfhload (False, str, None)
      The location of the \ :literal:`SDFHLOAD`\  library to override the template.



  destination (False, str, A)
    The transaction dump data set to create. If the value is left blank, A is implied, but you can specify A or B.

    \ :literal:`A`\  will create or delete the A transaction dump data set.

    \ :literal:`B`\  will create or delete the B transaction dump data set. This MUST be set for the creation of the B data set.


  state (True, str, None)
    The intended state for the transaction dump data set, which the module will aim to achieve.

    \ :literal:`absent`\  will remove the transaction dump data set data set entirely, if it already exists.

    \ :literal:`initial`\  will create the transaction dump data set if it does not already exist.

    \ :literal:`warm`\  will retain an existing transaction dump data set in its current state.









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

changed (always, bool, )
  True if the state was changed, otherwise False.


failed (always, bool, )
  True if the query job failed, otherwise False.


start_state (always, dict, )
  The state of the local request queue before the Ansible task runs.


  data_set_organization (always, str, Sequential)
    The organization of the data set at the start of the Ansible task.


  exists (always, bool, )
    True if the local request queue data set exists.



end_state (always, dict, )
  The state of the local request queue at the end of the Ansible task.


  data_set_organization (always, str, Sequential)
    The organization of the data set at the end of the Ansible task.


  exists (always, bool, )
    True if the local request queue data set exists.



executions (always, list, )
  A list of program executions performed during the Ansible task.


  name (always, str, )
    A human-readable name for the program execution.


  rc (always, int, )
    The return code for the program execution.


  stdout (always, str, )
    The standard out stream returned by the program execution.


  stderr (always, str, )
    The standard error stream returned from the program execution.






Status
------





Authors
~~~~~~~

- Thomas Foyle (@tom-foyle)


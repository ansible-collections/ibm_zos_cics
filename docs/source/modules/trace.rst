.. _trace_module:


trace -- Allocate auxiliary trace data sets
===========================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Allocates the two \ `auxiliary trace <https://www.ibm.com/docs/en/cics-ts/6.1?topic=sets-setting-up-auxiliary-trace-data>`__\  data sets used by a CICS® region. When CICS auxiliary trace is activated, trace entries produced by CICS are written to the auxiliary trace data sets. These data sets can hold large amounts of trace data.






Parameters
----------

  space_primary (False, int, 20)
    The size of the primary space allocated to the auxiliary trace data set. Note that this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option takes effect only when the auxiliary trace data set is being created. If the data set already exists, the option has no effect.

    The size value of the secondary space allocation for the auxiliary trace data set is 10; the unit is specified with \ :literal:`space\_type`\ .


  space_type (False, str, M)
    The unit portion of the auxiliary trace data set size. Note that this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option takes effect only when the auxiliary trace data set is being created. If the data set already exists, the option has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region data sets to be created using a template, for example, \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .

    If you want to use a data set that already exists, ensure that the data set is an auxiliary trace data set.


    template (False, str, None)
      The base location of the region data sets with a template.


    dfhauxt (False, dict, None)
      Overrides the templated location for the DFHAUXT data set.


      dsn (False, str, None)
        The data set name of DFHAUXT to override the template.



    dfhbuxt (False, dict, None)
      Overrides the templated location for the DFHBUXT data set.


      dsn (False, str, None)
        The data set name of DFHBUXT to override the template.




  cics_data_sets (False, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  library of the CICS installation, for example, \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .


    template (False, str, None)
      The templated location of the \ :literal:`SDFHLOAD`\  library.


    sdfhload (False, str, None)
      The location of the \ :literal:`SDFHLOAD`\  library to override the template.



  destination (False, str, A)
    The auxiliary trace data set to create. If the value is left blank, A is implied, but you can specify A or B.

    \ :literal:`A`\  will create or delete the A auxiliary trace data set.

    \ :literal:`B`\  will create or delete the B auxiliary trace data set. This MUST be set for the creation of B data set.


  state (True, str, None)
    The intended state for the auxiliary trace data set, which the module will aim to achieve.

    \ :literal:`absent`\  will remove the auxiliary trace data set data set entirely, if it already exists.

    \ :literal:`initial`\  will create the auxiliary trace data set if it does not already exist.

    \ :literal:`warm`\  will retain an existing auxiliary trace data set in its current state.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Allocate auxiliary trace data set A (implicit)
      ibm.ibm_zos_cics.trace:
        state: initial

    - name: Allocate auxiliary trace data set A
      ibm.ibm_zos_cics.trace:
        state: initial
        destination: A

    - name: Allocate auxiliary trace data set B
      ibm.ibm_zos_cics.trace:
        state: initial
        destination: B

    - name: Delete auxiliary trace data set A (implicit)
      ibm.ibm_zos_cics.trace:
        state: absent

    - name: Delete auxiliary trace data set B
      ibm.ibm_zos_cics.trace:
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

- Kye Maloy (@KyeMaloy97)


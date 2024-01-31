.. _trace_module:


trace -- Allocate auxillary trace data sets
===========================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Allocates the two \ `auxillary trace <https://www.ibm.com/docs/en/cics-ts/6.1?topic=sets-setting-up-auxiliary-trace-data>`__\  data sets used by a CICS® region.






Parameters
----------

  space_primary (False, int, 20)
    The size of the auxillary trace data set's primary space allocation. Note, this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option only takes effect when the auxillary trace data set is being created. If it already exists, it has no effect.


  space_type (False, str, M)
    The unit portion of the auxillary trace data set size. Note, this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option only takes effect when the auxillary trace data set is being created. If it already exists, it has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region's data sets using a template, e.g. \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .


    template (False, str, None)
      The base location of the region's data sets with a template.


    dfhauxt (False, dict, None)
      Overrides the templated location for the DFHAUXT data set.


      dsn (False, str, None)
        Data set name of the DFHAUXT to override the template.



    dfhbuxt (False, dict, None)
      Overrides the templated location for the DFHBUXT data set.


      dsn (False, str, None)
        Data set name of the DFHBUXT to override the template.




  cics_data_sets (False, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  data set, e.g. \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .


    template (False, str, None)
      Templated location of the cics install data sets.


    sdfhload (False, str, None)
      Location of the sdfhload data set.

      Overrides the templated location for sdfhload.



  destination (False, str, A)
    The auxillary trace data set to create, if left blank A is implied, but this can be used to specify A or B.

    \ :literal:`A`\  will create or delete the A auxillary trace data set.

    \ :literal:`B`\  will create or delete the B auxillary trace data set. This MUST be set for B data set creation.


  state (True, str, None)
    The desired state for the auxillary trace data set, which the module will aim to achieve.

    \ :literal:`absent`\  will remove the auxillary trace data set data set entirely, if it already exists.

    \ :literal:`initial`\  will create the auxillary trace data set if it does not already exist.

    \ :literal:`warm`\  will retain an existing auxiliary trace data set in its current state.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Allocate auxillary trace data set A (implicit)
      ibm.ibm_zos_cics.trace:
        state: initial

    - name: Allocate auxillary trace data set A
      ibm.ibm_zos_cics.trace:
        state: initial
        destination: A

    - name: Allocate auxillary trace data set B
      ibm.ibm_zos_cics.trace:
        state: initial
        destination: B

    - name: Delete auxillary trace data set A (implicit)
      ibm.ibm_zos_cics.trace:
        state: absent

    - name: Delete auxillary trace data set B
      ibm.ibm_zos_cics.trace:
        state: absent
        destination: B



Return Values
-------------

changed (always, bool, )
  True if the state was changed, otherwise False.


failed (always, bool, )
  True if the query job failed, otherwise False.


executions (always, list, )
  A list of program executions performed during the task.


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


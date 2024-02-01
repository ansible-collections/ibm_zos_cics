.. _intrapartition_module:


intrapartition -- Create and remove the CICS transient data intrapartition data set
===================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create and remove the \ `transient data intrapartition <https://www.ibm.com/docs/en/cics-ts/latest?topic=data-defining-intrapartition-set>`__\  data set used by a CICS® region.

Useful when provisioning or de-provisioning a CICS region.

Use the \ :literal:`state`\  option to specify the intended state for the transient data intrapartition. For example, \ :literal:`state=initial`\  will create a transient data intrapartition data set if it doesn't yet exist.






Parameters
----------

  space_primary (False, int, 100)
    The size of the transient data intrapartition data set's primary space allocation. Note, this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option only takes effect when the transient data intrapartition is being created. If it already exists, it has no effect.

    The transient data intrapartition data set's secondary space allocation is set to 1.


  space_type (False, str, REC)
    The unit portion of the transient data intrapartition data set size. Note, this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option only takes effect when the transient data intrapartition is being created. If it already exists, it has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region's data sets using a template, e.g. \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .


    template (False, str, None)
      The base location of the region's data sets with a template.


    dfhintra (False, dict, None)
      Overrides the templated location for the transient data intrapartition data set.


      dsn (False, str, None)
        Data set name of the transient data intrapartition to override the template.




  cics_data_sets (False, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  data set, e.g. \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .


    template (False, str, None)
      Templated location of the cics install data sets.


    sdfhload (False, str, None)
      Location of the sdfhload data set.

      Overrides the templated location for sdfhload.



  state (True, str, None)
    The desired state for the transient data intrapartition, which the module will aim to achieve.

    \ :literal:`absent`\  will remove the transient data intrapartition data set entirely, if it already exists.

    \ :literal:`initial`\  will create the transient data intrapartition data set if it does not already exist.

    \ :literal:`warm`\  will retain an existing transient data intrapartition data set in its current state.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Initialize a transient data intrapartition
      ibm.ibm_zos_cics.intrapartition:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        state: "initial"

    - name: Initialize a large transient data intrapartition
      ibm.ibm_zos_cics.intrapartition:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        space_primary: 50
        space_type: "M"
        state: "initial"

    - name: Delete transient data intrapartition
      ibm.ibm_zos_cics.intrapartition:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        state: "absent"



Return Values
-------------

changed (always, bool, )
  True if the state was changed, otherwise False.


failed (always, bool, )
  True if the query job failed, otherwise False.


start_state (always, dict, )
  The state of the transient data intrapartition before the task runs.


  vsam (always, bool, )
    True if the data set is a VSAM data set.


  exists (always, bool, )
    True if the transient data intrapartition data set exists.



end_state (always, dict, )
  The state of the transient data intrapartition at the end of the task.


  vsam (always, bool, )
    True if the data set is a VSAM data set.


  exists (always, bool, )
    True if the transient data intrapartition data set exists.



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

- Andrew Twydell (@andrewtwydell)


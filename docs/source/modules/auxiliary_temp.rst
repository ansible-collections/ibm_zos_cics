.. _auxiliary_temp_module:


auxiliary_temp -- Create and remove the CICS auxiliary temporary storage data set
=================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create and remove the \ `auxiliary temporary storage <https://www.ibm.com/docs/en/cics-ts/latest?topic=sets-defining-auxiliary-temporary-storage-data-set>`__\  data set used by a CICS® region.

Useful when provisioning or de-provisioning a CICS region.

Use the \ :literal:`state`\  option to specify the intended state for the auxiliary temp data set. For example, \ :literal:`state=initial`\  will create a auxiliary temp data set if it doesn't yet exist.






Parameters
----------

  space_primary (False, int, 200)
    The size of the auxiliary temporary storage data set's primary space allocation. Note, this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option only takes effect when the auxiliary temporary storage is being created. If it already exists, it has no effect.

    The auxiliary temporary storage data set's secondary space allocation is set to 10.


  space_type (False, str, REC)
    The unit portion of the auxiliary temporary storage data set size. Note, this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option only takes effect when the auxiliary temporary storage is being created. If it already exists, it has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region's data sets using a template, e.g. \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .


    template (False, str, None)
      The base location of the region's data sets with a template.


    dfhtemp (False, dict, None)
      Overrides the templated location for the auxiliary temporary storage data set.


      dsn (False, str, None)
        Data set name of the auxiliary temporary storage to override the template.




  cics_data_sets (False, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  data set, e.g. \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .


    template (False, str, None)
      Templated location of the cics install data sets.


    sdfhload (False, str, None)
      Location of the sdfhload data set.

      Overrides the templated location for sdfhload.



  state (True, str, None)
    The desired state for the auxiliary temporary storage, which the module will aim to achieve.

    \ :literal:`absent`\  will remove the auxiliary temporary storage data set entirely, if it already exists.

    \ :literal:`initial`\  will create the auxiliary temporary storage data set if it does not already exist.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Initialize an auxiliary temporary storage data set
      ibm.ibm_zos_cics.auxiliary_temp:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        state: "initial"

    - name: Initialize a large auxiliary temporary storage data set
      ibm.ibm_zos_cics.auxiliary_temp:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        space_primary: 50
        space_type: "M"
        state: "initial"

    - name: Delete an existing auxiliary temporary storage data set
      ibm.ibm_zos_cics.auxiliary_temp:
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
  The state of the auxiliary temporary storage before the task runs.


  vsam (always, bool, )
    True if the data set is a VSAM data set.


  exists (always, bool, )
    True if the auxiliary temporary storage data set exists.



end_state (always, dict, )
  The state of the auxiliary temporary storage at the end of the task.


  vsam (always, bool, )
    True if the data set is a VSAM data set.


  exists (always, bool, )
    True if the auxiliary temporary storage data set exists.



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


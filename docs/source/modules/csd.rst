.. _csd_module:


csd -- Create, remove, and manage the CICS CSD
==============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create, remove, and manage the \ `csd <https://www.ibm.com/docs/en/cics-ts/6.1?topic=configuring-setting-up-shared-data-sets-csd-sysin>`__\  data set used by a CICS® region.

Useful when provisioning or de-provisioning a CICS region, or when managing the state of the CSD during upgrades or restarts.

Use the \ :literal:`state`\  option to specify the intended state for the CSD. For example, \ :literal:`state=initial`\  will create and initialize a CSD data set if it doesn't yet exist, or it will take an existing CSD and empty it of all records.






Parameters
----------

  space_primary (False, int, 4)
    The size of the CSD data set's primary space allocation. Note, this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option only takes effect when the CSD is being created. If it already exists, it has no effect.

    The CSD data set's secondary space allocation is set to 1.


  space_type (False, str, M)
    The unit portion of the CSD data set size. Note, this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option only takes effect when the CSD is being created. If it already exists, it has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region's data sets using a template, e.g. \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .


    template (False, str, None)
      The base location of the region's data sets with a template.


    dfhcsd (False, dict, None)
      Overrides the templated location for the CSD data set.


      dsn (False, str, None)
        Data set name of the CSD to override the template.




  cics_data_sets (True, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  data set, e.g. \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .


    template (False, str, None)
      Templated location of the cics install data sets.


    sdfhload (False, str, None)
      Location of the sdfhload data set.

      Overrides the templated location for sdfhload.



  state (True, str, None)
    The desired state for the CSD, which the module will aim to achieve.

    \ :literal:`absent`\  will remove the CSD data set entirely, if it already exists.

    \ :literal:`initial`\  will create the CSD data set if it does not already exist, and initialise it using dfhcsdup

    \ :literal:`warm`\  will retain an existing CSD in its current state.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Initialize a CSD
      ibm.ibm_zos_cics.csd:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        state: "initial"

    - name: Initialize a large CSD data set
      ibm.ibm_zos_cics.csd:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        space_primary: 10
        space_type: "M"
        state: "initial"

    - name: Delete CSD
      ibm.ibm_zos_cics.csd:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        state: "absent"

    - name: Retain existing state of CSD
      ibm.ibm_zos_cics.csd:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        state: "warm"



Return Values
-------------

changed (always, bool, )
  True if the state was changed, otherwise False.


failed (always, bool, )
  True if the query job failed, otherwise False.


start_state (always, dict, )
  The state of the CSD before the task runs.


  vsam (always, bool, )
    True if the data set is a VSAM data set.


  exists (always, bool, )
    True if the CSD data set exists.



end_state (always, dict, )
  The state of the CSD at the end of the task.


  vsam (always, bool, )
    True if the data set is a VSAM data set.


  exists (always, bool, )
    True if the CSD data set exists.



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

- Thomas Latham (@Thomas-Latham3)


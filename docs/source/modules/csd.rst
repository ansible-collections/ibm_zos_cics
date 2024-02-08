.. _csd_module:


csd -- Create, remove, and manage the CICS CSD
==============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create, remove, and manage the \ `CICS system definition data set <https://www.ibm.com/docs/en/cics-ts/6.1?topic=configuring-setting-up-shared-data-sets-csd-sysin>`__\  (CSD) used by a CICS® region.

You can use this module when provisioning or de-provisioning a CICS region, or when managing the state of the CSD during upgrades or restarts.

Use the \ :literal:`state`\  option to specify the intended state for the CSD. For example, \ :literal:`state=initial`\  will create and initialize a CSD if it doesn't exist, or it will take an existing CSD and empty it of all records.






Parameters
----------

  space_primary (False, int, 4)
    The size of the primary space allocated to the CSD. Note that this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option takes effect only when the CSD is being created. If the CSD already exists, the option has no effect.

    The size value of the secondary space allocation for the CSD is 1; the unit is specified with \ :literal:`space\_type`\ .


  space_type (False, str, M)
    The unit portion of the CSD size. Note that this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option takes effect only when the CSD is being created. If the CSD already exists, the option has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region data sets to be created using a template, for example, \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .


    template (False, str, None)
      The base location of the region data sets with a template.


    dfhcsd (False, dict, None)
      Overrides the templated location for the CSD.


      dsn (False, str, None)
        The data set name of the CSD to override the template.




  cics_data_sets (True, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  library of the CICS installation, for example, \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .


    template (False, str, None)
      The templated location of the \ :literal:`SDFHLOAD`\  library.


    sdfhload (False, str, None)
      The location of the \ :literal:`SDFHLOAD`\  library to override the template.



  state (True, str, None)
    The intended state for the CSD, which the module will aim to achieve.

    \ :literal:`absent`\  will remove the CSD entirely, if it already exists.

    \ :literal:`initial`\  will create the CSD if it does not already exist, and initialize it by using DFHCSDUP.

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
  The state of the CSD before the Ansible task runs.


  data_set_organization (always, str, VSAM)
    The organization of the data set at the start of the Ansible task.


  exists (always, bool, )
    True if the CSD exists.



end_state (always, dict, )
  The state of the CSD at the end of the Ansible task.


  data_set_organization (always, str, VSAM)
    The organization of the data set at the end of the Ansible task.


  exists (always, bool, )
    True if the CSD exists.



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

- Thomas Latham (@Thomas-Latham3)


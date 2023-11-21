.. _local_catalog_module:


local_catalog -- Create, remove, and manage the CICS local catalog
==================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create, remove, and manage the \ `local catalog <https://www.ibm.com/docs/en/cics-ts/latest?topic=catalogs-local-catalog>`__\  data set used by a CICS® region.

Useful when provisioning or de-provisioning a CICS region, or when managing the state of the local catalog during upgrades or restarts.

Use the \ :literal:`state`\  option to specify the intended state for the local catalog. For example, \ :literal:`state=initial`\  will create and initialize a local catalog data set if it doesn't yet exist, or it will take an existing local catalog and empty it of all records.






Parameters
----------

  space_primary (False, int, 200)
    The size of the local catalog data set's primary space allocation. Note, this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option only takes effect when the local catalog is being created. If it already exists, it has no effect.

    The local catalog data set's secondary space allocation is set to 1.


  space_type (False, str, REC)
    The unit portion of the local catalog data set size. Note, this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option only takes effect when the local catalog is being created. If it already exists, it has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region's data sets using a template, e.g. \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .

    If it already exists, this data set must be cataloged.


    template (False, str, None)
      The base location of the region's data sets with a template.


    dfhlcd (False, dict, None)
      Overrides the templated location for the local catalog data set.


      dsn (False, str, None)
        Data set name of the local catalog to override the template.




  cics_data_sets (True, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  data set, e.g. \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .

    This module uses the \ :literal:`DFHCCUTL`\  utility internally, which is found in the \ :literal:`SDFHLOAD`\  data set in the CICS installation.


    template (False, str, None)
      Templated location of the cics install data sets.


    sdfhload (False, str, None)
      Location of the sdfhload data set.

      Overrides the templated location for sdfhload.



  state (True, str, None)
    The desired state for the local catalog, which the module will aim to achieve.

    \ :literal:`absent`\  will remove the local catalog data set entirely, if it already exists.

    \ :literal:`initial`\  will create the local catalog data set if it does not already exist, and empty it of all existing records.

    \ :literal:`warm`\  will retain an existing local catalog in its current state.







See Also
--------

.. seealso::

   :ref:`global_catalog_module`
      The official documentation on the **global_catalog** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Initialize a local catalog
      ibm.ibm_zos_cics.local_catalog:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        state: "initial"

    - name: Initialize a large catalog
      ibm.ibm_zos_cics.local_catalog:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        space_primary: 500
        space_type: "REC"
        state: "initial"

    - name: Delete local catalog
      ibm.ibm_zos_cics.local_catalog:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        state: "absent"



Return Values
-------------

changed (always, bool, )
  True if the state was changed, otherwise False.


failed (always, bool, )
  True if the query job failed, otherwise False.


start_state (always, dict, )
  The state of the local catalog before the task runs.


  vsam (always, bool, )
    True if the data set is a VSAM data set.


  exists (always, bool, )
    True if the local catalog data set exists.



end_state (always, dict, )
  The state of the local catalog at the end of the task.


  vsam (always, bool, )
    True if the data set is a VSAM data set.


  exists (always, bool, )
    True if the local catalog data set exists.



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

- Enam Khan (@enam-khan)


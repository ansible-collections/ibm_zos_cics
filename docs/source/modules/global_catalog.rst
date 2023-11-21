.. _global_catalog_module:


global_catalog -- Create, remove, and manage the CICS global catalog
====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create, remove, and manage the \ `global catalog <https://www.ibm.com/docs/en/cics-ts/latest?topic=catalogs-global-catalog>`__\  data set used by a CICS® region.

Useful when provisioning or de-provisioning a CICS region, or when managing the state of the global catalog during upgrades or restarts.

Use the \ :literal:`state`\  option to specify the intended state for the global catalog. For example, \ :literal:`state=initial`\  will create and initialize a global catalog data set if it doesn't yet exist, or it will take an existing global catalog and set its autostart override record to \ :literal:`AUTOINIT`\ . In either case, a CICS region using this global catalog and the \ :literal:`START=AUTO`\  system initialization parameter will perform an initial start.






Parameters
----------

  space_primary (False, int, 5)
    The size of the global catalog data set's primary space allocation. Note, this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option only takes effect when the global catalog is being created. If it already exists, it has no effect.

    The global catalog data set's secondary space allocation is set to 1.


  space_type (False, str, M)
    The unit portion of the global catalog data set size. Note, this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option only takes effect when the global catalog is being created. If it already exists, it has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region's data sets using a template, e.g. \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .

    If it already exists, this data set must be cataloged.


    template (False, str, None)
      The base location of the region's data sets with a template.


    dfhgcd (False, dict, None)
      Overrides the templated location for the global catalog data set.


      dsn (False, str, None)
        Data set name of the global catalog to override the template.




  cics_data_sets (True, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  data set, e.g. \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .

    This module uses the \ :literal:`DFHRMUTL`\  utility internally, which is found in the \ :literal:`SDFHLOAD`\  data set in the CICS installation.


    template (False, str, None)
      Templated location of the cics install data sets.


    sdfhload (False, str, None)
      Location of the sdfhload data set.

      Overrides the templated location for sdfhload.



  state (True, str, None)
    The desired state for the global catalog, which the module will aim to achieve.

    \ :literal:`absent`\  will remove the global catalog data set entirely, if it already exists.

    \ :literal:`initial`\  will set the autostart override record to \ :literal:`AUTOINIT`\ , creating the global catalog data set if it does not already exist.

    \ :literal:`cold`\  will set an existing global catalog's autostart override record to \ :literal:`AUTOCOLD`\ .

    \ :literal:`warm`\  will set an existing global catalog's autostart override record to \ :literal:`AUTOASIS`\ , undoing any previous setting of \ :literal:`AUTOINIT`\  or \ :literal:`AUTOCOLD`\ .







See Also
--------

.. seealso::

   :ref:`local_catalog_module`
      The official documentation on the **local_catalog** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Initialize a global catalog
      ibm.ibm_zos_cics.global_catalog:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        state: "initial"

    - name: Initialize a large catalog
      ibm.ibm_zos_cics.global_catalog:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        space_primary: 100
        space_type: "M"
        state: "initial"

    - name: Set autostart override record to AUTOASIS
      ibm.ibm_zos_cics.global_catalog:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        state: "warm"

    - name: Set autostart override record to AUTOCOLD
      ibm.ibm_zos_cics.global_catalog:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        state: "cold"

    - name: Delete global catalog
      ibm.ibm_zos_cics.global_catalog:
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
  The state of the global catalog before the task runs.


  autostart_override (always, str, )
    The current autostart override record.


  next_start (always, str, )
    The next start type listed in the global catalog.


  exists (always, bool, )
    True if the global catalog data set exists.



end_state (always, dict, )
  The state of the global catalog at the end of the task.


  autostart_override (always, str, )
    The current autostart override record.


  next_start (always, str, )
    The next start type listed in the global catalog


  exists (always, bool, )
    True if the global catalog data set exists.



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

- Andrew Twydell (@AndrewTwydell)


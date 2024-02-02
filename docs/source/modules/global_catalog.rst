.. _global_catalog_module:


global_catalog -- Create, remove, and manage the CICS global catalog
====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create, remove, and manage the \ `global catalog <https://www.ibm.com/docs/en/cics-ts/latest?topic=catalogs-global-catalog>`__\  data set used by a CICS® region. The global catalog is used to store start type information, location of the CICS system log, installed resource definitions, terminal control information and profiles. It contains information that CICS requires on a restart.

You can use this module when provisioning or de-provisioning a CICS region, or when managing the state of the global catalog during upgrades or restarts.

Use the \ :literal:`state`\  option to specify the intended state for the global catalog. For example, \ :literal:`state=initial`\  will create and initialize a global catalog data set if it doesn't yet exist, or it will take an existing global catalog and set its autostart override record to \ :literal:`AUTOINIT`\ . In either case, a CICS region using this global catalog and the \ :literal:`START=AUTO`\  system initialization parameter will perform an initial start.






Parameters
----------

  space_primary (False, int, 5)
    The size of the primary space allocated to the global catalog data set. Note that this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option takes effect only when the global catalog is being created. If the global catalog already exists, the option has no effect.

    The size value of the secondary space allocation for the global catalog data set is 1; the unit is specified with \ :literal:`space\_type`\ .


  space_type (False, str, M)
    The unit portion of the global catalog data set size. Note that this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option takes effect only when the global catalog is being created. If the global catalog already exists, the option has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region data sets to be created using a template, for example, \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .

    If you want to use a data set that already exists, ensure that the data set is a global catalog data set.


    template (False, str, None)
      The base location of the region data sets with a template.


    dfhgcd (False, dict, None)
      Overrides the templated location for the global catalog data set.


      dsn (False, str, None)
        The data set name of the global catalog to override the template.




  cics_data_sets (True, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  library of the CICS installation, for example, \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .

    This module uses the \ :literal:`DFHRMUTL`\  utility internally, which is found in the \ :literal:`SDFHLOAD`\  library.


    template (False, str, None)
      The templated location of the \ :literal:`SDFHLOAD`\  library.


    sdfhload (False, str, None)
      The location of the \ :literal:`SDFHLOAD`\  library to override the template.



  state (True, str, None)
    The intended state for the global catalog, which the module will aim to achieve.

    \ :literal:`absent`\  will remove the global catalog data set entirely, if it already exists.

    \ :literal:`initial`\  will set the autostart override record to \ :literal:`AUTOINIT`\ . The module will create the global catalog data set if it does not already exist.

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
  The state of the global catalog before the Ansible task runs.


  autostart_override (always, str, )
    The current autostart override record.


  next_start (always, str, )
    The next start type listed in the global catalog.


  exists (always, bool, )
    True if the global catalog data set exists.



end_state (always, dict, )
  The state of the global catalog at the end of the Ansible task.


  autostart_override (always, str, )
    The current autostart override record.


  next_start (always, str, )
    The next start type listed in the global catalog


  exists (always, bool, )
    True if the global catalog data set exists.



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

- Andrew Twydell (@AndrewTwydell)


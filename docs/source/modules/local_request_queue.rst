.. _local_request_queue_module:


local_request_queue -- Create and remove the CICS local request queue
=====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create and remove the \ `local request queue <https://www.ibm.com/docs/en/cics-ts/latest?topic=sets-local-request-queue-data-set>`__\  data set used by a CICS® region. The local request queue data set stores pending BTS requests. It ensures that, if CICS fails, no pending requests are lost.

You can use this module when provisioning or de-provisioning a CICS region.

Use the \ :literal:`state`\  option to specify the intended state for the local request queue. For example, \ :literal:`state=initial`\  will create a local request queue data set if it doesn't yet exist, or it will take an existing local request queue and empty it of all records.






Parameters
----------

  space_primary (False, int, 4)
    The size of the primary space allocated to the local request queue data set. Note that this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option takes effect when the local request queue data set is being created. If the data set already exists, the option has no effect.

    The size value of the secondary space allocation for the local request queue data set is 1; the unit is specified with \ :literal:`space\_type`\ .


  space_type (False, str, M)
    The unit portion of the local request queue data set size. Note that this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option takes effect only when the local request queue data set is being created. If the data set already exists, the option has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region data sets to be created using a template, for example, \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .

    If you want to use a data set that already exists, ensure that the data set is a local request queue data set.


    template (False, str, None)
      The base location of the region data sets with a template.


    dfhlrq (False, dict, None)
      Overrides the templated location for the local request queue data set.


      dsn (False, str, None)
        The data set name of the local request queue to override the template.




  cics_data_sets (False, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  library of the CICS installation, for example, \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .


    template (False, str, None)
      The templated location of the \ :literal:`SDFHLOAD`\  library.


    sdfhload (False, str, None)
      The location of the the \ :literal:`SDFHLOAD`\  library to override the template.



  state (True, str, None)
    The intended state for the local request queue, which the module will aim to achieve.

    \ :literal:`absent`\  will remove the local request queue data set entirely, if it already exists.

    \ :literal:`initial`\  will create the local request queue data set if it does not already exist, and empty it of all existing records.

    \ :literal:`warm`\  will retain an existing local request queue data set in its current state.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: Initialize a local request queue
      ibm.ibm_zos_cics.local_request_queue:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        state: "initial"

    - name: Initialize a large request queue
      ibm.ibm_zos_cics.local_request_queue:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        space_primary: 50
        space_type: "M"
        state: "initial"

    - name: Delete local request queue
      ibm.ibm_zos_cics.local_request_queue:
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
  The state of the local request queue before the Ansible task runs.


  data_set_organization (always, str, VSAM)
    The organization of the data set at the start of the Ansible task.


  exists (always, bool, )
    True if the local request queue data set exists.



end_state (always, dict, )
  The state of the local request queue at the end of the Ansible task.


  data_set_organization (always, str, VSAM)
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

- Drew Hughes (@andrewhughes101)


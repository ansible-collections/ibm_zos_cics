.. _intrapartition_module:


intrapartition -- Create and remove the CICS transient data intrapartition data set
===================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Create and remove the \ `transient data intrapartition <https://www.ibm.com/docs/en/cics-ts/latest?topic=data-defining-intrapartition-set>`__\  data set used by a CICS® region. This data set holds all the data for intrapartition queues.

You can use this module when provisioning or de-provisioning a CICS region.

Use the \ :literal:`state`\  option to specify the intended state for the transient data intrapartition data set. For example, \ :literal:`state=initial`\  will create a transient data intrapartition data set if it doesn't exist.






Parameters
----------

  space_primary (False, int, 100)
    The size of the primary space allocated to the transient data intrapartition data set. Note that this is just the value; the unit is specified with \ :literal:`space\_type`\ .

    This option takes effect only when the transient data intrapartition data set is being created. If the data set already exists, the option has no effect.

    The size value of the secondary space allocation for the transient data intrapartition data set is 1; the unit is specified with \ :literal:`space\_type`\ .


  space_type (False, str, REC)
    The unit portion of the transient data intrapartition data set size. Note that this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

    This option takes effect only when the transient data intrapartition data set is being created. If the data set already exists, the option has no effect.

    The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  region_data_sets (True, dict, None)
    The location of the region data sets to be created using a template, for example, \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .

    If you want to use a data set that already exists, ensure that the data set is a transient data intrapartition data set.


    template (False, str, None)
      The base location of the region data sets with a template.


    dfhintra (False, dict, None)
      Overrides the templated location for the transient data intrapartition data set.


      dsn (False, str, None)
        The data set name of the transient data intrapartition to override the template.




  cics_data_sets (False, dict, None)
    The name of the \ :literal:`SDFHLOAD`\  library of the CICS installation, for example, \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .


    template (False, str, None)
      The templated location of the \ :literal:`SDFHLOAD`\  library.


    sdfhload (False, str, None)
      The location of the \ :literal:`SDFHLOAD`\  library to override the template.



  state (True, str, None)
    The intended state for the transient data intrapartition data set, which the module will aim to achieve.

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
  The state of the transient data intrapartition data set before the Ansible task runs.


  data_set_organization (always, str, VSAM)
    The organization of the data set at the start of the Ansible task.


  exists (always, bool, )
    True if the transient data intrapartition data set exists.



end_state (always, dict, )
  The state of the transient data intrapartition data set at the end of the Ansible task.


  data_set_organization (always, str, VSAM)
    The organization of the data set at the end of the Ansible task.


  exists (always, bool, )
    True if the transient data intrapartition data set exists.



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

- Andrew Twydell (@andrewtwydell)


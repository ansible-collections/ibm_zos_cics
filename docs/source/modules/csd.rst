.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/main/plugins/modules/csd.py

.. _csd_module:


csd -- Create, remove, and manage the CICS CSD
==============================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create, remove, and manage the \ `CICS system definition data set <https://www.ibm.com/docs/en/cics-ts/latest?topic=configuring-setting-up-shared-data-sets-csd-sysin>`__ (CSD) used by a CICS® region.
- You can use this module when provisioning or de-provisioning a CICS region, or when managing the state of the CSD during upgrades or restarts.
- Use the :literal:`state` option to specify the intended state for the CSD. For example, use :literal:`state=initial` to create and initialize a CSD if it doesn't exist, or empty an existing CSD of all records.





Parameters
----------


     
cics_data_sets
  The name of the :literal:`SDFHLOAD` library of the CICS installation, for example, :literal:`CICSTS61.CICS.SDFHLOAD`.


  | **required**: True
  | **type**: dict


     
  sdfhload
    The location of the :literal:`SDFHLOAD` library. If :literal:`cics\_data\_sets.template` is provided, this value overrides the template.


    | **required**: False
    | **type**: str


     
  template
    The templated location of the :literal:`SDFHLOAD` library.


    | **required**: False
    | **type**: str



     
input_content
  The content of the DFHCSDUP script to submit, if you are using the :literal:`input\_location=INLINE` option.


  | **required**: False
  | **type**: str


     
input_location
  The type of location from which to load the DFHCSDUP script.

  Specify :literal:`DATA\_SET` to load from a PDS, PDSE, or sequential data set.

  Specify :literal:`USS` to load from a file on UNIX System Services (USS).

  Specify :literal:`LOCAL` to load from a file local to the Ansible control node.

  Specify :literal:`INLINE` to allow a script to be passed directly through the :literal:`input\_content` parameter.


  | **required**: False
  | **type**: str
  | **default**: DATA_SET
  | **choices**: DATA_SET, USS, LOCAL, INLINE


     
input_src
  The path to the source file that contains the DFHCSDUP script to submit.

  It can be a data set. For example: "TESTER.DEFS.SCRIPT" or "TESTER.DEFS(SCRIPT)"

  It can be a USS file. For example: "/u/tester/defs/script.csdup"

  It can be a local file. For example: "/User/tester/defs/script.csdup"


  | **required**: False
  | **type**: str


     
log
  Specify the recovery attribute for the CSD, overriding the CSD system initialization parameters.

  Specify NONE for a nonrecoverable CSD.

  Specify UNDO for a CSD that is limited to file backout only.

  Specify ALL for a CSD for which you want both forward recovery and file backout. If you specify :literal:`log=ALL`\ , you must also specify LOGSTREAMID to identify the 26-character name of the z/OS™ log stream to be used as the forward recovery log. The CICS collection does not support defining forward recovery log streams; you must follow the instructions in \ `Defining forward recovery log streams <https://www.ibm.com/docs/en/cics-ts/latest?topic=journaling-defining-forward-recovery-log-streams>`__.


  | **required**: False
  | **type**: str
  | **choices**: NONE, UNDO, ALL


     
logstream_id
  The 26-character name of the z/OS™ log stream to be used as the forward recovery log.

  This is required when you use :literal:`log=ALL`.


  | **required**: False
  | **type**: str


     
region_data_sets
  The location of the region data sets to be created by using a template, for example, :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`.


  | **required**: True
  | **type**: dict


     
  dfhcsd
    Overrides the templated location for the CSD.


    | **required**: False
    | **type**: dict


     
    dsn
      The data set name of the CSD to override the template.


      | **required**: False
      | **type**: str



     
  template
    The base location of the region data sets with a template.


    | **required**: False
    | **type**: str



     
space_primary
  The size of the primary space allocated to the CSD. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect only when the CSD is being created. If the CSD already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 4


     
space_secondary
  The size of the secondary space allocated to the CSD. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect only when the CSD is being created. If the CSD already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 1


     
space_type
  The unit portion of the CSD size. Note that this is just the unit; the value for the primary space is specified with :literal:`space\_primary` and the value for the secondary space is specified with :literal:`space\_secondary`.

  This option takes effect only when the CSD is being created. If the CSD already exists, the option has no effect.

  The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  | **required**: False
  | **type**: str
  | **default**: M
  | **choices**: M, K, REC, CYL, TRK


     
state
  The intended state for the CSD, which the module aims to achieve.

  Specify :literal:`absent` to remove the CSD entirely, if it already exists.

  Specify :literal:`initial` to create the CSD if it does not already exist, and initialize it by using DFHCSDUP.

  Specify :literal:`warm` to retain an existing CSD in its current state. The module verifies whether the specified data set exists and whether it contains any records. If both conditions are met, the module leaves the data set as is. If the data set does not exist or if it is empty, the operation fails.

  Specify :literal:`changed` to run a DFHCSDUP script to update an existing CSD.


  | **required**: True
  | **type**: str
  | **choices**: initial, absent, warm, changed


     
volumes
  The volume(s) where the data set is created. Use a string to define a singular volume or a list of strings for multiple volumes.


  | **required**: False
  | **type**: raw




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Initialize a CSD by using the templated location
     ibm.ibm_zos_cics.csd:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       state: "initial"

   - name: Initialize a user specified CSD
     ibm.ibm_zos_cics.csd:
       region_data_sets:
         dfhcsd:
           dsn: "REGIONS.ABCD0001.DFHCSD"
       cics_data_sets:
         sdfhload: "CICSTS61.CICS.SDFHLOAD"
       state: "initial"

   - name: Initialize a large CSD by using the templated location
     ibm.ibm_zos_cics.csd:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       space_primary: 10
       space_type: "M"
       state: "initial"

   - name: Delete a CSD defined by the template
     ibm.ibm_zos_cics.csd:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       state: "absent"

   - name: Delete a user specified CSD
     ibm.ibm_zos_cics.csd:
       region_data_sets:
         dfhcsd:
           dsn: "REGIONS.ABCD0001.DFHCSD"
       cics_data_sets:
         sdfhload: "CICSTS61.CICS.SDFHLOAD"
       state: "absent"

   - name: Retain the existing state of a CSD defined by the template
     ibm.ibm_zos_cics.csd:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       state: "warm"

   - name: Retain the existing state of a user specified CSD
     ibm.ibm_zos_cics.csd:
       region_data_sets:
         dfhcsd:
           dsn: "REGIONS.ABCD0001.DFHCSD"
       cics_data_sets:
         sdfhload: "CICSTS61.CICS.SDFHLOAD"
       state: "warm"

   - name: Run a DFHCSDUP script from a data set
     ibm.ibm_zos_cics.csd:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       state: "changed"
       input_location: "DATA_SET"
       input_src: "TESTER.DEFS.SCRIPT"

   - name: Run a DFHCSDUP script from a USS file
     ibm.ibm_zos_cics.csd:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       input_location: "USS"
       input_src: "/u/tester/defs/script.csdup"

   - name: Run a DFHCSDUP script from a local file
     ibm.ibm_zos_cics.csd:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       input_location: "LOCAL"
       input_src: "/User/tester/defs/script.csdup"

   - name: Run a DFHCSDUP script inline
     ibm.ibm_zos_cics.csd:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       input_location: "INLINE"
       input_content: |
         DEFINE PROGRAM(TESTPRG1) GROUP(TESTGRP1)
         DEFINE PROGRAM(TESTPRG2) GROUP(TESTGRP2)









Return Values
-------------


   
                              
       changed
        | True if the state was changed, otherwise False.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       failed
        | True if the Ansible task failed, otherwise False.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       start_state
        | The state of the CSD before the Ansible task runs.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the start of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
      
                              
        exists
          | True if the CSD exists.
      
          | **returned**: always
          | **type**: bool
      
        
      
      
                              
       end_state
        | The state of the CSD at the end of the Ansible task.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the end of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
      
                              
        exists
          | True if the CSD exists.
      
          | **returned**: always
          | **type**: bool
      
        
      
      
                              
       executions
        | A list of program executions performed during the Ansible task.
      
        | **returned**: always
        | **type**: list
              
   
                              
        name
          | A human-readable name for the program execution.
      
          | **returned**: always
          | **type**: str
      
      
                              
        rc
          | The return code for the program execution.
      
          | **returned**: always
          | **type**: int
      
      
                              
        stdout
          | The standard output stream returned from the program execution.
      
          | **returned**: always
          | **type**: str
      
      
                              
        stderr
          | The standard error stream returned from the program execution.
      
          | **returned**: always
          | **type**: str
      
        
      
      
                              
       msg
        | A string containing an error message if applicable
      
        | **returned**: always
        | **type**: str
      
        

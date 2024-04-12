.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/main/plugins/modules/local_catalog.py

.. _local_catalog_module:


local_catalog -- Create, remove, and manage the CICS local catalog
==================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create, remove, and manage the \ `local catalog <https://www.ibm.com/docs/en/cics-ts/latest?topic=catalogs-local-catalog>`__\  data set used by a CICS® region. CICS domains use the local catalog to save some of their information between CICS runs and to preserve this information across a cold start.
- You can use this module when provisioning or de-provisioning a CICS region, or when managing the state of the local catalog during upgrades or restarts.
- Use the \ :literal:`state`\  option to specify the intended state for the local catalog. For example, \ :literal:`state=initial`\  will create and initialize a local catalog data set if it doesn't yet exist, or it will take an existing local catalog and empty it of all records.





Parameters
----------


     
cics_data_sets
  The name of the \ :literal:`SDFHLOAD`\  library of the CICS installation, for example, \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .

  This module uses the \ :literal:`DFHCCUTL`\  utility internally, which is found in the \ :literal:`SDFHLOAD`\  library.


  | **required**: True
  | **type**: dict


     
  sdfhload
    The location of the  \ :literal:`SDFHLOAD`\  library to override the template.


    | **required**: False
    | **type**: str


     
  template
    The templated location of the \ :literal:`SDFHLOAD`\  library.


    | **required**: False
    | **type**: str



     
region_data_sets
  The location of the region data sets to be created using a template, for example, \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ .

  If you want to use a data set that already exists, ensure that the data set is a local catalog data set.


  | **required**: True
  | **type**: dict


     
  dfhlcd
    Overrides the templated location for the local catalog data set.


    | **required**: False
    | **type**: dict


     
    dsn
      The data set name of the local catalog to override the template.


      | **required**: False
      | **type**: str



     
  template
    The base location of the region data sets with a template.


    | **required**: False
    | **type**: str



     
space_primary
  The size of the primary space allocated to the local catalog data set. Note that this is just the value; the unit is specified with \ :literal:`space\_type`\ .

  This option takes effect only when the local catalog is being created. If the local catalog already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 200


     
space_secondary
  The size of the secondary space allocated to the local catalog data set. Note that this is just the value; the unit is specified with \ :literal:`space\_type`\ .

  This option takes effect only when the local catalog is being created. If the local catalog already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 5


     
space_type
  The unit portion of the local catalog data set size. Note that this is just the unit; the value is specified with \ :literal:`space\_primary`\ .

  This option takes effect only when the local catalog is being created. If the local catalog already exists, the option has no effect.

  The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  | **required**: False
  | **type**: str
  | **default**: REC
  | **choices**: M, K, REC, CYL, TRK


     
state
  The intended state for the local catalog, which the module will aim to achieve.

  \ :literal:`absent`\  will remove the local catalog data set entirely, if it already exists.

  \ :literal:`initial`\  will create the local catalog data set if it does not already exist, and empty it of all existing records.

  \ :literal:`warm`\  will retain an existing local catalog in its current state.


  | **required**: True
  | **type**: str
  | **choices**: initial, absent, warm




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






See Also
--------

.. seealso::

   - :ref:`global_catalog_module`



Return Values
-------------


   
                              
       changed
        | True if the state was changed, otherwise False.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       failed
        | True if the query job failed, otherwise False.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       start_state
        | The state of the local catalog before the Ansible task runs.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the start of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
      
                              
        exists
          | True if the local catalog data set exists.
      
          | **returned**: always
          | **type**: bool
      
        
      
      
                              
       end_state
        | The state of the local catalog at the end of the Ansible task.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the end of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
      
                              
        exists
          | True if the local catalog data set exists.
      
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
          | The standard out stream returned by the program execution.
      
          | **returned**: always
          | **type**: str
      
      
                              
        stderr
          | The standard error stream returned from the program execution.
      
          | **returned**: always
          | **type**: str
      
        
      
        

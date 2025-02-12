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
- Create, remove, and manage the \ `local catalog <https://www.ibm.com/docs/en/cics-ts/latest?topic=catalogs-local-catalog>`__ data set used by a CICS® region. CICS domains use the local catalog to save some of their information between CICS runs and to preserve this information across a cold start.
- You can use this module when provisioning or de-provisioning a CICS region, or when managing the state of the local catalog during upgrades or restarts.
- Use the :literal:`state` option to specify the intended state for the local catalog. For example, use :literal:`state=initial` to create and initialize a local catalog data set if it doesn't exist, or empty an existing local catalog of all records.





Parameters
----------


     
cics_data_sets
  The name of the :literal:`SDFHLOAD` library of the CICS installation, for example, :literal:`CICSTS61.CICS.SDFHLOAD`.

  This module uses the :literal:`DFHCCUTL` utility internally, which is found in the :literal:`SDFHLOAD` library.


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



     
region_data_sets
  The location of the region data sets to be created by using a template, for example, :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`.

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
  The size of the primary space allocated to the local catalog data set. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect only when the local catalog data set is being created. If the local catalog data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 200


     
space_secondary
  The size of the secondary space allocated to the local catalog data set. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect only when the local catalog data set is being created. If the local catalog data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 5


     
space_type
  The unit portion of the local catalog data set size. Note that this is just the unit; the value for the primary space is specified with :literal:`space\_primary` and the value for the secondary space is specified with :literal:`space\_secondary`.

  This option takes effect only when the local catalog data set is being created. If the local catalog data set already exists, the option has no effect.

  The size can be specified in megabytes (\ :literal:`m`\ ), kilobytes (\ :literal:`k`\ ), records (\ :literal:`rec`\ ), cylinders (\ :literal:`cyl`\ ), or tracks (\ :literal:`trk`\ ).


  | **required**: False
  | **type**: str
  | **default**: rec
  | **choices**: m, k, rec, cyl, trk


     
state
  The intended state for the local catalog, which the module aims to achieve.

  Specify :literal:`absent` to remove the local catalog data set entirely, if it already exists.

  Specify :literal:`initial` to create the local catalog data set if it does not exist, or empty this existing local catalog of all records.

  Specify :literal:`warm` to retain an existing local catalog in its current state. The module verifies whether the specified data set exists and whether it contains any records. If both conditions are met, the module leaves the data set as is. If the data set does not exist or if it is empty, the operation fails.


  | **required**: True
  | **type**: str
  | **choices**: initial, absent, warm


     
volumes
  The volume(s) where the data set is created. Use a string to define a singular volume or a list of strings for multiple volumes.


  | **required**: False
  | **type**: raw




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Initialize a local catalog data set by using the templated location
     ibm.ibm_zos_cics.local_catalog:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       state: "initial"

   - name: Initialize a user specified local catalog data set
     ibm.ibm_zos_cics.local_catalog:
       region_data_sets:
         dfhlcd:
           dsn: "REGIONS.ABCD0001.DFHLCD"
       cics_data_sets:
         sdfhload: "CICSTS61.CICS.SDFHLOAD"
       state: "initial"

   - name: Initialize a large catalog data set by using the templated location
     ibm.ibm_zos_cics.local_catalog:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       space_primary: 500
       space_type: "rec"
       state: "initial"

   - name: Retain the existing local catalog defined by the template
     ibm.ibm_zos_cics.local_catalog:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       state: "warm"

   - name: Retain a user specified local catalog in its current state
     ibm.ibm_zos_cics.local_catalog:
       region_data_sets:
         dfhlcd:
           dsn: "REGIONS.ABCD0001.DFHLCD"
       cics_data_sets:
         sdfhload: "CICSTS61.CICS.SDFHLOAD"
       state: "warm"

   - name: Delete a local catalog data set defined by the template
     ibm.ibm_zos_cics.local_catalog:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       state: "absent"

   - name: Delete a user specified local catalog data set
     ibm.ibm_zos_cics.local_catalog:
       region_data_sets:
         dfhlcd:
           dsn: "REGIONS.ABCD0001.DFHLCD"
       cics_data_sets:
         sdfhload: "CICSTS61.CICS.SDFHLOAD"
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
        | True if the Ansible task failed, otherwise False.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       start_state
        | The state of the local catalog data set before the Ansible task runs.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the start of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
      
                              
        exists
          | True if the specified local catalog data set exists.
      
          | **returned**: always
          | **type**: bool
      
        
      
      
                              
       end_state
        | The state of the local catalog data set at the end of the Ansible task.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        data_set_organization
          | The organization of the data set at the end of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
      
                              
        exists
          | True if the specified local catalog data set exists.
      
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
      
        

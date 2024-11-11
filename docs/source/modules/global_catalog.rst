.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/main/plugins/modules/global_catalog.py

.. _global_catalog_module:


global_catalog -- Create, remove, and manage the CICS global catalog
====================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create, remove, and manage the \ `global catalog <https://www.ibm.com/docs/en/cics-ts/latest?topic=catalogs-global-catalog>`__ data set used by a CICS® region. The global catalog is used to store start type information, location of the CICS system log, installed resource definitions, terminal control information and profiles. It contains information that CICS requires on a restart.
- You can use this module when provisioning or de-provisioning a CICS region, or when managing the state of the global catalog during upgrades or restarts.
- Use the :literal:`state` option to specify the intended state for the global catalog. For example, use :literal:`state=initial` to create and initialize a global catalog data set if it doesn't exist, or set the autostart override record of an existing global catalog to :literal:`AUTOINIT`. In either case, a CICS region that is using this global catalog and set with the :literal:`START=AUTO` system initialization parameter performs an initial start.





Parameters
----------


     
cics_data_sets
  The name of the :literal:`SDFHLOAD` library of the CICS installation, for example, :literal:`CICSTS61.CICS.SDFHLOAD`.

  This module uses the :literal:`DFHRMUTL` utility internally, which is found in the :literal:`SDFHLOAD` library.


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

  If you want to use a data set that already exists, ensure that the data set is a global catalog data set.


  | **required**: True
  | **type**: dict


     
  dfhgcd
    Overrides the templated location for the global catalog data set.


    | **required**: False
    | **type**: dict


     
    dsn
      The data set name of the global catalog to override the template.


      | **required**: False
      | **type**: str



     
  template
    The base location of the region data sets with a template.


    | **required**: False
    | **type**: str



     
space_primary
  The size of the primary space allocated to the global catalog data set. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect only when the global catalog data set is being created. If the global catalog data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 5


     
space_secondary
  The size of the secondary space allocated to the global catalog data set. Note that this is just the value; the unit is specified with :literal:`space\_type`.

  This option takes effect only when the global catalog data set is being created. If the global catalog data set already exists, the option has no effect.


  | **required**: False
  | **type**: int
  | **default**: 1


     
space_type
  The unit portion of the global catalog data set size. Note that this is just the unit; the value for the primary space is specified with :literal:`space\_primary` and the value for the secondary space is specified with :literal:`space\_secondary`.

  This option takes effect only when the global catalog data set is being created. If the global catalog data set already exists, the option has no effect.

  The size can be specified in megabytes (\ :literal:`M`\ ), kilobytes (\ :literal:`K`\ ), records (\ :literal:`REC`\ ), cylinders (\ :literal:`CYL`\ ), or tracks (\ :literal:`TRK`\ ).


  | **required**: False
  | **type**: str
  | **default**: M
  | **choices**: M, K, REC, CYL, TRK


     
state
  The intended state for the global catalog data set, which the module aims to achieve.

  Specify :literal:`absent` to remove the global catalog data set entirely, if it exists.

  Specify :literal:`initial` to set the autostart override record to :literal:`AUTOINIT`. If the specified global catalog data set does not already exist, the module creates the data set.

  Specify :literal:`cold` to set the autostart override record of an existing global catalog to :literal:`AUTOCOLD`. If the specified global catalog data set does not already exist, the operation fails.

  Specify :literal:`warm` to set the autostart override record of an existing global catalog to :literal:`AUTOASIS`\ , undoing any previous setting of :literal:`AUTOINIT` or :literal:`AUTOCOLD`. The module verifies whether the specified data set exists and whether it contains any records. If either condition is not met, the operation fails.


  | **required**: True
  | **type**: str
  | **choices**: absent, initial, cold, warm


     
volumes
  The volume(s) where the data set is created. Use a string to define a singular volume or a list of strings for multiple volumes.


  | **required**: False
  | **type**: raw




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Initialize a global catalog by using the templated location
     ibm.ibm_zos_cics.global_catalog:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       state: "initial"

   - name: Initialize a large global catalog by using the templated location
     ibm.ibm_zos_cics.global_catalog:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       space_primary: 100
       space_type: "M"
       state: "initial"

   - name: Initialize a large user specified global catalog
     ibm.ibm_zos_cics.global_catalog:
       region_data_sets:
         dfhgcd:
           dsn: "REGIONS.ABCD0001.DFHGCD"
       cics_data_sets:
         sdfhload: "CICSTS61.CICS.SDFHLOAD"
       space_primary: 100
       space_type: "M"
       state: "initial"

   - name: Set the autostart override record to AUTOASIS for a global catalog defined by the template
     ibm.ibm_zos_cics.global_catalog:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       state: "warm"

   - name: Set the autostart override record to AUTOASIS for a user specified global catalog
     ibm.ibm_zos_cics.global_catalog:
       region_data_sets:
         dfhgcd:
           dsn: "REGIONS.ABCD0001.DFHGCD"
       cics_data_sets:
         sdfhload: "CICSTS61.CICS.SDFHLOAD"
       state: "warm"

   - name: Set the autostart override record to AUTOCOLD for a global catalog defined by the template
     ibm.ibm_zos_cics.global_catalog:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       state: "cold"

   - name: Set the autostart override record to AUTOCOLD for a user specified global catalog
     ibm.ibm_zos_cics.global_catalog:
       region_data_sets:
         dfhgcd:
           dsn: "REGIONS.ABCD0001.DFHGCD"
       cics_data_sets:
         sdfhload: "CICSTS61.CICS.SDFHLOAD"
       state: "cold"

   - name: Delete a global catalog defined by the template
     ibm.ibm_zos_cics.global_catalog:
       region_data_sets:
         template: "REGIONS.ABCD0001.<< data_set_name >>"
       cics_data_sets:
         template: "CICSTS61.CICS.<< lib_name >>"
       state: "absent"

   - name: Delete a user specified global catalog
     ibm.ibm_zos_cics.global_catalog:
       region_data_sets:
         dfhgcd:
           dsn: "REGIONS.ABCD0001.DFHGCD"
       cics_data_sets:
         sdfhload: "CICSTS61.CICS.SDFHLOAD"
       state: "absent"






See Also
--------

.. seealso::

   - :ref:`local_catalog_module`



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
        | The state of the global catalog before the Ansible task runs.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        autostart_override
          | The current autostart override record.
      
          | **returned**: always
          | **type**: str
      
      
                              
        next_start
          | The next start type listed in the global catalog.
      
          | **returned**: always
          | **type**: str
      
      
                              
        exists
          | True if the specified global catalog data set exists.
      
          | **returned**: always
          | **type**: bool
      
      
                              
        data_set_organization
          | The organization of the data set at the start of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
        
      
      
                              
       end_state
        | The state of the global catalog at the end of the Ansible task.
      
        | **returned**: always
        | **type**: dict
              
   
                              
        autostart_override
          | The current autostart override record.
      
          | **returned**: always
          | **type**: str
      
      
                              
        next_start
          | The next start type listed in the global catalog
      
          | **returned**: always
          | **type**: str
      
      
                              
        exists
          | True if the specified global catalog data set exists.
      
          | **returned**: always
          | **type**: bool
      
      
                              
        data_set_organization
          | The organization of the data set at the end of the Ansible task.
      
          | **returned**: always
          | **type**: str
          | **sample**: VSAM

            
      
        
      
      
                              
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
      
        

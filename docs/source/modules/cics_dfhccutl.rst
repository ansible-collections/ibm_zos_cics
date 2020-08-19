
:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/dev/plugins/modules/cics_dfhccutl.py

.. _cics_dfhccutl_module:


cics_dfhccutl -- Initialize CICS local catalog
==============================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module initializes the CICS local catalog by invoking the DFHCCUTL program.





Parameters
----------


     
dfhlcd
  Specifies the input local catalog data set.


  | **required**: True
  | **type**: str


     
steplib
  Specifies a partioned data set containing DFHCCUTL.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
     - name: Initialize the LCD
       cics_local_catalog_initialization:
         steplib: CTS550.CICS720.SDFHLOAD
         dfhlcd: BJMAXY.CICS.IYK3ZMX7.DFHLCD









Return Values
-------------


   
                              
       msg
        | The execution result message.
      
        | **returned**: always
        | **type**: str
        | **sample**: The DFHCCUTL program executed successfully.

            
      
      
                              
       rc
        | The return code.
      
        | **returned**: always
        | **type**: str
      
      
                              
       content
        | The output data set containing results, information and error/dump messages.
      
        | **returned**: always
        | **type**: str
      
      
                              
       changed
        | Indicates if any changes were made during the operation.
      
        | **returned**: always
        | **type**: bool
      
        

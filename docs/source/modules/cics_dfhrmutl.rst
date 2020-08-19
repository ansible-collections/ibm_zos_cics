
:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/dev/plugins/modules/cics_dfhrmutl.py

.. _cics_dfhrmutl_module:


cics_dfhrmutl -- CICS recovery manager utility program
======================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This module runs the recovery manager utility program to:
- Examine the setting of the autostart override record on the global catalog.
- Set or reset the recovery manager autostart override record on the global catalog.
- Copy that part of the catalog needed for a cold start to a new global catalog. If a new catalog is built using DFHRMUTL, CICS is able to perform only a cold start or an initial start with the new catalog. The performance of these starts will, however, be better than that of a cold or initial start with a full catalog.





Parameters
----------


     
cold_copy
  Makes a reduced copy of an existing CICS global catalog (DFHGCD) in a cleared CICS global catalog (NEWGCD).

  It creates in NEWGCD a copy of only those records from DFHGCD that CICS needs to perform a cold start, and updates NEWGCD with the autostart override record specified by the ``set_auto_start`` parameter.

  All changes caused by ``set_auto_start`` are made to the NEWGCD data set, and DFHGCD is not changed.

  ``cold_play`` is incompatible with the AUTOASIS and AUTODIAG options of ``set_auto_start``. If ``cold_play`` and either of these values of ``set_auto_start`` are specified, an error is returned.


  | **required**: false
  | **type**: list


     
  newgcd
    Specifies the output global catalog (NEWGCD) data set that is to receive the copy.

    This option is required if the ``cold_copy`` parameter is specified.

    If ``cold_copy`` is specified, the NEWGCD data set is first cleared and then has DFHGCD records and an override record added to it. It must have been defined with the VSAM REUSE attribute.


    | **required**: false
    | **type**: str



     
dfhgcd
  Specifies the input global catalog data set (DFHGCD) from which is the copy is extracted.

  If the ``cold_copy`` parameter is specified, DFHGCD is read-only.

  In other cases, it can be updated.


  | **required**: True
  | **type**: str


     
set_auto_start
  The type of the next startup.

  If ``set_auto_start`` is not specified, the module will examine the value of current dfhgcd set_auto_start. The following values are available:

  AUTOASIS: performs the default startup, either warm or emergency.

  AUTOCOLD: performs a cold start.

  AUTODIAG: performs a diagnostic run.

  AUTOINIT: performs an initial start.


  | **required**: false
  | **type**: str
  | **choices**: AUTOASIS, AUTOCOLD, AUTODIAG, AUTOINIT, None


     
steplib
  Defines a partioned data set containing DFHRMUTL.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
     - name: Examining the override record
       cics_dfhrmutl:
         steplib: CTS550.CICS720.SDFHLOAD
         dfhgcd: BJMAXY.CICS.IYK3ZMX7.DFHGCD

     - name: set auto start to autoinit to the dfhgcd. Setting an initial start without operator intervention
       cics_dfhrmutl:
         steplib: CTS550.CICS720.SDFHLOAD
         dfhgcd: BJMAXY.CICS.IYK3ZMX7.DFHGCD
         set_auto_start: AUTOINIT

     - name: setting the global catalog for a cold start. COLD_COPY is used to improve performance.
       cics_dfhrmutl:
         steplib: CTS550.CICS720.SDFHLOAD
         dfhgcd: BJMAXY.CICS.IYK3ZMX7.DFHGCD
         set_auto_start: AUTOCOLD
         cold_copy:
           - newgcd: BJMAXY.CICS.IYK3ZMX7.NEWGCD









Return Values
-------------


   
                              
       msg
        | The execution result message.
      
        | **returned**: always
        | **type**: str
        | **sample**: The DFHRMUTL program executed successfully.

            
      
      
                              
       rc
        | The return code.
      
        | **returned**: always
        | **type**: str
      
      
                              
       content
        | The output data set containing results, information and error messages.
      
        | **returned**: always
        | **type**: str
      
      
                              
       changed
        | Indicates if any changes were made during the operation.
      
        | **returned**: always
        | **type**: bool
      
        

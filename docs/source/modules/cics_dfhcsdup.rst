
:github_url: https://github.com/ansible-collections/ibm_zos_core/blob/dev/plugins/modules/cics_dfhcsdup.py

.. _cics_dfhcsdup_module:


cics_dfhcsdup -- Run CICS system definition utility program DFHCSDUP
====================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The module runs the CICS system definition (CSD) utility program DFHCSDUP to read from and write to a CSD file.
- It manages CICS resource definitions using commands supplied as part of DFHCSDUP.
- All the commands supplied by DFHCSDUP can be invoked through this module, such as ADD, ALTER, COPY, DEFINE, DELETE, EXTRACT, and so on. Refer to CICS Resource Definition Guide for command usage.





Parameters
----------


     
cmd_dsn
  Specifies the file where the command statements are stored.

  Required if the ``cmd_stmt`` parameter is not specified.


  | **required**: False
  | **type**: str


     
cmd_stmt
  Specifies the command statements to be invoked through the utility.

  Required if the ``cmd_file`` parameter is not specified.


  | **required**: False
  | **type**: list


     
  command_type
    Specifies the command to be executed.


    | **required**: False
    | **type**: dict


     
    attr_list
      The resource attributes.


      | **required**: False
      | **type**: dict


     
    group_name
      The group name.


      | **required**: False
      | **type**: str


     
    list_name
      The list name.


      | **required**: False
      | **type**: str


     
    resource_name
      The resource name.


      | **required**: False
      | **type**: str


     
    resource_type
      The resource type.


      | **required**: False
      | **type**: str




     
cmd_str
  Specifies the file where the command statements are stored.

  Required if the ``cmd_stmt`` parameter is not specified.


  | **required**: False
  | **type**: list


     
dfhcsd
  Specifies the CSD file that you want to read from or write to.


  | **required**: True
  | **type**: str


     
parms
  The program arguments, for example, ``-a='UPPERCASE'``.


  | **required**: False
  | **type**: dict


     
  access_mode
    Specifies the access you need to the CSD file. It can be read and write (``rw``) or read-only (``ro``) access.


    | **required**: False
    | **type**: str
    | **default**: rw
    | **choices**: rw, ro


     
  compat
    Specifies whether the DFHCSDUP utility program is to run in compatibility mode.


    | **required**: False
    | **type**: bool


     
  page_size
    Specifies the number of lines per page on the output listing.

    The value ranges from 4 to 9999.


    | **required**: False
    | **type**: int
    | **default**: 60


     
  uppercase
    Formats the output from DFHCSDUP in uppercase.


    | **required**: False
    | **type**: bool



     
seccsd
  Specifies the CSD file that you want to read from or write to.

  Required if the FROMCSD parameter is specified on an APPEND, COPY, or SERVICE command.


  | **required**: False
  | **type**: str


     
steplib
  Specifies the library where the utility is stored.


  | **required**: True
  | **type**: str


     
userprog_dd
  Specifies the dd names used by the user program.

  Required if you specify the EXTRACT command and want to conduct some customized operation.


  | **required**: False
  | **type**: str


     
userprog_ds
  Specifies the input data set that is used by the user program.

  Required if you specify the EXTRACT command and need to do some customized operation.


  | **required**: False
  | **type**: str


     
userprog_lib
  Specifies the library where the utility is stored.

  Required if you specify the EXTRACT command and need to do some customized operation.


  | **required**: False
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
     - name: Test case for cics_dfhcsdup
       cics_dfhcsdup:
         steplib: CTS540.CICS710.SDFHLOAD
         dfhcsd: XXXXXX.ATEST.DFHCSD
         cmd_stmt:
           - add:
               list_name: LST01
               group_name: GRP01









Return Values
-------------


   
                              
       ret_code
        | The return code.
      
        | **returned**: always
        | **type**: int
      
      
                              
       csd
        | The CSD data set used.
      
        | **returned**: always
        | **type**: str
        | **sample**: XXXXXXX.TEST.DFHCSD

            
      
      
                              
       cmds
        | The CSD commands or command data set name.
      
        | **returned**: always
        | **type**: str
        | **sample**: ['ADD GROUP(GRP01) LIST(LST01)']

            
      
      
                              
       content
        | Provides additional information related to the resource definition for error debugging.
      
        | **returned**: if error
        | **type**: str
        | **sample**: XXXXXX.TEST.MSGPS

            
      
      
                              
       changed
        | Indicates if any changes were made during the operation.
      
        | **returned**: always
        | **type**: bool
      
        

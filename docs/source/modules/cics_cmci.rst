
:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/dev/plugins/modules/cics_cmci.py

.. _cics_cmci_module:


cics_cmci -- Manage CICS and CICSPlex SM resources
==================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The cics_cmci module can be used to manage installed and definitional CICS and CICSPlex® SM resources in CICS regions.





Parameters
----------


     
cmci_cert
  Location of the PEM-formatted certificate chain file to be used for HTTPS client authentication.

  Required when security type is certificate.


  | **required**: False
  | **type**: str


     
cmci_host
  The TCP/IP host name of CMCI connection.


  | **required**: True
  | **type**: str


     
cmci_key
  Location of the PEM-formatted file with your private key to be used for HTTPS client authentication.

  Required when security type is certificate.


  | **required**: False
  | **type**: str


     
cmci_password
  The password of ``cmci_user`` to pass to the basic authentication.


  | **required**: false
  | **type**: str


     
cmci_port
  The port number of CMCI connection.


  | **required**: True
  | **type**: str


     
cmci_user
  The user ID to run the CMCI request with.

  Required when security type is yes.


  | **required**: false
  | **type**: str


     
context
  If CMCI is installed in a CICSPlex SM environment, ``context`` is the name of the CICSplex or CMAS associated with the request; for example, PLEX1. See the relevant resource table in CICSPlex SM resource tables to determine whether to specify a CICSplex or CMAS.

  If CMCI is installed as a single server, ``context`` is the application ID of the CICS region associated with the request.

  The value of ``context`` must not contain spaces. ``context`` is not case-sensitive.


  | **required**: false
  | **type**: str


     
filter
  Refines the scope and nature of the request. The constituent parts of the query section can occur in any order, but each can occur only once in a URI.

  Although query parameter values are not case-sensitive, certain attribute values must have correct capitalization because some attributes such as TRANID and DESC can hold mixed-case values.

  The filter can work with options ``query``, ``update``, ``delete``; otherwise it will be ignored.


  | **required**: false
  | **type**: list


     
  criteria
    A string containing logical expressions that filters the data returned on the request.

    The string on the ``criteria`` parameter follows the same rule as the filter expression in the CICSPlex SM application programming interface (API).

    For more guidance about specifying filter expressions using the CICSPlex SM API, see (https://www.ibm.com/support/knowledgecenter /SSGMCP_5.4.0/system-programming/cpsm/eyup1a0.html).


    | **required**: False
    | **type**: str


     
  parameter
    A string of one or more parameters and values in the form of `parameter_name(data_value)` that refines the request. The rule for specifying these parameters is the same as in the CICSPlex SM API.

    For more guidance about specifying parameter expressions using the CICSPlex SM API, see (https://www.ibm.com/support/knowledgecenter /SSGMCP_5.4.0/system-programming/cpsm/eyup1bg.html)


    | **required**: False
    | **type**: str



     
option
  The definition or operation you want to perform with your CICS or CPSM resources.


  | **required**: false
  | **type**: str
  | **default**: query
  | **choices**: define, delete, update, install, query


     
record_count
  Only works with the ``query`` option; otherwise it will be ignored.

  Identifies a subset of records in the results cache, starting from the first record in the results cache or from the record specified by the index parameter.

  A negative number indicates a count back from the last record; for example, -1 means the last record, -2 the last record but one, and so on.

  ``record_count`` must be an integer, a value of zero is not permitted.


  | **required**: False
  | **type**: int


     
resource
  The resource that you want to define or operate with.


  | **required**: True
  | **type**: list


     
  attributes
    The resource attributes. For available attributes, see CICSPlex SM resource tables in IBM Knowledge Center for CICS.


    | **required**: False
    | **type**: list


     
  location
    The location where the resource was installed.

    This variable only works with the ``install`` option.


    | **required**: False
    | **type**: str
    | **choices**: BAS, CSD


     
  parameters
    The resource parameters. For availabled parameters, see CICSPlex SM resource tables in IBM Knowledge Center for CICS.


    | **required**: False
    | **type**: list


     
  type
    The resource type.


    | **required**: True
    | **type**: str



     
scope
  Specifies the name of a CICSplex, CICS group, CICS region, or logical scope associated with the query.

  ``scope`` is a subset of ``context`` and limits the request to particular CICS systems or resources.

  ``scope`` is not mandatory. When it is absent, the request is limited by the value of ``context`` alone.

  The value of ``scope`` must not contain spaces.

  ``scope`` is not case-sensitive.


  | **required**: false
  | **type**: str


     
security_type
  the authenticate type that the remote region requires.


  | **required**: True
  | **type**: str
  | **default**: none
  | **choices**: none, basic, certificate




Examples
--------

.. code-block:: yaml+jinja

   
   - name: get a localfile in a CICS region
     cics_cmci:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       cmci_user: 'ibmuser'
       cmci_password: '123456'
       context: 'iyk3z0r9'
       option: 'query'
       resource:
         - type: CICSLocalFile
       record_count: 2
       filter:
         - criteria: dsname=XIAOPIN* and file=DFH*

   - name: define a bundle in a CICS region
     cics_cmci:
         cmci_host: 'winmvs2c.hursley.ibm.com'
         cmci_port: '10080'
         context: 'iyk3z0r9'
         option: 'define'
         resource:
           - type: CICSDefinitionBundle
             attributes:
               - name: PONGALT
                 BUNDLEDIR: /u/ibmuser/bundle/pong/pongbundle_1.0.0
                 csdgroup: JVMGRP
             parameters:
               - name: CSD
         record_count: 1

   - name: install a bundle in a CICS region
     cics_cmci:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       context: 'iyk3z0r9'
       option: 'install'
       resource:
         - type: CICSDefinitionBundle
           location: CSD
       filter:
             - criteria: NAME=PONGALT
               parameter: CSDGROUP(JVMGRP)

   - name: update a bundle definition in a CICS region
     cics_cmci:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       context: 'iyk3z0r9'
       option: 'update'
       resource:
         - type: CICSDefinitionBundle
           attributes:
             - description: 'forget description'
           parameters:
             - name: CSD
       filter:
           - criteria: NAME=PONGALT
             parameter: CSDGROUP(JVMGRP)

   - name: install a bundle in a CICS region
     cics_cmci:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       context: 'iyk3z0r9'
       option: 'update'
       resource:
         - type: CICSBundle
           attributes:
             - Enablestatus: disabled
       filter:
           - criteria: NAME=PONGALT

   - name: delete a bundle in a CICS region
     cics_cmci:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       security_type: 'yes'
       context: 'iyk3z0r9'
       option: 'delete'
       resource:
         - type: CICSBundle
       filter:
         - criteria: NAME=PONGALT

   - name: delete a bundle definition in a CICS region
     cics_cmci:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       context: 'iyk3z0r9'
       option: 'delete'
       resource:
         - type: CICSDefinitionBundle
       filter:
         - criteria: NAME=PONGALT
           parameter: CSDGROUP(JVMGRP)

   - name: get a localfile in a CICS region
     cics_cmci:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       cmci_cert: './sec/ansible.pem'
       cmci_key: './sec/ansible.key'
       connection_type: 'certificate'
       context: 'iyk3z0r9'
       option: 'query'
       resource:
         - type: CICSLocalFile
       record_count: 1
       filter:
         - criteria:
             - dsname=XIAOPIN*
             - file=DFH*









Return Values
-------------


   
                              
       changed
        | True if the state was changed, otherwise False.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       failed
        | True if query_job failed, othewise False.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       url
        | The cmci url that was composed.
      
        | **returned**: always
        | **type**: str
      
      
                              
       api_response
        | Indicates whether the CMCI request was issued successfully or not.
      
        | **returned**: always
        | **type**: str
      
      
                              
       response
        | The response of the CMCI request.
      
        | **returned**: success
        | **type**: dict      
        | **sample**:

              .. code-block::

                       {"records": {"cicsdefinitionlibrary": {"_keydata": "D7D6D5C74040404000D1E5D4C7D9D74040", "changeagent": "CSDAPI", "changeagrel": "0710", "changetime": "2020-06-16T10:40:50.000000+00:00", "changeusrid": "CICSUSER", "createtime": "2020-06-16T10:40:50.000000+00:00", "critical": "NO", "csdgroup": "JVMGRP", "defver": "0", "desccodepage": "0", "description": "", "dsname01": "XIAOPIN.PONG.LOADLIB", "dsname02": "", "dsname03": "", "dsname04": "", "dsname05": "", "dsname06": "", "dsname07": "", "dsname08": "", "dsname09": "", "dsname10": "", "dsname11": "", "dsname12": "", "dsname13": "", "dsname14": "", "dsname15": "", "dsname16": "", "name": "PONG", "ranking": "50", "status": "ENABLED", "userdata1": "", "userdata2": "", "userdata3": ""}}, "resultsummary": {"api_response1": "1024", "api_response1_alt": "OK", "api_response2": "0", "api_response2_alt": "", "displayed_recordcount": "1", "recordcount": "1"}}
            
      
        

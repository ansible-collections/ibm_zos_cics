.. ...............................................................................
.. © Copyright IBM Corporation 2020                                              .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/dev/plugins/modules/cmci_get.py

.. _cmci_get_module:


cmci_get -- Query CICS and CICSplex SM resources
================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The cmci_get module can be used to get information about installed and definitional CICS and CICSPlex® SM resources from CICS regions, using the CMCI API.  The CMCI API is provided by CICSplex SM, or in SMSS regions.  For information about the CMCI API see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_overview.html. For information about how to compose GET requests, see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_get.html.





Parameters
----------


     
cmci_cert
  Location of the PEM-formatted certificate chain file to be used for HTTPS client authentication.

  Can also be specified using the environment variable CMCI_CERT.

  Required if *cmci_key* is specified.

  Authentication prioritises certificate authentication if *cmci_cert* and *cmci_key* are provided, then basic authentication if *cmci_user* and (cmci_password) are provided, and then unauthenticated if none is provided.


  | **required**: False
  | **type**: str


     
cmci_host
  The TCP/IP host name of CMCI connection.


  | **required**: True
  | **type**: str


     
cmci_key
  Location of the PEM-formatted file storing your private key to be used for HTTPS client authentication.

  Can also be specified using the environment variable CMCI_KEY.

  Required if *cmci_cert* is specified.

  Authentication prioritises certificate authentication if *cmci_cert* and *cmci_key* are provided, then basic authentication if *cmci_user* and (cmci_password) are provided, and then unauthenticated if none is provided.


  | **required**: False
  | **type**: str


     
cmci_password
  The password of *cmci_user* to pass HTTP basic authentication.

  Can also be specified using the environment variable CMCI_PASSWORD.

  Required if *cmci_user* is specified.

  Authentication prioritises certificate authentication if *cmci_cert* and *cmci_key* are provided, then basic authentication if *cmci_user* and (cmci_password) are provided, and then unauthenticated if none is provided.


  | **required**: false
  | **type**: str


     
cmci_port
  The port number of the CMCI connection.


  | **required**: True
  | **type**: int


     
cmci_user
  The user ID under which the CMCI request will run.

  Can also be specified using the environment variable CMCI_USER.

  Required if *cmci_password* is specified.

  Authentication prioritises certificate authentication if *cmci_cert* and *cmci_key* are provided, then basic authentication if *cmci_user* and (cmci_password) are provided, and then unauthenticated if none is provided.


  | **required**: false
  | **type**: str


     
context
  If CMCI is installed in a CICSPlex SM environment, *context* is the name of the CICSplex or CMAS associated with the request, for example, PLEX1. See the relevant CICSPlex SM resource table, for example, `PROGRAM resource table <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGRAMtab.html>`_, to determine whether to specify a CICSplex or CMAS.

  If CMCI is installed in a single region (SMSS), *context* is the APPLID of the CICS region associate with the request.

  The value of *context* must contain no spaces. *context* is not case-sensitive.


  | **required**: false
  | **type**: str


     
insecure
  When set to ``true``, disables SSL certificate trust chain verification when using HTTPS.


  | **required**: False
  | **type**: bool


     
parameters
  A list of one or more parameters with optional values used to identify the resources for this request. Eligible parameters for identifying the target resources can be found in the resource table reference for the  target resource type, as valid parameters for the GET operation in the "Valid CPSM operations" table.  For example, the valid parameters for identifying a PROGDEF resource are CICSSYS, CSDGROUP and RESGROUP, as found in the `PROGDEF resource table reference <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html>`_.



  | **required**: False
  | **type**: list


     
  name
    Parameter name available for the GET operation.


    | **required**: True
    | **type**: str


     
  value
    Parameter value if any.


    | **required**: False
    | **type**: str



     
record_count
  Identifies a subset of records in a results cache starting from the first record in the results cache or from the record specified by the index parameter.

  A negative number indicates a count back from the last record; for example, -1 means the last record, -2 the last record but one, and so on

  Count must be an integer, a value of zero is not permitted.


  | **required**: False
  | **type**: int


     
resources
  Options that specify a target resource.


  | **required**: False
  | **type**: dict


     
  complex_filter
    A string containing logical expressions that filter the resource table records in the data returned on the request.

    Can contain one or more filters. Multiple filters must be combined using ``and`` or ``or`` logical operators.

    Filters can be nested. At most four nesting layers are allowed.


    | **required**: False
    | **type**: str


     
    attribute
      The resource table attributes to be filtered.

      For supported attributes of different resource types, see their resource table reference, for example, `PROGDEF resource table reference <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html>`_.


      | **required**: False
      | **type**: str


     
    operator
      These operators are accepted: ``<`` or ``LT`` (less than), ``<=`` or ``LE`` (less than or equal to), ``=`` or ``EQ`` (equal to), ``>`` or ``GT`` (greater than), ``>=`` or ``GE`` (greater than or equal to), ``==`` or ``IS`` (is), ``¬=``, ``!=``, or ``NE`` (not equal to). 



      | **required**: False
      | **type**: str
      | **default**: EQ
      | **choices**: <, >, <=, >=, =, ==, !=, ¬=, EQ, GT, GE, LT, LE, NE, IS


     
    value
      The value by which you are to filter the resource attributes.

      The value must be a valid one for the resource table attribute as documented in the resource table reference, for example, `PROGDEF resource table reference <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html>`_.


      | **required**: False
      | **type**: str



     
  filter
    A string containing basic logical expressions that filter the resource table records in the data returned on the request.

    Supports only the equal logic when filtering attribute values.

    Can contain one or more filters.

    For supported attributes of different resource types, see their resource table reference, for example, `PROGDEF resource table reference <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html>`_.


    | **required**: False
    | **type**: str



     
scheme
  The HTTP scheme to use when establishing a connection to the CMCI REST API.


  | **required**: false
  | **type**: str
  | **default**: https
  | **choices**: http, https


     
scope
  Specifies the name of a CICSplex, CICS region group, CICS region, or logical scope that is associated with the query.

  *scope* is a subset of *context* and limits the request to particular CICS systems or resources.

  *scope* is optional. If it's not specified, the request is limited by the value of *context* alone.

  The value of *scope* must contain no spaces. *scope* is not case-sensitive.


  | **required**: false
  | **type**: str


     
type
  The CMCI external resource name that maps to the target CICS or CICSPlex SM resource type. For a list of CMCI external resource names, see `CMCI resource names <https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_resources.html>`_.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: get 2 LOCFILEs from a CICSplex
     cmci_get:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       cmci_user: 'ibmuser'
       cmci_password: '123456'
       context: 'iyk3z0r9'
       type:  CICSLocalFile
       record_count: 2
       resource:
         filter:
           dsname: 'CTS*'

   - name: get a localfile in a CICS region
     cmci_get:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       cmci_cert: './sec/ansible.pem'
       cmci_key: './sec/ansible.key'
       context: 'iyk3z0r9'
       type: 'CICSLocalFile' 
       resource:
         filter:
           dsname: 'XIAOPIN*'
           file: 'DFH*'
       record_count: 1

   - name: get a progdef from a CSD
     cmci_get:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       cmci_cert: './sec/ansible.pem'
       cmci_key: './sec/ansible.key'
       context: 'iyk3z0r9'
       type: cicsdefinitionprogram 
       resource:
         filter:
           name: MYPROG
         parameters:
           - name: csdgroup
             value: MYGRP
       record_count: 1









Return Values
-------------


   
                              
       changed
        | True if the state was changed, otherwise False
      
        | **returned**: always
        | **type**: bool
      
      
                              
       failed
        | True if query_job failed, othewise False
      
        | **returned**: always
        | **type**: bool
      
      
                              
       connect_version
        | Version of the CMCI API
      
        | **returned**: success
        | **type**: str
      
      
                              
       cpsm_reason
        | Character value of the CPSM API reason code returned.  For a list of reason values provided by each API command, see U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kr.html)
      
        | **returned**: success
        | **type**: str
      
      
                              
       cpsm_reason_code
        | Numeric value of the CPSM API reason code returned.  For a list of numeric values see U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2ks.html)
      
        | **returned**: success
        | **type**: int
      
      
                              
       cpsm_response
        | Character value of the CPSM API response code returned.  For a list of response values provided by each API command, see U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kr.html)
      
        | **returned**: success
        | **type**: str
      
      
                              
       cpsm_response_code
        | Numeric value of the CPSM API response code returned.  For a list of numeric values see U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2ks.html)
      
        | **returned**: success
        | **type**: str
      
      
                              
       http_status
        | Message associated with HTTP status code returned by CMCI
      
        | **returned**: success
        | **type**: str
      
      
                              
       http_status_code
        | HTTP status code returned by CMCI
      
        | **returned**: success
        | **type**: int
      
      
                              
       record_count
        | Number of records returned
      
        | **returned**: success
        | **type**: int
      
      
                              
       records
        | A list of the returned records
      
        | **returned**: success
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"_keydata": "C1D5E2C9E3C5E2E3", "aloadtime": "00:00:00.000000", "apist": "CICSAPI", "application": "", "applmajorver": "-1", "applmicrover": "-1", "applminorver": "-1", "basdefinever": "0", "cedfstatus": "CEDF", "changeagent": "CSDAPI", "changeagrel": "0730", "changetime": "2020-12-15T02:34:31.000000+00:00", "changeusrid": "YQCHEN", "coboltype": "NOTAPPLIC", "concurrency": "QUASIRENT", "copy": "NOTREQUIRED", "currentloc": "NOCOPY", "datalocation": "ANY", "definesource": "ANSITEST", "definetime": "2020-12-15T02:34:29.000000+00:00", "dynamstatus": "NOTDYNAMIC", "entrypoint": "FF000000", "execkey": "USEREXECKEY", "executionset": "FULLAPI", "eyu_cicsname": "IYCWEMW2", "eyu_cicsrel": "E730", "eyu_reserved": "0", "fetchcnt": "0", "fetchtime": "00:00:00.000000", "holdstatus": "NOTAPPLIC", "installagent": "CSDAPI", "installtime": "2020-12-15T02:34:33.000000+00:00", "installusrid": "YQCHEN", "jvmclass": "", "jvmserver": "", "language": "NOTDEFINED", "length": "0", "library": "", "librarydsn": "", "loadpoint": "FF000000", "lpastat": "NOTAPPLIC", "newcopycnt": "0", "operation": "", "pgrjusecount": "0", "platform": "", "program": "ANSITEST", "progtype": "PROGRAM", "remotename": "", "remotesystem": "", "removecnt": "0", "rescount": "0", "residency": "NONRESIDENT", "rloading": "0.000", "rplid": "0", "rremoval": "0.000", "runtime": "UNKNOWN", "ruse": "0.000", "sharestatus": "PRIVATE", "status": "DISABLED", "transid": "", "useagelstat": "0", "usecount": "0", "usefetch": "0.000"}]
            
      
      
                              
       request
        | Information about the request that was made to CMCI
      
        | **returned**: success
        | **type**: dict
              
   
                              
        body
          | The XML body sent with the request, if any
      
          | **returned**: success
          | **type**: str
      
      
                              
        method
          | The HTTP method used for the request
      
          | **returned**: success
          | **type**: str
      
      
                              
        url
          | The URL used for the request
      
          | **returned**: success
          | **type**: str
      
        
      
        

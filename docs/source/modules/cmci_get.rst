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

  Required when security_type is certificate.

  Can also be specified using the environment variable CMCI_CERT

  Required with cmci_key


  | **required**: False
  | **type**: str


     
cmci_host
  The TCP/IP host name of CMCI connection


  | **required**: True
  | **type**: str


     
cmci_key
  Location of the PEM-formatted file with your private key to be used for HTTPS client authentication.

  Required when security type is certificate.

  Can also be specified using the environment variable CMCI_KEY

  Required with cmci_cert


  | **required**: False
  | **type**: str


     
cmci_password
  The password of cmci_user to pass using HTTP basic authentication

  Can also be specified using the environment variable CMCI_PASSWORD

  Required with cmci_user


  | **required**: false
  | **type**: str


     
cmci_port
  The port number of the CMCI connection.


  | **required**: True
  | **type**: int


     
cmci_user
  The user id to run the CMCI request as

  Required when security type is yes

  Can also be specified using the environment variable CMCI_USER

  Required with cmci_password


  | **required**: false
  | **type**: str


     
context
  If CMCI is installed in a CICSPlex SM environment, context is the name of the CICSplex or CMAS associated with the request; for example, PLEX1. See the relevant resource table in CICSPlex SM resource tables to determine whether to specify a CICSplex or CMAS.

  If CMCI is installed as a single server (SMSS), context is the APPLID of the CICS region associated with the request.

  The value of context must not contain spaces. Context is not case-sensitive.


  | **required**: false
  | **type**: str


     
insecure
  Set to true to disable SSL certificate trust chain verification when using https


  | **required**: False
  | **type**: bool


     
parameters
  A list of one or more parameters with optional values used to identify the resources for this request. Eligible parameters for identifying resources can be found in the resource tables reference for the target resource type, for the GET operation. For example, the valid parameters for identifying a PROGDEF are CICSSYS, CSDGROUP and RESGROUP, as found in the resource tables reference https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html



  | **required**: False
  | **type**: list


     
  name
    Parameter name


    | **required**: True
    | **type**: str


     
  value
    Parameter value if any


    | **required**: False
    | **type**: str



     
record_count
  Identifies a subset of records in a results cache starting from the first record in the results cache or from the record specified by the index parameter.

  A negative number indicates a count back from the last record; for example, -1 means the last record, -2 the last record but one, and so on

  Count must be an integer, a value of zero is not permitted.


  | **required**: False
  | **type**: int


     
resources
  Options which specify a target resource


  | **required**: False
  | **type**: dict


     
  criteria
    A string containing logical expressions that filters the data returned on the request.

    The string that makes up the value of the CRITERIA parameter follows the same rules as the filter expressions in the CICSPlex SM application programming interface.

    The filter can work with options ``query``, ``update``, ``delete``; otherwise it will be ignored.

    For more guidance about specifying filter expressions using the CICSPlex SM API, see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/system-programming/cpsm/eyup1a0.html.


    | **required**: False
    | **type**: str



     
scheme
  The http scheme to use when establishing a connection to the CMCI API


  | **required**: false
  | **type**: str
  | **default**: https
  | **choices**: http, https


     
scope
  Specifies the name of a CICSplex, CICS region group, CICS region, or logical scope associated with the query.

  Scope is a subset of context, and limits the request to particular CICS systems or resources.

  Scope is not mandatory. If scope is absent, the request is limited by the value of the context alone.

  The value of scope must not contain spaces.

  Scope is not case-sensitive


  | **required**: false
  | **type**: str


     
type
  The CMCI resource name for the target resource type.  For the list of CMCI resource names, see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_resources.html


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
      
        
      
        

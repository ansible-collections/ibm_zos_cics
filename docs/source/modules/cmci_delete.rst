
:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/dev/plugins/modules/cmci_delete.py

.. _cmci_delete_module:


cmci_delete -- Delete CICS and CICSplex SM resources
====================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The cmci_delete module can be used to delete installed and definitional CICS and CICSPlex® SM resources from CICS regions, using the CMCI API.  The CMCI API is provided by CICSplex SM, or in SMSS regions.  For information about the CMCI API see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_overview.html. For information about how to compose DELETE requests, see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_delete.html.





Parameters
----------


     
cmci_cert
  Location of the PEM-formatted certificate chain file to be used for HTTPS client authentication.

  Required when security_type is certificate.

  Can also be specified using the environment variable CMCI_CERT


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


  | **required**: False
  | **type**: str


     
cmci_password
  The password of cmci_user to pass using HTTP basic authentication

  Can also be specified using the environment variable CMCI_PASSWORD


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
  The resource parameters,refer to the CICSPlex SM resource tables in the knowledge center to get the possible parameters.


  | **required**: False
  | **type**: dict


     
resource
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


     
  parameters
    A string of one or more parameters and values of the form parameter_name(data_value) that refines the request. The rules for specifying these parameters are the same as in the CICSPlex SM application programming interface.

    For more guidance about specifying parameter expressions using the CICSPlex SM API, see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/system-programming/cpsm/eyup1bg.html


    | **required**: False
    | **type**: dict



     
scheme
  Whether or not to use HTTPS


  | **required**: False
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

   
   - name: delete a bundle in a CICS region
     cmci_delete:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       context: 'iyk3z0r9'
       resource_name: CICSBundle
       resource:
         filter:
           name: 'PONGALT'

   - name: delete a bundle definition in a CICS region
     cmci_delete:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       context: 'iyk3z0r9'
       option: 'delete'
       resource_name: CICSDefinitionBundle
       resource: 
         filter:
           name: 'PONGALT'
         parameters:
           csdgroup: JVMGRP









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
            
      
      
                              
       success_count
        | Number of resources that were successfully deleted
      
        | **returned**: success
        | **type**: int
      
      
                              
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
      
        
      
        

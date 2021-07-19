.. ...............................................................................
.. © Copyright IBM Corporation 2020                                              .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/dev/plugins/modules/cmci_create.py

.. _cmci_create_module:


cmci_create -- Create CICS and CICSPlex SM definitions
======================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Create definitional CICS® or CICSPlex® SM resources in CSD and BAS repositories, by initiating POST requests via the CMCI REST API. The CMCI REST API can be configured in CICSPlex SM or stand-alone regions (SMSS). For information about the API, see `CMCI REST API <https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_overview.html>`_. For information about how to compose POST requests, see `CMCI POST requests <https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_post.html>`_.





Parameters
----------


     
attributes
  The resource attributes to be created or updated. Available attributes can be found in the CICSPlex® SM resource table reference for the target resource type, for example, `PROGDEF resource table reference <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html>`_.


  | **required**: False
  | **type**: dict


     
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
  If CMCI is installed in a CICSPlex® SM environment, *context* is the name of the CICSplex or CMAS associated with the request, for example, ``PLEX1``. To determine whether a CMAS can be specified as *context*, see the **CMAS context** entry in the CICSPlex SM resource table reference of a resource. For example, according to the `PROGRAM resource table <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGRAMtab.html>`_, CMAS context is not supported for PROGRAM.

  If CMCI is installed in a single region (SMSS), *context* is the APPLID of the CICS region associate with the request.

  The value of *context* must contain no spaces. *context* is not case-sensitive.


  | **required**: True
  | **type**: str


     
create_parameters
  A list of one or more parameters that control the *create* operation. Eligible parameters for the CREATE operation can be found in the resource table reference for the target resource type, as listed in the CREATE operation section of the "Valid CPSM operations" table. For example, the valid parameters for a PROGDEF CREATE operation are CSD and RESGROUP, as found in the `PROGDEF resource table reference <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html>`_.



  | **required**: False
  | **type**: list


     
  name
    Parameter name for the CREATE operation.


    | **required**: True
    | **type**: str


     
  value
    Parameter value if any. Can be omitted if the parameter requires no value to be supplied, as shown in the resource table reference. For example, the CSD parameter for the PROGDEF CREATE operation doesn't require a value.


    | **required**: False
    | **type**: str



     
insecure
  When set to ``true``, disables SSL certificate trust chain verification when using HTTPS.


  | **required**: False
  | **type**: bool


     
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

   
   - name: define a BUNDLE in a CSD
     cmci_create:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: 10080
       context: 'iyk3z0r9'
       type: 'CICSDefinitionBundle'
       attributes:
         name: PONGALT
         bundledir: /u/ibmuser/bundle/pong/pongbundle_1.0.0
         csdgroup: JVMGRP
       create_parameters:
         - name: 'csd'









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
      
      
                              
       connect_version
        | Version of the CMCI REST API.
      
        | **returned**: success
        | **type**: str
      
      
                              
       cpsm_reason
        | The character value of the REASON code returned by each CICSPlex SM API command. For a list of REASON character values, see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2ky.html.
      
        | **returned**: success
        | **type**: str
      
      
                              
       cpsm_reason_code
        | The numeric value of the REASON code returned by each CICSPlex SM API command. For a list of REASON numeric values, see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kw.html.
      
        | **returned**: success
        | **type**: int
      
      
                              
       cpsm_response
        | The character value of the RESPONSE code returned by each CICSPlex SM API command. For a list of RESPONSE character values, see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kx.html.
      
        | **returned**: success
        | **type**: str
      
      
                              
       cpsm_response_code
        | The numeric value of the RESPONSE code returned by each CICSPlex SM API command. For a list of RESPONSE numeric values, see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/commands-cpsm/eyup2kv.html.
      
        | **returned**: success
        | **type**: str
      
      
                              
       http_status
        | The message associated with HTTP status code that is returned by CMCI.
      
        | **returned**: success
        | **type**: str
      
      
                              
       http_status_code
        | The HTTP status code returned by CMCI.
      
        | **returned**: success
        | **type**: int
      
      
                              
       record_count
        | The number of records returned.
      
        | **returned**: success
        | **type**: int
      
      
                              
       records
        | A list of the returned records.
      
        | **returned**: success
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"_keydata": "C1D5E2C9E3C5E2E3", "aloadtime": "00:00:00.000000", "apist": "CICSAPI", "application": "", "applmajorver": "-1", "applmicrover": "-1", "applminorver": "-1", "basdefinever": "0", "cedfstatus": "CEDF", "changeagent": "CSDAPI", "changeagrel": "0730", "changetime": "2020-12-15T02:34:31.000000+00:00", "changeusrid": "YQCHEN", "coboltype": "NOTAPPLIC", "concurrency": "QUASIRENT", "copy": "NOTREQUIRED", "currentloc": "NOCOPY", "datalocation": "ANY", "definesource": "ANSITEST", "definetime": "2020-12-15T02:34:29.000000+00:00", "dynamstatus": "NOTDYNAMIC", "entrypoint": "FF000000", "execkey": "USEREXECKEY", "executionset": "FULLAPI", "eyu_cicsname": "IYCWEMW2", "eyu_cicsrel": "E730", "eyu_reserved": "0", "fetchcnt": "0", "fetchtime": "00:00:00.000000", "holdstatus": "NOTAPPLIC", "installagent": "CSDAPI", "installtime": "2020-12-15T02:34:33.000000+00:00", "installusrid": "YQCHEN", "jvmclass": "", "jvmserver": "", "language": "NOTDEFINED", "length": "0", "library": "", "librarydsn": "", "loadpoint": "FF000000", "lpastat": "NOTAPPLIC", "newcopycnt": "0", "operation": "", "pgrjusecount": "0", "platform": "", "program": "ANSITEST", "progtype": "PROGRAM", "remotename": "", "remotesystem": "", "removecnt": "0", "rescount": "0", "residency": "NONRESIDENT", "rloading": "0.000", "rplid": "0", "rremoval": "0.000", "runtime": "UNKNOWN", "ruse": "0.000", "sharestatus": "PRIVATE", "status": "DISABLED", "transid": "", "useagelstat": "0", "usecount": "0", "usefetch": "0.000"}]
            
      
      
                              
       request
        | Information about the request that was made to CMCI.
      
        | **returned**: success
        | **type**: dict
              
   
                              
        body
          | The XML body sent with the request, if any.
      
          | **returned**: success
          | **type**: str
      
      
                              
        method
          | The HTTP method used for the request.
      
          | **returned**: success
          | **type**: str
      
      
                              
        url
          | The URL used for the request.
      
          | **returned**: success
          | **type**: str
      
        
      
      
                              
       feedback
        | Diagnostic data from FEEDBACK records associated with the request
      
        | **returned**: cmci error
        | **type**: list
              
   
                              
        action
          | The name of the action that has failed.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        attribute1
          | The name of one of up to six attributes associated with the error.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        attribute2
          | The name of one of up to six attributes associated with the error.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        attribute3
          | The name of one of up to six attributes associated with the error.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        attribute4
          | The name of one of up to six attributes associated with the error.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        attribute5
          | The name of one of up to six attributes associated with the error.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        attribute6
          | The name of one of up to six attributes associated with the error.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        eibfn
          | The function code associated with the request.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        eibfn_alt
          | The name of the function associated with the request.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        errorcode
          | The CICSPlex® SM error code associated with the resource.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        eyu_cicsname
          | The name of the CICS region or CICSplex associated with the error.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        keydata
          | A string of data that identifies the instance of a resource associated with the error.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        resp
          | The CICS RESP code or the CICSPlex SM API EYUDA response code as a numeric value.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        resp2
          | The CICS RESP2 code or the CICSPlex SM API EYUDA reason code as a numeric value.
      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        resp_alt
          | The text equivalent for the resp value. For example, the text equivalent of a resp value of 16 is INVREQ.

      
          | **returned**: cmci error
          | **type**: str
      
      
                              
        installerror
          | Contains diagnostic data from a BINSTERR record associated with a CICS® management client interface PUT install request.

      
          | **returned**: cmci error
          | **type**: list
              
   
                              
         eibfn
            | The function code associated with the request.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         eyu_cicsname
            | The name of the CICS region or CICSplex associated with the installation error.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         cresp1
            | The CICS RESP code or the CICSPlex® SM API EYUDA response code as a numeric value.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         cresp2
            | The CICS RESP2 code or the CICSPlex SM API EYUDA reason code as a numeric value.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         errorcode
            | The CICSPlex SM error code associated with the resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         ressname
            | The name of the resource associated with the error.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         resver
            | The version number of the resource associated with the error.
      
            | **returned**: cmci error
            | **type**: str
      
        
      
      
                              
        inconsistentscope
          | Contains diagnostic data from a BINCONSC record associated with a CICS® management client interface PUT request.

      
          | **returned**: cmci error
          | **type**: list
              
   
                              
         eibfn
            | The function code associated with the request.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         eyu_cicsname
            | The name of the CICS region or CICSplex associated with the installation error.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         erroroperation
            | A numeric value that identifies the operation being performed when the error occurred.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         errorcode
            | The CICSPlex® SM error code associated with the resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         targetassignment
            | The assignment for the target scope.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         targetdescription
            | The resource description for the target scope.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         relatedassignment
            | The resource assignment for the related scope.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         relateddescription
            | The resource description for the related scope.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         relatedscope
            | The name of the related scope.
      
            | **returned**: cmci error
            | **type**: str
      
        
      
      
                              
        inconsistentset
          | Contains diagnostic data from a BINCONRS record associated with a CICS® management client interface PUT request.

      
          | **returned**: cmci error
          | **type**: list
              
   
                              
         candidatename
            | The name of the candidate resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         candidateversion
            | The version number of the candidate resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         candidategroup
            | The resource group of the candidate resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         candidateassignment
            | The assignment of the candidate resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         candidatedescription
            | The description of the candidate resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         candidateusage
            | The assignment usage of the candidate resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         candidatesystemgroup
            | The system group of the candidate resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         candidatetype
            | The system type of the candidate resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         candidateoverride
            | The assignment override of the candidate resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         eyu_cicsname
            | The name of the CICS region associated with the installation error.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         erroroperation
            | A numeric value that identifies that the operation being performed when the error occurred

      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         existingname
            | The name of the existing resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         existingversion
            | The version number of the existing resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         existinggroup
            | The resource group of the existing resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         existingassignment
            | The assignment of the existing resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         existingdescription
            | The description of the existing resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         existingusage
            | The assignment usage of the existing resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         existingsystemgroup
            | The system group of the existing resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         existingtype
            | The system type of the existing resource.
      
            | **returned**: cmci error
            | **type**: str
      
      
                              
         existingoverride
            | The assignment override of the existing resource.
      
            | **returned**: cmci error
            | **type**: str
      
        
      
        
      
        

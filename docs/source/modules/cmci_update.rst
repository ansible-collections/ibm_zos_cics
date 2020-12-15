
:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/dev/plugins/modules/cmci_update.py

.. _cmci_update_module:


cmci_update -- Get CICS and CICSplex SM resources
=================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The cmci_update module can be used to make changes to CICS and CICSPlex® SM resources in CICS regions using the CMCI API.  The CMCI API is provided by CICSplex SM, or in SMSS regions.  For information about the CMCI API see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_overview.html. For information about how to compose PUT requests, see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_put.html.





Parameters
----------


     
attributes
  The resource attributes, refer to the CICSPlex SM resource tables in the knowledge center to find the possible attributes.


  | **required**: False
  | **type**: dict


     
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
  | **type**: str


     
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



     
resource_name
  The CMCI resource name for the target resource type.  For the list of CMCI resource names, see https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_resources.html


  | **required**: True
  | **type**: str


     
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
       criteria: 'dsname=XIAOPIN* and file=DFH*'

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
       criteria: 'NAME=PONGALT'
       parameter: 'CSDGROUP(JVMGRP)'

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
       criteria: 'NAME=PONGALT'
       parameter: 'CSDGROUP(JVMGRP)'

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
       criteria: 'NAME=PONGALT'

   - name: delete a bundle in a CICS region
     cics_cmci:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       security_type: 'yes'
       context: 'iyk3z0r9'
       option: 'delete'
       resource:
         - type: CICSBundle
       criteria: 'NAME=PONGALT'

   - name: delete a bundle definition in a CICS region
     cics_cmci:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       context: 'iyk3z0r9'
       option: 'delete'
       resource:
         - type: CICSDefinitionBundle
       criteria: 'NAME=PONGALT'
       parameter: 'CSDGROUP(JVMGRP)'

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
       criteria: 'dsname=XIAOPIN* AND file=DFH*'









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
      
      
                              
       url
        | The cmci url that been composed
      
        | **returned**: always
        | **type**: str
      
      
                              
       api_response
        | Indicate if the cmci request been issued successfully or not
      
        | **returned**: always
        | **type**: str
      
      
                              
       response
        | The response of cmci request
      
        | **returned**: success
        | **type**: dict      
        | **sample**:

              .. code-block::

                       {"records": {"cicsdefinitionlibrary": {"_keydata": "D7D6D5C74040404000D1E5D4C7D9D74040", "changeagent": "CSDAPI", "changeagrel": "0710", "changetime": "2020-06-16T10:40:50.000000+00:00", "changeusrid": "CICSUSER", "createtime": "2020-06-16T10:40:50.000000+00:00", "critical": "NO", "csdgroup": "JVMGRP", "defver": "0", "desccodepage": "0", "description": "", "dsname01": "XIAOPIN.PONG.LOADLIB", "dsname02": "", "dsname03": "", "dsname04": "", "dsname05": "", "dsname06": "", "dsname07": "", "dsname08": "", "dsname09": "", "dsname10": "", "dsname11": "", "dsname12": "", "dsname13": "", "dsname14": "", "dsname15": "", "dsname16": "", "name": "PONG", "ranking": "50", "status": "ENABLED", "userdata1": "", "userdata2": "", "userdata3": ""}}, "resultsummary": {"api_response1": "1024", "api_response1_alt": "OK", "api_response2": "0", "api_response2_alt": "", "displayed_recordcount": "1", "recordcount": "1"}}
            
      
        

.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/main/plugins/modules/cmci_get.py

.. _cmci_get_module:


cmci_get -- Query CICS and CICSPlex SM resources and definitions
================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information about installed and definitional CICS® and CICSPlex® SM resources from CICS regions, by initiating GET requests via the CMCI REST API. The CMCI REST API can be configured in CICSPlex SM or stand-alone regions (SMSS). For information about the API, see \ `CMCI REST API <https://www.ibm.com/docs/en/cics-ts/latest?topic=programming-cmci-rest-api-reference>`__. For information about how to compose GET requests, see \ `CMCI GET requests <https://www.ibm.com/docs/en/cics-ts/latest?topic=requests-cmci-get>`__.





Parameters
----------


     
cmci_cert
  Location of the PEM-formatted certificate chain file to be used for HTTPS client authentication.

  Can also be specified using the environment variable CMCI\_CERT.

  Required if :emphasis:`cmci\_key` is specified.

  Authentication prioritises certificate authentication if :emphasis:`cmci\_cert` and :emphasis:`cmci\_key` are provided, then basic authentication if :emphasis:`cmci\_user` and :emphasis:`cmci\_password` are provided, and then unauthenticated if none is provided.


  | **required**: False
  | **type**: str


     
cmci_host
  The TCP/IP host name of CMCI connection.


  | **required**: True
  | **type**: str


     
cmci_key
  Location of the PEM-formatted file storing your private key to be used for HTTPS client authentication.

  Can also be specified using the environment variable CMCI\_KEY.

  Required if :emphasis:`cmci\_cert` is specified.

  Authentication prioritises certificate authentication if :emphasis:`cmci\_cert` and :emphasis:`cmci\_key` are provided, then basic authentication if :emphasis:`cmci\_user` and :emphasis:`cmci\_password` are provided, and then unauthenticated if none is provided.


  | **required**: False
  | **type**: str


     
cmci_password
  The password of :emphasis:`cmci\_user` to pass HTTP basic authentication.

  Can also be specified using the environment variable CMCI\_PASSWORD.

  Required if :emphasis:`cmci\_user` is specified.

  Authentication prioritises certificate authentication if :emphasis:`cmci\_cert` and :emphasis:`cmci\_key` are provided, then basic authentication if :emphasis:`cmci\_user` and :emphasis:`cmci\_password` are provided, and then unauthenticated if none is provided.


  | **required**: false
  | **type**: str


     
cmci_port
  The port number of the CMCI connection.


  | **required**: True
  | **type**: int


     
cmci_user
  The user ID under which the CMCI request will run.

  Can also be specified using the environment variable CMCI\_USER.

  Required if :emphasis:`cmci\_password` is specified.

  Authentication prioritises certificate authentication if :emphasis:`cmci\_cert` and :emphasis:`cmci\_key` are provided, then basic authentication if :emphasis:`cmci\_user` and :emphasis:`cmci\_password` are provided, and then unauthenticated if none is provided.


  | **required**: false
  | **type**: str


     
context
  If CMCI is installed in a CICSPlex® SM environment, :emphasis:`context` is the name of the CICSplex or CMAS associated with the request, for example, :literal:`PLEX1`. To determine whether a CMAS can be specified as :emphasis:`context`\ , see the :strong:`CMAS context` entry in the CICSPlex SM resource table reference of a resource. For example, according to the \ `PROGRAM resource table <https://www.ibm.com/docs/en/cics-ts/latest?topic=tables-program-resource-table>`__\ , CMAS context is not supported for PROGRAM.

  If CMCI is installed in a single region (SMSS), :emphasis:`context` is the APPLID of the CICS region associate with the request.

  The value of :emphasis:`context` must contain no spaces. :emphasis:`context` is not case-sensitive.


  | **required**: True
  | **type**: str


     
fail_on_nodata
  Specifies whether the module should fail if no data is returned by the query. If set to true, the module will fail if no data is returned.

  Default behaviour is for the module to fail if no data is returned. When set to false, the module will return OK, just with no records.


  | **required**: False
  | **type**: bool
  | **default**: True


     
insecure
  When set to :literal:`true`\ , disables SSL certificate trust chain verification when using HTTPS.


  | **required**: False
  | **type**: bool


     
record_count
  Identifies a subset of records in the results cache, starting either from the first record in the results cache or from the record specified by the index parameter. If not specified, all the records are returned by default.

  A negative number indicates a count back from the last record; for example, :literal:`-1` means the last record, :literal:`-2` the last record but one, and so on.

  The count value must be an integer; a value of zero is not permitted.


  | **required**: False
  | **type**: int


     
resources
  Options that specify a target resource.


  | **required**: False
  | **type**: dict


     
  complex_filter
    A dictionary representing a complex filter expression. Complex filters are composed of filter expressions, represented as dictionaries. Each dictionary can specify either an attribute expression, a list of filter expressions to be composed with the :literal:`and` operator, or a list of filter expressions to be composed with the :literal:`or` operator.

    The :literal:`attribute`\ , :literal:`and` and :literal:`or` options are mutually exclusive with each other.

    Can contain one or more filters. Multiple filters must be combined using :literal:`and` or :literal:`or` logical operators.

    Filters can be nested.

    When supplying the :literal:`attribute` option, you must also supply a :literal:`value` for the filter. You can also override the default operator of :literal:`=` with the :literal:`operator` option.

    For examples, see "Examples" in :ref:`ibm.ibm\_zos\_cics.cmci\_get <ansible_collections.ibm.ibm_zos_cics.cmci_get_module>`.


    | **required**: False
    | **type**: dict


     
    and
      A list of filter expressions to be combined with an :literal:`and` operation.

      Filter expressions are nested :literal:`complex\_filter` elements. Each nested filter expression can be either an :literal:`attribute`\ , :literal:`and` or :literal:`or` complex filter expression.


      | **required**: False
      | **type**: list


     
    attribute
      The name of a resource table attribute on which to filter.

      For supported attributes of different resource types, see their resource table reference, for example, \ `PROGDEF resource table reference <https://www.ibm.com/docs/en/cics-ts/latest?topic=tables-progdef-resource-table>`__.


      | **required**: False
      | **type**: str


     
    operator
      These operators are accepted: :literal:`\<` or :literal:`LT` (less than), :literal:`\<=` or :literal:`LE` (less than or equal to), :literal:`=` or :literal:`EQ` (equal to), :literal:`\>` or :literal:`GT` (greater than), :literal:`\>=` or :literal:`GE` (greater than or equal to), :literal:`==` or :literal:`IS` (is), :literal:`¬=`\ , :literal:`!=`\ , or :literal:`NE` (not equal to). If not supplied when :literal:`attribute` is used, :literal:`EQ` is assumed.


      | **required**: False
      | **type**: str
      | **choices**: <, >, <=, >=, =, ==, !=, ¬=, EQ, GT, GE, LT, LE, NE, IS


     
    or
      A list of filter expressions to be combined with an :literal:`or` operation.

      Filter expressions are nested :literal:`complex\_filter` elements. Each nested filter expression can be either an :literal:`attribute`\ , :literal:`and` or :literal:`or` complex filter expression.


      | **required**: False
      | **type**: list


     
    value
      The value by which you are to filter the resource attributes.

      The value must be a valid one for the resource table attribute as documented in the resource table reference, for example, \ `PROGDEF resource table reference <https://www.ibm.com/docs/en/cics-ts/latest?topic=tables-progdef-resource-table>`__.


      | **required**: False
      | **type**: str



     
  filter
    A dictionary with attribute names as keys, and target values, to be used as criteria to filter the set of resources returned from CICSPlex SM.

    Filters implicitly use the :literal:`=` operator.

    Filters for :literal:`string` type attributes can use the :literal:`\*` and :literal:`+` wildcard operators.

    :literal:`\*` is a wildcard representing an unknown number of characters, and must appear at the end of the value.

    :literal:`+` is a wildcard representing a single character, and can appear in any place in the value, potentially multiple times.

    To use more complicated filter expressions, including a range of different filter operators, and the ability to compose filters with :literal:`and` and :literal:`or` operators, see the :literal:`complex\_filter` parameter.

    For more details, see \ `How to build a filter expression <https://www.ibm.com/docs/en/cics-ts/latest?topic=expressions-how-build-filter-expression>`__.

    For examples, see :ref:`ibm.ibm\_zos\_cics.cmci\_get <ansible_collections.ibm.ibm_zos_cics.cmci_get_module>`.

    For supported attributes of different resource types, see their resource table reference, for example, \ `PROGDEF resource table reference <https://www.ibm.com/docs/en/cics-ts/latest?topic=tables-progdef-resource-table>`__.


    | **required**: False
    | **type**: dict


     
  get_parameters
    A list of one or more parameters with optional values used to identify the resources for this request. Eligible parameters for identifying the target resources can be found in the resource table reference for the target resource type, as valid parameters for the GET operation in the "Valid CPSM operations" table. For example, the valid parameters for identifying a PROGDEF resource are CICSSYS, CSDGROUP and RESGROUP, as found in the \ `PROGDEF resource table reference <https://www.ibm.com/docs/en/cics-ts/latest?topic=tables-progdef-resource-table>`__.


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




     
scheme
  The HTTP scheme to use when establishing a connection to the CMCI REST API.


  | **required**: false
  | **type**: str
  | **default**: https
  | **choices**: http, https


     
scope
  Specifies the name of a CICSplex, CICS region group, CICS region, or logical scope that is associated with the query.

  :emphasis:`scope` is a subset of :emphasis:`context` and limits the request to particular CICS systems or resources.

  :emphasis:`scope` is optional. If it's not specified, the request is limited by the value of :emphasis:`context` alone.

  The value of :emphasis:`scope` must contain no spaces. :emphasis:`scope` is not case-sensitive.


  | **required**: false
  | **type**: str


     
timeout
  HTTP request timeout in seconds


  | **required**: False
  | **type**: int
  | **default**: 30


     
type
  The CMCI external resource name that maps to the target CICS or CICSPlex SM resource type. For a list of CMCI external resource names, see \ `CMCI resource names <https://www.ibm.com/docs/en/cics-ts/latest?topic=reference-cmci-resource-names>`__.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Get 2 LOCFILEs from a CICSplex
     cmci_get:
       cmci_host: "example.com"
       cmci_port: 12345
       cmci_user: ibmuser
       cmci_password: "123456"
       context: ABCDEFGH # context is the name of your CICSplex in a CPSM environment or the applid of your region in an SMSS environment
       type: CICSLocalFile
       record_count: 2
       resources:
         filter:
           dsname: "CTS*"

   - name: Get a localfile in a CICS region
     cmci_get:
       cmci_host: "example.com"
       cmci_port: 12345
       cmci_cert: "./sec/ansible.pem"
       cmci_key: "./sec/ansible.key"
       context: ABCDEFGH # context is the name of your CICSplex in a CPSM environment or the applid of your region in an SMSS environment
       type: CICSLocalFile
       resources:
         filter:
           dsname: "XIAOPIN*"
           file: "DFH*"
       record_count: 1

   - name: Get a progdef from CSD
     cmci_get:
       cmci_host: "example.com"
       cmci_port: 12345
       cmci_cert: "./sec/ansible.pem"
       cmci_key: "./sec/ansible.key"
       context: ABCDEFGH # context is the name of your CICSplex in a CPSM environment or the applid of your region in an SMSS environment
       type: cicsdefinitionprogram
       resources:
         filter:
           name: MYPROG
         get_parameters:
           - name: csdgroup
             value: MYGRP
       record_count: 1

   - name: Ignore errors when bundle definition is not found
     cmci_get:
       cmci_host: "example.com"
       cmci_port: 12345
       cmci_cert: "./sec/ansible.pem"
       cmci_key: "./sec/ansible.key"
       context: ABCDEFGH # context is the name of your CICSplex in a CPSM environment or the applid of your region in an SMSS environment
       scope: IJKLMNOP # scope only applies if you're in a CPSM environment and is the name of a CICS system definition (CSYSDEF) or CICS system group (CSYSGRP)
       type: cicsdefinitionbundle
       resources:
         filter:
           name: MYBUNDLE
         get_parameters:
           - name: csdgroup
             value: MYGRP
       record_count: 1
       fail_on_nodata: false

   - name: Using complex_filter to combine filter expressions and change operators
     cmci_get:
       cmci_host: "example.com"
       cmci_port: 12345
       cmci_cert: "./sec/ansible.pem"
       cmci_key: "./sec/ansible.key"
       context: ABCDEFGH # context is the name of your CICSplex in a CPSM environment or the applid of your region in an SMSS environment
       type: CICSRegion
       resources:
         complex_filter:
           or:
             [
               { attribute: "currtasks", value: "10", operator: "<" },
               { attribute: "currtasks", value: "100", operator: ">" },
             ]
       record_count: 1









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
        | Version of the CMCI API
      
        | **returned**: success
        | **type**: str
      
      
                              
       cpsm_reason
        | The character value of the REASON code returned by each CICSPlex SM API command. For a list of REASON character values, see https://www.ibm.com/docs/en/cics-ts/latest?topic=values-eyuda-reason-in-alphabetical-order.
      
        | **returned**: success
        | **type**: str
      
      
                              
       cpsm_reason_code
        | The numeric value of the REASON code returned by each CICSPlex SM API command. For a list of REASON numeric values, see https://www.ibm.com/docs/en/cics-ts/latest?topic=values-eyuda-reason-in-numerical-order.
      
        | **returned**: success
        | **type**: int
      
      
                              
       cpsm_response
        | The character value of the RESPONSE code returned by each CICSPlex SM API command. For a list of RESPONSE character values, see https://www.ibm.com/docs/en/cics-ts/latest?topic=values-eyuda-response-in-alphabetical-order.
      
        | **returned**: success
        | **type**: str
      
      
                              
       cpsm_response_code
        | The numeric value of the RESPONSE code returned by each CICSPlex SM API command. For a list of RESPONSE numeric values, see https://www.ibm.com/docs/en/cics-ts/latest?topic=values-eyuda-response-in-numerical-order.
      
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
      
        
      
        
      
        

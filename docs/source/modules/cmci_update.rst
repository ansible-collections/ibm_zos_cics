.. ...............................................................................
.. © Copyright IBM Corporation 2020                                              .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

:github_url: https://github.com/ansible-collections/ibm_zos_cics/blob/dev/plugins/modules/cmci_update.py

.. _cmci_update_module:


cmci_update -- Update CICS and CICSPlex resources and definitions
=================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Make changes to CICS® and CICSPlex® SM resources in CICS regions, by initiating PUT requests via the CMCI REST API. The CMCI REST API can be configured in CICSPlex SM or stand-alone regions (SMSS). For information about the API, see `CMCI REST API <https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_overview.html>`_. For information about how to compose PUT requests, see `CMCI PUT requests <https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_put.html>`_.





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


     
insecure
  When set to ``true``, disables SSL certificate trust chain verification when using HTTPS.


  | **required**: False
  | **type**: bool


     
resources
  Options that specify a target resource.


  | **required**: False
  | **type**: dict


     
  complex_filter
    A dictionary representing a complex filter expression. Complex filters are composed of filter expressions, represented as dictionaries. Each dictionary can specify either an attribute expression, a list of filter expressions to be composed with the ``and`` operator, or a list of filter expressions to be composed with the ``or`` operator.

    The ``attribute``, ``and`` and ``or`` options are mutually exclusive with each other.

    Can contain one or more filters. Multiple filters must be combined using ``and`` or ``or`` logical operators.

    Filters can be nested. At most four nesting layers are allowed.

    When supplying the ``attribute`` option, you must also supply a ``value`` for the filter.  You can also override the default operator of ``=`` with the ``operator`` option.

    For examples, see :ref:`cmci_get <cmci_get_module>`


    | **required**: False
    | **type**: dict


     
    and
      A list of filter expressions to be combined with an ``and`` operation.

      Filter expressions are nested ``complex_filter`` elements.  Each nested filter expression can be either an ``attribute``, ``and`` or ``or`` complex filter expression.


      | **required**: False
      | **type**: list


     
    attribute
      The name of a resource table attribute on which to filter.

      For supported attributes of different resource types, see their resource table reference, for example, `PROGDEF resource table reference <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html>`_.


      | **required**: False
      | **type**: str


     
    operator
      These operators are accepted: ``<`` or ``LT`` (less than), ``<=`` or ``LE`` (less than or equal to), ``=`` or ``EQ`` (equal to), ``>`` or ``GT`` (greater than), ``>=`` or ``GE`` (greater than or equal to), ``==`` or ``IS`` (is), ``¬=``, ``!=``, or ``NE`` (not equal to).  If not supplied when 'attribute' is used, ``EQ`` will be assumed.



      | **required**: False
      | **type**: str
      | **choices**: <, >, <=, >=, =, ==, !=, ¬=, EQ, GT, GE, LT, LE, NE, IS


     
    or
      A list of filter expressions to be combined with an ``or`` operation.

      Filter expressions are nested ``complex_filter`` elements.  Each nested filter expression can be either an ``attribute``, ``and`` or ``or`` complex filter expression.


      | **required**: False
      | **type**: list


     
    value
      The value by which you are to filter the resource attributes.

      The value must be a valid one for the resource table attribute as documented in the resource table reference, for example, `PROGDEF resource table reference <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html>`_.


      | **required**: False
      | **type**: str



     
  filter
    A dictionary with attribute names as keys, and target values, to be used as criteria to filter the set of resources returned from CICSPlex SM.

    Filters implicitly use the ``=`` operator

    Filters for ``string`` type attributes can use the ``*`` and ``+`` wildcard operators

    ``*`` is a wildcard representing an unknown number of characters, and must appear at the end of the value

    ``+`` is a wildcard representing a single character, and can appear in any place in the value, potentially multiple times.

    To use more complicated filter expressions, including a range of different filter operators, and the ability to compose filters with ``and`` and ``or`` operators, see the ``complex_filter`` parameter.

    For examples, see :ref:`cmci_get <cmci_get_module>`

    For more details, see `How to build a filter expression <https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/system-programming/cpsm/eyup1a0.html>`_.

    For supported attributes of different resource types, see their resource table reference, for example, `PROGDEF resource table reference <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html>`_.


    | **required**: False
    | **type**: dict


     
  get_parameters
    A list of one or more parameters with optional values used to identify the resources for this request. Eligible parameters for identifying the target resources can be found in the resource table reference for the target resource type, as valid parameters for the GET operation in the "Valid CPSM operations" table. For example, the valid parameters for identifying a PROGDEF resource are CICSSYS, CSDGROUP and RESGROUP, as found in the `PROGDEF resource table reference <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html>`_.



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

  *scope* is a subset of *context* and limits the request to particular CICS systems or resources.

  *scope* is optional. If it's not specified, the request is limited by the value of *context* alone.

  The value of *scope* must contain no spaces. *scope* is not case-sensitive.


  | **required**: false
  | **type**: str


     
type
  The CMCI external resource name that maps to the target CICS or CICSPlex SM resource type. For a list of CMCI external resource names, see `CMCI resource names <https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_resources.html>`_.


  | **required**: True
  | **type**: str


     
update_parameters
  A list of one or more parameters that control the *update* operation. Eligible parameters for the UPDATE operation can be found in the resource table reference for the target resource type, as listed in the UPDATE operation section of the "Valid CPSM operations" table. For example, the only valid parameter for a PROGDEF UPDATE operation is CSD, as found in the `PROGDEF resource table reference <https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html>`_.



  | **required**: False
  | **type**: list


     
  name
    Parameter name for the UPDATE operation.


    | **required**: True
    | **type**: str


     
  value
    Parameter value if any. Can be omitted if the parameter requires no value to be supplied, as shown in the resource table reference. For example, the CSD parameter for the PROGDEF UPDATE operation doesn't require a value.


    | **required**: False
    | **type**: str





Examples
--------

.. code-block:: yaml+jinja

   
   - name: update a bundle definition in a CICS region
     cmci_update:
       cmci_host: 'winmvs2c.hursley.ibm.com'
       cmci_port: '10080'
       context: 'iyk3z0r9'
       type: 'CICSDefinitionBundle'
       attributes:
         description: 'New description'
       parameters:
         csd: null
       resource:
         filter:
           name: 'PONGALT'
         parameters:
           - name: csdgroup
             value: JVMGRP









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
      
        
      
        

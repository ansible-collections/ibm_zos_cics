# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class ModuleDocFragment(object):

    COMMON = r'''
options:
  cmci_host:
    description:
      - The TCP/IP host name of CMCI connection.
    type: str
    required: true
  cmci_port:
    description:
      - The port number of the CMCI connection.
    type: int
    required: true
  cmci_user:
    description:
      - The user ID under which the CMCI request will run.
      - Can also be specified using the environment variable CMCI_USER.
      - Required if I(cmci_password) is specified.
      - Authentication prioritises certificate authentication if I(cmci_cert) and I(cmci_key) are provided, then
        basic authentication if I(cmci_user) and (cmci_password) are provided, and then unauthenticated if none is 
        provided.
    type: str
  cmci_password:
    description:
      - The password of I(cmci_user) to pass HTTP basic authentication. 
      - Can also be specified using the environment variable CMCI_PASSWORD.
      - Required if I(cmci_user) is specified.
      - Authentication prioritises certificate authentication if I(cmci_cert) and I(cmci_key) are provided, then
        basic authentication if I(cmci_user) and (cmci_password) are provided, and then unauthenticated if none is 
        provided.
    type: str
  cmci_cert:
    description:
      - Location of the PEM-formatted certificate chain file to be used for
        HTTPS client authentication.
      - Can also be specified using the environment variable CMCI_CERT.
      - Required if I(cmci_key) is specified.
      - Authentication prioritises certificate authentication if I(cmci_cert) and I(cmci_key) are provided, then
        basic authentication if I(cmci_user) and (cmci_password) are provided, and then unauthenticated if none is 
        provided.
    required: false
    type: str
  cmci_key:
    description:
      - Location of the PEM-formatted file storing your private key to be used
        for HTTPS client authentication.
      - Can also be specified using the environment variable CMCI_KEY.
      - Required if I(cmci_cert) is specified.
      - Authentication prioritises certificate authentication if I(cmci_cert) and I(cmci_key) are provided, then
        basic authentication if I(cmci_user) and (cmci_password) are provided, and then unauthenticated if none is 
        provided.
    required: false
    type: str
  context:
    description:
      - If CMCI is installed in a CICSPlex SM environment, I(context) is the
        name of the CICSplex or CMAS associated with the request, for example,
        PLEX1. See the relevant CICSPlex SM resource table, for example, L(PROGRAM resource table,
        https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGRAMtab.html),
        to determine whether to specify a CICSplex or CMAS.
      - If CMCI is installed in a single region (SMSS), I(context) is the
        APPLID of the CICS region associate with the request.
      - The value of I(context) must contain no spaces. I(context) is not
        case-sensitive.
    type: str
  scope:
    description:
      - Specifies the name of a CICSplex, CICS region group, CICS region, or
        logical scope that is associated with the query.
      - I(scope) is a subset of I(context) and limits the request to particular
        CICS systems or resources.
      - I(scope) is optional. If it's not specified, the request is limited by
        the value of I(context) alone.
      - The value of I(scope) must contain no spaces. I(scope) is not case-sensitive.
    type: str
  type:
    description:
      - The CMCI external resource name that maps to the target CICS or CICSPlex SM resource type. 
        For a list of CMCI external resource names, see L(CMCI resource names, 
        https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_resources.html).
    type: str
    required: true
  scheme:
    description: The HTTP scheme to use when establishing a connection to the CMCI REST API.
    type: str
    choices:
      - http
      - https
    default: https
  insecure:
    description: When set to C(true), disables SSL certificate trust chain verification when using HTTPS.
    type: bool
    required: false
    default: false
'''

    RESOURCES = r'''
options:
  resources:
    description:
      - Options that specify a target resource.
    type: dict
    required: false
    suboptions:   
      filter:
        description:
          - A string containing basic logical expressions that filter the resource table records
            in the data returned on the request.
          - Supports only the equal logic when filtering attribute values.
          - Can contain one or more filters.
          - For supported attributes of different resource types, see their resource table reference,
            for example, L(PROGDEF resource table reference,
            https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html).
        type: str
        required: false
      complex_filter:
        description:
          - A string containing logical expressions that filter the resource table records
            in the data returned on the request.
          - Can contain one or more filters. Multiple filters must be combined using C(and) or C(or) logical operators.
          - Filters can be nested. At most four nesting layers are allowed.
        type: str
        required: false
        suboptions:
          attribute:
            description:
              - The resource table attributes to be filtered.
              - For supported attributes of different resource types, see their resource table reference,
                for example, L(PROGDEF resource table reference,
                https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html).
            type: str
            required: false
          operator:
            description: >
              These operators are accepted: C(<) or C(LT) (less than), C(<=) or C(LE) (less than or equal to),
              C(=) or C(EQ) (equal to), C(>) or C(GT) (greater than), C(>=) or C(GE) (greater than or equal to),
              C(==) or C(IS) (is), C(¬=), C(!=), or C(NE) (not equal to). 
            type: str
            required: false
            choices: 
              - "<"
              - ">"
              - "<="
              - ">="
              - "="
              - "=="
              - "!="
              - "¬="
              - EQ
              - GT
              - GE
              - LT
              - LE
              - NE
              - IS
            default: EQ              
          value:
            description: 
              - The value by which you are to filter the resource attributes. 
              - The value must be a valid one for the resource table attribute as documented in the 
                resource table reference, for example, L(PROGDEF resource table reference,
                https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html).
            required: false
  parameters:
    description: >
      A list of one or more parameters with optional values used to identify the resources for this request.
      Eligible parameters for identifying the target resources can be found in the resource table reference for the 
      target resource type, as valid parameters for the GET operation in the "Valid CPSM operations" table. 
      For example, the valid parameters for identifying a PROGDEF resource are
      CICSSYS, CSDGROUP and RESGROUP, as found in the L(PROGDEF resource table reference,
      https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html).
    type: list
    suboptions:
      name:
        description: Parameter name available for the GET operation.
        required: true
        type: str
      value:
        description: Parameter value if any.
        required: false
        type: str
    required: false
'''

    ATTRIBUTES = r'''
options:
  attributes:
    description:
      - The resource attributes to be defined. Available attributes can be found in the CICSPlex SM resource table reference for the
        target resource type, for example, L(PROGDEF resource table reference,
        https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html).
    type: dict
    required: false
'''

    PARAMETERS = r'''
options:
  parameters:
    description: >
      A list of one or more parameters for the target operation.  TODO should we document this parameter separately for
      each operation?  E.g. might be easier to show how to find the parameters for an action distinct from create...
      TODO Provide an example of how to use flag style parameters
    type: list
    suboptions:
      name:
        description: Parameter name
        required: true
        type: str
      value:
        description: Parameter value if any
        required: false
        type: str
    required: false
'''

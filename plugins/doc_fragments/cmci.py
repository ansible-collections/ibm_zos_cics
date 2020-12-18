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
      - The TCP/IP host name of CMCI connection
    type: str
    required: true
  cmci_port:
    description:
      - The port number of the CMCI connection.
    type: int
    required: true
  cmci_user:
    description:
      - The user id to run the CMCI request as
      - Required when security type is yes
      - Can also be specified using the environment variable CMCI_USER
      - Required with cmci_password
    type: str
  cmci_password:
    description:
      - The password of cmci_user to pass using HTTP basic authentication
      - Can also be specified using the environment variable CMCI_PASSWORD
      - Required with cmci_user
    type: str
  cmci_cert:
    description:
      - Location of the PEM-formatted certificate chain file to be used for
        HTTPS client authentication.
      - Required when security_type is certificate.
      - Can also be specified using the environment variable CMCI_CERT
      - Required with cmci_key
    required: false
    type: str
  cmci_key:
    description:
      - Location of the PEM-formatted file with your private key to be used
        for HTTPS client authentication.
      - Required when security type is certificate.
      - Can also be specified using the environment variable CMCI_KEY
      - Required with cmci_cert
    required: false
    type: str
  context:
    description:
      - If CMCI is installed in a CICSPlex SM environment, context is the
        name of the CICSplex or CMAS associated with the request; for example,
        PLEX1. See the relevant resource table in CICSPlex SM resource tables
        to determine whether to specify a CICSplex or CMAS.
      - If CMCI is installed as a single server (SMSS), context is the
        APPLID of the CICS region associated with the request.
      - The value of context must not contain spaces. Context is not
        case-sensitive.
    type: str
  scope:
    description:
      - Specifies the name of a CICSplex, CICS region group, CICS region, or
        logical scope associated with the query.
      - Scope is a subset of context, and limits the request to particular
        CICS systems or resources.
      - Scope is not mandatory. If scope is absent, the request is limited by
        the value of the context alone.
      - The value of scope must not contain spaces.
      - Scope is not case-sensitive
    type: str
  type:
    description:
      - The CMCI resource name for the target resource type.  For the list of CMCI resource names, see
        U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/reference-system-programming/cmci/clientapi_resources.html)
    type: str
    required: true
  scheme:
    description: The http scheme to use when establishing a connection to the CMCI API
    type: str
    choices:
      - http
      - https
    default: https
  insecure:
    description: Set to true to disable SSL certificate trust chain verification when using https
    type: bool
    required: false
    default: false
'''

    RESOURCES = r'''
options:
  resources:
    description:
      - Options which specify a target resource
    type: dict
    required: false
    suboptions:   
      criteria:
        description:
          - A string containing logical expressions that filters the data 
            returned on the request.
          - The string that makes up the value of the CRITERIA parameter
            follows the same rules as the filter expressions in the CICSPlex
            SM application programming interface.
          - The filter can work with options ``query``, ``update``, ``delete``; 
            otherwise it will be ignored.
          - For more guidance about specifying filter expressions using the
            CICSPlex SM API, see
            U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/system-programming/cpsm/eyup1a0.html).
        type: str
        required: false
  parameters:
    description: >
      A list of one or more parameters with optional values used to identify the resources for this request.
      Eligible parameters for identifying resources can be found in the resource tables reference for the target
      resource type, for the GET operation. For example, the valid parameters for identifying a PROGDEF are
      CICSSYS, CSDGROUP and RESGROUP, as found in the resource tables reference
      U(https://www.ibm.com/support/knowledgecenter/en/SSGMCP_5.6.0/reference-cpsm-restables/cpsm-restables/PROGDEFtab.html)
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

    ATTRIBUTES = r'''
options:
  attributes:
    description:
      - The resource attributes, refer to the CICSPlex SM resource tables
        in the knowledge center to find the possible attributes.
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
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
  scheme:
    description:
      - Whether or not to use HTTPS
    required: false
    type: str
    choices:
      - http
      - https
    default: https
  cmci_user:
    description:
      - The user id to run the CMCI request as
      - Required when security type is yes
      - Can also be specified using the environment variable CMCI_USER
    type: str
  cmci_password:
    description:
      - The password of cmci_user to pass using HTTP basic authentication
      - Can also be specified using the environment variable CMCI_PASSWORD
    type: str
  cmci_cert:
    description:
      - Location of the PEM-formatted certificate chain file to be used for
        HTTPS client authentication.
      - Required when security_type is certificate.
      - Can also be specified using the environment variable CMCI_CERT
    required: false
    type: str
  cmci_key:
    description:
      - Location of the PEM-formatted file with your private key to be used
        for HTTPS client authentication.
      - Required when security type is certificate.
      - Can also be specified using the environment variable CMCI_KEY
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
        description:
          - A string of one or more parameters and values of the form
            parameter_name(data_value) that refines the request. The
            rules for specifying these parameters are the same as in
            the CICSPlex SM application programming interface.
          - For more guidance about specifying parameter expressions using the
            CICSPlex SM API, see
            U(https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/system-programming/cpsm/eyup1bg.html)
        type: dict
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
    description:
      - The resource parameters,refer to the CICSPlex SM resource tables
        in the knowledge center to get the possible parameters.
    type: dict
    required: false
'''
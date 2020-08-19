#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) IBM Corporation 2019, 2020

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

DOCUMENTATION = r"""
---
module: cics_cmci
short_description: Manage CICS and CPSM resources
description:
  - The cics_cmci module could be used to  manage installed and definitional
    CICS and CICSPlex® SM resources on CICS regions.
author: "Ping Xiao (@xiaoping)"
options:
  cmci_host:
    description:
      - The TCP/IP host name of CMCI connection
    type: str
    required: true
  cmci_port:
    description:
      - The port number for CMCI connection.
    type: str
    required: true
  cmci_user:
    description:
      - The user id to run the CMCI request with.
      - Required when security type is yes.
    type: str
  cmci_password:
    description:
      - The password of cmci_user to pass to the basic authentication
    type: str
  cmci_cert:
    description:
      - Location of the PEM-formatted certificate chain file to be used for
        HTTPS client authentication.
      - Required when security type is certificate.
    required: false
    type: str
  cmci_key:
    description:
      - Location of the PEM-formatted file with your private key to be used
        for HTTPS client authentication.
      - Required when security type is certificate.
    required: false
    type: str
  security_type:
    description:
      - the authenticate type that remote region requires
    required: true
    type: str
    choices:
      - none
      - basic
      - certificate
    default: none
  context:
    description:
      - If CMCI is installed in a CICSPlex SM environment, context is the
        name.
        of the CICSplex or CMAS associated with the request; for example,
        PLEX1. See the relevant resource table in CICSPlex SM resource tables
        to determine whether to specify a CICSplex or CMAS.
      - If CMCI is installed as a single server, context is the application
        ID of the CICS region associated with the request.
      - The value of context must not contain spaces. Context is not
        case-sensitive.
    type: str
  scope:
    description:
      - Specifies the name of a CICSplex, CICS group, CICS region, or logical
        scope associated with the query.
      - Scope is a subset of context, and limits the request to particular
        CICS systems or resources.
      - Scope is not mandatory. If scope is absent, the request is limited by
        the value of the context alone.
      - The value of scope must not contain spaces.
      - Scope is not case-sensitive
    type: str
  option:
    description:
      - The definition or operation you want to perform with your CICS or CPSM
        resources
    type: str
    choices:
      - define
      - delete
      - update
      - install
      - query
    default: query
  resource:
    description:
      - The resource that you want to define or operate with
    type: list
    required: true
    suboptions:
      type:
        description:
          - The resource type.
        type: str
        required: true
      attributes:
        description:
          - The resource attributes,refer to the CICSPlex SM resource tables
            in KC to find the possible attributes.
        type: list
        required: false
      parameters:
        description:
          - The resource parameters,refer to the CICSPlex SM resource tables
            in KC to get the possible parameters.
        type: list
        required: false
      location:
        description:
          - The location that resource been installed to.
          - This variable only work with option 'install'.
        type: str
        required: false
        choices:
          - BAS
          - CSD
  filter:
    description:
      - Refine the scope and nature of the request. The constituent parts of
        the query section can occur in any order, but each can occur only once
        in a URI.
      - Although query parameter values are not case-sensitive, certain
        attribute values must have the correct capitalization because some
        attributes such as TRANID and DESC can hold mixed-case values.
      - The filter could work with option 'query','update','delete', otherwise
        it will be ignored
    type: list
    suboptions:
      criteria:
        description:
          - A string of logical expressions that filters the data returned on
            the request.
          - The string that makes up the value of the CRITERIA parameter
            follows the same rules as the filter expressions in the CICSPlex
            SM application programming interface.
          - For more guidance about specifying filter expressions using the
            CICSPlex SM API, see (https://www.ibm.com/support/knowledgecenter
            /SSGMCP_5.4.0/system-programming/cpsm/eyup1a0.html).
        type: str
        required: false
      parameter:
        description:
          - A string of one or more parameters and values of the form
            parameter_name(data_value) that refines the request. The
            rules for specifying these parameters are the same as in
            the CICSPlex SM application programming interface.
          - For more guidance about specifying parameter expressions using the
            CICSPlex SM API, see (https://www.ibm.com/support/knowledgecenter
            /SSGMCP_5.4.0/system-programming/cpsm/eyup1bg.html)
        type: str
        required: false
  record_count:
    description:
      - Only work with 'query' option, otherwise it will be ignored
      - Identifies a subset of records in a results cache starting from the
        first record in the results cache or from the record specified
        by the index parameter.
      - A negative number indicates a count back from the last record; for
        example, -1 means the last record, -2 the last record but one, and so
        on
      - Count must be an integer, a value of zero is not permitted.
    type: int
    required: false
"""

EXAMPLES = r"""
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
    filter:
      - criteria: dsname=XIAOPIN* and file=DFH*

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
    filter:
          - criteria: NAME=PONGALT
            parameter: CSDGROUP(JVMGRP)

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
    filter:
        - criteria: NAME=PONGALT
          parameter: CSDGROUP(JVMGRP)

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
    filter:
        - criteria: NAME=PONGALT

- name: delete a bundle in a CICS region
  cics_cmci:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    security_type: 'yes'
    context: 'iyk3z0r9'
    option: 'delete'
    resource:
      - type: CICSBundle
    filter:
      - criteria: NAME=PONGALT

- name: delete a bundle definition in a CICS region
  cics_cmci:
    cmci_host: 'winmvs2c.hursley.ibm.com'
    cmci_port: '10080'
    context: 'iyk3z0r9'
    option: 'delete'
    resource:
      - type: CICSDefinitionBundle
    filter:
      - criteria: NAME=PONGALT
        parameter: CSDGROUP(JVMGRP)

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
    filter:
      - criteria:
          - dsname=XIAOPIN*
          - file=DFH*
"""

RETURN = r"""
changed:
    description: True if the state was changed, otherwise False
    returned: always
    type: bool
failed:
    description: True if query_job failed, othewise False
    returned: always
    type: bool
url:
    description: The cmci url that been composed
    returned: always
    type: str
api_response:
    description: Indicate if the cmci request been issued successfully or not
    returned: always
    type: str
response:
    description: The response of cmci request
    returned: success
    type: dict
    sample:
        {   "records": {
                "cicsdefinitionlibrary": {
                    "_keydata": "D7D6D5C74040404000D1E5D4C7D9D74040",
                    "changeagent": "CSDAPI",
                    "changeagrel": "0710",
                    "changetime": "2020-06-16T10:40:50.000000+00:00",
                    "changeusrid": "CICSUSER",
                    "createtime": "2020-06-16T10:40:50.000000+00:00",
                    "critical": "NO",
                    "csdgroup": "JVMGRP",
                    "defver": "0",
                    "desccodepage": "0",
                    "description": "",
                    "dsname01": "XIAOPIN.PONG.LOADLIB",
                    "dsname02": "",
                    "dsname03": "",
                    "dsname04": "",
                    "dsname05": "",
                    "dsname06": "",
                    "dsname07": "",
                    "dsname08": "",
                    "dsname09": "",
                    "dsname10": "",
                    "dsname11": "",
                    "dsname12": "",
                    "dsname13": "",
                    "dsname14": "",
                    "dsname15": "",
                    "dsname16": "",
                    "name": "PONG",
                    "ranking": "50",
                    "status": "ENABLED",
                    "userdata1": "",
                    "userdata2": "",
                    "userdata3": ""
                }
            },
          "resultsummary": {
                "api_response1": "1024",
                "api_response1_alt": "OK",
                "api_response2": "0",
                "api_response2_alt": "",
                "displayed_recordcount": "1",
                "recordcount": "1"
            }
      }

"""

import re
import traceback
try:
    import requests
except Exception:
    requests = None
    LIB_IMP_ERR = traceback.format_exc()
try:
    from encoder import XML2Dict
except Exception:
    XML2Dict = None
    LIB_IMP_ERR = traceback.format_exc()
# import requests
from ansible.module_utils.basic import AnsibleModule
from xml.dom.minidom import Document


class Error(Exception):
    pass


class ValidationError(Error):
    def __init__(self, message):
        self.msg = 'An error occurred during validate the input parameters:\
           "{0}"'.format(message)


class CMCIError(Error):
    def __init__(self, err):
        self.msg = 'An error occurred during issue cmci request:\
           "{0}"'.format(err)


def get_connect_session(params):
    if requests is None:
        raise CMCIError('ImportError: cannot import requests')
    session = requests.Session()
    user = params['cmci_user']
    pw = params['cmci_password']
    crt = params['cmci_cert']
    key = params['cmci_key']
    if (params['security_type'] == 'certificate'):
        if(crt is not None and crt.strip() != '') and (key is not None and key.strip() != ''):
            session.cert = (crt.strip(), key.strip())
        else:
            raise CMCIError('HTTP setup error: cmci_cert/cmci_key are required ')
    if (params['security_type'] == 'yes'):
        if (user is not None and user.strip() != '') and (pw is not None and pw.strip() != ''):
            session.auth = (user.strip(), pw.strip())
        else:
            raise CMCIError('HTTP setup error: cmci_user/cmci_password are required')
    return session


def handle_request(session, method, url, body=None, rcode=200, timeout=30):
    try:
        if method == 'get':
            response = session.get(url, verify=False, timeout=timeout)
        elif method == 'put':
            response = session.put(url, data=body, verify=False, timeout=timeout)
        elif method == 'post':
            response = session.post(url, data=body, verify=False, timeout=timeout)
        elif method == 'delete':
            response = session.delete(url, verify=False, timeout=timeout)
    except Exception as ex:
        raise CMCIError('HTTP request error: ' + str(ex))
    else:
        # response_code = response.status_code
        if response.content:
            response_content = response.content
        else:
            response_content = ''
    xml_parser = XML2Dict()
    response = xml_parser.parse(response_content)
    return response


def create_xml_body(params):
    doc = Document()
    action = params.get('option')
    request_element = doc.createElement('request')
    doc.appendChild(request_element)
    if action == 'install':
        action_element = doc.createElement('action')
        if params.get('location') == 'CSD':
            action_element.setAttribute('name', 'CSDINSTALL')
        if params.get('location') == 'BAS':
            action_element.setAttribute('name', 'INSTALL')
        request_element.appendChild(action_element)
    if action in ['update', 'define']:
        root = 'update'
        if action == 'define':
            root = 'create'
        root_element = doc.createElement(root)
        if params.get('parameters'):
            parameter_element = doc.createElement('parameter')
            for parameter in params.get('parameters'):
                for key, value in parameter.items():
                    parameter_element.setAttribute(key, value)
            root_element.appendChild(parameter_element)
        if params.get('attributes'):
            attribute_element = doc.createElement('attributes')
            for attribute in params.get('attributes'):
                for key, value in attribute.items():
                    attribute_element.setAttribute(key, value)
            root_element.appendChild(attribute_element)
        request_element.appendChild(root_element)
    # return doc.data
    return doc.toxml()


def get_cmci_url(params):
    if params.get('security_type') == 'none':
        scheme = 'http://'
    else:
        scheme = 'https://'
    url = scheme + params.get('cmci_host') + ':' + params.get('cmci_port') + '/CICSSystemManagement/' + params.get('type') + '/' + params.get('context') + '/'
    if params.get('scope'):
        url = url + params.get('scope')
    if params.get('option') != 'define':
        # get, delete, put will all need CRITERIA
        if params.get('option') == 'query':
            if params.get('record_count'):
                url = url + '//' + str(params.get('record_count'))
        if params.get('filter'):
            url = url + '?'
            flt = params.get('filter')
            see_criteria = False
            for i in flt:
                for key, value in i.items():
                    if value and key == 'criteria':
                        url = url + 'CRITERIA=(' + value + ')'
                        see_criteria = True
                    if value and key == 'parameter':
                        if(see_criteria):
                            url = url + '&'
                        url = url + 'PARAMETER=' + value
    return url


def validate_module_params(params):
    r = "^((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.)"
    r += "{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|((([a-zA-Z0-9]|[a-zA-Z0-9]"
    r += "[a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*"
    r += "[A-Za-z0-9]))$"
    regex_ip_or_host = r
    regex_port = "^([0-9]|[1-9]\\d{1,3}|[1-5]\\d{4}|6[0-4]\\d{3}|65[0-4]\\d{2}|"
    regex_port += "655[0-2]\\d|6553[0-5])$"
    regex_context = "^([A-Za-z0-9]{1,8})$"
    regex_scope = "^([A-Za-z0-9]{1,8})$"
    regex_pair = {"cmci_host": regex_ip_or_host,
                  "cmci_port": regex_port,
                  "context": regex_context,
                  "scope": regex_scope}
    for k, regex in regex_pair.items():
        value = params.get(k)
        validate_parameters_based_on_regex(str(value), regex)


def validate_parameters_based_on_regex(value, regex):
    pattern = re.compile(regex)
    if pattern.fullmatch(value):
        pass
    else:
        raise ValidationError(str(value))
    return value


def handle_module_params(params, result):
    # if params.get('record_count') and params.get('option') != 'query':
    #     result['warnings'].append('"record_count" will be ignored it is only
    #  work with option "query" ')
    parameters = {}
    for key, value in params.items():
        if key == 'resource':
            resource = params.get('resource')
            for i in resource:
                for k, v in i.items():
                    parameters[k] = v
        else:
            parameters[key] = value
    method_action_pair = {'define': 'post', 'install': 'put', 'update': 'put', 'delete': 'delete', 'query': 'get'}
    for key, value in method_action_pair.items():
        if params.get('option') == key:
            parameters['method'] = value
    return parameters


def handle_api_response(api_response):
    # to delete the namespace info in api_response
    str_api_response = str(api_response)
    pattern = re.compile(r'(|@)\{http:\/\/www.ibm.com\/xmlns\/prod\/CICS\/smw2int\}')
    new_api_response = re.sub(pattern, "", str_api_response)
    return eval(new_api_response)


def main():
    resource_rule_spec = dict(
        type=dict(type='str', required=True),
        attributes=dict(type='list', elements='dict', required=False),
        parameters=dict(type='list', elements='dict', required=False),
        location=dict(type='str', required=False, choices=['BAS', 'CSD'])
    )

    module = AnsibleModule(
        argument_spec=dict(
            cmci_host=dict(required=True, type='str'),
            cmci_port=dict(required=True, type='str'),
            cmci_user=dict(type='str', no_log=True),
            cmci_password=dict(type='str', no_log=True),
            cmci_cert=dict(type='str', no_log=True),
            cmci_key=dict(type='str', no_log=True),
            security_type=dict(
                type='str',
                default='none',
                choices=[
                    'none',
                    'basic',
                    'certificate'
                ]),
            context=dict(required=True, type='str'),
            scope=dict(type='str'),
            option=dict(
                type='str',
                default='query',
                choices=[
                        'define',
                        'delete',
                        'update',
                        'install',
                        'query'
                ]),
            filter=dict(
                type='list',
                options=dict(
                    criteria=dict(type='str', required=False),
                    parameter=dict(type='str', required=False)
                ),
                elements='dict'
            ),
            record_count=dict(type='int'),
            resource=dict(
                type='list',
                options=resource_rule_spec,
                elements='dict'
            ),
        )
    )
    result = dict(changed=False)
    try:
        validate_module_params(module.params)
        params = handle_module_params(module.params, result)
        # result['parsed_parms'] = params
        method = params.get('method')
        action = params.get('option')
        session = get_connect_session(params)
        url = get_cmci_url(params)
        result['url'] = url
        if params.get('option') in ['query', 'delete']:
            response = handle_request(session, method, url)
        else:
            body = create_xml_body(params)
            # result['body'] = body
            response = handle_request(session, method, url, body)
    except Exception as e:
        module.fail_json(msg=e.msg, **result)
    key1 = "{http://www.ibm.com/xmlns/prod/CICS/smw2int}response"
    key2 = "@{http://www.ibm.com/xmlns/prod/CICS/smw2int}resultsummary"
    if (response.get(key1) and response.get(key1).get(key2) and
            response.get(key1).get(key2).get('api_response1')):
        api_response1 = response.get(key1).get(key2).get('api_response1')
        api_response = response.get(key1).get(key2).get('api_response1_alt')
        result['api_response'] = api_response
        if action == 'query' or api_response1 != '1024':
            result['changed'] = False
        else:
            result['changed'] = True
    result['response'] = handle_api_response(response.get(key1))
    module.exit_json(**result)


if __name__ == '__main__':
    main()

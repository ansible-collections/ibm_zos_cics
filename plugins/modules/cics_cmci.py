#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) IBM Corporation 2019, 2020

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

import re
import traceback

try:
    import requests
except ImportError:
    requests = None
    REQUESTS_IMP_ERR = traceback.format_exc()

try:
    import xmltodict
except ImportError:
    xmltodict = None
    XMLTODICT_IMP_ERR = traceback.format_exc()

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
          - The resource attributes, refer to the CICSPlex SM resource tables
            in the knowledge center to find the possible attributes.
        type: list
        required: false
      parameters:
        description:
          - The resource parameters,refer to the CICSPlex SM resource tables
            in the knowledge center to get the possible parameters.
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
      - Filter values can be case-sensitive, where the value of the target
        attributes are case-sensitive (e.g. TRANID and DESC), though this
        is not true for most attributes.
      - Filter values are not applied when using option `define` 
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


def _create_body(params):
    action = params.get('option')
    if action not in ['install', 'update', 'define']:
        return None

    request = {}
    if action == 'install':
        # TODO: we don't currently validate location is mandatory, so possible it won't be specified,
        #  which we should validate against
        location = params.get('location')
        request['action'] = {'@name': 'INSTALL' if location == 'BAS' else 'CSDINSTALL'}
    elif action == 'update':
        update = {}
        _append_parameters(update, params)
        _append_attributes(update, params)
        request['update'] = update
    elif action == 'define':
        create = {}
        _append_parameters(create, params)
        _append_attributes(create, params)
    document = {"request": request}

    return document


def _append_parameters(element, params):
    # Parameters are <parameters><parameter name="pname" value="pvalue" /></parameters>
    action_parameters = params.get('parameters')
    if action_parameters:
        element['parameter'] = [{'@name': key, '@value': value} for key, value in action_parameters.items()]


def _append_attributes(element, params):
    # Attributes are <attributes name="value" name2="value2"/>
    action_attributes = params.get('attributes')
    if action_attributes:
        element['attributes'] = {'@' + key: value for key, value in action_attributes.items()}


def _validate_module_params(module, result, params):
    r = "^((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.)"
    r += "{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|((([a-zA-Z0-9]|[a-zA-Z0-9]"
    r += "[a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*"
    r += "[A-Za-z0-9]))$"
    regex_ip_or_host = r
    regex_port = "^([0-9]|[1-9]\\d{1,3}|[1-5]\\d{4}|6[0-4]\\d{3}|65[0-4]\\d{2}|"
    regex_port += "655[0-2]\\d|6553[0-5])$"
    regex_context = "^([A-Za-z0-9]{1,8})$"
    regex_scope = "^([A-Za-z0-9]{1,8})$"
    validations = {
        ("cmci_host", regex_ip_or_host, "an IP address or host name."),
        ("cmci_port", regex_port, "a port number 0-65535."),
        (
            "context",
            regex_context,
            "a CPSM context name.  CPSM context names are max 8 characters.  Valid characters are A-Z a-z 0-9."
        ),
        (
            "scope",
            regex_scope,
            "a CPSM scope name.  CPSM scope names are max 8 characters.  Valid characters are A-Z a-z 0-9."
        )
    }

    # TODO: Should probably change this so the validations are lambdas or classes
    for name, regex, message in validations:
        value = str(params.get(name))
        pattern = re.compile(regex)
        if not pattern.fullmatch(value):
            fail(
                module,
                result,
                'Parameter "{0}" with value "{1} was not valid.  Expected {2}'.format(name, value, message)
            )


def _handle_module_params(module):
    parameters = {}
    # TODO: This bit that flattens the params is relied on in the action bit, it's how the parameters get there.
    #  Don't know why it's necessary though, I should fix it!
    #  Is also relied on by the get_url function, which uses 'type' at the top level.  There's nothing that makes
    #  resource mandatory at the moment.
    for key, value in module.params.items():
        if key == 'resource':
            resource = module.params.get('resource')
            for i in resource:
                for k, v in i.items():
                    parameters[k] = v
        else:
            parameters[key] = value
    method_action_pair = {'define': 'post', 'install': 'put', 'update': 'put', 'delete': 'delete', 'query': 'get'}
    for key, value in method_action_pair.items():
        if module.params.get('option') == key:
            parameters['method'] = value
    return parameters


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
                ]
            ),
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
                ]
            ),
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

    if not requests:
        fail_e(module, result, missing_required_lib('requests'), exception=REQUESTS_IMP_ERR)

    if not xmltodict:
        fail_e(module, result, missing_required_lib('encoder'), exception=XMLTODICT_IMP_ERR)

    session, request = _handle_params(module, result)
    response = _do_request(module, result, session, request)
    _handle_response(module, result, response, request.method)
    module.exit_json(**result)


def _handle_params(module, result):
    # TODO: this flattens the params a bit, and sets 'method' amongst other things, get rid of this!
    params = _handle_module_params(module)
    _validate_module_params(module, result, params)
    session = _create_session(module, result, **params)
    url = _get_url(params)
    body = _create_body(params)
    # TODO: can this fail?
    body_xml = xmltodict.unparse(body) if body else None
    request = requests.Request(method=params.get('method'), url=url, data=body_xml).prepare()

    result['request'] = {
        'url': request.url,
        'method': request.method,
        'body': request.body
    }

    return session, request


def _handle_response(module, result, response, method):
    # Try and parse the XML response body into a dict
    content_type = response.headers.get('content-type')
    if content_type != 'application/xml':
        fail(module, result, 'CMCI request returned a non application/xml content type: {0}'.format(content_type))

    # Missing content
    if not response.content:
        fail(module, result, 'CMCI response did not contain any data')

    # Fail the task in the event of a CMCI error
    try:
        # TODO: What exception do we actually get from this? Do I actually need to strip namespaces
        namespaces = {
            'http://www.ibm.com/xmlns/prod/CICS/smw2int': None,
            'http://www.w3.org/2001/XMLSchema-instance': None
        }  # namespace information
        response_dict = xmltodict.parse(response.content, process_namespaces=True, namespaces=namespaces)

        # Attached parsed xml to response
        result['response']['body'] = response_dict

        try:
            result_summary = response_dict['response']['resultsummary']
            cpsm_response = result_summary['@api_response1']

            # Non-OK queries fail the module, except if we get NODATA on a query, when there are no records
            if cpsm_response != '1024' and not (method == 'query' and cpsm_response == '1027'):
                cpsm_response_alt = result_summary['@api_response1_alt']
                cpsm_reason = result_summary['@api_response2']
                fail(module, result, 'CMCI request failed with response "{0}", reason: "{1}"'
                     .format(cpsm_response_alt, cpsm_reason))

            if method != 'GET':
                result['changed'] = True
        except KeyError as e:
            # CMCI response parse error
            fail(module, result, 'Could not parse CMCI response: missing node "{0}"'.format(e.args[0]))

    except xmltodict.expat.ExpatError as e:
        # Content couldn't be parsed as XML
        # TODO: verbose log content if it couldn't be parsed?.  And maybe the other info from the ExpatError
        fail_e(module, result, 'CMCI response XML document could not be successfully parsed: {0}'.format(e), e)


def _get_url(params):  # kwargs to allow us to destructure params when calling
    cmci_host = params.get('cmci_host')
    cmci_port = params.get('cmci_port')
    t = params.get('type')
    context = params.get('context')
    option = params.get('option')
    security_type = params.get('security_type', 'none')
    scope = params.get('scope')
    record_count = params.get('record_count')
    fltr = params.get('filter')

    if security_type == 'none':
        scheme = 'http://'
    else:
        scheme = 'https://'
    url = scheme + cmci_host + ':' + cmci_port + '/CICSSystemManagement/' + t + '/' + context + '/'
    if scope:
        url = url + scope
    if option != 'define':
        # get, delete, put will all need CRITERIA
        if option == 'query':
            if record_count:
                url = url + '//' + str(record_count)
        if fltr:
            url = url + '?'
            see_criteria = False
            for i in fltr:
                for key, value in i.items():
                    if value and key == 'criteria':
                        url = url + 'CRITERIA=(' + value + ')'
                        see_criteria = True
                    if value and key == 'parameter':
                        if see_criteria:
                            url = url + '&'
                        url = url + 'PARAMETER=' + value
    return url


def _create_session(module, result, security_type='none', crt=None, key=None, user=None, pw=None, **kwargs):
    session = requests.Session()
    if security_type == 'certificate':
        if (crt is not None and crt.strip() != '') and (key is not None and key.strip() != ''):
            session.cert = (crt.strip(), key.strip())
        else:
            fail(module, result, 'HTTP setup error: cmci_cert/cmci_key are required ')
    # TODO: there's no clear distinction between unauthenticated HTTPS and authenticated HTTP
    if security_type == 'basic':
        if (user is not None and user.strip() != '') and (pw is not None and pw.strip() != ''):
            session.auth = (user.strip(), pw.strip())
        else:
            fail(module, result, 'HTTP setup error: cmci_user/cmci_password are required')
    return session


def _do_request(module, result, session, request):
    try:
        response = session.send(request, timeout=30, verify=False)
        reason = response.reason if response.reason else response.status_code
        result['response'] = {'status_code': response.status_code, 'reason': reason}

        if response.status_code != 200:
            fail(module, result, 'CMCI request returned non-OK status: {0}'.format(reason))

        return response
    except requests.exceptions.RequestException as e:
        cause = e
        if isinstance(cause, requests.exceptions.ConnectionError):
            cause = cause.args[0]
        if isinstance(cause, requests.packages.urllib3.exceptions.MaxRetryError):
            cause = cause.reason
        fail_e(module, result, 'Error performing CMCI request: {0}'.format(cause), e)


def fail(module, result, msg):
    module.fail_json(msg=msg, **result)


def fail_e(module, result, msg, exception):
    module.fail_json(msg=msg, exception=exception, **result)


if __name__ == '__main__':
    main()

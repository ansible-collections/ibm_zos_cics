#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule, missing_required_lib, env_fallback
from typing import Optional, Dict
from urllib.parse import urlencode, quote
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


CMCI_HOST = 'cmci_host'
CMCI_PORT = 'cmci_port'
CMCI_USER = 'cmci_user'
CMCI_PASSWORD = 'cmci_password'
CMCI_CERT = 'cmci_cert'
CMCI_KEY = 'cmci_key'
SECURITY_TYPE = 'security_type'
CONTEXT = 'context'
SCOPE = 'scope'
PARAMETER = 'parameter'
RESOURCES = 'resources'
TYPE = 'type'
ATTRIBUTES = 'attributes'
PARAMETERS = 'parameters'
NAME = 'name'
VALUE = 'value'
FILTER = 'filter'
COMPLEX_FILTER = 'complex_filter'

attribute_dict = dict(
    type='str',
    required=False
)
operator_dict = dict(
    type='str',
    required=False,
    default='EQ',
    choices=['<', '<=', '=', '>=', '>=', '¬=', '==', '!=', 'EQ', 'NE', 'LT', 'LE', 'GE', 'GT', 'IS']
)
value_dict = dict(
    type='str',
    required=False
)

def _nest_and_or_dicts():
    return _get_and_or_dict(
        _create_and_or_dicts(_create_and_or_dicts(_create_and_or_dicts(_create_and_or_dicts()))))


def _create_and_or_dicts(children={}):
    return {
        'and': _get_and_or_dict(children),
        'or': _get_and_or_dict(children)
    }


def _get_and_or_dict(my_dict={}):
    return {
        'type': 'list',
        'required': False,
        'elements': 'dict',
        'options': {
            'attribute': attribute_dict,
            'operator': operator_dict,
            'value': value_dict,
            **my_dict
        },
        'required_together': [('attribute', 'value')]
    }

RESOURCES_ARGUMENT = {
    RESOURCES: {
        'type': 'dict',
        'required': False,
        'options': {
            FILTER: {
                'type': 'dict',
                'required': False
            },
            COMPLEX_FILTER: {
                'type': 'dict',
                'required': False,
                'options': {
                    'attribute': attribute_dict,
                    'operator': operator_dict,
                    'value': value_dict,
                    'and': _nest_and_or_dicts(),
                    'or': _nest_and_or_dicts()
                },
                'required_together': '[(\'attribute\', \'value\')]'
            },
            PARAMETER: {
                'type': 'str',
                'required': False
            }
        }
    }
}

PARAMETERS_ARGUMENT = {
    PARAMETERS: {
        'type': 'list',
        'required': False,
        'elements': 'dict',
        'options': {
            NAME: {
                'type': 'str',
                'required': True
            },
            # Value is not required for flag-type parameters like CSD
            VALUE: {
                'type': 'str'
            }
        }
    }
}

ATTRIBUTES_ARGUMENT = {
    ATTRIBUTES: {
        'type': 'dict',
        'required': False
    }
}


class AnsibleCMCIModule(object):

    def __init__(self, method):
        self._module = AnsibleModule(argument_spec=self.init_argument_spec())  # type: AnsibleModule
        self.result = dict(changed=False)  # type: dict

        if not requests:
            self._fail_tb(missing_required_lib('requests'), REQUESTS_IMP_ERR)

        if not xmltodict:
            self._fail_tb(missing_required_lib('encoder'), XMLTODICT_IMP_ERR)

        self._method = method  # type: str
        self._p = self.init_p()  # type: dict
        self._session = self.init_session()  # type: requests.Session
        self._url = self.init_url()  # type: str
        # TODO: can this fail?
        # full_document=False suppresses the xml prolog, which CMCI doesn't like
        body_dict = self.init_body()
        self._body = xmltodict.unparse(self.init_body(), full_document=False) if body_dict else None  # type: str

        request_params = self.init_request_params()
        if request_params:
            self._url = self._url +\
                        "?" +\
                        urlencode(requests.utils.to_key_val_list(request_params), quote_via=quote)

        result_request = {
            'url': self._url,
            'method': self._method,
            'body': self._body
        }

        self.result['request'] = result_request

    def init_argument_spec(self):  # type: () -> Dict
        return {
            CMCI_HOST: {
                'required': True,
                'type': 'str'
            },
            CMCI_PORT: {
                'required': True,
                'type': int
            },
            CMCI_USER: {
                'type': 'str',
                'fallback': (env_fallback, ['CMCI_USER'])
            },
            CMCI_PASSWORD: {
                'type': 'str',
                'no_log': True,
                'fallback': (env_fallback, ['CMCI_PASSWORD'])
            },
            CMCI_CERT: {
                'type': 'str',
                'no_log': True,
                'fallback': (env_fallback, ['CMCI_CERT'])
            },
            CMCI_KEY: {
                'type': 'str',
                'no_log': True,
                'fallback': (env_fallback, ['CMCI_KEY'])
            },
            SECURITY_TYPE: {
                'type': 'str',
                'default': 'none',
                'choices': ['none', 'basic', 'certificate']
            },
            CONTEXT: {
                'required': True,
                'type': 'str'
            },
            SCOPE: {
                'type': 'str'
            },
            TYPE: {
                'type': 'str',
                'required': True
            }
        }

    def main(self):
        response = self._do_request()  # type: Dict
        self.handle_response(response)
        self._module.exit_json(**self.result)

    def init_p(self):
        self.validate(
            CMCI_HOST,
            '^((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.)'
            '{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|((([a-zA-Z0-9]|[a-zA-Z0-9]'
            '[a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*'
            '[A-Za-z0-9]))$',
            'an IP address or host name.'
        )

        port = self._module.params.get(CMCI_PORT)
        if port < 0 or port > 65535:
            self._fail(
                'Parameter "{0}" with value "{1}" was not valid.  Expected a port number 0-65535.'
                .format(CMCI_PORT, str(port)))

        self.validate(
            CONTEXT,
            '^([A-Za-z0-9]{1,8})$',
            'a CPSM context name.  CPSM context names are max 8 characters.  Valid characters are A-Z a-z 0-9.'
        )

        self.validate(
            SCOPE,
            '^([A-Za-z0-9]{1,8})$',
            'a CPSM scope name.  CPSM scope names are max 8 characters.  Valid characters are A-Z a-z 0-9.'
        )

        return self._module.params

    def validate(self, name, regex, message):  # type: (str, str, str) -> None
        value = self._module.params.get(name)
        if value:
            pattern = re.compile(regex)
            if not pattern.fullmatch(value):
                self._fail('Parameter "{0}" with value "{1}" was not valid.  Expected {2}'.format(name, value, message))

    def init_body(self):  # type: () -> Optional[Dict]
        return None

    def handle_response(self, response_dict):  # type: (Dict) -> None
        try:
            response_node = response_dict['response']

            self.result['connect_version'] = response_node.get('@connect_version')

            result_summary = response_node['resultsummary']
            cpsm_response_code = int(result_summary['@api_response1'])
            cpsm_response = result_summary['@api_response1_alt']
            cpsm_reason = result_summary['@api_response2_alt']
            cpsm_reason_code = int(result_summary['@api_response2'])

            self.result['cpsm_response'] = cpsm_response
            self.result['cpsm_response_code'] = cpsm_response_code
            self.result['cpsm_reason'] = cpsm_reason
            self.result['cpsm_reason_code'] = cpsm_reason_code

            if '@recordcount' in result_summary:
                self.result['record_count'] = int(result_summary['@recordcount'])

            if '@successcount' in result_summary:
                self.result['success_count'] = int(result_summary['@successcount'])

            # TODO: maybe only allow this bit in results that will definitely include records
            if 'records' in response_node:
                records_node = response_node['records']
                resource_type = self._p[TYPE].lower()
                if resource_type in records_node:
                    records = records_node[resource_type]
                    # Copy records in result, stripping @ from attributes
                    self.result['records'] =\
                        [
                            {k[1:]: v for k, v in record.items()}
                            for record in records
                        ]

            # Non-OK CPSM responses fail the module
            if cpsm_response_code != 1024:
                self._fail('CMCI request failed with response "{0}" reason "{1}"'.format(
                        cpsm_response, cpsm_reason if cpsm_reason else cpsm_response_code
                ))

            if self._method != 'GET':
                self.result['changed'] = True
        except KeyError as e:
            # CMCI response parse error
            self._fail('Could not parse CMCI response: missing node "{0}"'.format(e.args[0]))

    def init_url(self):  # type: () -> str
        t = self._p.get(TYPE).lower()
        security_type = self._p.get(SECURITY_TYPE)

        if security_type == 'none':
            scheme = 'http://'
        else:
            scheme = 'https://'
        url = scheme + self._p.get(CMCI_HOST) + ':' + str(self._p.get(CMCI_PORT)) + '/CICSSystemManagement/'\
            + t + '/' + self._p.get(CONTEXT) + '/'
        if self._p.get(SCOPE):
            url = url + self._p.get(SCOPE)

        return url

    def init_request_params(self):  # type: () -> Optional[Dict[str, str]]
        return None

    def get_resources_request_params(self):  # type: () -> Dict[str, str]
        # get, delete, put will all need CRITERIA{}
        request_params = {}
        resources = self._p.get(RESOURCES)
        if resources:
            filter = resources.get(FILTER)
            if filter:
                # AND basic filters together, and use the = operator for each one
                filter_string = ''
                if not request_params:
                    request_params = {}
                for key, value in filter.items():
                    filter_string = _append_filter_string(filter_string, key + '=' + '\'' + value + '\'',
                                                          joiner=' AND ')
                request_params['CRITERIA'] = filter_string

            complex_filter = resources.get(COMPLEX_FILTER)
            if complex_filter:
                complex_filter_string = ''
                if not request_params:
                    request_params = {}

                and_item = complex_filter['and']
                or_item = complex_filter['or']
                attribute_item = complex_filter['attribute']

                if ((and_item is not None and or_item is not None) or
                    (or_item is not None and attribute_item is not None) or
                    (attribute_item is not None and and_item is not None)):
                    self._fail("complex_filter can only have 'and', 'or', or 'attribute' dictionaries at the top level")

                if and_item is not None:
                    complex_filter_string = _get_filter(and_item, complex_filter_string, ' AND ')

                if or_item is not None:
                    complex_filter_string = _get_filter(or_item, complex_filter_string, ' OR ')

                if attribute_item is not None:
                    operator = _convert_filter_operator(complex_filter['operator'])
                    value = complex_filter['value']
                    complex_filter_string = _append_filter_string(complex_filter_string,
                                                                  attribute_item + operator + '\'' + value + '\'')

                request_params['CRITERIA'] = complex_filter_string

            if resources.get(PARAMETER):
                request_params['PARAMETER'] = resources.get(PARAMETER)

        return request_params

    def init_session(self):  # type: () -> requests.Session
        session = requests.Session()
        security_type = self._p.get(SECURITY_TYPE)
        if security_type == 'certificate':
            cmci_cert = self._p.get(CMCI_CERT)
            cmci_key = self._p.get(CMCI_KEY)
            if cmci_cert is not None and cmci_cert.strip() != '' and cmci_key is not None and cmci_key.strip() != '':
                session.cert = cmci_cert.strip(), cmci_key.strip()
            else:
                self._fail('HTTP setup error: cmci_cert/cmci_key are required ')
        # TODO: there's no clear distinction between unauthenticated HTTPS and authenticated HTTP
        if security_type == 'basic':
            cmci_user = self._p.get(CMCI_USER)
            cmci_password = self._p.get(CMCI_PASSWORD)
            if cmci_user is not None and cmci_user.strip() != '' and \
                    cmci_password is not None and cmci_password.strip() != '':
                session.auth = cmci_user.strip(), cmci_password.strip()
            else:
                self._fail('HTTP setup error: cmci_user/cmci_password are required')
        return session  # type: requests.Session

    def _do_request(self):  # type: () -> Dict
        try:
            response = self._session.request(
                self._method,
                self._url,
                verify=False,
                timeout=30,
                data=self._body
            )

            self.result['http_status_code'] = response.status_code
            self.result['http_status'] = response.reason if response.reason else str(response.status_code)

            # TODO: in OK responses CPSM sometimes returns error feedback information.

            # TODO: in non-OK responses CPSM returns a body with error information
            #  Can recreate this by supplying a malformed body with a create request.
            #  We should surface this error information somehow.  Not sure what content type we get.
            if response.status_code != 200:
                # TODO: <?xml version=\"1.0\" encoding=\"UTF-8\"?> \r\n<error message_id=\"DFHWU4007\" connect_version=
                #  \"0560\">\r\n\t<title> 400 CICS management client interface HTTP Error</title>\r\n\t<short>An error
                #  has occurred in the CICS management client interface. The request cannot be processed.</short>\r\n\t
                #  <full> The body of the HTTP request was not specified correctly.</full> \r\n</error>
                #  This sort of thing's probably relevant for warning count errors too
                self._fail('CMCI request returned non-OK status: {0}'.format(self.result.get('http_status')))

            # Try and parse the XML response body into a dict
            content_type = response.headers.get('content-type')
            # Content type header may include the encoding.  Just look at the first segment if so
            content_type = content_type.split(';')[0]
            if content_type != 'application/xml':
                self._fail('CMCI request returned a non application/xml content type: {0}'.format(content_type))

            # Missing content
            if not response.content:
                self._fail('CMCI response did not contain any data')

            namespaces = {
                'http://www.ibm.com/xmlns/prod/CICS/smw2int': None,
                'http://www.w3.org/2001/XMLSchema-instance': None
            }  # namespace information

            r = xmltodict.parse(
                response.content,
                process_namespaces=True,
                namespaces=namespaces,
                # Make sure we always return a list for the resource node
                force_list=(self._p.get(TYPE).lower(),)
            )

            return r
        except requests.exceptions.RequestException as e:
            cause = e
            if isinstance(cause, requests.exceptions.ConnectionError):
                cause = cause.args[0]
            if isinstance(cause, requests.packages.urllib3.exceptions.MaxRetryError):
                cause = cause.reason
            # Can't use self._fail_tb here, because we'll end up with tb for RequestException, not the cause
            #  which invalidates our attempts to clean up the message
            self._fail('Error performing CMCI request: {0}'.format(cause))
        except xmltodict.expat.ExpatError as e:
            # Content couldn't be parsed as XML
            self._fail_tb(
                'CMCI response XML document could not be successfully parsed: {0}'.format(e),
                traceback.format_exc()
            )

    def append_parameters(self, element):
        # Parameters are <parameter name="pname" value="pvalue" />
        parameters = self._p.get(PARAMETERS)
        if parameters:
            ps = []
            for p in parameters:
                np = {'@name': p.get('name')}
                value = p.get('value')
                if value:
                    np['@value'] = value
                ps.append(np)
            element['parameter'] = ps

    def append_attributes(self, element):
        # Attributes are <attributes name="value" name2="value2"/>
        attributes = self._p.get(ATTRIBUTES)
        if attributes:
            element['attributes'] = {'@' + key: value for key, value in attributes.items()}

    def _fail(self, msg):  # type: (str) -> None
        self._module.fail_json(msg=msg, **self.result)

    def _fail_tb(self, msg, tb):  # type: (str, str) -> None
        self._module.fail_json(msg=msg, exception=tb, **self.result)


def append_attributes_parameters_arguments(argument_spec):
    argument_spec.update({
        ATTRIBUTES: {
            'type': 'dict',
            'required': False
        },
        PARAMETERS: {
            'type': 'list',
            'required': False,
            'elements': 'dict',
            'options': {
                NAME: {
                    'type': 'str',
                    'required': True
                },
                # Value is not required for flag-type parameters like CSD
                VALUE: {
                    'type': 'str'
                }
            }
        }
    })


def append_resources_argument(argument_spec):  # type: (Dict) -> None
    argument_spec.update({
        RESOURCES: {
            'type': 'dict',
            'required': False,
            'options': {
                FILTER: {
                    'type': 'dict',
                    'required': False
                },
                COMPLEX_FILTER: {
                    'type': 'dict',
                    'required': False,
                    'options': {
                        'attribute': attribute_dict,
                        'operator': operator_dict,
                        'value': value_dict,
                        'and': _nest_and_or_dicts(),
                        'or': _nest_and_or_dicts()
                    },
                    'required_together': '[(\'attribute\', \'value\')]'
                },
                PARAMETER: {
                    'type': 'str',
                    'required': False
                }
            }
        }
    })


def append_parameters(element, parameters):
    # Parameters are <parameter name="pname" value="pvalue" />
    if parameters:
        ps = []
        for p in parameters:
            np = {'@name': p.get('name')}
            value = p.get('value')
            if value:
                np['@value'] = value
            ps.append(np)
        element['parameter'] = ps


def append_attributes(element, attributes):
    # Attributes are <attributes name="value" name2="value2"/>
    if attributes:
        element['attributes'] = {'@' + key: value for key, value in attributes.items()}


def _convert_filter_operator(operator):
    if operator in ['<', 'LT']: return '<'
    if operator in ['<=', 'LE']: return '<='
    if operator in ['=', 'EQ']: return '='
    if operator in ['>=', 'GE']: return '>='
    if operator in ['>', 'GT']: return '>'
    if operator in ['¬=', '!=', 'NE']: return '¬='
    if operator in ['==', 'IS']: return '=='


def _get_filter(list_of_filters, complex_filter_string, joiner):
    for i in list_of_filters:
        and_item = _safe_get_dict(i, 'and')
        or_item = _safe_get_dict(i, 'or')
        attribute = _safe_get_dict(i, 'attribute')

        if and_item is not None:
            and_filter_string = _get_filter(and_item, '', ' AND ')
            complex_filter_string = _append_filter_string(complex_filter_string, and_filter_string, joiner)
        if or_item is not None:
            or_filter_string = _get_filter(or_item, '', ' OR ')
            complex_filter_string = _append_filter_string(complex_filter_string, or_filter_string, joiner)
        if attribute is not None:
            operator = _convert_filter_operator(i['operator'])
            value = i['value']
            attribute_filter_string = attribute + operator + '\'' + value + '\''
            complex_filter_string = _append_filter_string(complex_filter_string, attribute_filter_string, joiner)

    return complex_filter_string


def _safe_get_dict(list, key):
    try:
        return list[key]
    except KeyError:
        return None


def _append_filter_string(existing_filter_string, filter_string_to_append, joiner=' AND '):
    # joiner is ' AND ' or ' OR '
    if not existing_filter_string:
        # if the existing string is empty, just return the new filter string
        return '(' + filter_string_to_append + ')'
    if existing_filter_string.endswith(joiner):
        return existing_filter_string + '(' + filter_string_to_append + ')'
    else:
        return existing_filter_string + joiner + '(' + filter_string_to_append + ')'
# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule, missing_required_lib,\
    env_fallback
from typing import Optional, Dict, Any, List
from collections import OrderedDict
from sys import version_info
import re
import traceback
import urllib

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
CONTEXT = 'context'
SCOPE = 'scope'
RESOURCES = 'resources'
TYPE = 'type'
ATTRIBUTES = 'attributes'
NAME = 'name'
VALUE = 'value'
FILTER = 'filter'
COMPLEX_FILTER = 'complex_filter'
SCHEME = 'scheme'
INSECURE = 'insecure'

GET_PARAMETERS = 'get_parameters'


def parameters_argument(name):  # type: (str) -> Dict[str, Any]
    return {
        name: {
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


OPERATORS = ['<', '<=', '=', '>', '>=', '¬=', '==', '!=', 'EQ', 'NE', 'LT',
             'LE', 'GE', 'GT', 'IS']

ATTRIBUTE = 'attribute'
AND = 'and'
OR = 'or'
OPERATOR = 'operator'

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
                'required_together': [
                    (ATTRIBUTE, VALUE)
                ],
                'required_one_of': [
                    (ATTRIBUTE, AND, OR)
                ],
                'required_by': {
                    OPERATOR: ATTRIBUTE
                },
                'mutually_exclusive': [
                    (ATTRIBUTE, AND, OR)
                ],
                'options': {
                    ATTRIBUTE: {
                        'type': 'str',
                        'required': False
                    },
                    OPERATOR: {
                        'type': 'str',
                        'required': False,
                        'choices': OPERATORS
                    },
                    VALUE: {
                        'type': 'str',
                        'required': False
                    },
                    AND: {
                        'type': 'list',
                        'elements': 'dict',
                        'required': False
                    },
                    OR: {
                        'type': 'list',
                        'elements': 'dict',
                        'required': False
                    }
                }
            },
            GET_PARAMETERS:
                parameters_argument(GET_PARAMETERS).get(GET_PARAMETERS)
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
        self._module = AnsibleModule(
            argument_spec=self.init_argument_spec(),
            required_together=[
                (CMCI_USER, CMCI_PASSWORD),
                (CMCI_CERT, CMCI_KEY)
            ]
        )  # type: AnsibleModule
        self.result = dict(changed=False)  # type: dict

        if not requests:
            self._fail_tb(missing_required_lib('requests'), REQUESTS_IMP_ERR)

        if not xmltodict:
            self._fail_tb(missing_required_lib('encoder'), XMLTODICT_IMP_ERR)

        self._method = method  # type: str
        self._p = self.init_p()  # type: dict
        self._session = self.init_session()  # type: requests.Session
        self._url = self.init_url()  # type: str

        # full_document=False suppresses the xml prolog, which CMCI doesn't like
        body_dict = self.init_body()
        self._body = xmltodict.unparse(self.init_body(), full_document=False)\
            if body_dict else None  # type: str

        request_params = self.init_request_params()

        if request_params:
            if version_info.major <= 2:
                # This is a workaround for python 2, where we can't specify the
                # encoding as a parameter in urlencode. Store the quote_plus
                # setting, then override it with quote, so that spaces will be
                # encoded as %20 instead of +. Then set the quote_plus value
                # back so we haven't changed the behaviour long term
                default_quote_plus = urllib.quote_plus
                urllib.quote_plus = urllib.quote
                self._url = self._url + \
                    "?" + \
                    urllib.urlencode(
                        requests.utils.to_key_val_list(request_params)
                    )
                urllib.quote_plus = default_quote_plus
            else:
                # If running at python 3 and above
                self._url = self._url + \
                    "?" + \
                    urllib.parse.urlencode(
                        requests.utils.to_key_val_list(request_params),
                        quote_via=urllib.parse.quote
                    )

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
                'type': 'int'
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
            },
            SCHEME: {
                'type': 'str',
                'choices': ['http', 'https'],
                'default': 'https'
            },
            INSECURE: {
                'type': 'bool',
                'default': False
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
            '{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|'
            '((([a-zA-Z0-9]|[a-zA-Z0-9]'
            '[a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*'
            '([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*'
            '[A-Za-z0-9]))$',
            'an IP address or host name.'
        )

        port = self._module.params.get(CMCI_PORT)
        if port < 0 or port > 65535:
            self._fail(
                'Parameter "{0}" with value "{1}" was not valid.  Expected a '
                'port number 0-65535.'
                .format(CMCI_PORT, str(port))
            )

        self.validate(
            CONTEXT,
            '^([A-Za-z0-9]{1,8})$',
            'a CPSM context name.  CPSM context names are max 8 characters. '
            'Valid characters are A-Z a-z 0-9.'
        )

        self.validate(
            SCOPE,
            '^([A-Za-z0-9]{1,8})$',
            'a CPSM scope name. CPSM scope names are max 8 characters. '
            'Valid characters are A-Z a-z 0-9.'
        )

        return self._module.params

    def validate(self, name, regex, message):  # type: (str, str, str) -> None
        value = self._module.params.get(name)
        if value:

            # Emulate python-3.4 re.fullmatch()
            if not re.match(regex, value, flags=0):
                self._fail(
                    'Parameter "{0}" with value "{1}" was not valid. '
                    'Expected {2}'
                    .format(name, value, message)
                )

    def init_body(self):  # type: () -> Optional[Dict]
        return None

    def handle_response(self, response_dict):  # type: (Dict) -> None
        try:
            response_node = response_dict['response']

            self.result['connect_version'] = response_node\
                .get('@connect_version')

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
                self.result['record_count'] = int(
                    result_summary['@recordcount']
                )

            if '@successcount' in result_summary:
                self.result['success_count'] = int(
                    result_summary['@successcount']
                )

            if 'records' in response_node:
                records_node = response_node['records']
                resource_type = self._p[TYPE].lower()
                if resource_type in records_node:
                    records = records_node[resource_type]
                    # Copy records in result, stripping @ from attributes
                    self.result['records'] = [
                        {k[1:]: v for k, v in record.items()}
                        for record in records
                    ]

            # Non-OK CPSM responses fail the module
            if cpsm_response_code != 1024:
                self._fail(
                    'CMCI request failed with response "{0}" reason "{1}"'
                    .format(
                        cpsm_response,
                        cpsm_reason if cpsm_reason else cpsm_response_code
                    )
                )

            if self._method != 'GET':
                self.result['changed'] = True
        except KeyError as e:
            # CMCI response parse error
            self._fail(
                'Could not parse CMCI response: missing node "{0}"'
                .format(e.args[0])
            )

    def init_url(self):  # type: () -> str
        t = self._p.get(TYPE).lower()
        url = self._p.get(SCHEME) + \
            '://' + \
            self._p.get(CMCI_HOST) + \
            ':' + \
            str(self._p.get(CMCI_PORT)) + \
            '/CICSSystemManagement/' + \
            t + \
            '/' + \
            self._p.get(CONTEXT) + '/'
        if self._p.get(SCOPE):
            url = url + self._p.get(SCOPE)

        return url

    def init_request_params(self):  # type: () -> Optional[Dict[str, str]]
        return None

    # TODO: why do we have this and/or parsing twice?
    def get_resources_request_params(self):  # type: () -> Dict[str, str]
        # get, delete, put will all need CRITERIA{}
        request_params = OrderedDict({})
        resources = self._p.get(RESOURCES)
        if resources:
            f = resources.get(FILTER)
            if f:
                # AND basic filters together and use the = operator for each one
                filter_string = ''
                if not request_params:
                    request_params = OrderedDict({})
                for key, value in f.items():
                    filter_string = _append_filter_string(
                        filter_string,
                        key + '=' + '\'' + value + '\'',
                        joiner=' AND '
                    )
                request_params['CRITERIA'] = filter_string

            complex_filter = resources.get(COMPLEX_FILTER)
            if complex_filter:
                complex_filter_string = ''
                if not request_params:
                    request_params = OrderedDict({})

                and_item = complex_filter[AND]
                or_item = complex_filter[OR]
                attribute_item = complex_filter[ATTRIBUTE]

                if and_item is not None:
                    complex_filter_string = self._get_filter(
                        and_item,
                        complex_filter_string,
                        ' AND ',
                        ' -> ' + AND
                    )

                if or_item is not None:
                    complex_filter_string = self._get_filter(
                        or_item,
                        complex_filter_string,
                        ' OR ',
                        ' -> ' + OR
                    )

                if attribute_item is not None:
                    operator = self._convert_filter_operator(
                        complex_filter[OPERATOR],
                        ""
                    )
                    value = complex_filter[VALUE]

                    if operator == '¬=':
                        # Provides a filter string in the format NOT(FOO=='BAR')
                        complex_filter_string = _append_filter_string(
                            complex_filter_string,
                            'NOT('
                            + attribute_item + '==' + '\'' + value + '\''
                            + ')'
                        )
                    else:
                        complex_filter_string = _append_filter_string(
                            complex_filter_string,
                            attribute_item + operator + '\'' + value + '\''
                        )

                request_params['CRITERIA'] = complex_filter_string

            parameters = resources.get(GET_PARAMETERS)
            if parameters:
                def mapper(p):
                    return p.get('name') + '(' + p.get('value') + ')'\
                        if p.get('value') else p.get('name')

                request_params['PARAMETER'] = ' '.join(map(mapper, parameters))
        return request_params

    def init_session(self):  # type: () -> requests.Session
        session = requests.Session()

        # Try cert auth first
        cmci_cert = self._p.get(CMCI_CERT)
        cmci_key = self._p.get(CMCI_KEY)
        if cmci_cert is not None \
                and cmci_cert.strip() != '' \
                and cmci_key is not None \
                and cmci_key.strip() != '':
            if self._p.get(SCHEME) == 'http':
                self._fail(
                    'scheme can not be set to http '
                    'if you are using certificate auth'
                )
            session.cert = cmci_cert.strip(), cmci_key.strip()
        else:
            # If we didn't get valid cert info, try basic auth
            user = self._p.get(CMCI_USER)
            passwd = self._p.get(CMCI_PASSWORD)
            if user is not None \
                    and user.strip() != '' \
                    and passwd is not None \
                    and passwd.strip() != '':
                session.auth = user.strip(), passwd.strip()

        return session

    def _do_request(self):  # type: () -> Dict
        try:
            response = self._session.request(
                self._method,
                self._url,
                verify=not self._p[INSECURE],
                timeout=30,
                data=self._body
            )

            self.result['http_status_code'] = response.status_code
            self.result['http_status'] = response.reason \
                if response.reason else str(response.status_code)

            if response.status_code != 200:
                self._fail(
                    'CMCI request returned non-OK status: {0}'
                    .format(self.result.get('http_status'))
                )

            # Try and parse the XML response body into a dict
            content_type = response.headers.get('content-type')
            # Content type header may include the encoding.
            # Just look at the first segment if so
            content_type = content_type.split(';')[0]
            if content_type != 'application/xml':
                self._fail(
                    'CMCI request returned a non application/xml content type:'
                    ' {0}'
                    .format(content_type)
                )

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
            if isinstance(
                    cause, requests.packages.urllib3.exceptions.MaxRetryError):
                cause = cause.reason
            # Can't use self._fail_tb here, because we'll end up with tb for
            # RequestException, not the cause which invalidates our attempts to
            # clean up the message
            self._fail('Error performing CMCI request: {0}'.format(cause))
        except xmltodict.expat.ExpatError as e:
            # Content couldn't be parsed as XML
            self._fail_tb(
                'CMCI response XML document could not be successfully parsed: '
                '{0}'
                .format(e),
                traceback.format_exc()
            )

    def append_parameters(self, name, element):
        # type: (str, OrderedDict) -> None
        # Parameters are <parameter name="pname" value="pvalue" />
        parameters = self._p.get(name)
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
            items = attributes.items()
            element['attributes'] = OrderedDict(
                {'@' + key: value for key, value in items}
            )

    def _get_filter(self, list_of_filters, complex_filter_string, joiner, path):
        #  type: (List[Dict], str, str, str) -> str

        if not isinstance(list_of_filters, list):
            self._fail(
                "nested filters must be a list, was: %s found in "
                "resources -> complex_filter%s"
                % (type(list_of_filters), path)
            )
        for i in list_of_filters:
            if not isinstance(i, dict):
                self._fail(
                    "nested filter must be of type dict, was: %s found in "
                    "resources -> complex_filter%s" % (type(i), path)
                )

            valid_keys = [AND, ATTRIBUTE, OPERATOR, OR, VALUE]
            diff = set(i.keys()) - set(valid_keys)
            if len(diff) != 0:
                self._fail(
                    "Unsupported parameters for (basic.py) module: %s found"
                    " in resources -> complex_filter%s. Supported parameters "
                    "include: %s"
                    % (", ".join(diff), path, ", ".join(valid_keys))
                )

            # Validate required_one_of
            and_item = i.get(AND)
            or_item = i.get(OR)
            attribute = i.get(ATTRIBUTE)

            if not and_item and not or_item and not attribute:
                self._fail(
                    "one of the following is required: %s found"
                    " in resources -> complex_filter%s"
                    % (", ".join([ATTRIBUTE, AND, OR]), path)
                )

            # Validate required_by
            op = i.get(OPERATOR)

            if op and not attribute:
                self._fail(
                    "missing parameter(s) required by '%s': %s"
                    % (OPERATOR, ATTRIBUTE)
                )

            value = i.get(VALUE)

            if (value and not attribute) or (attribute and not value):
                self._fail(
                    'parameters are required together: %s, %s found in '
                    'resources -> complex_filter%s'
                    % (ATTRIBUTE, VALUE, path)
                )

            # Validate mutually exclusive parameters
            if (and_item and or_item) or (and_item and attribute) or \
                    (or_item and attribute):
                self._fail(
                    'parameters are mutually exclusive: %s|%s|%s found in '
                    'resources -> complex_filter%s' % (ATTRIBUTE, AND, OR, path)
                )

            if and_item is not None:
                and_filter_string = self._get_filter(
                    and_item,
                    '',
                    ' AND ',
                    '%s -> %s' % (path, AND)
                )
                complex_filter_string = _append_filter_string(
                    complex_filter_string,
                    and_filter_string, joiner
                )
            if or_item is not None:
                or_filter_string = self._get_filter(
                    or_item,
                    '',
                    ' OR ',
                    '%s -> %s' % (path, OR)
                )
                complex_filter_string = _append_filter_string(
                    complex_filter_string,
                    or_filter_string, joiner
                )
            if attribute is not None:
                operator = self._convert_filter_operator(op, path)

                # Validate attribute type
                if not isinstance(attribute, str):
                    self._fail(
                        "%s must be of type str, was: %s found in "
                        "resources -> complex_filter%s"
                        % (ATTRIBUTE, type(attribute), path)
                    )

                # Validate value type
                if not isinstance(value, str):
                    self._fail(
                        "%s must be of type str, was: %s found in "
                        "resources -> complex_filter%s"
                        % (VALUE, type(value), path)
                    )

                if operator == '¬=':
                    # Provides a filter string in the format NOT(FOO=='BAR')
                    attribute_filter_string = \
                        'NOT(' + attribute + '==' + '\'' + value + '\'' + ')'
                else:
                    attribute_filter_string = \
                        attribute + operator + '\'' + value + '\''

                complex_filter_string = _append_filter_string(
                    complex_filter_string,
                    attribute_filter_string,
                    joiner
                )

        return complex_filter_string

    def _convert_filter_operator(self, operator, path):
        if operator in ['<', 'LT']:
            return '<'
        if operator in ['<=', 'LE']:
            return '<='
        if operator in ['=', 'EQ', None]:
            return '='
        if operator in ['>=', 'GE']:
            return '>='
        if operator in ['>', 'GT']:
            return '>'
        if operator in ['¬=', '!=', 'NE']:
            return '¬='
        if operator in ['==', 'IS']:
            return '=='
        self._fail(
            'value of operator must be one of: %s, got: %s found in '
            'resources -> complex_filter%s'
            % (", ".join(OPERATORS), operator, path)
        )

    def _fail(self, msg):  # type: (str) -> None
        self._module.fail_json(msg=msg, **self.result)

    def _fail_tb(self, msg, tb):  # type: (str, str) -> None
        self._module.fail_json(msg=msg, exception=tb, **self.result)


def _append_filter_string(existing, to_append, joiner=' AND '):
    # joiner is ' AND ' or ' OR '
    if not existing:
        # if the existing string is empty, just return the new filter string
        return '(' + to_append + ')'
    if existing.endswith(joiner):
        return existing + '(' + to_append + ')'
    else:
        return existing + joiner + '(' + to_append + ')'

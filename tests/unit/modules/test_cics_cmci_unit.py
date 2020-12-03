# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes
import pytest
import json
import re
import unittest
import xmltodict
from collections import OrderedDict
from plugins.modules import cics_cmci
from requests import PreparedRequest

CONTEXT = 'CICSEX56'
SCOPE = 'IYCWEMW2'
HOST = 'winmvs2c.hursley.ibm.com'
PORT = '26040'


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""
    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""
    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


class CMCITestHelper:
    def __init__(self, requests_mock=None):
        self.requests_mock = requests_mock
        self.expected = {}

    def stub_request(self, *args, complete_qs=True, **kwargs):
        self.requests_mock.request(*args, complete_qs=complete_qs, **kwargs)

    def stub_get_records(self, resource_type, records, *args, **kwargs):
        return self.stub_cmci('GET', resource_type, *args, records=records, **kwargs)

    def stub_create_record(self, resource_type, record, **kwargs):
        return self.stub_cmci('POST', resource_type, records=[record], **kwargs)

    def stub_update_record(self, resource_type, record, **kwargs):
        return self.stub_cmci('PUT', resource_type, records=[record], **kwargs)

    def stub_cmci(self, method, resource_type, scheme='http', host=HOST, port=PORT,
                  context=CONTEXT, scope=None, parameters='', records=None,
                  headers={'CONTENT-TYPE': 'application/xml'}, status_code=200, reason='OK', **kwargs):

        text = create_records_response_xml(resource_type, records) if records else None
        url = '{0}://{1}:{2}/CICSSystemManagement/{3}/{4}{5}{6}'\
            .format(scheme, host, port, resource_type, context, '/' + scope if scope else '', parameters)

        return self.stub_request(
            method,
            url,
            text=text,
            headers=headers,
            status_code=status_code,
            reason=reason,
            **kwargs
        )

    def expect(self, expected):
        self.expected = expected

    def run(self, config):
        set_module_args(config)

        with pytest.raises(AnsibleFailJson if self.expected.get('failed') else AnsibleExitJson) as exc_info:
            cics_cmci.main()

        result = exc_info.value.args[0]

        case = unittest.TestCase()
        case.maxDiff = None
        case.assertDictEqual(self.expected, result)


def create_records_response(resource_type, records):
    return od(
        ('response', od(
            ('@schemaLocation', 'http://www.ibm.com/xmlns/prod/CICS/smw2int '
                                'http://winmvs28.hursley.ibm.com:26040/CICSSystemManagement/schema/'
                                'CICSSystemManagement.xsd'),
            ('@version', '3.0'),
            ('@connect_version', '0560'),
            ('@xmlns', od(
                ('', 'http://www.ibm.com/xmlns/prod/CICS/smw2int'),
                ('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
            )),
            ('resultsummary', od(
                ('@api_response1', '1024'),
                ('@api_response2', '0'),
                ('@api_response_alt', 'OK'),
                ('@api_response2_alt', ''),
                ('@recordcount', str(len(records))),
                ('@displayed_recordcount', str(len(records)))
            )),
            ('records', od(
                (resource_type, records)
            ))
        ))
    )


def create_records_response_xml(resource_type, records):
    return xmltodict.unparse(
        create_records_response(
            resource_type,
            # Convert to ordered dict, with @ sign for attribute prefix
            # Suspect I'll be able to remove this when we switch to a get-specific action
            [OrderedDict([('@' + key, value) for key, value in record.items()]) for record in records])
    )


@pytest.fixture
def cmci_module(requests_mock, monkeypatch):
    monkeypatch.setattr(basic.AnsibleModule, "exit_json", exit_json)
    monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail_json)

    yield CMCITestHelper(requests_mock)


@pytest.fixture
def cmci_module_http(monkeypatch):
    monkeypatch.setattr(basic.AnsibleModule, "exit_json", exit_json)
    monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail_json)

    yield CMCITestHelper()


def body_matcher(expected):
    def match(request: PreparedRequest):
        return expected == xmltodict.parse(request.body)
    return match


def od(*args):
    return OrderedDict(args)


def test_401_fails(cmci_module):
    cmci_module.stub_request(
        'GET',
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/CICSDefinitionBundle/CICPY012/',
        status_code=401,
        reason='Not authorized',
        text='<!doctype html public "-//IETF//DTD HTML 2.0//EN">\n'
             '<html>'
             '<head>'
             '<title>CICS Web Interface error</title>'
             '</head>'
             '<body>'
             '<H1>401 Basic Authentication Error</H1>'
             '</body>'
             '</html>',
        headers={
            'CONTENT-TYPE': 'text/html'
        })

    cmci_module.expect({
        'msg': 'CMCI request returned non-OK status: Not authorized',
        'changed': False,
        'failed': True,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'CICSDefinitionBundle/CICPY012/',
            'method': 'GET',
            'body': None
        },
        'response': {'reason': 'Not authorized', 'status_code': 401}
    })

    # Module config
    cmci_module.run({
        'cmci_host': 'winmvs2c.hursley.ibm.com',
        'cmci_port': '26040',
        'context': 'CICPY012',
        'option': 'query',
        'security_type': 'none',
        'resource': {
            'type': 'CICSDefinitionBundle'
        }
    })


def test_invalid_host(cmci_module):
    cmci_module.expect({
        'msg': 'Parameter "cmci_host" with value "^*.99.99.199 was not valid.  Expected an IP address or host name.',
        'changed': False,
        'failed': True
    })

    cmci_module.run({
        'cmci_host': '^*.99.99.199',
        'cmci_port': '10080',
        'context': 'iyk3z0r9',
        'scope': 'iyk3z0r8',
        'resource': {
            'type': 'cicslocalfile'
        }
    })


def test_invalid_port(cmci_module):
    cmci_module.expect({
        'msg': 'Parameter "cmci_port" with value "^%^080 was not valid.  Expected a port number 0-65535.',
        'changed': False,
        'failed': True
    })

    cmci_module.run({
        'cmci_host': '100.99.99.199',
        'cmci_port': '^%^080',
        'context': 'iyk3z0r9',
        'scope': 'iyk3z0r8',
        'resource': {
            'type': 'cicslocalfile'
        },
    })


def test_invalid_context(cmci_module):
    cmci_module.expect({
        'msg': 'Parameter "context" with value "^&iyk3z0r9 was not valid.  Expected a CPSM context name.  CPSM '
               'context names are max 8 characters.  Valid characters are A-Z a-z 0-9.',
        'changed': False,
        'failed': True
    })

    cmci_module.run({
        'cmci_host': '100.99.99.199',
        'cmci_port': '10080',
        'context': '^&iyk3z0r9',
        'scope': 'iyk3z0r8',
        'resource': {
            'type': 'cicslocalfile'
        },
    })


def test_invalid_scope(cmci_module):
    cmci_module.expect({
        'msg': 'Parameter "scope" with value "&^iyk3z0r8 was not valid.  Expected a CPSM scope name.  CPSM scope '
               'names are max 8 characters.  Valid characters are A-Z a-z 0-9.',
        'changed': False,
        'failed': True
    })
    cmci_module.run({
        'cmci_host': '100.99.99.199',
        'cmci_port': '10080',
        'context': 'iyk3z0r9',
        'scope': '&^iyk3z0r8',
        'resource': {
            'type': 'cicslocalfile'
        },
    })


def test_invalid_security(cmci_module):
    cmci_module.expect({
        'msg': 'value of security_type must be one of: none, basic, certificate, got: yes',
        'failed': True
    })

    cmci_module.run({
        'cmci_host': '100.99.99.199',
        'cmci_port': '10080',
        'context': 'iyk3z0r9',
        'scope': 'iyk3z0r8',
        'security_type': 'yes',
        'resource': {
            'type': 'cicslocalfile'
        },
    })


def test_auth(cmci_module):
    cmci_module.stub_get_records(
        'cicslocalfile',
        [
            {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'},
            {'name': 'bing', 'dsname': 'STEWF.BAT.BAZ'}
        ],
        scope=SCOPE,
        request_headers={
            'authorization': 'Basic Zm9vOmJhcg=='
        },
        scheme='https'
    )

    cmci_module.expect({
        'changed': False,
        'request': {
            'url': 'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicslocalfile/CICSEX56/IYCWEMW2',
            'method': 'GET',
            'body': None
        },
        'response': {
            'body': create_records_response(
                'cicslocalfile',
                [
                    od(
                        ('@name', 'bat'),
                        ('@dsname', 'STEWF.BLOP.BLIP')
                    ),
                    od(
                        ('@name', 'bing'),
                        ('@dsname', 'STEWF.BAT.BAZ')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run({
        'cmci_host': HOST,
        'cmci_port': PORT,
        'cmci_user': 'foo',
        'cmci_password': 'bar',
        'security_type': 'basic',
        'context': CONTEXT,
        'scope': SCOPE,
        'resource': {'type': 'cicslocalfile'},
    })


def test_update(cmci_module):
    cmci_module.stub_update_record(
        'cicsdefinitionprogram',
        dict(
            changeagent='CSDAPI',
            changeagrel='0730',
            csdgroup='DUMMY',
            description='new description',
            name='DUMMY'
        ),
        scope=SCOPE,
        parameters='?CRITERIA=NAME%3DDUMMY&PARAMETER=CSDGROUP%28DUMMY%29',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('update', od(
                    ('parameter', od(
                        ('@name', 'CSD')
                    )),
                    ('attributes', od(
                        ('@description', 'new description')
                    ))
                ))
            ))
        ))
    )

    cmci_module.expect({
        'changed': True,
        'request': {
            'body':
                '<request><update>'
                '<parameter name="CSD"></parameter>'
                '<attributes description="new description"></attributes>'
                '</update></request>',
            'method': 'PUT',
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionprogram/CICSEX56/IYCWEMW2',
            'params': {
                'PARAMETER': 'CSDGROUP(DUMMY)',
                'CRITERIA': 'NAME=DUMMY'
            }
        },
        'response': {
            'body': create_records_response(
                'cicsdefinitionprogram',
                [
                    od(
                        ('@changeagent', 'CSDAPI'),
                        ('@changeagrel', '0730'),
                        ('@csdgroup', 'DUMMY'),
                        ('@description', 'new description'),
                        ('@name', 'DUMMY')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200}
    })

    cmci_module.run(dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope=SCOPE,
        option='update',
        security_type='none',
        resource=dict(
            type='cicsdefinitionprogram',
            parameters=[dict(
                name='CSD'
            )],
            attributes=dict(
                description='new description'
            )
        ),
        criteria='NAME=DUMMY',
        parameter='CSDGROUP(DUMMY)'
    ))


def test_ok_context_scope(cmci_module):
    cmci_module.stub_get_records(
        'cicslocalfile',
        [
            {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'},
            {'name': 'bing', 'dsname': 'STEWF.BAT.BAZ'}
        ],
        scope=SCOPE
    )

    cmci_module.expect({
        'changed': False,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicslocalfile/CICSEX56/IYCWEMW2',
            'method': 'GET',
            'body': None
        },
        'response': {
            'body': create_records_response(
                'cicslocalfile', [
                    od(
                        ('@name', 'bat'),
                        ('@dsname', 'STEWF.BLOP.BLIP')
                    ),
                    od(
                        ('@name', 'bing'),
                        ('@dsname', 'STEWF.BAT.BAZ')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run({
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicslocalfile'},
    })


def test_ok_context_scope_single_record(cmci_module):
    cmci_module.stub_get_records(
        'cicslocalfile',
        [
            {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}
        ],
        scope=SCOPE
    )

    cmci_module.expect({
        'changed': False,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicslocalfile/CICSEX56/IYCWEMW2',
            'method': 'GET',
            'body': None
        },
        'response': {
            'body': create_records_response(
                'cicslocalfile', [
                    od(
                        ('@name', 'bat'),
                        ('@dsname', 'STEWF.BLOP.BLIP')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run({
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicslocalfile'},
    })


def test_ok_context_scope_jvmserver_header(cmci_module):
    cmci_module.stub_get_records(
        'cicslocalfile',
        [
            {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'},
            {'name': 'bing', 'dsname': 'STEWF.BAT.BAZ'}
        ],
        scope=SCOPE,
        headers={
            # JVM server returns a content type with the charset embedded
            'Content-Type': 'application/xml;charset=UTF-8'
        }
    )

    cmci_module.expect({
        'changed': False,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicslocalfile/CICSEX56/IYCWEMW2',
            'method': 'GET',
            'body': None
        },
        'response': {
            'body': create_records_response(
                'cicslocalfile',
                [
                    od(
                        ('@name', 'bat'),
                        ('@dsname', 'STEWF.BLOP.BLIP')
                    ),
                    od(
                        ('@name', 'bing'),
                        ('@dsname', 'STEWF.BAT.BAZ')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run({
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicslocalfile'},
    })


def test_unknown_host(monkeypatch):
    monkeypatch.setattr(basic.AnsibleModule, "exit_json", exit_json)
    monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail_json)

    set_module_args({
        'cmci_host': 'invalid.hursley.ibm.com',
        'cmci_port': '26040',
        'context': 'CICPY012',
        'option': 'query',
        'security_type': 'none',
        'resource': {
            'type': 'CICSDefinitionBundle'
        }
    })

    with pytest.raises(AnsibleFailJson) as exc_info:
        cics_cmci.main()

    exp = \
        'Error performing CMCI request: <[^>]*>: Failed to establish a new connection: '\
        '\\[Errno 8\\] nodename nor servname provided, or not known'
    assert re.match(exp, exc_info.value.args[0]['msg'])


def test_csd_create(cmci_module):
    cmci_module.stub_create_record(
        'cicsdefinitionbundle',
        dict(
            name='bar',
            bundledir='/u/bundles/bloop',
            csdgroup='bat'
        ),
        scope='IYCWEMW2',
        additional_matcher=body_matcher(od(
            ('request', od(
                ('create', od(
                    ('parameter', od(
                        ('@name', 'CSD')
                    )),
                    ('attributes', od(
                        ('@name', 'bar'),
                        ('@bundledir', '/u/bundles/bloop'),
                        ('@csdgroup', 'bat')
                    ))
                ))
            ))
        ))
    )

    cmci_module.expect({
        'changed': True,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicsdefinitionbundle/CICSEX56/IYCWEMW2',
            'method': 'POST',
            'body': '<request><create>'
                    '<parameter name="CSD"></parameter>'
                    '<attributes name="bar" bundledir="/u/bundles/bloop" csdgroup="bat"></attributes>'
                    '</create></request>'
        },
        'response': {
            'body': create_records_response(
                'cicsdefinitionbundle',
                [
                    od(
                        ('@name', 'bar'),
                        ('@bundledir', '/u/bundles/bloop'),
                        ('@csdgroup', 'bat')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(dict(
        cmci_host=HOST,
        cmci_port=PORT,
        context=CONTEXT,
        scope='IYCWEMW2',
        option='define',
        resource=dict(
            type='cicsdefinitionbundle',
            parameters=[dict(
                name='CSD'
            )],
            attributes=dict(
                name='bar',
                bundledir='/u/bundles/bloop',
                csdgroup='bat'
            )
        )
    ))


def test_query_criteria(cmci_module):
    cmci_module.stub_get_records(
        'cicslocalfile',
        [
            {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}
        ],
        scope=SCOPE,
        parameters='?CRITERIA=FOO%3DBAR'
    )

    cmci_module.expect({
        'changed': False,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicslocalfile/CICSEX56/IYCWEMW2',
            'method': 'GET',
            'body': None,
            'params': {'CRITERIA': 'FOO=BAR'}
        },
        'response': {
            'body': create_records_response(
                'cicslocalfile', [
                    od(
                        ('@name', 'bat'),
                        ('@dsname', 'STEWF.BLOP.BLIP')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run({
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicslocalfile'},
        'criteria': 'FOO=BAR'
    })


def test_query_parameter(cmci_module):
    cmci_module.stub_get_records(
        'cicsdefinitionfile',
        [
            {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}
        ],
        scope=SCOPE,
        parameters='?PARAMETER=CSDGROUP%28%2A%29'
    )

    cmci_module.expect({
        'changed': False,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicsdefinitionfile/CICSEX56/IYCWEMW2',
            'method': 'GET',
            'body': None,
            'params': {'PARAMETER': 'CSDGROUP(*)'}
        },
        'response': {
            'body': create_records_response(
                'cicsdefinitionfile', [
                    od(
                        ('@name', 'bat'),
                        ('@dsname', 'STEWF.BLOP.BLIP')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run({
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicsdefinitionfile'},
        'parameter': 'CSDGROUP(*)'
    })


def test_query_parameter_criteria(cmci_module):
    cmci_module.stub_get_records(
        'cicsdefinitionfile',
        [
            {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}
        ],
        scope=SCOPE,
        parameters='?CRITERIA=FOO%3DBAR&PARAMETER=CSDGROUP%28%2A%29'
    )

    cmci_module.expect({
        'changed': False,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicsdefinitionfile/CICSEX56/IYCWEMW2',
            'method': 'GET',
            'body': None,
            'params': {
                'PARAMETER': 'CSDGROUP(*)',
                'CRITERIA': 'FOO=BAR'
            }
        },
        'response': {
            'body': create_records_response(
                'cicsdefinitionfile', [
                    od(
                        ('@name', 'bat'),
                        ('@dsname', 'STEWF.BLOP.BLIP')
                    )
                ]
            ),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run({
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicsdefinitionfile'},
        'parameter': 'CSDGROUP(*)',
        'criteria': 'FOO=BAR'
    })

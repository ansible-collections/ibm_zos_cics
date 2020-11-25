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
    def __init__(self, requests_mock):
        self.requests_mock = requests_mock
        self.expected = {}

    def stub_request(self, *args, **kwargs):
        self.requests_mock.request(*args, **kwargs)

    def stub_get_records(self, resource_type: str, records: [{}], host=HOST,
                         port=PORT, context=CONTEXT, scope='', parameters=''):
        document = {
            'response': {
                '@xmlns': 'http://www.ibm.com/xmlns/prod/CICS/smw2int',
                '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                '@xsi:schemaLocation': 'http://www.ibm.com/xmlns/prod/CICS/smw2int '
                                       'http://winmvs28.hursley.ibm.com:28953/CICSSystemManagement/schema/'
                                       'CICSSystemManagement.xsd',
                '@version': '3.0',
                '@connect_version': '0560',
                'resultsummary': {
                    '@api_response1': '1024',
                    '@api_response2': '0',
                    '@api_response_alt': 'OK',
                    '@api_response2_alt': '',
                    '@recordcount': len(records),
                    '@displayed_recordcount': len(records)
                },
                'records': {
                    # Translate records to use attributes in the rendered xml
                    resource_type.lower(): [{'@' + key: value for key, value in record.items()} for record in records]
                }
            }
        }

        return self.stub_request(
            'GET',
            'http://{0}:{1}/CICSSystemManagement/{2}/{3}{4}{5}'
                .format(host, port, resource_type, context, '/' + scope if scope else '', parameters),
            status_code=200,
            reason='OK',
            headers={
                'CONTENT-TYPE': 'application/xml'
            },
            text=xmltodict.unparse(document)
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
        case.assertDictEqual(result, self.expected)


@pytest.fixture
def cmci_module(requests_mock, monkeypatch):
    monkeypatch.setattr(basic.AnsibleModule, "exit_json", exit_json)
    monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail_json)

    yield CMCITestHelper(requests_mock)


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
        'resource': [{
            'type': 'CICSDefinitionBundle'
        }]
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
        'resource': [{
            'type': 'cicslocalfile'
        }]
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
        'resource': [{
            'type': 'cicslocalfile'
        }],
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
        'resource': [{
            'type': 'cicslocalfile'
        }],
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
        'resource': [{
            'type': 'cicslocalfile'
        }],
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
        'resource': [{
            'type': 'cicslocalfile'
        }],
    })


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
            'body': OrderedDict([
                ('response', OrderedDict([
                    ('@schemaLocation', 'http://www.ibm.com/xmlns/prod/CICS/smw2int '
                                        'http://winmvs28.hursley.ibm.com:28953/CICSSystemManagement/schema/'
                                        'CICSSystemManagement.xsd'),
                    ('@version', '3.0'),
                    ('@connect_version', '0560'),
                    ('@xmlns', OrderedDict([
                        ('', 'http://www.ibm.com/xmlns/prod/CICS/smw2int'),
                        ('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
                    ])),
                    ('resultsummary', OrderedDict([
                        ('@api_response1', '1024'),
                        ('@api_response2', '0'),
                        ('@api_response_alt', 'OK'),
                        ('@api_response2_alt', ''),
                        ('@recordcount', '2'),
                        ('@displayed_recordcount', '2')
                    ])),
                    ('records', OrderedDict([
                        ('cicslocalfile', [
                            OrderedDict([
                                ('@name', 'bat'),
                                ('@dsname', 'STEWF.BLOP.BLIP')
                            ]),
                            OrderedDict([
                                ('@name', 'bing'),
                                ('@dsname', 'STEWF.BAT.BAZ')
                            ])
                        ])
                    ]))
                ]))
            ]),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run({
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': [{'type': 'cicslocalfile'}],
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
        'resource': [{
            'type': 'CICSDefinitionBundle'
        }],
        'filter': [{
            'criteria': 'NAME=PONGALT',
            'parameter': 'CSDGROUP(JVMGRP1)'
        }]
    })

    with pytest.raises(AnsibleFailJson) as exc_info:
        cics_cmci.main()

    exp = \
        'Error performing CMCI request: <[^>]*>: Failed to establish a new connection: '\
        '\\[Errno 8\\] nodename nor servname provided, or not known'
    assert re.match(exp, exc_info.value.args[0]['msg'])
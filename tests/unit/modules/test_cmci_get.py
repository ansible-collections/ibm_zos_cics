# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_get
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, SCOPE, create_records_response, AnsibleFailJson,
    set_module_args, exit_json, fail_json, cmci_module, CMCITestHelper
)
from ansible.module_utils import basic

import pytest
import re


def test_401_fails(cmci_module):  # type: (CMCITestHelper) -> None
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
    cmci_module.run(cmci_get, {
        'cmci_host': 'winmvs2c.hursley.ibm.com',
        'cmci_port': '26040',
        'context': 'CICPY012',
        'security_type': 'none',
        'resource': {
            'type': 'CICSDefinitionBundle'
        }
    })


def test_invalid_host(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'Parameter "cmci_host" with value "^*.99.99.199 was not valid.  Expected an IP address or host name.',
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': '^*.99.99.199',
        'cmci_port': '10080',
        'context': 'iyk3z0r9',
        'scope': 'iyk3z0r8',
        'resource': {
            'type': 'cicslocalfile'
        }
    })


def test_unknown_host(monkeypatch):
    monkeypatch.setattr(basic.AnsibleModule, "exit_json", exit_json)
    monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail_json)

    set_module_args({
        'cmci_host': 'invalid.hursley.ibm.com',
        'cmci_port': '26040',
        'context': 'CICPY012',
        'security_type': 'none',
        'resource': {
            'type': 'CICSDefinitionBundle'
        }
    })

    with pytest.raises(AnsibleFailJson) as exc_info:
        cmci_get.main()

    exp = \
        'Error performing CMCI request: <[^>]*>: Failed to establish a new connection: ' \
        '\\[Errno 8\\] nodename nor servname provided, or not known'
    assert re.match(exp, exc_info.value.args[0]['msg'])


def test_invalid_port(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'Parameter "cmci_port" with value "^%^080 was not valid.  Expected a port number 0-65535.',
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': '100.99.99.199',
        'cmci_port': '^%^080',
        'context': 'iyk3z0r9',
        'scope': 'iyk3z0r8',
        'resource': {
            'type': 'cicslocalfile'
        },
    })


def test_invalid_context(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'Parameter "context" with value "^&iyk3z0r9 was not valid.  Expected a CPSM context name.  CPSM '
               'context names are max 8 characters.  Valid characters are A-Z a-z 0-9.',
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': '100.99.99.199',
        'cmci_port': '10080',
        'context': '^&iyk3z0r9',
        'scope': 'iyk3z0r8',
        'resource': {
            'type': 'cicslocalfile'
        },
    })


def test_invalid_scope(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'Parameter "scope" with value "&^iyk3z0r8 was not valid.  Expected a CPSM scope name.  CPSM scope '
               'names are max 8 characters.  Valid characters are A-Z a-z 0-9.',
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': '100.99.99.199',
        'cmci_port': '10080',
        'context': 'iyk3z0r9',
        'scope': '&^iyk3z0r8',
        'resource': {
            'type': 'cicslocalfile'
        },
    })


def test_invalid_security(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'value of security_type must be one of: none, basic, certificate, got: yes',
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': '100.99.99.199',
        'cmci_port': '10080',
        'context': 'iyk3z0r9',
        'scope': 'iyk3z0r8',
        'security_type': 'yes',
        'resource': {
            'type': 'cicslocalfile'
        },
    })


def test_auth(cmci_module):  # type: (CMCITestHelper) -> None
    records = [
        {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'},
        {'name': 'bing', 'dsname': 'STEWF.BAT.BAZ'}
    ]
    cmci_module.stub_records(
        'GET',
        'cicslocalfile',
        records,
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
            'body': create_records_response('cicslocalfile', records),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'cmci_user': 'foo',
        'cmci_password': 'bar',
        'security_type': 'basic',
        'context': CONTEXT,
        'scope': SCOPE,
        'resource': {'type': 'cicslocalfile'},
    })


def test_ok_context_scope(cmci_module):  # type: (CMCITestHelper) -> None
    records = [
        {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'},
        {'name': 'bing', 'dsname': 'STEWF.BAT.BAZ'}
    ]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE)

    cmci_module.expect({
        'changed': False,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicslocalfile/CICSEX56/IYCWEMW2',
            'method': 'GET',
            'body': None
        },
        'response': {
            'body': create_records_response('cicslocalfile', records),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicslocalfile'},
    })


def test_ok_context_scope_single_record(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE)

    cmci_module.expect({
        'changed': False,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicslocalfile/CICSEX56/IYCWEMW2',
            'method': 'GET',
            'body': None
        },
        'response': {
            'body': create_records_response('cicslocalfile', records),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicslocalfile'},
    })


def test_ok_context_scope_jvmserver_header(cmci_module):  # type: (CMCITestHelper) -> None
    records = [
        {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'},
        {'name': 'bing', 'dsname': 'STEWF.BAT.BAZ'}
    ]

    cmci_module.stub_records(
        'GET',
        'cicslocalfile',
        records,
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
            'body': create_records_response('cicslocalfile', records),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicslocalfile'},
    })


def test_query_criteria(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,  parameters='?CRITERIA=FOO%3DBAR')

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
            'body': create_records_response('cicslocalfile', records),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicslocalfile'},
        'criteria': 'FOO=BAR'
    })


def test_query_parameter(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records(
        'GET',
        'cicsdefinitionfile',
        records,
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
            'body': create_records_response('cicsdefinitionfile', records),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicsdefinitionfile'},
        'parameter': 'CSDGROUP(*)'
    })


def test_query_parameter_criteria(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]

    cmci_module.stub_records(
        'GET',
        'cicsdefinitionfile',
        records,
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
            'body': create_records_response('cicsdefinitionfile', records),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicsdefinitionfile'},
        'parameter': 'CSDGROUP(*)',
        'criteria': 'FOO=BAR'
    })


def test_ok_context_record_count(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]

    cmci_module.stub_records('GET', 'cicslocalfile', records, record_count=1)

    cmci_module.expect({
        'changed': False,
        'request': {
            'url': 'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicslocalfile/CICSEX56///1',
            'method': 'GET',
            'body': None
        },
        'response': {
            'body': create_records_response('cicslocalfile', records),
            'reason': 'OK',
            'status_code': 200,
        }
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'record_count': 1,
        'resource': {'type': 'cicslocalfile'},
    })

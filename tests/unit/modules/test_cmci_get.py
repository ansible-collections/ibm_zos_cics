# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_get
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, SCOPE, AnsibleFailJson,
    set_module_args, exit_json, fail_json, cmci_module, CMCITestHelper
)
from ansible.module_utils import basic

import pytest
import re
import sys


def test_401_fails(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.stub_request(
        'GET',
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/CICSDefinitionBundle/CICPY012/',
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
        'http_status': 'Not authorized',
        'http_status_code': 401,
        'request': {
            'url': 'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
                   'cicsdefinitionbundle/CICPY012/',
            'method': 'GET',
            'body': None
        }
    })

    # Module config
    cmci_module.run(cmci_get, {
        'cmci_host': 'winmvs2c.hursley.ibm.com',
        'cmci_port': '26040',
        'context': 'CICPY012',
        'type': 'CICSDefinitionBundle'
    })


def test_invalid_host(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'Parameter "cmci_host" with value "^*.99.99.199" was not valid.  Expected an IP address or host name.',
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': '^*.99.99.199',
        'cmci_port': '10080',
        'context': 'iyk3z0r9',
        'scope': 'iyk3z0r8',
        'type': 'cicslocalfile'
    })


def test_unknown_host(monkeypatch):
    monkeypatch.setattr(basic.AnsibleModule, "exit_json", exit_json)
    monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail_json)

    set_module_args({
        'cmci_host': 'invalid.hursley.ibm.com',
        'cmci_port': '26040',
        'context': 'CICPY012',
        'type': 'CICSDefinitionBundle'
    })

    with pytest.raises(AnsibleFailJson) as exc_info:
        cmci_get.main()

    exp = \
        'Error performing CMCI request: <[^>]*>: Failed to establish a new connection: ' \
        '\\[Errno 8\\] nodename nor servname provided, or not known'
    assert re.match(exp, exc_info.value.args[0]['msg'])


def test_invalid_port_type(cmci_module):  # type: (CMCITestHelper) -> None
    #the error message is slightly different between Python 2 and 3
    expectedType = 'class'
    if sys.version_info.major <= 2:
        expectedType = 'type'

    cmci_module.expect({
        'msg': "argument cmci_port is of type <" + expectedType + " 'str'> and we were unable to "
               "convert to int: <class 'str'> cannot be converted to an int",
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': '100.99.99.199',
        'cmci_port': '^%^080',
        'context': 'iyk3z0r9',
        'scope': 'iyk3z0r8',
        'type': 'cicslocalfile'
    })


def test_valid_port_string(cmci_module):  # type: (CMCITestHelper) -> None
    records = [
        {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'},
        {'name': 'bing', 'dsname': 'STEWF.BAT.BAZ'}
    ]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE)

    cmci_module.expect(result(
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicslocalfile/CICSEX56/IYCWEMW2',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': '26040',
        'context': CONTEXT,
        'scope': SCOPE,
        'type': 'cicslocalfile'
    })


def test_invalid_port_low(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'Parameter "cmci_port" with value "-1" was not valid.  Expected a port number 0-65535.',
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': '100.99.99.199',
        'cmci_port': -1,
        'context': 'iyk3z0r9',
        'scope': 'iyk3z0r8',
        'type': 'cicslocalfile'
    })


def test_invalid_port_high(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'Parameter "cmci_port" with value "65536" was not valid.  Expected a port number 0-65535.',
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': '100.99.99.199',
        'cmci_port': 65536,
        'context': 'iyk3z0r9',
        'scope': 'iyk3z0r8',
        'type': 'cicslocalfile'
    })


def test_invalid_context(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'Parameter "context" with value "^&iyk3z0r9" was not valid.  Expected a CPSM context name.  CPSM '
               'context names are max 8 characters.  Valid characters are A-Z a-z 0-9.',
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': '100.99.99.199',
        'cmci_port': '10080',
        'context': '^&iyk3z0r9',
        'scope': 'iyk3z0r8',
        'type': 'cicslocalfile'
    })


def test_invalid_scope(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'Parameter "scope" with value "&^iyk3z0r8" was not valid.  Expected a CPSM scope name.  CPSM scope '
               'names are max 8 characters.  Valid characters are A-Z a-z 0-9.',
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': '100.99.99.199',
        'cmci_port': '10080',
        'context': 'iyk3z0r9',
        'scope': '&^iyk3z0r8',
        'type': 'cicslocalfile'
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

    cmci_module.expect(result(
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicslocalfile/CICSEX56/IYCWEMW2',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'cmci_user': 'foo',
        'cmci_password': 'bar',
        'context': CONTEXT,
        'scope': SCOPE,
        'type': 'cicslocalfile'
    })


def test_basic_auth_required_together(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'parameters are required together: cmci_user, cmci_password',
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'cmci_user': 'foo',
        'context': CONTEXT,
        'scope': SCOPE,
        'type': 'cicslocalfile'
    })


def test_cert_key_required_together(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'parameters are required together: cmci_cert, cmci_key',
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'cmci_cert': 'foo',
        'context': CONTEXT,
        'scope': SCOPE,
        'type': 'cicslocalfile'
    })


def test_cert_key_http_incompatible(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': 'scheme can not be set to http if you are using certificate auth',
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'cmci_cert': 'foo',
        'cmci_key': 'bar',
        'scheme': 'http',
        'context': CONTEXT,
        'scope': SCOPE,
        'type': 'cicslocalfile'
    })


def test_ok_context_scope(cmci_module):  # type: (CMCITestHelper) -> None
    records = [
        {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'},
        {'name': 'bing', 'dsname': 'STEWF.BAT.BAZ'}
    ]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE)

    cmci_module.expect(result(
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicslocalfile/CICSEX56/IYCWEMW2',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile'
    })


def test_ok_context_scope_http(cmci_module):  # type: (CMCITestHelper) -> None
    records = [
        {'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'},
        {'name': 'bing', 'dsname': 'STEWF.BAT.BAZ'}
    ]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE, scheme='http')

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicslocalfile/CICSEX56/IYCWEMW2',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'scheme': 'http'
    })


def test_ok_context_scope_single_record(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE)

    cmci_module.expect(result(
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicslocalfile/CICSEX56/IYCWEMW2',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile'
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

    cmci_module.expect(result(
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicslocalfile/CICSEX56/IYCWEMW2',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile'
    })


def test_query_criteria(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE, parameters='?CRITERIA=%28FOO%3D%27BAR%27%29')

    cmci_module.expect(result(
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'filter': {
                'FOO': 'BAR'
            }
        }
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

    cmci_module.expect(result(
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicsdefinitionfile/CICSEX56/IYCWEMW2?PARAMETER=CSDGROUP%28%2A%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicsdefinitionfile',
        'resources': {
            'parameters': [{
                'name': 'CSDGROUP',
                'value': '*'
            }]
        }
    })


def test_query_parameters(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records(
        'GET',
        'cicsdefinitionfile',
        records,
        scope=SCOPE,
        parameters='?PARAMETER=CSDGROUP%28%2A%29%20FOO%28BO%20BO%29%20blah'
    )

    cmci_module.expect(result(
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicsdefinitionfile/CICSEX56/IYCWEMW2?PARAMETER=CSDGROUP%28%2A%29%20FOO%28BO%20BO%29%20blah',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicsdefinitionfile',
        'resources': {
            'parameters': [{
                'name': 'CSDGROUP',
                'value': '*'
            }, {
                'name': 'FOO',
                'value': 'BO BO'
            }, {
                'name': 'blah'
            }]
        }
    })


def test_query_parameter_criteria(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]

    cmci_module.stub_records(
        'GET',
        'cicsdefinitionfile',
        records,
        scope=SCOPE,
        parameters='?CRITERIA=%28FOO%3D%27BAR%27%29&PARAMETER=CSDGROUP%28%2A%29'
    )

    cmci_module.expect(result(
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicsdefinitionfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29&PARAMETER=CSDGROUP%28%2A%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicsdefinitionfile',
        'resources': {
            'parameters': [{'name': 'CSDGROUP', 'value': '*'}],
            'filter': {
                'FOO': 'BAR'
            }
        }
    })


def test_bas_query(cmci_module):  # type: (CMCITestHelper) -> None
    records = [
        {'defname': 'DUMMY1', 'deftype': 'PROGDEF', 'ingtype': 'PGMINGRP', 'resgroup': 'BASGRP1'},
        {'defname': 'DUMMY2', 'deftype': 'TRANDEF', 'ingtype': 'PGMINGRP', 'resgroup': 'BASGRP1'},
        {'defname': 'DUMMY3', 'deftype': 'LIBDEF', 'ingtype': 'PGMINGRP', 'resgroup': 'BASGRP1'}
    ]

    cmci_module.stub_records(
        'GET',
        'cicsresourceingroup',
        records,
        parameters='?CRITERIA=%28RESGROUP%3D%27BASGRP1%27%29'
    )

    cmci_module.expect(result(
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicsresourceingroup/CICSEX56/?CRITERIA=%28RESGROUP%3D%27BASGRP1%27%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'resources': {
            'filter': {
                'RESGROUP': 'BASGRP1'
            }
        },
        'type': 'cicsresourceingroup'
    })


def test_ok_context_record_count(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]

    cmci_module.stub_records('GET', 'cicslocalfile', records, record_count=1)

    cmci_module.expect(result(
        'https://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicslocalfile/CICSEX56///1',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'record_count': 1,
        'type': 'cicslocalfile'
    })


def result(url, records, http_status='OK', http_status_code=200):
    return {
        'changed': False,
        'connect_version': '0560',
        'cpsm_reason': '',
        'cpsm_reason_code': 0,
        'cpsm_response': 'OK',
        'cpsm_response_code': 1024,
        'http_status': http_status,
        'http_status_code': http_status_code,
        'record_count': len(records),
        'records': records,
        'request': {
            'url': url,
            'method': 'GET',
            'body': None
        }
    }

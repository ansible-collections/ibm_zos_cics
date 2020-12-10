# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules import cmci_delete
from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.cmci_helper import (
    HOST, PORT, CONTEXT, create_delete_response, cmci_module, CMCITestHelper
)


def test_delete_context(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.stub_delete('cicsdefinitionbundle', 1)

    cmci_module.expect(
        result(
            'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionbundle/CICSEX56/',
            1
        )
    )

    cmci_module.run(cmci_delete, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'resource': {'type': 'cicsdefinitionbundle'},
    })


def test_delete_context_scope(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.stub_delete('cicsdefinitionbundle', 1, scope='IYCWEMW2')

    cmci_module.expect(
        result(
            'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionbundle/CICSEX56/IYCWEMW2',
            1
        )
    )

    cmci_module.run(cmci_delete, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'resource': {'type': 'cicsdefinitionbundle'},
    })


def test_delete_criteria(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.stub_delete('cicsdefinitionbundle', 1, parameters='?CRITERIA=FOO%3DBAR')

    cmci_module.expect(
        result(
            'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionbundle/CICSEX56/',
            1,
            other_request={
                'params': {
                    'CRITERIA': 'FOO=BAR'
                }
            }
        )
    )

    cmci_module.run(cmci_delete, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'resource': {'type': 'cicsdefinitionbundle'},
        'criteria': 'FOO=BAR'
    })


def test_delete_parameter(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.stub_delete('cicsdefinitionbundle', 1, parameters='?PARAMETER=CSDGROUP%28%2A%29')

    cmci_module.expect(
        result(
            'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionbundle/CICSEX56/',
            1,
            other_request={
                'params': {
                    'PARAMETER': 'CSDGROUP(*)'
                }
            }
        )
    )

    cmci_module.run(cmci_delete, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'resource': {'type': 'cicsdefinitionbundle'},
        'parameter': 'CSDGROUP(*)'
    })


def test_delete_criteria_parameter(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.stub_delete(
        'cicsdefinitionbundle',
        1,
        parameters='?CRITERIA=FOO%3DBAR&PARAMETER=CSDGROUP%28%2A%29'
    )

    cmci_module.expect(
        result(
            'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/cicsdefinitionbundle/CICSEX56/',
            1,
            other_request={
                'params': {
                    'CRITERIA': 'FOO=BAR',
                    'PARAMETER': 'CSDGROUP(*)'
                }
            }
        )
    )

    cmci_module.run(cmci_delete, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'resource': {'type': 'cicsdefinitionbundle'},
        'criteria': 'FOO=BAR',
        'parameter': 'CSDGROUP(*)'
    })


def result(url, success_count, other_request={}):
    return {
        'changed': True,
        'request': {
            'url': url,
            'method': 'DELETE',
            'body': None,
            **other_request
        },
        'response': {
            'body': create_delete_response(success_count),
            'reason': 'OK',
            'status_code': 200,
        }
    }

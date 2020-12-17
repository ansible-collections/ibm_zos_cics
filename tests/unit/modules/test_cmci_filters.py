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


def test_query_criteria(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE, parameters='?CRITERIA=%28FOO%3D%27BAR%27%29')

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
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


def test_filter_multi(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28GOO%3D%27LAR%27%29')

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28GOO%3D%27LAR%27%29',
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
                'FOO': 'BAR',
                'GOO': 'LAR'
            }
        }
    })


def test_complex_filter_and(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28GOO%3D%27LAR%27%29')

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28GOO%3D%27LAR%27%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'operator': '=',
                    'value': 'BAR'
                },
                    {
                        'attribute': 'GOO',
                        'operator': '=',
                        'value': 'LAR'
                    }]
            }
        }
    })


def test_complex_filter_or(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%3D%27BAR%27%29%20OR%20%28GOO%3D%27LAR%27%29')

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29%20OR%20%28GOO%3D%27LAR%27%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{
                    'attribute': 'FOO',
                    'operator': '=',
                    'value': 'BAR'
                },
                    {
                        'attribute': 'GOO',
                        'operator': '=',
                        'value': 'LAR'
                    }
                ]
            }
        }
    })


def test_complex_filter_operator(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    # TODO currently this is wrong as it adds %C2 before the operator, which CPSM doesn't like.
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%C2%AC%3D%27BAR%27%29')

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%C2%AC%3D%27BAR%27%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'attribute': 'FOO',
                'operator': '!=',
                'value': 'BAR'
            }
        }
    })


def test_complex_filter_and_or(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28BAT%3D%27BAZ%27%29%20AND%20%28'
                                        '%28BING%3D%271%27%29%20OR%20%28BING%3D%272%27%29%29')

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28BAT%3D%27BAZ%27%29%20AND%20%28'
        '%28BING%3D%271%27%29%20OR%20%28BING%3D%272%27%29%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'value': 'BAR'
                }, {
                    'attribute': 'BAT',
                    'value': 'BAZ'
                }, {
                    'or': [{
                        'attribute': 'BING',
                        'operator': '=',
                        'value': '1'
                    }, {
                        'attribute': 'BING',
                        'value': '2'
                    }]
                }]
            }
        }
    })


def test_complex_filter_and_and(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28BAT%3D%3D%27BAZ%27%29%20AND%20%28'
                                        '%28BING%3D%271%27%29%20AND%20%28BING%3D%272%27%29%29')

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3D%27BAR%27%29%20AND%20%28BAT%3D%3D%27BAZ%27%29%20AND%20%28'
        '%28BING%3D%271%27%29%20AND%20%28BING%3D%272%27%29%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'value': 'BAR'
                },
                    {
                        'attribute': 'BAT',
                        'operator': '==',
                        'value': 'BAZ'
                    },
                    {
                        'and': [{
                            'attribute': 'BING',
                            'value': '1'
                        }, {
                            'attribute': 'BING',
                            'value': '2'
                        }]
                    }]
            }
        }
    })


def test_complex_filter_or_or(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE,
                             parameters='?CRITERIA=%28FOO%3E%3D%27BAR%27%29%20OR%20%28%28BING%3D%3D%271%27%29%20OR%20'
                                        '%28BING%3D%272%27%29%29')

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3E%3D%27BAR%27%29%20OR%20%28%28BING%3D%3D%271%27%29%20OR%20'
        '%28BING%3D%272%27%29%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'or': [{
                    'attribute': 'FOO',
                    'operator': '>=',
                    'value': 'BAR'
                }, {
                    'or': [{
                        'attribute': 'BING',
                        'operator': 'IS',
                        'value': '1'
                    }, {
                        'attribute': 'BING',
                        'operator': 'EQ',
                        'value': '2'
                    }]
                }]
            }
        }
    })


def test_complex_filter_invalid_and_or_combo(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "complex_filter can only have 'and', 'or', or 'attribute' dictionaries at the top level",
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'operator': '=',
                    'value': 'BAR'
                },
                    {
                        'attribute': 'GOO',
                        'operator': '=',
                        'value': 'LAR'
                    }],
                'or': [{
                    'attribute': 'FOO',
                    'operator': '=',
                    'value': 'BAR'
                },
                    {
                        'attribute': 'GOO',
                        'operator': '=',
                        'value': 'LAR'
                    }]
            }
        }
    })


def test_query_criteria_complex_filter_no_value(cmci_module):
    cmci_module.expect({
        'msg': 'parameters are required together: attribute, value found in resources -> complex_filter -> and',
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO'
                }, {
                    'attribute': 'BAR',
                    'value': 'BOO'
                }]
            }
        }
    })


def test_complex_filter_operator_letters(cmci_module):  # type: (CMCITestHelper) -> None
    records = [{'name': 'bat', 'dsname': 'STEWF.BLOP.BLIP'}]
    cmci_module.stub_records('GET', 'cicslocalfile', records, scope=SCOPE, parameters='?CRITERIA=%28FOO%3E%27BAR%27%29')

    cmci_module.expect(result(
        'http://winmvs2c.hursley.ibm.com:26040/CICSSystemManagement/'
        'cicslocalfile/CICSEX56/IYCWEMW2?CRITERIA=%28FOO%3E%27BAR%27%29',
        records=records
    ))

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'attribute': 'FOO',
                'operator': 'GT',
                'value': 'BAR'
            }
        }
    })


def test_complex_filter_invalid_and_attribute(cmci_module):  # type: (CMCITestHelper) -> None
    cmci_module.expect({
        'msg': "complex_filter can only have 'and', 'or', or 'attribute' dictionaries at the top level",
        'changed': False,
        'failed': True
    })

    cmci_module.run(cmci_get, {
        'cmci_host': HOST,
        'cmci_port': PORT,
        'context': CONTEXT,
        'scope': 'IYCWEMW2',
        'type': 'cicslocalfile',
        'resources': {
            'complex_filter': {
                'and': [{
                    'attribute': 'FOO',
                    'value': 'BAR'
                },{
                        'attribute': 'BAT',
                        'operator': '==',
                        'value': 'BAZ'
                }],
                'attribute': 'FOO2',
                'value': 'BAR2'
            }
        }
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

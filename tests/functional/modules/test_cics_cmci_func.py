# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from pprint import pprint


def test_cics_cmci_define_resource(ansible_module):
    hosts = ansible_module
    results = hosts.cics_cmci(
        cmci_host='winmvs2c.hursley.ibm.com',
        cmci_port='10080',
        context='iyk3z0r9',
        option='define',
        resource=[{
            'type': 'CICSDefinitionBundle',
            'attributes': [{
                'name': 'PONGALT',
                'BUNDLEDIR': '/u/xiaopin/bundle/pongbundle_1.0.0',
                'csdgroup': 'JVMGRP1'
            }],
            'parameters': [{'name': 'CSD'}]
        }]
    )
    for result in results.contacted.values():
        assert result.get("changed") is True
        assert result.get("api_response") == 'OK'


def test_cics_cmci_update_resource_def(ansible_module):
    hosts = ansible_module
    results = hosts.cics_cmci(
        cmci_host='winmvs2c.hursley.ibm.com',
        cmci_port='10080',
        context='iyk3z0r9',
        option='update',
        resource=[{
            'type': 'CICSDefinitionBundle',
            'attributes': [{'description': 'forget description'}],
            'parameters': [{'name': 'CSD'}]
        }],
        filter=[{
            'criteria': 'NAME=PONGALT',
            'parameter': 'CSDGROUP(JVMGRP1)'
        }]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get("changed") is True
        assert result.get("api_response") == 'OK'


def test_cics_cmci_install_resource(ansible_module):
    hosts = ansible_module
    results = hosts.cics_cmci(
        cmci_host='winmvs2c.hursley.ibm.com',
        cmci_port='10080',
        context='iyk3z0r9',
        option='install',
        resource=[{
            'type': 'CICSDefinitionBundle',
            'location': 'CSD',
        }],
        filter=[{
            'criteria': 'NAME=PONGALT',
            'parameter': 'CSDGROUP(JVMGRP1)'
        }]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get("changed") is True
        assert result.get("api_response") == 'OK'


def test_cics_cmci_disable_resource(ansible_module):
    hosts = ansible_module
    results = hosts.cics_cmci(
        cmci_host='winmvs2c.hursley.ibm.com',
        cmci_port='10080',
        context='iyk3z0r9',
        option='update',
        resource=[{
            'type': 'CICSBundle',
            'attributes': [{'Enablestatus': 'disabled'}],
        }],
        filter=[{
            'criteria': 'NAME=PONGALT'
        }]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get("changed") is True
        assert result.get("api_response") == 'OK'


def test_cics_cmci_delete_resource(ansible_module):
    hosts = ansible_module
    results = hosts.cics_cmci(
        cmci_host='winmvs2c.hursley.ibm.com',
        cmci_port='10080',
        context='iyk3z0r9',
        option='delete',
        resource=[{
            'type': 'CICSBundle',
        }],
        filter=[{
            'criteria': 'NAME=PONGALT'
        }]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get("changed") is True
        assert result.get("api_response") == 'OK'


def test_cics_cmci_delete_resource_def(ansible_module):
    hosts = ansible_module
    results = hosts.cics_cmci(
        cmci_host='winmvs2c.hursley.ibm.com',
        cmci_port='10080',
        context='iyk3z0r9',
        option='delete',
        resource=[{
            'type': 'CICSDefinitionBundle',
        }],
        filter=[{
            'criteria': 'NAME=PONGALT',
            'parameter': 'CSDGROUP(JVMGRP1)'

        }]
    )
    pprint(vars(results))
    for result in results.contacted.values():
        assert result.get("changed") is True
        assert result.get("api_response") == 'OK'

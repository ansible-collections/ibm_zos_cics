# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.common.text.converters import to_bytes
from ansible.module_utils import basic
from collections import OrderedDict
from requests import PreparedRequest
from typing import List

import json
import pytest
import unittest
import xmltodict

CONTEXT = 'CICSEX56'
SCOPE = 'IYCWEMW2'
HOST = 'winmvs2c.hursley.ibm.com'
PORT = '26040'


class CMCITestHelper:
    def __init__(self, requests_mock=None):
        self.requests_mock = requests_mock
        self.expected = {}

    def stub_request(self, *args, complete_qs=True, **kwargs):
        self.requests_mock.request(*args, complete_qs=complete_qs, **kwargs)

    def stub_delete(self, resource_type, success_count, *args, **kwargs):
        return self.stub_cmci(
            'DELETE',
            resource_type,
            *args,
            response_dict=create_delete_response(success_count),
            **kwargs
        )

    def stub_records(self, method, resource_type, records, *args, **kwargs):
        return self.stub_cmci(
            method,
            resource_type,
            *args,
            response_dict=create_records_response(resource_type, records),
            **kwargs
        )

    def stub_cmci(self, method, resource_type, scheme='http', host=HOST, port=PORT,
                  context=CONTEXT, scope=None, parameters='', response_dict=None,
                  headers={'CONTENT-TYPE': 'application/xml'}, status_code=200, reason='OK',
                  record_count=None, **kwargs):
        url = '{0}://{1}:{2}/CICSSystemManagement/{3}/{4}/{5}{6}{7}'\
            .format(scheme, host, port, resource_type, context, '//' + str(record_count) if record_count else '',
                    scope if scope else '', parameters)

        return self.stub_request(
            method,
            url,
            text=xmltodict.unparse(response_dict) if response_dict else None,
            headers=headers,
            status_code=status_code,
            reason=reason,
            **kwargs
        )

    def expect(self, expected):
        self.expected = expected

    def run(self, module, config):
        # upper-case the resource name, so it definitely doesn't match the CMCI response, to ensure
        # we don't rely on them matching
        config['type'] = config['type'].upper()
        set_module_args(config)

        with pytest.raises(AnsibleFailJson if self.expected.get('failed') else AnsibleExitJson) as exc_info:
            module.main()

        result = exc_info.value.args[0]

        case = unittest.TestCase()
        case.maxDiff = None
        case.assertDictEqual(self.expected, result)


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


def create_delete_response(success_count):  # type: (int) -> OrderedDict
    return create_cmci_response(
        ('resultsummary', od(
            ('@api_response1', '1024'),
            ('@api_response2', '0'),
            ('@api_response1_alt', 'OK'),
            ('@api_response2_alt', ''),
            ('@recordcount', str(success_count)),
            ('@successcount', str(success_count))
        ))
    )


def create_records_response(resource_type, records):  # type: (str, List) -> OrderedDict
    # Convert to ordered dict, with @ sign for attribute prefix
    # CMCI always returns lower case names
    return create_cmci_response(
        ('resultsummary', od(
            ('@api_response1', '1024'),
            ('@api_response2', '0'),
            ('@api_response1_alt', 'OK'),
            ('@api_response2_alt', ''),
            ('@recordcount', str(len(records))),
            ('@displayed_recordcount', str(len(records)))
        )),
        ('records', od(
            (
                resource_type.lower(),
                [OrderedDict([('@' + key, value) for key, value in record.items()]) for record in records]
            )
        ))
    )


def create_cmci_response(*args):  # type () -> OrderedDict
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
            *args
        ))
    )


def body_matcher(expected):
    def match(request: PreparedRequest):
        return expected == xmltodict.parse(request.body)
    return match


def od(*args):
    return OrderedDict(args)

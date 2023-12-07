# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2020,2021
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
import json
from ansible.module_utils.common.text.converters import to_bytes
from ansible.module_utils import basic


default_data_set = {
    "exists": False,
    "name": None,
    "size": {
        "primary": 5,
        "secondary": 1,
        "unit": "M"
    },
    "state": "initial",
    "vsam": False
}


def set_data_set(**kwargs):
    data_set = default_data_set
    data_set.update(kwargs)
    return data_set


def set_module_args(args):
    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)

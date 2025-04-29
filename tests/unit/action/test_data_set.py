# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.plugin_utils._module_action_plugin import (
    _process_module_args
)


def test_data_set_with_template():
    args_with_template = {
        "region_data_sets": {"template": "data.set.template.<< data_set_name >>"},
        "space_primary": 2,
        "space_secondary": 1,
        "space_type": "m",
        "state": "initial"
    }

    _process_module_args(args_with_template, "dfhlrq", False)

    assert args_with_template == {
        "region_data_sets": {
            "dfhlrq": {"dsn": "data.set.template.DFHLRQ"},
            "template": "data.set.template.<< data_set_name >>",
        },
        "space_primary": 2,
        "space_secondary": 1,
        "space_type": "m",
        "state": "initial"
    }


def test_data_set_with_override():
    args_with_override = {
        "region_data_sets": {"dfhlrq": {"dsn": "data.set.path"}},
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }

    _process_module_args(args_with_override, "dfhlrq", False)

    assert args_with_override == {
        "region_data_sets": {
            "dfhlrq": {"dsn": "data.set.path"}
        },
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }


def test_data_set_with_override_but_no_dsn_key():
    args_with_override = {
        "region_data_sets": {"dfhlrq": {"garbage": "more.garbage"}},
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }

    try:
        _process_module_args(args_with_override, "dfhlrq", False)
    except KeyError as e:
        assert e.args[0] == "No template or data set override found for dfhlrq"
    else:
        assert False


def test_data_set_with_override_but_no_dsn_value():
    args_with_override = {
        "region_data_sets": {"dfhlrq": {"dsn": None}},
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }

    try:
        _process_module_args(args_with_override, "dfhlrq", False)
    except KeyError as e:
        assert e.args[0] == "No template or data set override found for dfhlrq"
    else:
        assert False


def test_data_set_without_override_or_template():
    args_with_garbage = {
        "region_data_sets": {"garbage": "more.garbage"},
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }

    try:
        _process_module_args(args_with_garbage, "dfhlrq", False)
    except KeyError as e:
        assert e.args[0] == "No template or data set override found for dfhlrq"
    else:
        assert False


def test_data_set_with_unnecessary_cics_data_sets_arg():
    args_with_template = {
        "region_data_sets": {"template": "data.set.template.<< data_set_name >>"},
        "cics_data_sets": {"template": "data.set.template.<< lib_name >>"},
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }

    _process_module_args(args_with_template, "dfhlrq", False)

    assert args_with_template == {
        "region_data_sets": {
            "dfhlrq": {"dsn": "data.set.template.DFHLRQ"},
            "template": "data.set.template.<< data_set_name >>",
        },
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }


def test_data_set_with_le_data_sets_arg():
    args_with_template = {
        "region_data_sets": {"template": "data.set.template.<< data_set_name >>"},
        "le_data_sets": {"template": "le.data.set.template.<< lib_name >>"},
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }

    _process_module_args(args_with_template, "dfhlrq", False)

    assert args_with_template == {
        "region_data_sets": {
            "dfhlrq": {"dsn": "data.set.template.DFHLRQ"},
            "template": "data.set.template.<< data_set_name >>",
        },
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }


def test_data_set_with_cpsm_data_sets_arg():
    args_with_template = {
        "region_data_sets": {"template": "data.set.template.<< data_set_name >>"},
        "cpsm_data_sets": {"template": "cpsm.data.set.template.<< lib_name >>"},
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }

    _process_module_args(args_with_template, "dfhlrq", False)

    assert args_with_template == {
        "region_data_sets": {
            "dfhlrq": {"dsn": "data.set.template.DFHLRQ"},
            "template": "data.set.template.<< data_set_name >>",
        },
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }


def test_data_set_with_required_cics_data_sets_templated():
    args_with_template = {
        "region_data_sets": {"template": "data.set.template.<< data_set_name >>"},
        "cics_data_sets": {"template": "data.set.template.<< lib_name >>"},
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }

    _process_module_args(args_with_template, "dfhgcd", True)

    assert args_with_template == {
        "region_data_sets": {
            "dfhgcd": {"dsn": "data.set.template.DFHGCD"},
            "template": "data.set.template.<< data_set_name >>",
        },
        "cics_data_sets": {
            "template": "data.set.template.<< lib_name >>",
            "sdfhload": "data.set.template.SDFHLOAD"
        },
        "space_primary": 1,
        "space_type": "m",
        "state": "initial"
    }

# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules.region_jcl import DSN
from ansible_collections.ibm.ibm_zos_cics.plugins.action.region_jcl import _process_module_args


def test_process_args_with_only_template():
    module_args = {
        "region_data_sets": {"template": "TEST.CICSPY1.RDEV.<< data_set_name >>"},
        "cics_data_sets": {"template": "TEST.CICS.<< lib_name >>"},
        "le_data_sets": {"template": "TEST.LE.<< lib_name >>"}
    }
    _process_module_args(module_args)
    assert module_args == {
        "region_data_sets": {
            'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.DFHAUXT"},
            'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.DFHBUXT"},
            'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.DFHCSD"},
            'dfhgcd': {DSN: "TEST.CICSPY1.RDEV.DFHGCD"},
            'dfhintra': {DSN: "TEST.CICSPY1.RDEV.DFHINTRA"},
            'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.DFHLCD"},
            'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.DFHLRQ"},
            'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.DFHTEMP"},
            'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DFHDMPA"},
            'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DFHDMPB"},
            'dfhstart': {DSN: "TEST.CICSPY1.RDEV.DFHSTART"},
        },
        "cics_data_sets": {
            "sdfhload": "TEST.CICS.SDFHLOAD",
            "sdfhauth": "TEST.CICS.SDFHAUTH",
            "sdfhlic": "TEST.CICS.SDFHLIC",
            "template": "TEST.CICS.<< lib_name >>"
        },
        "le_data_sets": {
            "sceecics": "TEST.LE.SCEECICS",
            "sceerun": "TEST.LE.SCEERUN",
            "sceerun2": "TEST.LE.SCEERUN2",
            "template": "TEST.LE.<< lib_name >>"
        },
        "steplib": {
            "top_data_sets": []
        },
        "dfhrpl": {
            "top_data_sets": []
        }
    }


def test_process_args_with_some_overrides():
    module_args = {
        "region_data_sets": {
            "template": "TEST.CICSPY1.RDEV.<< data_set_name >>",
            "dfhauxt": {DSN: "TEST.CICSPY1.RDEV.TRACE1"}
        },
        "cics_data_sets": {
            "template": "TEST.CICS.<< lib_name >>",
            "sdfhload": "TEST.CICS.LOAD"
        },
        "le_data_sets": {
            "template": "TEST.LE.<< lib_name >>",
            "sceerun": "TEST.LE.RUN"
        }
    }
    _process_module_args(module_args)
    assert module_args == {
        "region_data_sets": {
            'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.TRACE1"},
            'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.DFHBUXT"},
            'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.DFHCSD"},
            'dfhgcd': {DSN: "TEST.CICSPY1.RDEV.DFHGCD"},
            'dfhintra': {DSN: "TEST.CICSPY1.RDEV.DFHINTRA"},
            'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.DFHLCD"},
            'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.DFHLRQ"},
            'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.DFHTEMP"},
            'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DFHDMPA"},
            'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DFHDMPB"},
            'dfhstart': {DSN: "TEST.CICSPY1.RDEV.DFHSTART"},
        },
        "cics_data_sets": {
            "sdfhload": "TEST.CICS.LOAD",
            "sdfhauth": "TEST.CICS.SDFHAUTH",
            "sdfhlic": "TEST.CICS.SDFHLIC",
            "template": "TEST.CICS.<< lib_name >>"
        },
        "le_data_sets": {
            "sceecics": "TEST.LE.SCEECICS",
            "sceerun": "TEST.LE.RUN",
            "sceerun2": "TEST.LE.SCEERUN2",
            "template": "TEST.LE.<< lib_name >>"
        },
        "steplib": {
            "top_data_sets": []
        },
        "dfhrpl": {
            "top_data_sets": []
        }
    }


def test_process_args_with_only_overrides():
    module_args = {
        "region_data_sets": {
            'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.TRACE1"},
            'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.TRACE2"},
            'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.CSD"},
            'dfhgcd': {DSN: "TEST.CICSPY1.RDEV.GCD"},
            'dfhintra': {DSN: "TEST.CICSPY1.RDEV.INTRA"},
            'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.LCD"},
            'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.LRQ"},
            'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.TEMP"},
            'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DUMPA"},
            'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DUMPB"},
            'dfhstart': {DSN: "TEST.CICSPY1.RDEV.START"},
        },
        "cics_data_sets": {
            "sdfhload": "TEST.CICS.LOAD",
            "sdfhauth": "TEST.CICS.AUTH",
            "sdfhlic": "TEST.CICS.LIC",
        },
        "le_data_sets": {
            "sceecics": "TEST.LE.CICS",
            "sceerun": "TEST.LE.RUN",
            "sceerun2": "TEST.LE.RUN2",
        },
    }
    _process_module_args(module_args)
    assert module_args == {
        "region_data_sets": {
            'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.TRACE1"},
            'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.TRACE2"},
            'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.CSD"},
            'dfhgcd': {DSN: "TEST.CICSPY1.RDEV.GCD"},
            'dfhintra': {DSN: "TEST.CICSPY1.RDEV.INTRA"},
            'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.LCD"},
            'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.LRQ"},
            'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.TEMP"},
            'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DUMPA"},
            'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DUMPB"},
            'dfhstart': {DSN: "TEST.CICSPY1.RDEV.START"},
        },
        "cics_data_sets": {
            "sdfhload": "TEST.CICS.LOAD",
            "sdfhauth": "TEST.CICS.AUTH",
            "sdfhlic": "TEST.CICS.LIC",
        },
        "le_data_sets": {
            "sceecics": "TEST.LE.CICS",
            "sceerun": "TEST.LE.RUN",
            "sceerun2": "TEST.LE.RUN2",
        },
        "steplib": {
            "top_data_sets": []
        },
        "dfhrpl": {
            "top_data_sets": []
        }
    }


def test_process_args_with_missing_overrides_no_template():
    module_args = {
        "region_data_sets": {
            'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.TRACE1"},
            'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.TRACE2"},
        },
        "cics_data_sets": {
            "sdfhload": "TEST.CICS.LOAD",
        },
        "le_data_sets": {
            "sceecics": "TEST.LE.CICS",
        },
    }
    try:
        _process_module_args(module_args)
    except KeyError as e:
        assert e.args[0] == "No template or library override found for sdfhauth"
    else:
        assert False


def test_process_args_with_one_missing_override_no_template():
    module_args = {
        "region_data_sets": {
            "template": "TEST.CICSPY1.RDEV.<< data_set_name >>"
        },
        "cics_data_sets": {
            "template": "TEST.CICS.<< lib_name >>"
        },
        "le_data_sets": {
            "sceecics": "TEST.LE.CICS",
            "sceerun2": "TEST.LE.RUN2",
        }
    }
    try:
        _process_module_args(module_args)
    except KeyError as e:
        assert e.args[0] == "No template or library override found for sceerun"
    else:
        assert False


def test_process_args_with_missing_region_data_sets():
    module_args = {
        "cics_data_sets": {
            "template": "TEST.CICS.<< lib_name >>"
        },
        "le_data_sets": {
            "template": "TEST.LE.<< lib_name >>"
        }
    }
    try:
        _process_module_args(module_args)
    except KeyError as e:
        assert e.args[0] == "Required argument region_data_sets not found"
    else:
        assert False


def test_process_args_with_missing_dsn_key():
    module_args = {
        "region_data_sets": {
            'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.TRACE1"},
            'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.TRACE2"},
            'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.CSD"},
            'dfhintra': {DSN: "TEST.CICSPY1.RDEV.INTRA"},
            'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.LCD"},
            'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.LRQ"},
            'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.TEMP"},
            'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DUMPA"},
            'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DUMPB"},
            'dfhstart': {DSN: "TEST.CICSPY1.RDEV.START"},
            "dfhgcd": {"garbage": "more.garbage"}
        },
        "cics_data_sets": {
            "template": "TEST.CICS.<< lib_name >>"
        },
        "le_data_sets": {
            "template": "TEST.LE.<< lib_name >>"
        }
    }
    try:
        _process_module_args(module_args)
    except KeyError as e:
        assert e.args[0] == "No template or data set override found for dfhgcd"
    else:
        assert False


def test_process_args_with_missing_dsn_value():
    module_args = {
        "region_data_sets": {
            'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.TRACE1"},
            'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.TRACE2"},
            'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.CSD"},
            'dfhintra': {DSN: "TEST.CICSPY1.RDEV.INTRA"},
            'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.LCD"},
            'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.LRQ"},
            'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.TEMP"},
            'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DUMPA"},
            'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DUMPB"},
            'dfhstart': {DSN: "TEST.CICSPY1.RDEV.START"},
            "dfhgcd": {"dsn": None}
        },
        "cics_data_sets": {
            "template": "TEST.CICS.<< lib_name >>"
        },
        "le_data_sets": {
            "template": "TEST.LE.<< lib_name >>"
        }
    }
    try:
        _process_module_args(module_args)
    except KeyError as e:
        assert e.args[0] == "No template or data set override found for dfhgcd"
    else:
        assert False


def test_process_args_with_only_template_and_optional_cpsm_arg():
    module_args = {
        "region_data_sets": {"template": "TEST.CICSPY1.RDEV.<< data_set_name >>"},
        "cics_data_sets": {"template": "TEST.CICS.<< lib_name >>"},
        "le_data_sets": {"template": "TEST.LE.<< lib_name >>"},
        "cpsm_data_sets": {"template": "TEST.CPSM.<< lib_name >>"}
    }
    _process_module_args(module_args)
    assert module_args == {
        "region_data_sets": {
            'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.DFHAUXT"},
            'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.DFHBUXT"},
            'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.DFHCSD"},
            'dfhgcd': {DSN: "TEST.CICSPY1.RDEV.DFHGCD"},
            'dfhintra': {DSN: "TEST.CICSPY1.RDEV.DFHINTRA"},
            'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.DFHLCD"},
            'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.DFHLRQ"},
            'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.DFHTEMP"},
            'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DFHDMPA"},
            'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DFHDMPB"},
            'dfhstart': {DSN: "TEST.CICSPY1.RDEV.DFHSTART"},
        },
        "cics_data_sets": {
            "sdfhload": "TEST.CICS.SDFHLOAD",
            "sdfhauth": "TEST.CICS.SDFHAUTH",
            "sdfhlic": "TEST.CICS.SDFHLIC",
            "template": "TEST.CICS.<< lib_name >>"
        },
        "le_data_sets": {
            "sceecics": "TEST.LE.SCEECICS",
            "sceerun": "TEST.LE.SCEERUN",
            "sceerun2": "TEST.LE.SCEERUN2",
            "template": "TEST.LE.<< lib_name >>"
        },
        "cpsm_data_sets": {
            "seyuauth": "TEST.CPSM.SEYUAUTH",
            "seyuload": "TEST.CPSM.SEYULOAD",
            "template": "TEST.CPSM.<< lib_name >>"
        },
        "steplib": {
            "top_data_sets": []
        },
        "dfhrpl": {
            "top_data_sets": []
        }
    }


def test_process_args_with_optional_cpsm_arg_and_overrides():
    module_args = {
        "region_data_sets": {"template": "TEST.CICSPY1.RDEV.<< data_set_name >>"},
        "cics_data_sets": {"template": "TEST.CICS.<< lib_name >>"},
        "le_data_sets": {"template": "TEST.LE.<< lib_name >>"},
        "cpsm_data_sets": {
            "template": "TEST.CPSM.<< lib_name >>",
            "seyuauth": "TEST.SEYUAUTH",
            "seyuload": "TEST.SEYULOAD"
        }
    }
    _process_module_args(module_args)
    assert module_args == {
        "region_data_sets": {
            'dfhauxt': {DSN: "TEST.CICSPY1.RDEV.DFHAUXT"},
            'dfhbuxt': {DSN: "TEST.CICSPY1.RDEV.DFHBUXT"},
            'dfhcsd': {DSN: "TEST.CICSPY1.RDEV.DFHCSD"},
            'dfhgcd': {DSN: "TEST.CICSPY1.RDEV.DFHGCD"},
            'dfhintra': {DSN: "TEST.CICSPY1.RDEV.DFHINTRA"},
            'dfhlcd': {DSN: "TEST.CICSPY1.RDEV.DFHLCD"},
            'dfhlrq': {DSN: "TEST.CICSPY1.RDEV.DFHLRQ"},
            'dfhtemp': {DSN: "TEST.CICSPY1.RDEV.DFHTEMP"},
            'dfhdmpa': {DSN: "TEST.CICSPY1.RDEV.DFHDMPA"},
            'dfhdmpb': {DSN: "TEST.CICSPY1.RDEV.DFHDMPB"},
            'dfhstart': {DSN: "TEST.CICSPY1.RDEV.DFHSTART"},
        },
        "cics_data_sets": {
            "sdfhload": "TEST.CICS.SDFHLOAD",
            "sdfhauth": "TEST.CICS.SDFHAUTH",
            "sdfhlic": "TEST.CICS.SDFHLIC",
            "template": "TEST.CICS.<< lib_name >>"
        },
        "le_data_sets": {
            "sceecics": "TEST.LE.SCEECICS",
            "sceerun": "TEST.LE.SCEERUN",
            "sceerun2": "TEST.LE.SCEERUN2",
            "template": "TEST.LE.<< lib_name >>"
        },
        "cpsm_data_sets": {
            "seyuauth": "TEST.SEYUAUTH",
            "seyuload": "TEST.SEYULOAD",
            "template": "TEST.CPSM.<< lib_name >>"
        },
        "steplib": {
            "top_data_sets": []
        },
        "dfhrpl": {
            "top_data_sets": []
        }
    }

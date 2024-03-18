# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
from ansible_collections.ibm.ibm_zos_cics.plugins.controller_utils.module_action_plugin import (
    _check_library_override,
    _check_region_override,
    _remove_region_data_set_args,
    _remove_cics_data_set_args,
    _process_region_data_set_args,
    _process_libraries_args,
    _check_template,
    _set_top_libraries_key,
    _remove_data_set_args
)


def get_templar(module_args):
    loader = DataLoader()
    templar = Templar(loader=loader, variables=module_args)
    return templar


def test__check_region_override():
    args_with_override = {"region_data_sets": {"dfhgcd" : {"dsn": "data.set.path"}}}
    args_with_template = {"region_data_sets": {"template" : "data.set.template.<< data_set_name >>"}}
    args_with_both = {"region_data_sets": {"template" : "data.set.template.<< data_set_name >>", "dfhgcd" : {"dsn": "data.set.path"}}}

    assert _check_region_override(args_with_override, "dfhgcd") is True
    assert _check_region_override(args_with_template, "dfhgcd") is False
    assert _check_region_override(args_with_both, "dfhgcd") is True


def test__check_library_override():
    args_with_override = {"cics_data_sets": {"sdfhload" : "data.set.path"}}
    args_with_template = {"cics_data_sets": {"template" : "data.set.template.<< data_set_name >>"}}
    args_with_both = {"cics_data_sets": {"template" : "data.set.template.<< data_set_name >>", "sdfhload" : "data.set.path"}}

    assert _check_library_override(args_with_override, "cics_data_sets", "sdfhload") is True
    assert _check_library_override(args_with_template, "cics_data_sets", "sdfhload") is False
    assert _check_library_override(args_with_both, "cics_data_sets", "sdfhload") is True


def test__remove_region_data_set_args():
    args_with_extra_region_data_sets = {"region_data_sets": {"dfhgcd" : {"dsn": "data.set.path"}, "dfhlcd": {"dsn": "data.set.path"}}}
    _remove_region_data_set_args(args_with_extra_region_data_sets, "dfhgcd")

    assert "dfhgcd" in list(args_with_extra_region_data_sets["region_data_sets"].keys())
    assert "dfhlcd" not in list(args_with_extra_region_data_sets["region_data_sets"].keys())


def test__remove_cics_data_set_args():
    args_with_extra_cics_data_sets = {"cics_data_sets": {"sdfhload" : "data.set.path", "sdfhlic" : "data.set.path", "sdfhauth" : "data.set.path"}}
    _remove_cics_data_set_args(args_with_extra_cics_data_sets, "sdfhload")

    assert "sdfhload" in list(args_with_extra_cics_data_sets["cics_data_sets"].keys())
    assert "sdfhlic" not in list(args_with_extra_cics_data_sets["cics_data_sets"].keys())
    assert "sdfhauth" not in list(args_with_extra_cics_data_sets["cics_data_sets"].keys())


def test__process_region_data_set_args_with_template():
    args_with_template = {"region_data_sets": {"template" : "data.set.template.<< data_set_name >>"}}
    templar = get_templar(args_with_template)
    task_vars = args_with_template

    _process_region_data_set_args(args_with_template, templar, "dfhgcd", task_vars)

    assert "dfhgcd" in list(args_with_template["region_data_sets"].keys())
    assert args_with_template["region_data_sets"]["dfhgcd"] == {"dsn": "data.set.template.DFHGCD"}


def test__process_region_data_set_args_without_template():
    args_with_override = {"region_data_sets": {"dfhgcd" : {"dsn": "data.set.template.global"}}}
    templar = get_templar(args_with_override)
    task_vars = args_with_override

    _process_region_data_set_args(args_with_override, templar, "dfhgcd", task_vars)

    assert args_with_override["region_data_sets"]["dfhgcd"]["dsn"] == "data.set.template.global"


def test__process_region_data_set_args_without_template_or_override():
    args_with_garbage = {"region_data_sets": {"garbage" : "more.garbage"}}
    templar = get_templar(args_with_garbage)
    task_vars = args_with_garbage

    try:
        _process_region_data_set_args(args_with_garbage, templar, "dfhgcd", task_vars)
    except KeyError as e:
        assert e.args[0] == "template and dfhgcd"


def test__process_libraries_args_with_template():
    args_with_template = {"cics_data_sets": {"template" : "data.set.template.<< lib_name >>"}}
    templar = get_templar(args_with_template)
    task_vars = args_with_template

    _process_libraries_args(args_with_template, templar, task_vars, "cics_data_sets", "sdfhload")

    assert "sdfhload" in list(args_with_template["cics_data_sets"].keys())
    assert args_with_template["cics_data_sets"]["sdfhload"] == "data.set.template.SDFHLOAD"


def test__process_libraries_args_without_template():
    args_with_override = {"cics_data_sets": {"sdfhload" : "data.set.template.load"}}
    templar = get_templar(args_with_override)
    task_vars = args_with_override

    _process_libraries_args(args_with_override, templar, task_vars, "cics_data_sets", "sdfhload")

    assert args_with_override["cics_data_sets"]["sdfhload"] == "data.set.template.load"


def test__process_libraries_args_without_template_or_override():
    args_with_garbage = {"cics_data_sets": {"garbage" : "more.garbage"}}
    templar = get_templar(args_with_garbage)
    task_vars = args_with_garbage

    try:
        _process_libraries_args(args_with_garbage, templar, task_vars, "cics_data_sets", "sdfhload")
    except KeyError as e:
        assert e.args[0] == "template and sdfhload"


def test__check_template():
    args_with_override = {"region_data_sets": {"dfhgcd" : {"dsn": "data.set.path"}}}
    args_with_template = {"region_data_sets": {"template" : "data.set.template.<< data_set_name >>"}}
    args_with_both = {"region_data_sets": {"template" : "data.set.template.<< data_set_name >>", "dfhgcd" : {"dsn": "data.set.path"}}}

    assert _check_template(args_with_override, "region_data_sets") is False
    assert _check_template(args_with_template, "region_data_sets") is True
    assert _check_template(args_with_both, "region_data_sets") is True


def test__set_top_libraries_key():
    args_without_top_libs = {"region_data_sets": {"template" : "data.set.template.<< data_set_name >>"}}
    _set_top_libraries_key(args_without_top_libs, "dfhrpl")

    assert "top_libraries" in list(args_without_top_libs["dfhrpl"].keys())
    assert len(list(args_without_top_libs.keys())) == 2


def test__set_top_libraries_key_with_existing_key():
    args_without_top_libs = {"region_data_sets": {"template" : "data.set.template.<< data_set_name >>"}, "dfhrpl": {"top_libraries": "data.set.path"}}

    assert len(list(args_without_top_libs.keys())) == 2

    _set_top_libraries_key(args_without_top_libs, "dfhrpl")

    assert len(list(args_without_top_libs.keys())) == 2
    assert "top_libraries" in list(args_without_top_libs["dfhrpl"].keys())


def test__remove_data_set_args_just_state():
    args_with_extra_args_not_applicable_to_start = {
        "region_data_sets": {"template" : "region.data.set.template.<< data_set_name >>"},
        "cics_data_sets": {"template" : "cics.data.set.template.<< lib_name >>"},
        "le_data_sets": {"template" : "le.data.set.template.<< lib_name >>"},
        "state": "initial"
    }

    _remove_data_set_args(args_with_extra_args_not_applicable_to_start)

    assert len(list(args_with_extra_args_not_applicable_to_start.keys())) == 3
    assert args_with_extra_args_not_applicable_to_start == {
        "region_data_sets": {"template" : "region.data.set.template.<< data_set_name >>"},
        "cics_data_sets": {"template" : "cics.data.set.template.<< lib_name >>"},
        "le_data_sets": {"template" : "le.data.set.template.<< lib_name >>"},
    }


def test__remove_data_set_args_just_space_primary():
    args_with_extra_args_not_applicable_to_start = {
        "region_data_sets": {"template" : "region.data.set.template.<< data_set_name >>"},
        "cics_data_sets": {"template" : "cics.data.set.template.<< lib_name >>"},
        "le_data_sets": {"template" : "le.data.set.template.<< lib_name >>"},
        "space_primary": 1,
    }

    _remove_data_set_args(args_with_extra_args_not_applicable_to_start)

    assert len(list(args_with_extra_args_not_applicable_to_start.keys())) == 3
    assert args_with_extra_args_not_applicable_to_start == {
        "region_data_sets": {"template" : "region.data.set.template.<< data_set_name >>"},
        "cics_data_sets": {"template" : "cics.data.set.template.<< lib_name >>"},
        "le_data_sets": {"template" : "le.data.set.template.<< lib_name >>"},
    }


def test__remove_data_set_args_just_space_type():
    args_with_extra_args_not_applicable_to_start = {
        "region_data_sets": {"template" : "region.data.set.template.<< data_set_name >>"},
        "cics_data_sets": {"template" : "cics.data.set.template.<< lib_name >>"},
        "le_data_sets": {"template" : "le.data.set.template.<< lib_name >>"},
        "space_type": "M",
    }

    _remove_data_set_args(args_with_extra_args_not_applicable_to_start)

    assert len(list(args_with_extra_args_not_applicable_to_start.keys())) == 3
    assert args_with_extra_args_not_applicable_to_start == {
        "region_data_sets": {"template" : "region.data.set.template.<< data_set_name >>"},
        "cics_data_sets": {"template" : "cics.data.set.template.<< lib_name >>"},
        "le_data_sets": {"template" : "le.data.set.template.<< lib_name >>"},
    }


def test__remove_data_set_args():
    args_with_extra_args_not_applicable_to_start = {
        "region_data_sets": {"template" : "region.data.set.template.<< data_set_name >>"},
        "cics_data_sets": {"template" : "cics.data.set.template.<< lib_name >>"},
        "le_data_sets": {"template" : "le.data.set.template.<< lib_name >>"},
        "space_primary": 1,
        "space_type": "M",
        "state": "initial"
    }

    _remove_data_set_args(args_with_extra_args_not_applicable_to_start)

    assert len(list(args_with_extra_args_not_applicable_to_start.keys())) == 3
    assert args_with_extra_args_not_applicable_to_start == {
        "region_data_sets": {"template" : "region.data.set.template.<< data_set_name >>"},
        "cics_data_sets": {"template" : "cics.data.set.template.<< lib_name >>"},
        "le_data_sets": {"template" : "le.data.set.template.<< lib_name >>"},
    }

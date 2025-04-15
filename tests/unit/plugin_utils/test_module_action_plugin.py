# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
from ansible_collections.ibm.ibm_zos_cics.plugins.plugin_utils._module_action_plugin import (
    _check_library_override,
    _check_region_override,
    _remove_region_data_set_args,
    _remove_cics_data_set_args,
    _process_region_data_set_args,
    _process_data_set_unit_args,
    _validate_data_set_length,
    _validate_list_of_data_set_lengths,
    _process_libraries_args,
    _check_template,
    _set_top_libraries_key
)


def test__check_region_override():
    args_with_override = {"region_data_sets": {"dfhgcd": {"dsn": "data.set.path"}}}
    args_with_template = {"region_data_sets": {"template": "data.set.template.<< data_set_name >>"}}
    args_with_both = {"region_data_sets": {"template": "data.set.template.<< data_set_name >>", "dfhgcd": {"dsn": "data.set.path"}}}

    assert _check_region_override(args_with_override, "dfhgcd") is True
    assert _check_region_override(args_with_template, "dfhgcd") is False
    assert _check_region_override(args_with_both, "dfhgcd") is True


def test__check_library_override():
    args_with_override = {"cics_data_sets": {"sdfhload": "data.set.path"}}
    args_with_template = {"cics_data_sets": {"template": "data.set.template.<< data_set_name >>"}}
    args_with_both = {"cics_data_sets": {"template": "data.set.template.<< data_set_name >>", "sdfhload": "data.set.path"}}

    assert _check_library_override(args_with_override, "cics_data_sets", "sdfhload") is True
    assert _check_library_override(args_with_template, "cics_data_sets", "sdfhload") is False
    assert _check_library_override(args_with_both, "cics_data_sets", "sdfhload") is True


def test__remove_region_data_set_args():
    args_with_extra_region_data_sets = {"region_data_sets": {"dfhgcd": {"dsn": "data.set.path"}, "dfhlcd": {"dsn": "data.set.path"}}}
    _remove_region_data_set_args(args_with_extra_region_data_sets, "dfhgcd")

    assert "dfhgcd" in list(args_with_extra_region_data_sets["region_data_sets"].keys())
    assert "dfhlcd" not in list(args_with_extra_region_data_sets["region_data_sets"].keys())


def test__remove_cics_data_set_args():
    args_with_extra_cics_data_sets = {"cics_data_sets": {"sdfhload": "data.set.path", "sdfhlic": "data.set.path", "sdfhauth": "data.set.path"}}
    _remove_cics_data_set_args(args_with_extra_cics_data_sets, "sdfhload")

    assert "sdfhload" in list(args_with_extra_cics_data_sets["cics_data_sets"].keys())
    assert "sdfhlic" not in list(args_with_extra_cics_data_sets["cics_data_sets"].keys())
    assert "sdfhauth" not in list(args_with_extra_cics_data_sets["cics_data_sets"].keys())


def test__process_region_data_set_args_with_template():
    args_with_template = {"region_data_sets": {"template": "data.set.template.<< data_set_name >>"}}

    assert "dfhgcd" in list(args_with_template["region_data_sets"].keys())
    assert args_with_template["region_data_sets"]["dfhgcd"] == {"dsn": "data.set.template.DFHGCD"}


def test__process_region_data_set_args_without_template():
    args_with_override = {"region_data_sets": {"dfhgcd": {"dsn": "data.set.template.global"}}}

    _process_region_data_set_args(args_with_override, "dfhgcd")

    assert args_with_override["region_data_sets"]["dfhgcd"]["dsn"] == "data.set.template.global"


def test__process_region_data_set_args_without_template_or_override():
    args_with_garbage = {"region_data_sets": {"garbage": "more.garbage"}}

    try:
        _process_region_data_set_args(args_with_garbage, "dfhgcd")
    except KeyError as e:
        assert e.args[0] == "No template or data set override found for dfhgcd"
    else:
        assert False


def test__process_data_set_unit_args():
    args_with_garbage = {"space_type": "K"}

    _process_data_set_unit_args(args_with_garbage)

    assert args_with_garbage["space_type"] == "k"


def test__process_data_set_unit_args_already_lower():
    args_with_garbage = {"space_type": "rec"}

    _process_data_set_unit_args(args_with_garbage)

    assert args_with_garbage["space_type"] == "rec"


def test__validate_data_set_length():
    _validate_data_set_length("DATA.SET.DFHAUXT")
    _validate_data_set_length("DATA.SET.TEST.UNITS.SDFHAUTH")
    # 44 characters
    _validate_data_set_length("TESTDATA.TESTDATA.TESTDATA.TESTDATA.DFHINTRA")


def test__validate_data_set_length_too_long():
    ds_name = "data.set.template.long.name.should.fail.global.dfhcsd"
    try:
        _validate_data_set_length(ds_name)
    except ValueError as e:
        assert e.args[0] == "Data set: {0} is longer than 44 characters.".format(ds_name)
    else:
        assert False


def test__validate_data_set_length_45_characters():
    ds_name = "testdata.testdata.testdata.tests.dfh.dfhintra"
    try:
        _validate_data_set_length(ds_name)
    except ValueError as e:
        assert e.args[0] == "Data set: {0} is longer than 44 characters.".format(ds_name)
    else:
        assert False


def test__validate_list_of_data_set_lengths():
    ds_list = ["testdata.testdata.testdata.tests.dfhcsd", "testdata.testdata.testdata.tests.dfhintra"]
    _validate_list_of_data_set_lengths(ds_list)


def test__validate_list_of_data_set_lengths_one_too_long():
    ds_list = ["testdata.testdata.testdata.tests.dfhcsd", "testdata.testdata.testdata.tests.intra.dfhintra"]
    try:
        _validate_list_of_data_set_lengths(ds_list)
    except ValueError as e:
        assert e.args[0] == "Data set: {0} is longer than 44 characters.".format("testdata.testdata.testdata.tests.intra.dfhintra")
    else:
        assert False


def test__process_libraries_args_with_template():
    args_with_template = {"cics_data_sets": {"template": "data.set.template.<< lib_name >>"}}

    _process_libraries_args(args_with_template, "cics_data_sets", "sdfhload")

    assert "sdfhload" in list(args_with_template["cics_data_sets"].keys())
    assert args_with_template["cics_data_sets"]["sdfhload"] == "data.set.template.SDFHLOAD"


def test__process_libraries_args_with_too_long_cics_data_set():
    args_with_template = {"cics_data_sets": {"template": "data.set.template.too.long.for.jcl.rules.<< lib_name >>"}}

    try:
        _process_libraries_args(args_with_template, "cics_data_sets", "sdfhload")
    except ValueError as e:
        assert e.args[0] == "Data set: data.set.template.too.long.for.jcl.rules.SDFHLOAD is longer than 44 characters."
    else:
        assert False
    assert args_with_template["cics_data_sets"]["sdfhload"] == "data.set.template.too.long.for.jcl.rules.SDFHLOAD"


def test__process_libraries_args_with_too_long_le_data_set():
    args_with_template = {"le_data_sets": {"template": "data.set.template.too.long.for.jcl.rules.<< lib_name >>"}}

    try:
        _process_libraries_args(args_with_template, "le_data_sets", "sceecics")
    except ValueError as e:
        assert e.args[0] == "Data set: data.set.template.too.long.for.jcl.rules.SCEECICS is longer than 44 characters."
    else:
        assert False
    assert args_with_template["le_data_sets"]["sceecics"] == "data.set.template.too.long.for.jcl.rules.SCEECICS"


def test__process_libraries_args_without_template():
    args_with_override = {"cics_data_sets": {"sdfhload": "data.set.template.load"}}

    _process_libraries_args(args_with_override, "cics_data_sets", "sdfhload")

    assert args_with_override["cics_data_sets"]["sdfhload"] == "data.set.template.load"


def test__process_libraries_args_without_template_or_override():
    args_with_garbage = {"cics_data_sets": {"garbage": "more.garbage"}}

    try:
        _process_libraries_args(args_with_garbage, "cics_data_sets", "sdfhload")
    except KeyError as e:
        assert e.args[0] == "No template or library override found for sdfhload"
    else:
        assert False


def test__check_template():
    args_with_override = {"region_data_sets": {"dfhgcd": {"dsn": "data.set.path"}}}
    args_with_template = {"region_data_sets": {"template": "data.set.template.<< data_set_name >>"}}
    args_with_both = {"region_data_sets": {"template": "data.set.template.<< data_set_name >>", "dfhgcd": {"dsn": "data.set.path"}}}

    assert _check_template(args_with_override, "region_data_sets") is False
    assert _check_template(args_with_template, "region_data_sets") is True
    assert _check_template(args_with_both, "region_data_sets") is True


def test__set_top_libraries_key():
    args_without_top_libs = {"region_data_sets": {"template": "data.set.template.<< data_set_name >>"}}
    _set_top_libraries_key(args_without_top_libs, "dfhrpl")

    assert "top_data_sets" in list(args_without_top_libs["dfhrpl"].keys())
    assert len(list(args_without_top_libs.keys())) == 2


def test__set_top_libraries_key_with_existing_key():
    args_without_top_libs = {"region_data_sets": {"template": "data.set.template.<< data_set_name >>"}, "dfhrpl": {"top_data_sets": "data.set.path"}}

    assert len(list(args_without_top_libs.keys())) == 2

    _set_top_libraries_key(args_without_top_libs, "dfhrpl")

    assert len(list(args_without_top_libs.keys())) == 2
    assert "top_data_sets" in list(args_without_top_libs["dfhrpl"].keys())
    assert args_without_top_libs["dfhrpl"]["top_data_sets"] == "data.set.path"


def test__set_top_libraries_key_with_existing_libraries_key_not_top_libraries_key():
    args_without_top_libs = {"region_data_sets": {"template": "data.set.template.<< data_set_name >>"}, "dfhrpl": {"data_sets": "data.set.path"}}

    assert len(list(args_without_top_libs.keys())) == 2
    _set_top_libraries_key(args_without_top_libs, "dfhrpl")

    assert len(list(args_without_top_libs.keys())) == 2
    assert "top_data_sets" in list(args_without_top_libs["dfhrpl"].keys())
    assert args_without_top_libs["dfhrpl"]["data_sets"] == "data.set.path"

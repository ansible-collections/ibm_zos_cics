# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from mock import MagicMock
from ansible_collections.ibm.ibm_zos_cics.plugins.modules.stop_region import (
    AnsibleStopCICSModule as stop_region, SDTRAN
)

from ansible_collections.ibm.ibm_zos_cics.tests.unit.helpers.data_set_helper import (
    set_module_args
)
default_arg_parms = {
    "job_id": "ANS12345",
    "mode": "normal"
}


def initialise_module(**kwargs):
    initial_args = default_arg_parms
    initial_args.update(kwargs)
    set_module_args(initial_args)
    stop_module = stop_region()
    # Mock Ansible module fail and exits, this prevents sys.exit being called but retains an accurate results
    stop_module._module.fail_json = MagicMock(return_value=None)
    stop_module._module.exit_json = MagicMock(return_value=None)
    return stop_module


def test__validate_sdtran():
    stop_module = initialise_module()
    stop_module._module.params[SDTRAN] = "CESD"
    stop_module.main()
    assert stop_module.failed is False


def test__validate_sdtran_3_chars():
    stop_module = initialise_module()
    stop_module._module.params[SDTRAN] = "C$D"
    stop_module.main()
    assert stop_module.failed is False


def test__validate_sdtran_numerical():
    stop_module = initialise_module()
    stop_module._module.params[SDTRAN] = "1234"
    stop_module.main()
    assert stop_module.failed is False


def test__validate_sdtran_too_long():
    stop_module = initialise_module()
    stop_module._module.params[SDTRAN] = "CESDS"
    stop_module.main()
    assert stop_module.failed
    assert (
        stop_module.msg
        == "Value: CESDS, is invalid. SDTRAN value must be  1-4 characters."
    )

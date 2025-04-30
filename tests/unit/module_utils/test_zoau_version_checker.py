# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2025
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)


import pytest
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _zoau_version_checker


def test_check_zoau_version_higher_than_min():
    _zoau_version_checker.ZOAU_API_VERSION = "1.3.0.1"
    _zoau_version_checker._check_zoau_version()


def test_check_zoau_version_higher_equal_to_min():
    _zoau_version_checker.ZOAU_API_VERSION = "1.3.0.0"
    _zoau_version_checker._check_zoau_version()


def test_check_zoau_version_lower_than_min():
    _zoau_version_checker.ZOAU_API_VERSION = "1.2.9.9"
    with pytest.raises(ImportError) as err:
        _zoau_version_checker._check_zoau_version()
    assert _zoau_version_checker.IMPORT_ERROR_MESSAGE in err.value.msg

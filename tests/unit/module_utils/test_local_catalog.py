# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.modules import local_catalog
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
import pytest
import sys


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_get_idcams_cmd_megabytes():
    catalog_size = dataset_utils._dataset_size(
        unit="M", primary=3, secondary=1)
    catalog = local_catalog._data_set(
        size=catalog_size,
        name="ANSI.CYLS.DFHLCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        exists=False,
        vsam=False)
    idcams_cmd_lcd = dataset_utils._build_idcams_define_cmd(local_catalog._get_idcams_cmd_lcd(catalog))
    assert idcams_cmd_lcd == '''
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHLCD) -
    MEGABYTES(3 1) -
    RECORDSIZE(70 2041) -
    INDEXED -
    KEYS(52 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE) -
    DATA (NAME(ANSI.CYLS.DFHLCD.DATA) -
    CONTROLINTERVALSIZE(2048)) -
    INDEX(NAME(ANSI.CYLS.DFHLCD.INDEX))
    '''


@pytest.mark.skipif(sys.version_info.major < 3, reason="Requires python 3 language features")
def test_get_idcams_cmd_cylinders():
    catalog_size = dataset_utils._dataset_size(
        unit="CYL", primary=3, secondary=1)
    catalog = local_catalog._data_set(
        size=catalog_size,
        name="ANSI.CYLS.DFHLCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        exists=False,
        vsam=False)
    idcams_cmd_lcd = dataset_utils._build_idcams_define_cmd(local_catalog._get_idcams_cmd_lcd(catalog))
    assert idcams_cmd_lcd == '''
    DEFINE CLUSTER (NAME(ANSI.CYLS.DFHLCD) -
    CYLINDERS(3 1) -
    RECORDSIZE(70 2041) -
    INDEXED -
    KEYS(52 0) -
    FREESPACE(10 10) -
    SHAREOPTIONS(2) -
    REUSE) -
    DATA (NAME(ANSI.CYLS.DFHLCD.DATA) -
    CONTROLINTERVALSIZE(2048)) -
    INDEX(NAME(ANSI.CYLS.DFHLCD.INDEX))
    '''


def test_local_catalog_class():
    catalog_size = dataset_utils._dataset_size(unit="M", primary=10, secondary=1)
    catalog = local_catalog._data_set(
        size=catalog_size,
        name="ANSI.TEST.DFHLCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        exists=False,
        vsam=False)
    assert catalog == {
        "size": {
            "unit": "M",
            "primary": 10,
            "secondary": 1
        },
        "name": "ANSI.TEST.DFHLCD",
        "sdfhload": "CICSTS.IN56.SDFHLOAD",
        "state": "initial",
        "exists": False,
        "vsam": False,
    }

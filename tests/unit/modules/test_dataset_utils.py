# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import global_catalog
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import local_catalog


def test_catalog_size_class():
    catalog_size = dataset_utils._dataset_size(unit="M", primary=10, secondary=1, record_count=70, record_size=2041, control_interval_size=2048)
    assert catalog_size == {
        'unit': "M",
        'primary': 10,
        'secondary': 1,
        'record_count': 70,
        'record_size': 2041,
        'control_interval_size': 2048
    }


def test_global_catalog_class():
    catalog_size = dataset_utils._dataset_size(unit="M", primary=10, secondary=1, record_count=4089, record_size=32760, control_interval_size=32768)
    catalog = global_catalog._global_catalog(
        size=catalog_size,
        name="ANSI.TEST.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        vsam=False)
    assert catalog == {
        "size": {
            "unit": "M",
            "primary": 10,
            "secondary": 1,
            "record_count": 4089,
            "record_size": 32760,
            "control_interval_size": 32768
        },
        "name": "ANSI.TEST.DFHGCD",
        "sdfhload": "CICSTS.IN56.SDFHLOAD",
        "state": "initial",
        "autostart_override": "",
        "nextstart": "",
        "exists": False,
        "vsam": False,
    }


def test_local_catalog_class():
    catalog_size = dataset_utils._dataset_size(unit="M", primary=10, secondary=1, record_count=4089, record_size=32760, control_interval_size=32768)
    catalog = local_catalog._local_catalog(
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
            "secondary": 1,
            "record_count": 4089,
            "record_size": 32760,
            "control_interval_size": 32768
        },
        "name": "ANSI.TEST.DFHLCD",
        "sdfhload": "CICSTS.IN56.SDFHLOAD",
        "state": "initial",
        "exists": False,
        "vsam": False,
    }


def test_unit_size_m():
    unit = "M"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "MEGABYTES"


def test_unit_size_k():
    unit = "K"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "KILOBYTES"


def test_unit_size_cyl():
    unit = "CYL"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "CYLINDERS"


def test_unit_size_rec():
    unit = "REC"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "RECORDS"


def test_unit_size_trk():
    unit = "TRK"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "TRACKS"


def test_unit_size_bad_unit():
    unit = "FISHES"
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "MEGABYTES"


def test_unit_size_empty():
    unit = ""
    unit_string = dataset_utils._get_dataset_size_unit(unit)
    assert unit_string == "MEGABYTES"

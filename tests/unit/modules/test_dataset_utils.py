# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from unittest.mock import Mock


def test_catalog_size_class():
    catalog_size = dataset_utils.CatalogSize(unit="M", primary=10, secondary=1)
    catalog_dict = catalog_size.to_dict()
    assert catalog_dict == {
        "unit": "M",
        "primary": 10,
        "secondary": 1
    }


def test_global_catalog_class():
    catalog_size = dataset_utils.CatalogSize(unit="M", primary=10, secondary=1)
    global_catalog = dataset_utils.GlobalCatalog(
        size=catalog_size,
        name="ANSI.TEST.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        vsam=False)
    catalog_dict = global_catalog.to_dict()
    assert catalog_dict == {
        "size": {
            "unit": "M",
            "primary": 10,
            "secondary": 1
        },
        "name": "ANSI.TEST.DFHGCD",
        "sdfhload": "CICSTS.IN56.SDFHLOAD",
        "state": "initial",
        "autostart_override": "",
        "nextstart": "",
        "exists": False,
        "vsam": False,
    }


def test_catalog_response_class():
    catalog_resp = dataset_utils.CatalogResponse(
        success=True, rc=0, msg="Great success!")
    response_dict = catalog_resp.to_dict()
    assert response_dict == {
        "success": True,
        "rc": 0,
        "msg": "Great success!"
    }


def test_update_catalog_props_exists():
    mock_dep = Mock()
    mock_dep.exists.return_value = True
    mock_dep.ds_type.return_value = "VSAM"
    dataset_utils.DataSetUtils = Mock(return_value=mock_dep)

    catalog_size = dataset_utils.CatalogSize(unit="M", primary=10, secondary=1)
    global_catalog = dataset_utils.GlobalCatalog(
        size=catalog_size,
        name="ANSI.TEST.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        vsam=False)
    result = dataset_utils.update_catalog_props(global_catalog)
    assert result.to_dict()['exists']
    assert result.to_dict()['vsam']
    mock_dep.exists.assert_called_once()


def test_update_catalog_props_vsam():
    mock_dep = Mock()
    mock_dep.exists.return_value = False
    mock_dep.ds_type.return_value = None
    dataset_utils.DataSetUtils = Mock(return_value=mock_dep)

    catalog_size = dataset_utils.CatalogSize(unit="M", primary=10, secondary=1)
    global_catalog = dataset_utils.GlobalCatalog(
        size=catalog_size,
        name="ANSI.TEST.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        vsam=False)
    result = dataset_utils.update_catalog_props(global_catalog)
    assert not result.to_dict()['exists']
    assert not result.to_dict()['vsam']
    mock_dep.exists.assert_called_once()


def test_unit_size_m():
    unit = "M"
    unit_string = dataset_utils.get_catalog_size_unit(unit)
    assert unit_string == "MEGABYTES"


def test_unit_size_k():
    unit = "K"
    unit_string = dataset_utils.get_catalog_size_unit(unit)
    assert unit_string == "KILOBYTES"


def test_unit_size_cyl():
    unit = "CYL"
    unit_string = dataset_utils.get_catalog_size_unit(unit)
    assert unit_string == "CYLINDERS"


def test_unit_size_rec():
    unit = "REC"
    unit_string = dataset_utils.get_catalog_size_unit(unit)
    assert unit_string == "RECORDS"


def test_unit_size_trk():
    unit = "TRK"
    unit_string = dataset_utils.get_catalog_size_unit(unit)
    assert unit_string == "TRACKS"


def test_unit_size_bad_unit():
    unit = "FISHES"
    unit_string = dataset_utils.get_catalog_size_unit(unit)
    assert unit_string == "MEGABYTES"


def test_unit_size_empty():
    unit = ""
    unit_string = dataset_utils.get_catalog_size_unit(unit)
    assert unit_string == "MEGABYTES"


def test_get_idcams_cmd_m():
    catalog_size = dataset_utils.CatalogSize(unit="M", primary=10, secondary=1)
    catalog = dataset_utils.GlobalCatalog(
        size=catalog_size,
        name="ANSI.TEST.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        vsam=False)
    idcams_cmd = dataset_utils.get_idcams_create_cmd(catalog)
    assert idcams_cmd == '''
    DEFINE CLUSTER -
        (NAME(ANSI.TEST.DFHGCD) -
        INDEXED                      -
        MEGABYTES(10 1)             -
        SHR(2)              -
        FREESPACE(10 10)              -
        RECORDSIZE(4089 32760)       -
        REUSE)              -
        DATA                           -
        (NAME(ANSI.TEST.DFHGCD.DATA)  -
        CONTROLINTERVALSIZE(32768)    -
        KEYS(52 0))  -
        INDEX                          -
        (NAME(ANSI.TEST.DFHGCD.INDEX))
    '''


def test_get_idcams_cmd_cyl():
    catalog_size = dataset_utils.CatalogSize(
        unit="CYL", primary=3, secondary=1)
    catalog = dataset_utils.GlobalCatalog(
        size=catalog_size,
        name="ANSI.CYLS.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        vsam=False)
    idcams_cmd = dataset_utils.get_idcams_create_cmd(catalog)
    assert idcams_cmd == '''
    DEFINE CLUSTER -
        (NAME(ANSI.CYLS.DFHGCD) -
        INDEXED                      -
        CYLINDERS(3 1)             -
        SHR(2)              -
        FREESPACE(10 10)              -
        RECORDSIZE(4089 32760)       -
        REUSE)              -
        DATA                           -
        (NAME(ANSI.CYLS.DFHGCD.DATA)  -
        CONTROLINTERVALSIZE(32768)    -
        KEYS(52 0))  -
        INDEX                          -
        (NAME(ANSI.CYLS.DFHGCD.INDEX))
    '''

# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


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
    dataset_utils.listcat = MagicMock(return_value=(0, "1IDCAMS  SYSTEM SERVICES                 "
                                                    "                          TIME: 13:29:18    "
                                                    "    06/26/23     PAGE      1\n0        \n  L"
                                                    "ISTCAT ENTRIES('ANSIBIT.CICS.TESTS.A294D11B."
                                                    "DFHGCD')\n0CLUSTER ------- ANSIBIT.CICS.TEST"
                                                    "S.A294D11B.DFHGCD\n      IN-CAT --- ICFCAT.S"
                                                    "YSPLEX2.CATALOGB\n0   DATA ------- ANSIBIT.C"
                                                    "ICS.TESTS.A294D11B.DFHGCD.DATA\n      IN-CAT"
                                                    " --- ICFCAT.SYSPLEX2.CATALOGB\n0   INDEX ---"
                                                    "--- ANSIBIT.CICS.TESTS.A294D11B.DFHGCD.INDEX"
                                                    "\n      IN-CAT --- ICFCAT.SYSPLEX2.CATALOGB\n"
                                                    "1IDCAMS  SYSTEM SERVICES                    "
                                                    "                       TIME: 13:29:18       "
                                                    " 06/26/23     PAGE      2\n0         THE NUM"
                                                    "BER OF ENTRIES PROCESSED WAS:\n             "
                                                    "       AIX -------------------0\n           "
                                                    "         ALIAS -----------------0\n         "
                                                    "           CLUSTER ---------------1\n       "
                                                    "             DATA ------------------1\n     "
                                                    "               GDG -------------------0\n   "
                                                    "                 INDEX -----------------1\n "
                                                    "                   NONVSAM ---------------0\n"
                                                    "                    PAGESPACE -------------0\n"
                                                    "                    PATH ------------------0\n"
                                                    "                    SPACE -----------------0\n"
                                                    "                    USERCATALOG -----------0\n"
                                                    "                    TAPELIBRARY -----------0\n"
                                                    "                    TAPEVOLUME ------------0\n"
                                                    "                    TOTAL -----------------3\n"
                                                    "0         THE NUMBER OF PROTECTED ENTRIES SUPP"
                                                    "RESSED WAS 0\n0IDC0001I FUNCTION COMPLETED, HI"
                                                    "GHEST CONDITION CODE WAS 0\n0        \n0IDC000"
                                                    "2I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITI"
                                                    "ON CODE WAS 0", ""))

    catalog_size = dataset_utils.CatalogSize(unit="M", primary=10, secondary=1)
    global_catalog = dataset_utils.GlobalCatalog(
        size=catalog_size,
        name="ANSIBIT.CICS.TESTS.A294D11B.DFHGCD",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        vsam=False)
    result = dataset_utils.update_catalog_props(global_catalog)
    assert result.to_dict()['exists']
    assert result.to_dict()['vsam']
    dataset_utils.listcat.assert_called_once()


def test_update_catalog_props_vsam():
    dataset_utils.listcat = MagicMock(return_value=(0, "\n1IDCAMS  SYSTEM SERVICES                "
                                                    "                           TIME: 13:57:46    "
                                                    "    06/26/23    \nPAGE      1\n0        \n  L"
                                                    "ISTCAT ENTRIES('ANSIBIT.CICS.TESTS.A294D11B.D"
                                                    "FHGAA')\n0IDC3012I ENTRY ANSIBIT.CICS.TESTS.A"
                                                    "294D11B.DFHGAA NOT FOUND\n IDC3009I ** VSAM C"
                                                    "ATALOG RETURN CODE IS 8 - REASON CODE IS IGG0"
                                                    "CLEG-42\n IDC1566I ** ANSIBIT.CICS.TESTS.A294"
                                                    "D11B.DFHGAA NOT LISTED\n1IDCAMS  SYSTEM SERVI"
                                                    "CES                                          "
                                                    " TIME: 13:57:46        06/26/23    \nPAGE    "
                                                    "  2\n0         THE NUMBER OF ENTRIES PROCESSE"
                                                    "D WAS:\n0                   AIX -------------"
                                                    "------0\n                    ALIAS ----------"
                                                    "-------0\n                    CLUSTER -------"
                                                    "--------0\n                    DATA ---------"
                                                    "---------0\n                    GDG ---------"
                                                    "----------0\n                    INDEX ------"
                                                    "-----------0\n                    NONVSAM ---"
                                                    "------------0\n                    PAGESPACE "
                                                    "-------------0\n                    PATH ----"
                                                    "--------------0\n                    SPACE --"
                                                    "---------------0\n                    USERCAT"
                                                    "ALOG -----------0\n                    TAPELI"
                                                    "BRARY -----------0\n                    TAPEV"
                                                    "OLUME ------------0\n                    TOTA"
                                                    "L -----------------0\n0         THE NUMBER OF"
                                                    " PROTECTED ENTRIES SUPPRESSED WAS 0\n0IDC0001"
                                                    "I FUNCTION COMPLETED, HIGHEST CONDITION CODE "
                                                    "WAS 4\n0        \n0IDC0002I IDCAMS PROCESSING"
                                                    " COMPLETE. MAXIMUM CONDITION CODE WAS 4", ""))

    catalog_size = dataset_utils.CatalogSize(unit="M", primary=10, secondary=1)
    global_catalog = dataset_utils.GlobalCatalog(
        size=catalog_size,
        name="ANSIBIT.CICS.TESTS.A294D11B.DFHGAA",
        sdfhload="CICSTS.IN56.SDFHLOAD",
        state="initial",
        autostart_override="",
        nextstart="",
        exists=False,
        vsam=False)
    result = dataset_utils.update_catalog_props(global_catalog)
    assert not result.to_dict()['exists']
    assert not result.to_dict()['vsam']
    dataset_utils.listcat.assert_called_once()


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

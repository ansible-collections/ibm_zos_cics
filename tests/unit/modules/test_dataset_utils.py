# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import dataset_utils
from unittest.mock import Mock


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

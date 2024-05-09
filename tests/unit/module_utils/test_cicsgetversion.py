from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import _cicsgetversion as cicsgetversion
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


def test_get_dataset_member_version_record():
    stdout = '''
    *                                                               *
    * STATUS = 7.1.0                                                *
    *                                                               *
    *---------------------------------------------------------------*
    *                                                               *
    * DESCRIPTION :                                                 *

    '''
    cicsgetversion.read = MagicMock(return_value=stdout)

    ds = 'CICS.TEST.PATH'
    result = cicsgetversion.get_dataset_member_version_record(ds)
    assert result == '7.1.0'


def test_get_dataset_member_version_record_not_present():
    stdout = '''
    *                                                               *
    * STATUS =                                                      *
    *                                                               *
    *---------------------------------------------------------------*
    *                                                               *
    * DESCRIPTION :                                                 *

    '''
    cicsgetversion.read = MagicMock(return_value=stdout)

    error_raised = False
    try:
        cicsgetversion.get_dataset_member_version_record('CICS.TEST.PATH')
    except Exception as e:
        print((repr(e)))
        error_raised = True
    assert error_raised


def test_get_dataset_member_version_record_too_long():
    stdout = '''
    *                                                               *
    * STATUS = 1234647473636738383762728                            *
    *                                                               *
    *---------------------------------------------------------------*
    *                                                               *
    * DESCRIPTION :                                                 *

    '''
    cicsgetversion.read = MagicMock(return_value=stdout)

    error_raised = False
    try:
        cicsgetversion.get_dataset_member_version_record('CICS.TEST.PATH')
    except Exception as e:
        print((repr(e)))
        error_raised = True
    assert error_raised


def test_get_dataset_member_version_record_blank():
    stdout = '''
    '''
    cicsgetversion.read = MagicMock(return_value=stdout)

    error_raised = False
    try:
        cicsgetversion.get_dataset_member_version_record('CICS.TEST.PATH')
    except Exception as e:
        print((repr(e)))
        error_raised = True
    assert error_raised

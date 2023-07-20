from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import cicsgetversion
try:
    import unittest
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


class CICSGetVersionUnitTests(unittest.TestCase):
    def test_get_dataset_member_version_record(self):
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
        self.assertEqual(result, '7.1.0')

    def test_get_dataset_member_version_record_not_present(self):
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

    def test_get_dataset_member_version_record_too_long(self):
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

    def test_get_dataset_member_version_record_blank(self):
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

    if __name__ == '__main__':
        unittest.main()

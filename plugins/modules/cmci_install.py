# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.cmci import (
    AnsibleCMCIModule, RESOURCE
)

from typing import Dict, Optional


LOCATION = 'location'


class AnsibleCMCIInstallModule(AnsibleCMCIModule):
    def __init__(self):
        super(AnsibleCMCIInstallModule, self).__init__('PUT', 'install')

    def init_argument_spec(self):  # type: () -> Dict
        argument_spec = super(AnsibleCMCIInstallModule, self).init_argument_spec()
        argument_spec[RESOURCE]['options'][LOCATION] = {
            'type': 'str',
            'required': False,
            'choices': ['BAS', 'CSD']
        }
        return argument_spec

    def init_body(self):  # type: () -> Optional[Dict]
        location = self._p.get(RESOURCE).get(LOCATION)
        return {
            'request': {
                'action': {
                    '@name': 'INSTALL' if location == 'BAS' else 'CSDINSTALL'
                }
            }
        }


def main():
    AnsibleCMCIInstallModule().main()


if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.cicsgetversion import (get_dataset_member_version_record)

from typing import Dict

HIGH_LEVEL_QUALIFIER = 'CICS_HLQ'


class CicsVersion(object):

    def __init__(self):
        self._module = AnsibleModule(
            argument_spec=self.init_argument_spec(),
        )  # type AnsibleModule
        self.result = dict(changed=False)   # type: dict

    def init_argument_spec(self):   # type: () -> Dict
        return {
            HIGH_LEVEL_QUALIFIER: {
                'required': True,
                'type': 'str'
            },
        }

    def _fail(self, msg):  # type: (str) -> None
        self._module.fail_json(msg=msg, **self.result)

    def _exit(self):
        self._module.exit_json(**self.result)

    def main(self):
        self.result['params'] = self._module.params

        try:
            cics_version = get_dataset_member_version_record(self._module.params.get(HIGH_LEVEL_QUALIFIER))
            self.result['cics_version'] = cics_version
            self.result['rc'] = 0
            self._exit()
        except Exception as e:
            self.result['rc'] = 1
            self.result['exception'] = e
            self._fail("Error fetching version information from dataset with {0}".format(self._module.params.get(HIGH_LEVEL_QUALIFIER)))


def main():
    CicsVersion().main()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.cmci import (
    AnsibleCMCIModule
)


_RECORD_COUNT = 'record_count'


class AnsibleCMCIGetModule(AnsibleCMCIModule):
    def __init__(self):
        super(AnsibleCMCIGetModule, self).__init__('GET', 'query')

    def init_argument_spec(self):  # type: () -> dict
        argument_spec = super(AnsibleCMCIGetModule, self).init_argument_spec()
        argument_spec.update({
            _RECORD_COUNT: {
                'type': 'int'
            }
        })
        return argument_spec

    def _init_url(self):  # type: () -> str
        url = super(AnsibleCMCIGetModule, self)._init_url()

        if self._p.get(_RECORD_COUNT):
            url = url + '//' + str(self._p.get(_RECORD_COUNT))

        return url


def main():
    AnsibleCMCIGetModule().main()


if __name__ == '__main__':
    main()

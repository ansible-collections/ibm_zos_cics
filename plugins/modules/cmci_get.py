# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.cmci import (
    AnsibleCMCIModule, append_criteria_parameter_arguments
)

from typing import Dict, Optional


_RECORD_COUNT = 'record_count'


class AnsibleCMCIGetModule(AnsibleCMCIModule):
    def __init__(self):
        super(AnsibleCMCIGetModule, self).__init__('GET')

    def init_argument_spec(self):  # type: () -> Dict
        argument_spec = super(AnsibleCMCIGetModule, self).init_argument_spec()
        argument_spec.update({
            _RECORD_COUNT: {
                'type': 'int'
            }
        })
        append_criteria_parameter_arguments(argument_spec)
        return argument_spec

    def init_request_params(self):  # type: () -> Optional[Dict[str, str]]
        return self.get_criteria_parameter_request_params()

    def init_url(self):  # type: () -> str
        url = super(AnsibleCMCIGetModule, self).init_url()

        if self._p.get(_RECORD_COUNT):
            url = url + '//' + str(self._p.get(_RECORD_COUNT))

        return url


def main():
    AnsibleCMCIGetModule().main()


if __name__ == '__main__':
    main()

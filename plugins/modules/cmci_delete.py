# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.cmci import (
    AnsibleCMCIModule, append_criteria_parameter_arguments
)

from typing import Dict, Optional


class AnsibleCMCIDeleteModule(AnsibleCMCIModule):
    def __init__(self):
        super(AnsibleCMCIDeleteModule, self).__init__('DELETE')

    def init_argument_spec(self):  # type: () -> Dict
        argument_spec = super(AnsibleCMCIDeleteModule, self).init_argument_spec()
        append_criteria_parameter_arguments(argument_spec)
        return argument_spec

    def init_request_params(self):  # type: () -> Optional[Dict[str, str]]
        return self.get_criteria_parameter_request_params()


def main():
    AnsibleCMCIDeleteModule().main()


if __name__ == '__main__':
    main()

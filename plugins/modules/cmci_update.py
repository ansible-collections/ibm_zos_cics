# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.cmci import (
    AnsibleCMCIModule, RESOURCE, PARAMETERS, ATTRIBUTES, append_parameters, append_attributes,
    append_attributes_parameters_arguments
)
from typing import Optional, Dict


class AnsibleCMCIUpdateModule(AnsibleCMCIModule):
    def __init__(self):
        super(AnsibleCMCIUpdateModule, self).__init__('PUT', 'update')

    def init_argument_spec(self):  # type: () -> Dict
        argument_spec = super(AnsibleCMCIUpdateModule, self).init_argument_spec()
        append_attributes_parameters_arguments(argument_spec)
        return argument_spec

    def init_body(self):  # type: () -> Optional[Dict]
        resource = self._p.get(RESOURCE)

        update = {}
        append_parameters(update, resource.get(PARAMETERS))
        append_attributes(update, resource.get(ATTRIBUTES))

        return {
            'request': {
                'update': update
            }
        }


def main():
    AnsibleCMCIUpdateModule().main()


if __name__ == '__main__':
    main()

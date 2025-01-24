# (c) Copyright IBM Corp. 2025
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):

    # Simple action plugin that just returns the ansible_user var

    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)

        processed_ouput = {
            "name": task_vars["ansible_user"]
        }

        return processed_ouput

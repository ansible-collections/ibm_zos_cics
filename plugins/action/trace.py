# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.controller_utils.module_action_plugin import _DataSetActionPlugin


class ActionModule(_DataSetActionPlugin):
    def run(self, tmp=None, task_vars=None):
        module_args = self._task.args.copy()

        if (not (module_args.get("destination"))) or (
                module_args.get("destination") == "A"):
            ds_name = "dfhauxt"
        else:
            ds_name = "dfhbuxt"

        return super(ActionModule, self)._run(
            ds_name=ds_name,
            module_name="trace",
            cics_data_sets_required=False,
            tmp=tmp,
            task_vars=task_vars,
        )

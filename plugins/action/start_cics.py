# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible_collections.ibm.ibm_zos_cics.plugins.controller_utils.module_action_plugin import (
    LE_DS_KEYS,
    REGION_DS_KEYS,
    CICS_DS_KEYS,
    LIBRARY_KEYS,
    _process_libraries_args,
    _process_region_data_set_args,
    _remove_data_set_args,
    _set_top_libraries_key,
    _validate_list_of_data_set_lengths
)

MODULE_NAME = 'ibm.ibm_zos_cics.start_cics'


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        self.module_args = self._task.args.copy()

        try:
            _process_module_args(self.module_args, self._templar, task_vars)
        except KeyError as e:
            message = "Argument {0} undefined".format(e.args[0])
            return {"failed": True, "changed": False, "msg": message, "args": self.module_args}

        return self._execute_module(
            module_name=MODULE_NAME,
            module_args=self.module_args,
            task_vars=task_vars,
            tmp=tmp
        )


def _process_module_args(module_args, _templar, task_vars):
    for library_key in LIBRARY_KEYS:
        _set_top_libraries_key(module_args, library_key)
        _validate_list_of_data_set_lengths(module_args[library_key]["top_libraries"])
        _validate_list_of_data_set_lengths(module_args[library_key].get("libraries", []))

    for cics_lib in CICS_DS_KEYS:
        _process_libraries_args(module_args, _templar, task_vars, "cics_data_sets", cics_lib)

    for region_ds in REGION_DS_KEYS:
        _process_region_data_set_args(module_args, _templar, region_ds, task_vars)
    # Template field in region_data_sets needs to be removed before module execution
    if module_args["region_data_sets"].get("template"):
        del module_args["region_data_sets"]["template"]

    for le_lib in LE_DS_KEYS:
        _process_libraries_args(module_args, _templar, task_vars, "le_data_sets", le_lib)

    # Remove extra args
    _remove_data_set_args(module_args)

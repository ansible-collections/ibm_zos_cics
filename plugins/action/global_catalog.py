# (c) Copyright IBM Corp. 2020,2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()

        # data_set_template = module_args["region_datasets"]

        # task_vars2 = task_vars.copy()
        # task_vars2.update(data_set_name="DFHGCD")
        # dfhgcd = self._templar.copy_with_new_env(
        #     variable_start_string="<<",
        #     variable_end_string=">>",
        #     available_variables=task_vars2
        # ).template(data_set_template)

        # module_args.update({
        #     'global_catalog_dataset': dfhgcd,
        # })

        module_return = self._execute_module(
            module_name='ibm.ibm_zos_cics.global_catalog',
            module_args=module_args,
            task_vars=task_vars,
            tmp=tmp)

        return module_return

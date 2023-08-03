# (c) Copyright IBM Corp. 2020,2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()

        region_datasets = module_args["region_datasets"]
        cics_install = module_args["cics_install"]

        if region_datasets.get(
                "dfhgcd",
                None) is None or region_datasets.get("dfhgcd").get(
                "dsn",
                None) is None:
            dsn = self.template_dsn(
                task_vars,
                "data_set_name",
                "DFHGCD",
                region_datasets.get("template"))
            module_args.update({
                'region_datasets': {
                    'dfhgcd': {
                        'dsn': dsn,
                    },
                    'template': region_datasets.get("template"),
                },
            })

        if cics_install.get("sdfhload", None) is None:
            dsn = self.template_dsn(
                task_vars,
                "lib_name",
                "SDFHLOAD",
                cics_install.get("template"))

            module_args.update({
                'cics_install': {
                    'sdfhload': dsn,
                    'template': cics_install.get("template"),
                },
            })

        return self._execute_module(
            module_name='ibm.ibm_zos_cics.global_catalog',
            module_args=module_args,
            task_vars=task_vars,
            tmp=tmp)

    def template_dsn(self, task_vars, var_name, replace_val, template):
        cpy = task_vars.copy()
        cpy.update({var_name: replace_val})
        return self._templar.copy_with_new_env(
            variable_start_string="<<",
            variable_end_string=">>",
            available_variables=cpy
        ).template(template)

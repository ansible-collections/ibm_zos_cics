# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.parameter_templating import template_dsn
from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()

        region_data_sets = module_args["region_data_sets"]
        cics_data_sets = module_args["cics_data_sets"]

        if region_data_sets.get(
                "dfhgcd",
                None) is None or region_data_sets.get("dfhgcd").get(
                "dsn",
                None) is None:
            dsn = template_dsn(
                task_vars,
                "data_set_name",
                "DFHGCD",
                region_data_sets.get("template"))
            module_args.update({
                'region_data_sets': {
                    'dfhgcd': {
                        'dsn': dsn,
                    },
                    'template': region_data_sets.get("template"),
                },
            })

        if cics_data_sets.get("sdfhload", None) is None:
            dsn = template_dsn(
                task_vars,
                "lib_name",
                "SDFHLOAD",
                cics_data_sets.get("template"))

            module_args.update({
                'cics_data_sets': {
                    'sdfhload': dsn,
                    'template': cics_data_sets.get("template"),
                },
            })

        return self._execute_module(
            module_name='ibm.ibm_zos_cics.global_catalog',
            module_args=module_args,
            task_vars=task_vars,
            tmp=tmp)

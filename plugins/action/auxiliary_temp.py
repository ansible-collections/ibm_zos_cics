# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.parameter_templating import (
    template_dsn,
)
from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()

        if not module_args.get("region_data_sets", None):
            return {
                "failed": True,
                "changed": False,
                "msg": "region_data_sets required",
            }

        region_data_sets = module_args["region_data_sets"]

        if (
            region_data_sets.get("dfhtemp", None) is None
            or region_data_sets.get("dfhtemp").get("dsn", None) is None
        ):
            if region_data_sets.get("template", None) is None:
                return {
                    "failed": True,
                    "changed": False,
                    "msg": "Specify either template or dfhtemp in region_data_sets",
                }
            dsn = template_dsn(
                _templar=self._templar,
                task_vars=task_vars,
                var_name="data_set_name",
                replace_val="DFHTEMP",
                template=region_data_sets.get("template", None),
            )
            module_args.update(
                {
                    "region_data_sets": {
                        "dfhtemp": {
                            "dsn": dsn,
                        },
                        "template": region_data_sets.get("template"),
                    },
                }
            )

        if "cics_data_sets" in module_args:
            cics_data_sets = module_args["cics_data_sets"]

            if (
                cics_data_sets.get("template", None) is None
                and cics_data_sets.get("sdfhload", None) is None
            ):
                return {
                    "failed": True,
                    "changed": False,
                    "msg": "Specify either template or sdfhload in cics_data_sets",
                }
            dsn = template_dsn(
                _templar=self._templar,
                task_vars=task_vars,
                var_name="lib_name",
                replace_val="SDFHLOAD",
                template=cics_data_sets.get("template", None),
            )

            module_args.update(
                {
                    "cics_data_sets": {
                        "sdfhload": dsn,
                        "template": cics_data_sets.get("template"),
                    },
                }
            )

        return self._execute_module(
            module_name="ibm.ibm_zos_cics.auxiliary_temp",
            module_args=module_args,
            task_vars=task_vars,
            tmp=tmp,
        )

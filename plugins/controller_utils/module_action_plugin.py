from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.plugins.action import ActionBase


class _ModuleActionPlugin(ActionBase):
    def _get_region_data_set_args(self, module_args, ds_name, task_vars):

        if not module_args.get("region_data_sets", None):
            raise KeyError("region_data_sets required")

        region_data_sets = module_args.get("region_data_sets")

        if not region_data_sets.get(ds_name, None) or not region_data_sets.get(ds_name).get("dsn", None):
            # Template?
            if region_data_sets.get("template", None):
                dsn = self._template_dsn(
                    _templar=self._templar,
                    task_vars=task_vars,
                    var_name="data_set_name",
                    replace_val=ds_name.upper(),
                    template=region_data_sets.get("template", None),
                )
                module_args.update(
                    {
                        "region_data_sets": {
                            ds_name: {
                                "dsn": dsn,
                            },
                            "template": region_data_sets.get("template"),
                        },
                    }
                )
            else:
                raise KeyError(
                    "Specify either template or {0} in region_data_sets".format(
                        ds_name)
                )

        return module_args

    def _get_cics_data_set_args(self, module_args, task_vars):

        if not module_args.get("cics_data_sets", None):
            raise KeyError("cics_data_sets required")

        cics_data_sets = module_args["cics_data_sets"]

        if not cics_data_sets.get("sdfhload", None):
            if not cics_data_sets.get("template", None):
                raise KeyError(
                    "Specify either template or sdfhload in cics_data_sets")
            dsn = self._template_dsn(
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
        return module_args

    def _template_dsn(self, _templar, task_vars, var_name, replace_val, template):
        cpy = task_vars.copy()
        cpy.update({var_name: replace_val})
        return _templar.copy_with_new_env(
            variable_start_string="<<",
            variable_end_string=">>",
            available_variables=cpy,
        ).template(template)

    def _run(self, ds_name, module_name, cics_data_sets_required, tmp=None, task_vars=None):
        super(_ModuleActionPlugin, self).run(tmp, task_vars)
        module_args = self._task.args.copy()

        try:
            module_args.update(
                self._get_region_data_set_args(module_args, ds_name, task_vars)
            )
        except KeyError as e:
            return {"failed": True, "changed": False, "msg": e.args[0]}

        try:
            if cics_data_sets_required:
                module_args.update(
                    self._get_cics_data_set_args(module_args, task_vars))
        except KeyError as e:
            return {"failed": True, "changed": False, "msg": e.args[0], "args": module_args}

        return self._execute_module(
            module_name="ibm.ibm_zos_cics.{0}".format(module_name),
            module_args=module_args,
            task_vars=task_vars,
            tmp=tmp,
        )

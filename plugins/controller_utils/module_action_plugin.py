from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.plugins.action import ActionBase

REGION_DS_KEYS = ["dfhgcd", "dfhlcd", "dfhintra", "dfhlrq", "dfhtemp", "dfhauxt", "dfhbuxt", "dfhdmpa", "dfhdmpb", "dfhcsd"]
CICS_DS_KEYS = ["sdfhload", "sdfhauth", "sdfhlic"]


class _ModuleActionPlugin(ActionBase):

    def _check_template(self, arg_dict):
        if self.module_args[arg_dict].get("template"):
            return True
        else:
            return False

    def _check_region_override(self, ds_name):
        if self.module_args["region_data_sets"].get(ds_name):
            if self.module_args["region_data_sets"][ds_name]["dsn"]:
                return True
        return False

    def _check_cics_override(self, ds_name):
        if self.module_args["cics_data_sets"].get(ds_name):
            return True
        else:
            return False

    def _remove_region_data_set_args(self, ds_name):
        for region_key in list(self.module_args["region_data_sets"]):
            if region_key in REGION_DS_KEYS and region_key != ds_name:
                del self.module_args["region_data_sets"][region_key]

    def _remove_cics_data_set_args(self, ds_name):
        for cics_key in list(self.module_args["cics_data_sets"]):
            if cics_key in CICS_DS_KEYS and cics_key != ds_name:
                del self.module_args["cics_data_sets"][cics_key]

    def _process_region_data_set_args(self, ds_name, task_vars):
        if self._check_region_override(ds_name):
            pass
        elif self._check_template("region_data_sets"):
            self.module_args["region_data_sets"].update({
                ds_name: {
                    "dsn": _template_dsn(
                        _templar=self._templar,
                        task_vars=task_vars,
                        var_name="data_set_name",
                        replace_val=ds_name.upper(),
                        template=self.module_args["region_data_sets"]["template"]
                    )
                }
            })
        else:
            raise KeyError("template and {0}".format(ds_name))

        self._remove_region_data_set_args(ds_name)

    def _process_cics_data_set_args(self, task_vars):
        if self._check_cics_override("sdfhload"):
            pass
        elif self._check_template("cics_data_sets"):
            self.module_args["cics_data_sets"]["sdfhload"] = _template_dsn(
                _templar=self._templar,
                task_vars=task_vars,
                var_name="lib_name",
                replace_val="SDFHLOAD",
                template=self.module_args["cics_data_sets"]["template"],
            )
        else:
            raise KeyError("template and {0}".format("sdfhload"))

        self._remove_cics_data_set_args("sdfhload")

    def _run(self, ds_name, module_name, cics_data_sets_required, tmp=None, task_vars=None):
        super(_ModuleActionPlugin, self).run(tmp, task_vars)
        self.module_args = self._task.args.copy()

        try:
            self._process_region_data_set_args(ds_name, task_vars)
        except KeyError as e:
            message = "Argument {0} undefined".format(e.args[0])
            return {"failed": True, "changed": False, "msg": message, "args": self.module_args}

        try:
            if cics_data_sets_required:
                self._process_cics_data_set_args(task_vars)
            else:
                if self.module_args.get("cics_data_sets"):
                    del self.module_args["cics_data_sets"]

        except KeyError as e:
            message = "Argument {0} undefined".format(e.args[0])
            return {"failed": True, "changed": False, "msg": message, "args": self.module_args}

        return self._execute_module(
            module_name="ibm.ibm_zos_cics.{0}".format(module_name),
            module_args=self.module_args,
            task_vars=task_vars,
            tmp=tmp,
        )


def _template_dsn(_templar, task_vars, var_name, replace_val, template):
    cpy = task_vars.copy()
    cpy.update({var_name: replace_val})
    return _templar.copy_with_new_env(
        variable_start_string="<<",
        variable_end_string=">>",
        available_variables=cpy,
    ).template(template)

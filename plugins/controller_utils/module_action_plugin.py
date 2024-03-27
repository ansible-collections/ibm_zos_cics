# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.plugins.action import ActionBase

REGION_DS_KEYS = ["dfhgcd", "dfhlcd", "dfhintra", "dfhlrq", "dfhtemp", "dfhauxt", "dfhbuxt", "dfhdmpa", "dfhdmpb", "dfhcsd"]
CICS_DS_KEYS = ["sdfhload", "sdfhauth", "sdfhlic"]
LE_DS_KEYS = ["sceecics", "sceerun", "sceerun2"]
LIBRARY_KEYS = ["steplib", "dfhrpl"]


class _DataSetActionPlugin(ActionBase):
    def _run(self, ds_name, module_name, cics_data_sets_required, tmp=None, task_vars=None):
        super(_DataSetActionPlugin, self).run(tmp, task_vars)
        self.module_args = self._task.args.copy()

        try:
            _process_module_args(self.module_args, self._templar, ds_name, task_vars, cics_data_sets_required)
        except KeyError as e:
            message = "Argument {0} undefined".format(e.args[0])
            return {"failed": True, "changed": False, "msg": message, "args": self.module_args}

        except ValueError as e:
            return {"failed": True, "changed": False, "msg": e.args[0], "args": self.module_args}

        return self._execute_module(
            module_name="ibm.ibm_zos_cics.{0}".format(module_name),
            module_args=self.module_args,
            task_vars=task_vars,
            tmp=tmp,
        )


def _process_module_args(module_args, _templar, ds_name, task_vars, cics_data_sets_required):
    _process_region_data_set_args(module_args, _templar, ds_name, task_vars)
    _remove_region_data_set_args(module_args, ds_name)

    if cics_data_sets_required:
        _process_libraries_args(module_args, _templar, task_vars, "cics_data_sets", "sdfhload")
        _remove_cics_data_set_args(module_args, "sdfhload")
    else:
        if module_args.get("cics_data_sets"):
            del module_args["cics_data_sets"]

    if module_args.get("le_data_sets"):
        del module_args["le_data_sets"]


def _check_region_override(module_args, ds_name):
    if module_args["region_data_sets"].get(ds_name):
        if module_args["region_data_sets"][ds_name]["dsn"]:
            return True
    return False


def _check_library_override(module_args, lib_type, lib_ds_name):
    if module_args[lib_type].get(lib_ds_name):
        return True
    else:
        return False


def _remove_region_data_set_args(module_args, ds_name):
    for region_key in list(module_args["region_data_sets"]):
        if region_key in REGION_DS_KEYS and region_key != ds_name:
            del module_args["region_data_sets"][region_key]


def _remove_cics_data_set_args(module_args, ds_name):
    for cics_key in list(module_args["cics_data_sets"]):
        if cics_key in CICS_DS_KEYS and cics_key != ds_name:
            del module_args["cics_data_sets"][cics_key]


def _process_region_data_set_args(module_args, _templar, ds_name, task_vars):
    if _check_region_override(module_args, ds_name):
        pass
    elif _check_template(module_args, "region_data_sets"):
        module_args["region_data_sets"].update({
            ds_name: {
                "dsn": _template_dsn(
                    _templar=_templar,
                    task_vars=task_vars,
                    var_name="data_set_name",
                    replace_val=ds_name.upper(),
                    template=module_args["region_data_sets"]["template"]
                )
            }
        })
    else:
        raise KeyError("template and {0}".format(ds_name))
    _validate_data_set_length(module_args["region_data_sets"][ds_name]["dsn"])


def _validate_list_of_data_set_lengths(data_set_list):
    for data_set in data_set_list:
        _validate_data_set_length(data_set)


def _validate_data_set_length(data_set):
    if len(data_set) > 44:
        raise ValueError("Data set: {0} is longer than 44 characters.".format(data_set))


def _process_libraries_args(module_args, _templar, task_vars, lib_type, lib_ds_name):
    if _check_library_override(module_args, lib_type, lib_ds_name):
        pass
    elif _check_template(module_args, lib_type):
        module_args[lib_type][lib_ds_name] = _template_dsn(
            _templar=_templar,
            task_vars=task_vars,
            var_name="lib_name",
            replace_val=lib_ds_name.upper(),
            template=module_args[lib_type]["template"],
        )
    else:
        raise KeyError("template and {0}".format(lib_ds_name))
    _validate_data_set_length(module_args[lib_type][lib_ds_name])


def _template_dsn(_templar, task_vars, var_name, replace_val, template):
    cpy = task_vars.copy()
    cpy.update({var_name: replace_val})
    return _templar.copy_with_new_env(
        variable_start_string="<<",
        variable_end_string=">>",
        available_variables=cpy,
    ).template(template)


def _check_template(module_args, arg_dict):
    if module_args[arg_dict].get("template"):
        return True
    else:
        return False


def _set_top_libraries_key(module_args, dict_key):
    if module_args.get(dict_key) is None:
        module_args[dict_key] = {"top_libraries": []}
    elif module_args[dict_key].get("top_libraries") is None:
        module_args[dict_key].update({"top_libraries": []})


def _remove_data_set_args(module_args):
    if "state" in list(module_args):
        del module_args["state"]
    if "space_primary" in list(module_args):
        del module_args["space_primary"]
    if "space_type" in list(module_args):
        del module_args["space_type"]

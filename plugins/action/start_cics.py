# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.ibm.ibm_zos_cics.plugins.modules.start_cics import (
    STEPLIB, REGION_DATA_SETS, CICS_DATA_SETS, LE_DATA_SETS, DSN, TEMPLATE,
    DFHRPL, TOP_LIBRARIES, region_data_sets_list)
from ansible.plugins.action import ActionBase
from ansible_collections.ibm.ibm_zos_cics.plugins.controller_utils import module_action_plugin

CICS = "CICS"
LE = 'LE'
MODULE_NAME = 'ibm.ibm_zos_cics.start_cics'


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()

        helper = ActionHelper(module_args, task_vars, self._templar)
        helper.add_steplib_libraries()
        helper.add_dfhrpl_libraries()
        helper.add_per_region_data_sets()
        if helper.result["failed"] is True:
            return helper.result
        module_return = self._execute_module(module_name=MODULE_NAME,
                                             module_args=helper.module_args,
                                             task_vars=task_vars, tmp=tmp)
        return module_return


class ActionHelper:
    def __init__(self, module_args, task_vars, templar):
        self.module_args = module_args
        self.task_vars = task_vars
        self._templar = templar
        self.result = dict(
            failed=False,
            err=[]
        )

    def add_steplib_libraries(self):
        libraries_dict = {CICS: ["sdfhauth", "sdfhlic"], LE: ["sceerun", "sceerun2"]}
        self.template_libraries(STEPLIB, libraries_dict)

    def add_dfhrpl_libraries(self):
        libraries_dict = {CICS: ["sdfhload"], LE: ["sceecics", "sceerun", "sceerun2"]}
        self.template_libraries(DFHRPL, libraries_dict)

    def add_per_region_data_sets(self):
        region_data_set_args = self.module_args[REGION_DATA_SETS]

        # Get the template they have specified, otherwise set it to None.
        template = region_data_set_args.pop(TEMPLATE, None)

        # Loop through each of the data_sets needing to be added.
        for data_set in region_data_sets_list:
            # Add the templated data_set name, or the user specified name to the data structure.
            self.write_parameters_for_per_region_data_set(region_data_set_args, data_set, template)
        self.module_args[REGION_DATA_SETS] = region_data_set_args

    def write_parameters_for_per_region_data_set(self, data_set_args, data_set_key, template):
        if template is not None:
            if data_set_args.get(data_set_key) is None:
                data_set_args[data_set_key] = {DSN: None}
        else:
            if data_set_args.get(data_set_key) is None:
                self._fail("Must provide either a template or data set name for data set: {0}"
                           .format(data_set_key.upper()))
                return

        data_set_args[data_set_key] = {DSN: self.get_dsn(data_set_args, data_set_key, template)}

    def get_dsn(self, data_sets, data_set_key, template):
        if data_sets[data_set_key].get(DSN):
            dsn = data_sets[data_set_key].get(DSN)
            return dsn.upper()
        else:
            if template is not None:
                return module_action_plugin._template_dsn(
                    _templar=self._templar,
                    task_vars=self.task_vars,
                    var_name="data_set_name",
                    replace_val=data_set_key,
                    template=template).upper()

    def _fail(self, msg):
        self.result["failed"] = True
        if not self.result["err"]:
            self.result["err"] = msg

    def template_libraries(self, dict_key, dict_of_all_libraries):
        # list of parameters they've provided

        dict_of_all_parameters = self.build_list_of_all_data_set_parameters()
        #  For each type of library (eg, LE)
        for lib_type, list_of_libs in dict_of_all_libraries.items():
            # For each of its libraries (eg, SCEERUN, SCEERUN2)
            for lib in list_of_libs:
                # We have specified a template for this data set, or an alternative name.
                if dict_of_all_parameters.get(lib_type).get(lib):
                    # They have specified a data set name
                    self.write_library_to_module_args(dict_key, dict_of_all_parameters[lib_type][lib])
                elif dict_of_all_parameters.get(lib_type).get(TEMPLATE):
                    # They have specified a template.
                    template = dict_of_all_parameters.get(lib_type).get(TEMPLATE)
                    self.write_library_to_module_args(
                        dict_key, module_action_plugin._template_dsn(
                            self._templar, self.task_vars, "lib_name", lib, template))
                else:
                    self._fail('No template or data set name provided for: {0}'.format(lib.upper()))

    def build_list_of_all_data_set_parameters(self):
        mod_args = self.module_args
        cics_data_sets = mod_args[CICS_DATA_SETS] if mod_args.get(
            CICS_DATA_SETS) else None
        le_data_sets = mod_args[LE_DATA_SETS] if mod_args.get(
            LE_DATA_SETS) else None

        return {CICS: cics_data_sets, LE: le_data_sets}

    def write_library_to_module_args(self, dict_key, library_name):
        # If they haven't specified either steplib or dfhrpl dict at all, initiate this.
        if self.module_args.get(dict_key) is None or self.module_args[dict_key].get(TOP_LIBRARIES) is None:
            self.module_args[dict_key] = {TOP_LIBRARIES: []}
        self.module_args[dict_key][TOP_LIBRARIES].append(
            library_name.upper())

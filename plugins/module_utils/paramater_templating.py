# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


def template_dsn(self, task_vars, var_name, replace_val, template):
    cpy = task_vars.copy()
    cpy.update({var_name: replace_val})
    return self._templar.copy_with_new_env(
        variable_start_string="<<",
        variable_end_string=">>",
        available_variables=cpy
    ).template(template)

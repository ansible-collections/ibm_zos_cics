#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: start_cics
short_description: Start a CICS region
description:
  - Start a CICS® region by providing CICS system data sets and system initialization parameters for CICS startup using the C(DFHSIP) program.
author: Kiera Bennett (@KieraBennett)
version_added: 1.1.0-beta.5
seealso:
  - module: stop_cics
extends_documentation_fragment:
  - ibm.ibm_zos_cics.start_cics.documentation
"""

EXAMPLES = r"""
- name: Start CICS
  ibm.ibm_zos_cics.start_cics:
    submit_jcl: True
    applid: ABC9ABC1
    cics_data_sets:
      template: 'CICSTS61.CICS.<< lib_name >>'
    le_data_sets:
      template: 'LANG.ENVIORNMENT.<< lib_name >>'
    region_data_sets:
      template: 'REGIONS.ABC9ABC1.<< data_set_name >>'
    sit_parameters:
      start: COLD
      sit: 6$
      aicons: AUTO
      auxtr: 'ON'
      auxtrsw: ALL
      cicssvc: 217
      csdrecov: BACKOUTONLY
      edsalim: 500M
      grplist: (DFHLIST,DFHTERML)
      gmtext: 'ABC9ABC1. CICS Region'
      icvr: 20000
      isc: 'YES'
      ircstrt: 'YES'
      mxt: 500
      pgaipgm: ACTIVE
      sec: 'YES'
      spool: 'YES'
      srbsvc: 218
      tcpip: 'NO'
      usshome: /usshome/directory
      wlmhealth: "OFF"
      wrkarea: 2048
      sysidnt: ZPY1
- name: Start CICS with more customization
  ibm.ibm_zos_cics.start_cics:
    submit_jcl: True
    applid: ABC9ABC1
    job_parameters:
      class: A
    cics_data_sets:
      template: 'CICSTS61.CICS.<< lib_name >>'
      sdfhauth: 'CICSTS61.OVERRDE.TEMPLT.SDFHAUTH'
    le_data_sets:
      template: 'LANG.ENVIORNMENT.<< lib_name >>'
    region_data_sets:
      template: 'REGIONS.ABC9ABC1.<< data_set_name >>'
    output_data_sets:
      default_sysout_class: B
      ceemsg:
        sysout: A
      sysprint:
        omit: True
    steplib:
      top_libraries:
        - TOP.LIBRARY.ONE
        - TOP.LIBRARY.TWO
      libraries:
        - BOTTOM.LIBRARY.ONE
    sit_parameters:
      start: COLD
      sit: 6$
      aicons: AUTO
      auxtr: 'ON'
      auxtrsw: ALL
      cicssvc: 217
      csdrecov: BACKOUTONLY
      edsalim: 500M
      grplist: (DFHLIST,DFHTERML)
      gmtext: 'ABC9ABC1. CICS Region'
      icvr: 20000
      isc: 'YES'
      ircstrt: 'YES'
      mxt: 500
      pgaipgm: ACTIVE
      stntrxx:
        ab: ALL
      skrxxxx:
        PA21: 'COMMAND'
      sec: 'YES'
      spool: 'YES'
      srbsvc: 218
      tcpip: 'NO'
      usshome: /usshome/directory
      wlmhealth: "OFF"
      wrkarea: 2048
      sysidnt: ZPY1
"""

RETURN = r"""
  changed:
    description: True if the CICS startup JCL was submitted, otherwise False.
    returned: always
    type: bool
  failed:
    description: True if the query job failed, otherwise False.
    returned: always
    type: bool
  jcl:
    description: The CICS startup JCL that is built during module execution.
    returned: always
    type: list
  job_id:
    description: The job ID of the CICS startup job.
    returned: If the CICS startup JCL has been submitted.
    type: str
  err:
    description: The error message returned when building the JCL.
    returned: always
    type: str
  executions:
    description: A list of program executions performed during the Ansible task.
    returned: always
    type: list
    elements: dict
    contains:
      name:
        description: A human-readable name for the program execution.
        type: str
        returned: always
      rc:
        description: The return code for the program execution.
        type: int
        returned: always
      stdout:
        description: The standard out stream returned by the program execution.
        type: str
        returned: always
      stderr:
        description: The standard error stream returned from the program execution.
        type: str
        returned: always
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.jcl_helper import (
    JCLHelper, DLM, DD_INSTREAM, CONTENT, END_INSTREAM, JOB_CARD, EXECS, JOB_NAME, DDS, NAME
)
import string
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser

APPLID = 'applid'
CICS_DATA_SETS = 'cics_data_sets'
CEEMSG = 'ceemsg'
CEEOUT = 'ceeout'
DD_DATA = 'DD DATA'
DD_NAME = 'dd_name'
DEFAULT_SYSOUT_CLASS = 'default_sysout_class'
DFHCXRF = 'dfhcxrf'
DFHRPL = 'dfhrpl'
DFHSIP = 'DFHSIP'
DISP = 'disp'
DSN = 'dsn'
JOB_PARAMETERS = 'job_parameters'
LE_DATA_SETS = 'le_data_sets'
LOGUSR = 'logusr'
LIBRARIES = 'libraries'
MSGUSR = 'msgusr'
OMIT = 'omit'
OUTPUT_DATA_SETS = 'output_data_sets'
PGM = 'pgm'
REGION_DATA_SETS = 'region_data_sets'
SIT_PARAMETERS = 'sit_parameters'
SHR = 'SHR'
STEPLIB = 'steplib'
SYSABEND = 'sysabend'
SYSIN = 'sysin'
SYSOUT = 'sysout'
SYSPRINT = 'sysprint'
SYSUDUMP = 'sysudump'
TEMPLATE = 'template'
TOP_LIBRARIES = 'top_libraries'

region_data_sets_list = ['dfhauxt', 'dfhbuxt', 'dfhcsd', 'dfhgcd', 'dfhintra',
                         'dfhlcd', 'dfhlrq', 'dfhtemp', 'dfhdmpa', 'dfhdmpb']


class AnsibleStartCICSModule(object):

    def __init__(self):
        self.dds = []
        self._module = AnsibleModule(
            argument_spec=self.init_argument_spec()
        )
        self.module_args = self._module.params
        self.result = dict(jcl=[], changed=False, failed=False, err="", executions=[])
        self.jcl_helper = JCLHelper()

    def main(self):
        self.validate_parameters()
        self._build_data_structure_of_arguments()
        self.jcl_helper.render_jcl()

        jcl = self.jcl_helper.jcl
        self._submit_jcl(jcl)
        self.result["jcl"] = jcl
        self._module.exit_json(**self.result)

    def _build_data_structure_of_arguments(self):
        self._remove_none_values_from_dict(self.module_args)
        self._populate_job_card_dict()
        self._populate_exec_dict()

    def _populate_job_card_dict(self):
        job_name = self.module_args[APPLID]
        self.jcl_helper.job_data[JOB_CARD] = self.module_args.get(JOB_PARAMETERS, {JOB_NAME: job_name})
        if self.jcl_helper.job_data[JOB_CARD].get(JOB_NAME) is None:
            self.jcl_helper.job_data[JOB_CARD].update({JOB_NAME: job_name})

    def _populate_exec_dict(self):
        exec_data = {NAME: "",
                     PGM: DFHSIP,
                     DDS: self._populate_dds()}
        exec_data = self._add_exec_parameters(exec_data)

    def _populate_dds(self):
        self._copy_libraries_to_steplib_and_dfhrpl()
        self._add_block_of_libraries(STEPLIB)
        self._add_block_of_libraries(DFHRPL)
        self._add_per_region_data_sets()
        self._add_output_data_sets()
        self._add_sit_parameters()
        return self.dds

    def _copy_libraries_to_steplib_and_dfhrpl(self):
        steplib_args = {"cics_data_sets": ["sdfhauth", "sdfhlic"], "le_data_sets": ["sceerun", "sceerun2"]}
        dfhrpl_args = {"cics_data_sets": ["sdfhload"], "le_data_sets": ["sceecics", "sceerun", "sceerun2"]}
        self._copy_libraries(steplib_args, "steplib")
        self._copy_libraries(dfhrpl_args, "dfhrpl")

    def _copy_libraries(self, libraries_to_copy, target_arg):
        for lib_type, list_of_libs in libraries_to_copy.items():
            for lib in list_of_libs:
                if self.module_args.get(lib_type) and self.module_args[lib_type].get(lib):
                    self.module_args[target_arg][TOP_LIBRARIES].append(self.module_args[lib_type][lib].upper())

    def _add_exec_parameters(self, exec_data):
        if self._check_parameter_is_provided(SIT_PARAMETERS):
            # We will need PARM=SI if they've provided SIT parameters, we add this for them.
            exec_data.update({"PARM": "SI"})
        self.jcl_helper.job_data[EXECS].append(exec_data)
        return exec_data

    def _add_block_of_libraries(self, lib_name):
        if self._check_parameter_is_provided(lib_name):
            libraries = self._concat_libraries(lib_name)
            list_of_lib_dicts = self._add_libraries(libraries)
            if list_of_lib_dicts:
                self.dds.append({lib_name: list_of_lib_dicts})

    def _get_delimiter(self, content):
        # If they've used the instream delimiter in their instream data
        if AnsibleStartCICSModule._check_for_existing_dlm_within_content(content):
            dlm = self._find_unused_character(content)
            if dlm is None:
                self._fail(
                    "Cannot replace instream delimiter as all character instances have been used.")
            # Return a new delimiter so that they dont accidentally terminate their instream early.
            return dlm
        #  They've not used a dlm in their instream data so we don't have to replace it.
        return None

    @staticmethod
    def _find_unused_character(content):
        all_chars = '@$#' + string.ascii_uppercase + string.digits
        char_combinations_present = set()
        preferred_dlms = ['@', '$', '#']

        for line in content:
            first_two_chars_in_line = line[:2]
            char_combinations_present.add(first_two_chars_in_line)
        combination = AnsibleStartCICSModule._get_unused_combination_of_chars(
            char_combinations_present, preferred_dlms)
        if combination:
            return combination
        else:
            return AnsibleStartCICSModule._get_unused_combination_of_chars(char_combinations_present,
                                                                           all_chars)

    @staticmethod
    def _get_unused_combination_of_chars(combinations, all_chars):
        for char1 in all_chars:
            for char2 in all_chars:
                combination = char1 + char2
                if combination not in combinations:
                    return combination
        return None

    @staticmethod
    def _check_for_existing_dlm_within_content(content):
        for current_item in content:
            if END_INSTREAM in current_item:
                return True
        return False

    def _validate_content(self, content):
        for current_item in content:
            if DD_INSTREAM in current_item.upper():
                self._fail("Invalid content for an in-stream: {0}".format(DD_INSTREAM))
            if DD_DATA in current_item.upper():
                self._fail("Invalid content for an in-stream: {0}".format(DD_DATA))

    def _add_output_data_sets(self):
        output_data_sets = [CEEMSG, CEEOUT, MSGUSR, SYSPRINT, SYSUDUMP, SYSABEND, SYSOUT,
                            DFHCXRF, LOGUSR]

        user_provided_data_sets = self.module_args.get(OUTPUT_DATA_SETS, {})
        default_class = user_provided_data_sets.pop(DEFAULT_SYSOUT_CLASS, '*')

        for data_set in output_data_sets:
            self._set_sysout_class_for_data_set(
                data_set, default_class, user_provided_data_sets)
            self._remove_omitted_data_set(data_set, user_provided_data_sets)

        for data_set_name, parameters in user_provided_data_sets.items():
            self.dds.append({data_set_name: [parameters]})

    @staticmethod
    def _remove_omitted_data_set(data_set, user_provided_data_sets):
        if user_provided_data_sets.get(data_set) and user_provided_data_sets[data_set].get(
                OMIT) is True:
            user_provided_data_sets.pop(data_set)

    @staticmethod
    def _set_sysout_class_for_data_set(data_set, default_class, user_provided_data_sets):
        if user_provided_data_sets.get(data_set):
            if user_provided_data_sets.get(data_set).get(SYSOUT) is None:
                user_provided_data_sets[data_set][SYSOUT] = default_class.upper()
        else:
            user_provided_data_sets[data_set] = {SYSOUT: default_class.upper()}

    def _add_per_region_data_sets(self):
        data_set_dict = self.module_args.get(REGION_DATA_SETS)

        for dd_name, parameters in data_set_dict.items():
            parameters[DISP] = SHR
            self.dds.append({dd_name: [parameters]})

    def _add_libraries(self, data_sets):
        dsn_dict = []
        for data_set in data_sets:
            if data_set:
                dsn_dict.append({DSN: data_set, DISP: SHR})
        return dsn_dict

    def _add_sit_parameters(self):
        if self._check_parameter_is_provided(SIT_PARAMETERS):
            self.module_args[SIT_PARAMETERS][APPLID] = self.module_args[APPLID]
            sit_parms = self._manage_dictionaries_in_sit_parameters(
                self.module_args[SIT_PARAMETERS])
            list_of_strings = JCLHelper._concatenate_key_value_pairs_into_list(
                sit_parms)
            self._validate_content(list_of_strings)
            wrapped_content = AnsibleStartCICSModule._wrap_sit_parameters(list_of_strings)
            dlm = self._get_delimiter(wrapped_content)
            if dlm:
                self.dds.append(
                    {SYSIN: {DLM: dlm, CONTENT: wrapped_content}})
            else:
                self.dds.append({SYSIN: {CONTENT: wrapped_content}})

    def _manage_dictionaries_in_sit_parameters(self, dictionary):
        key_values_to_add = {}
        keys_to_remove = []
        for k, v in dictionary.items():
            if isinstance(v, dict):
                new_key = k.rstrip('x')
                for inner_k, inner_v in v.items():
                    self._validate_dictionary_value_within_sit_parms(
                        k, inner_k)
                    key_values_to_add[new_key + inner_k] = inner_v
                keys_to_remove.append(k)
        for k, v in key_values_to_add.items():
            dictionary[k] = v
        for key in keys_to_remove:
            dictionary.pop(key)
        return dictionary

    def _submit_jcl(self, jcl):
        if self.module_args.get("submit_jcl"):
            # Submit the JCL using ZOAU jsub
            try:
                jcl = "\n".join(jcl)
                rc, stdout, stderr = self._module.run_command(["echo", jcl])
                rc, stdout, stderr = self._module.run_command(["jsub"], data=stdout)
                self.result["changed"] = True
                self.result["executions"].append({"name": "z/OS Job Submit - Submit CICS Startup JCL",
                                                  "stdout": stdout, "stderr": stderr, "rc": rc})
                self.result["job_id"] = stdout.strip('\n')
            except Exception:
                self._fail("Failed to submit jcl as job with return code: {0}".format(rc))

    def _validate_dictionary_value_within_sit_parms(self, sit_param_key_with_trailing_x, chars_to_replace_trailing_x):
        number_of_x_chars = len(sit_param_key_with_trailing_x) - len(sit_param_key_with_trailing_x.rstrip('x'))

        if sit_param_key_with_trailing_x.upper() == "SKRXXXX":
            if len(chars_to_replace_trailing_x) != 3 and len(chars_to_replace_trailing_x) != 4:
                self._fail("Invalid key: {0}. Key must be a length of 3 or 4.".format(chars_to_replace_trailing_x))
        elif len(chars_to_replace_trailing_x) != number_of_x_chars:
            self._fail("Invalid key: {0}. Key must be the same length as the x's within {1}.".format(
                chars_to_replace_trailing_x, sit_param_key_with_trailing_x))

    def _remove_none_values_from_dict(self, dictionary):
        for k, v in list(dictionary.items()):
            if v is None:
                del dictionary[k]
            elif isinstance(v, dict):
                self._remove_none_values_from_dict(v)

    def _check_parameter_is_provided(self, parameter_name):
        if self.module_args.get(parameter_name) is None or self.module_args.get(parameter_name) is {}:
            return False
        return True

    def _fail(self, msg):
        self.result["failed"] = True
        self._module.fail_json(msg=msg, **self.result)

    def _concat_libraries(self, lib_name):
        data_sets = []
        library_type = [TOP_LIBRARIES, LIBRARIES]
        for library_name in library_type:
            if self.module_args.get(lib_name).get(library_name):
                data_sets.extend(self.module_args[lib_name][library_name])
        return data_sets

    def validate_parameters(self):
        try:
            BetterArgParser(self.get_arg_defs()).parse_args(self.module_args)
        except ValueError as e:
            self._fail(e.args[0])

    def get_arg_defs(self):
        defs = self.init_argument_spec()
        # Setting arg_type to be the correct type required for the validation within BetterArgParser
        self.batch_update_arg_defs_for_ds(defs, REGION_DATA_SETS, region_data_sets_list, True)
        self.batch_update_arg_defs_for_ds(defs, CICS_DATA_SETS, ["sdfhauth", "sdfhlic", "sdfhload"])
        self.batch_update_arg_defs_for_ds(defs, LE_DATA_SETS, ["sceecics", "sceerun", "sceerun2"])
        defs[STEPLIB]["options"][TOP_LIBRARIES].update({"elements": "data_set_base"})
        defs[STEPLIB]["options"][LIBRARIES].update({"elements": "data_set_base"})
        defs[DFHRPL]["options"][TOP_LIBRARIES].update({"elements": "data_set_base"})
        defs[DFHRPL]["options"][LIBRARIES].update({"elements": "data_set_base"})

        # Qualifier is the arg type for things like Applid's, job names which follow the 8 character rule.
        self.update_arg_def(defs[APPLID], "qualifier")
        if defs.get("job_parameters"):
            if defs["job_parameters"]["options"].get(JOB_NAME):
                # If they've provided a job_name we need to validate this too
                self.update_arg_def(defs["job_parameters"]["options"][JOB_NAME], "qualifier")
        # Popping sit parameters as these dont need validation and it will complain at arbitary keys.
        defs.pop(SIT_PARAMETERS)
        return defs

    def batch_update_arg_defs_for_ds(self, defs, key, list_of_args_to_update, dsn=False):
        for arg in list_of_args_to_update:
            if dsn:
                self.update_arg_def(defs[key]["options"][arg]["options"][DSN])
            else:
                self.update_arg_def(defs[key]["options"][arg])

    def update_arg_def(self, dict_to_update, arg_type="data_set_base"):
        dict_to_update.update({"arg_type": arg_type})
        dict_to_update.pop("type")

    @staticmethod
    def _wrap_sit_parameters(content):
        wrapped_content = []
        # These sit parameters are the only ones which can be wrapped.
        wrappable_sit_parameters = ["CRLPROFILE", "USSHOME", "GMTEXT", "USSCONFIG", "HTTPSERVERHDR",
                                    "HTTPUSRAGENTHDR", "INFOCENTER", "JVMPROFILEDIR"]
        for line in content:
            wrapped = False
            for sit_parm in wrappable_sit_parameters:
                extracted_sit_parameter_from_line = AnsibleStartCICSModule._find_sit_parm_key(line)
                if extracted_sit_parameter_from_line == sit_parm:
                    if len(line) > 80:
                        # If the lines too long, break after character 80 and put 80 character chunks into the list.
                        wrapped_content.extend([line[i:i + 80] for i in range(0, len(line), 80)])
                        wrapped = True
                        break
            if not wrapped:
                wrapped_content.append(line)
        return wrapped_content

    @staticmethod
    def _find_sit_parm_key(input_string):
        index = input_string.find('=')
        if index != -1:
            return input_string[:index].strip()
        else:
            return None

    @staticmethod
    def init_argument_spec():  # type: () -> dict
        return {
            JOB_PARAMETERS: {
                'type': 'dict',
                'required': False,
                'options': {

                    'accounting_information': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'pano': {
                                'type': 'str',
                                'required': False,
                            },
                            'room': {
                                'type': 'str',
                                'required': False,
                            },
                            'time': {
                                'type': 'int',
                                'required': False,
                            },
                            'lines': {
                                'type': 'int',
                                'required': False,
                            },
                            'cards': {
                                'type': 'int',
                                'required': False,
                            },
                            'forms': {
                                'type': 'str',
                                'required': False,
                            },
                            'copies': {
                                'type': 'int',
                                'required': False,
                            },
                            'log': {
                                'type': 'str',
                                'required': False,
                            },
                            'linect': {
                                'type': 'int',
                                'required': False,
                            }
                        }
                    },
                    'class': {
                        'type': 'str',
                        'required': False
                    },
                    'job_name': {
                        'type': 'str',
                        'required': False
                    },
                    'memlimit': {
                        'type': 'str',
                        'required': False
                    },
                    'msgclass': {
                        'type': 'str',
                        'required': False
                    },
                    'msglevel': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'statements': {
                                'type': 'int',
                                'required': False,
                                'choices': [0, 1, 2]
                            },
                            'messages': {
                                'type': 'int',
                                'required': False,
                                'choices': [0, 1]
                            }
                        }
                    },
                    'programmer_name': {
                        'type': 'str',
                        'required': False,
                    },
                    'region': {
                        'type': 'str',
                        'required': False
                    },
                    'user': {
                        'type': 'str',
                        'required': False
                    },
                }
            },
            APPLID: {
                'type': 'str',
                'required': True,
            },
            'submit_jcl': {
                'type': 'bool',
                'required': False,
                'default': False,
            },
            CICS_DATA_SETS: {
                'type': 'dict',
                'required': True,
                'options': {
                    'template': {
                        'type': 'str',
                        'required': False
                    },
                    'sdfhload': {
                        'type': 'str',
                        'required': False
                    },
                    'sdfhauth': {
                        'type': 'str',
                        'required': False
                    },
                    'sdfhlic': {
                        'type': 'str',
                        'required': False
                    }
                }
            },
            LE_DATA_SETS: {
                'type': 'dict',
                'required': True,
                'options': {
                    TEMPLATE: {
                        'type': 'str',
                        'required': False
                    },
                    'sceecics': {
                        'type': 'str',
                        'required': False
                    },
                    'sceerun': {
                        'type': 'str',
                        'required': False
                    },
                    'sceerun2': {
                        'type': 'str',
                        'required': False
                    }
                }
            },
            STEPLIB: {
                'type': 'dict',
                'required': False,
                'options': {
                    TOP_LIBRARIES: {
                        'type': 'list',
                        'required': False,
                        'elements': 'str'
                    },
                    LIBRARIES: {
                        'type': 'list',
                        'required': False,
                        'elements': 'str'
                    },
                }
            },
            DFHRPL: {
                'type': 'dict',
                'required': False,
                'options': {
                    TOP_LIBRARIES: {
                        'type': 'list',
                        'required': False,
                        'elements': 'str'
                    },
                    LIBRARIES: {
                        'type': 'list',
                        'required': False,
                        'elements': 'str'
                    }
                }
            },
            REGION_DATA_SETS: {
                'type': 'dict',
                'required': True,
                'options': {
                    TEMPLATE: {
                        'type': 'str',
                        'required': False
                    },
                    'dfhcsd': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            DSN: {
                                'type': 'str',
                                'required': False
                            },
                        }
                    },
                    'dfhlrq': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            DSN: {
                                'type': 'str',
                                'required': False
                            },
                        }
                    },
                    'dfhdmpa': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            DSN: {
                                'type': 'str',
                                'required': False
                            },
                        }
                    },
                    'dfhdmpb': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            DSN: {
                                'type': 'str',
                                'required': False
                            },
                        }
                    },
                    'dfhauxt': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            DSN: {
                                'type': 'str',
                                'required': False
                            },
                        }
                    },
                    'dfhbuxt': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            DSN: {
                                'type': 'str',
                                'required': False
                            },
                        }
                    },
                    'dfhlcd': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            DSN: {
                                'type': 'str',
                                'required': False
                            },
                        }
                    },
                    'dfhgcd': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            DSN: {
                                'type': 'str',
                                'required': False
                            },
                        }
                    },
                    'dfhintra': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            DSN: {
                                'type': 'str',
                                'required': False
                            },
                        }
                    },
                    'dfhtemp': {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            DSN: {
                                'type': 'str',
                                'required': False
                            },
                        }
                    },
                }
            },
            OUTPUT_DATA_SETS: {
                'type': 'dict',
                'required': False,
                'options': {
                    DEFAULT_SYSOUT_CLASS: {
                        'type': 'str',
                        'required': False
                    },
                    CEEMSG: {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'sysout': {
                                'type': 'str',
                                'required': False
                            },
                            OMIT: {
                                'type': 'bool',
                                'required': False
                            },
                        }
                    },
                    CEEOUT: {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'sysout': {
                                'type': 'str',
                                'required': False
                            },
                            OMIT: {
                                'type': 'bool',
                                'required': False
                            },
                        }
                    },
                    MSGUSR: {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'sysout': {
                                'type': 'str',
                                'required': False
                            },
                            OMIT: {
                                'type': 'bool',
                                'required': False
                            },
                        }
                    },
                    SYSPRINT: {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'sysout': {
                                'type': 'str',
                                'required': False
                            },
                            OMIT: {
                                'type': 'bool',
                                'required': False
                            },
                        }
                    },
                    SYSUDUMP: {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'sysout': {
                                'type': 'str',
                                'required': False
                            },
                            OMIT: {
                                'type': 'bool',
                                'required': False
                            },
                        }
                    },
                    SYSABEND: {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'sysout': {
                                'type': 'str',
                                'required': False
                            },
                            OMIT: {
                                'type': 'bool',
                                'required': False
                            },
                        }
                    },
                    SYSOUT: {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'sysout': {
                                'type': 'str',
                                'required': False
                            },
                            OMIT: {
                                'type': 'bool',
                                'required': False
                            },
                        }
                    },
                    DFHCXRF: {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'sysout': {
                                'type': 'str',
                                'required': False
                            },
                            OMIT: {
                                'type': 'bool',
                                'required': False
                            },
                        }
                    },
                    LOGUSR: {
                        'type': 'dict',
                        'required': False,
                        'options': {
                            'sysout': {
                                'type': 'str',
                                'required': False
                            },
                            OMIT: {
                                'type': 'bool',
                                'required': False
                            }
                        }
                    }
                }
            },
            SIT_PARAMETERS: {
                'type': 'dict',
                'required': False,
                'options': {
                    'adi': {
                        'type': 'int',
                        'required': False,
                    },
                    'aibridge': {
                        'type': 'str',
                        'required': False,
                        'choices': ['AUTO', 'YES']
                    },
                    'aicons': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'AUTO', 'YES']
                    },
                    'aiexit': {
                        'type': 'str',
                        'required': False,
                    },
                    'aildelay': {
                        'type': 'int',
                        'required': False,
                    },
                    'aiqmax': {
                        'type': 'int',
                        'required': False,
                    },
                    'airdelay': {
                        'type': 'int',
                        'required': False,
                    },
                    'akpfreq': {
                        'type': 'int',
                        'required': False,
                    },
                    'autconn': {
                        'type': 'int',
                        'required': False,
                    },
                    'autodst': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'autoresettime': {
                        'type': 'str',
                        'required': False,
                        'choices': ['IMMEDIATE', 'NO', 'YES'],
                    },
                    'auxtr': {
                        'type': 'str',
                        'required': False,
                        'choices': ['OFF', 'ON'],
                    },
                    'auxtrsw': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'ALL', 'NEXT'],
                    },
                    'bms': {
                        'type': 'str',
                        'required': False,
                    },
                    'brmaxkeeptime': {
                        'type': 'int',
                        'required': False,
                    },
                    'cdsasze': {
                        'type': 'int',
                        'required': False,
                    },
                    'chkstrm': {
                        'type': 'str',
                        'required': False,
                        'choices': ['CURRENT', 'NONE'],
                    },
                    'chkstsk': {
                        'type': 'str',
                        'required': False,
                        'choices': ['CURRENT', 'NONE'],
                    },
                    'cicssvc': {
                        'type': 'int',
                        'required': False,
                    },
                    'cilock': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'clintcp': {
                        'type': 'str',
                        'required': False,
                    },
                    'clsdstp': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NOTIFY', 'NONOTIFY'],
                    },
                    'clt': {
                        'type': 'str',
                        'required': False,
                    },
                    'cmdprot': {
                        'type': 'str',
                        'required': False,
                        'choices': ['YES', 'NO'],
                    },
                    'cmdsec': {
                        'type': 'str',
                        'required': False,
                        'choices': ['ASIS', 'ALWAYS'],
                    },
                    'confdata': {
                        'type': 'str',
                        'required': False,
                        'choices': ['SHOW', 'HIDE'],
                    },
                    'conftxt': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'cpsmconn': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'CMAS', 'LMAS', 'WUI', 'SMSSJ'],
                    },
                    'crlprofile': {
                        'type': 'str',
                        'required': False,
                    },
                    'csdacc': {
                        'type': 'str',
                        'required': False,
                        'choices': ['READWRITE', 'READONLY'],
                    },
                    'csdbkup': {
                        'type': 'str',
                        'required': False,
                        'choices': ['STATIC', 'DYNAMIC'],
                    },
                    'csdbufnd': {
                        'type': 'int',
                        'required': False,
                    },
                    'csdbufni': {
                        'type': 'int',
                        'required': False,
                    },
                    'csddisp': {
                        'type': 'str',
                        'required': False,
                        'choices': ['OLD', 'SHR'],
                    },
                    'csddsn': {
                        'type': 'str',
                        'required': False,
                    },
                    'csdfrlog': {
                        'type': 'int',
                        'required': False,
                    },
                    'csdinteg': {
                        'type': 'str',
                        'required': False,
                        'choices': ['UNCOMMITTED', 'CONSISTENT', 'REPEATABLE'],
                    },
                    'csdjid': {
                        'type': 'str',
                        'required': False,
                    },
                    'csdlsrno': {
                        'type': 'str',
                        'required': False,
                    },
                    'csdrecov': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NONE', 'ALL', 'BACKOUTONLY'],
                    },
                    'csdrls': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'csdstrno': {
                        'type': 'int',
                        'required': False,
                    },
                    'cwakey': {
                        'type': 'str',
                        'required': False,
                        'choices': ['USER', 'CICS'],
                    },
                    'dae': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'datform': {
                        'type': 'str',
                        'required': False,
                        'choices': ['MMDDYY', 'DDMMYY', 'YYMMDD'],
                    },
                    'db2conn': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'dbctlcon': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'debugtool': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'dfltuser': {
                        'type': 'str',
                        'required': False,
                    },
                    'dip': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'dismacp': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'doccodepage': {
                        'type': 'str',
                        'required': False,
                    },
                    'dsalim': {
                        'type': 'str',
                        'required': False,
                    },
                    'dshipidl': {
                        'type': 'int',
                        'required': False,
                    },
                    'dshipint': {
                        'type': 'int',
                        'required': False,
                    },
                    'dsrtpgm': {
                        'type': 'str',
                        'required': False,
                    },
                    'dtrpgm': {
                        'type': 'str',
                        'required': False,
                    },
                    'dtrtran': {
                        'type': 'str',
                        'required': False,
                    },
                    'dump': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES', 'TABLEONLY'],
                    },
                    'dumpds': {
                        'type': 'str',
                        'required': False,
                        'choices': ['AUTO', 'A', 'B'],
                    },
                    'dumpsw': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'NEXT', 'ALL'],
                    },
                    'duretry': {
                        'type': 'int',
                        'required': False,
                    },
                    'ecdsasze': {
                        'type': 'str',
                        'required': False,
                    },
                    'edsalim': {
                        'type': 'str',
                        'required': False,
                    },
                    'eodi': {
                        'type': 'str',
                        'required': False,
                    },
                    'epcdsasze': {
                        'type': 'str',
                        'required': False,
                    },
                    'epudsasze': {
                        'type': 'str',
                        'required': False,
                    },
                    'erdsasze': {
                        'type': 'str',
                        'required': False,
                    },
                    'esdsasze': {
                        'type': 'str',
                        'required': False,
                    },
                    'esmexits': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NOINSTLN', 'INSTLN'],
                    },
                    'eudsasze': {
                        'type': 'str',
                        'required': False,
                    },
                    'fct': {
                        'type': 'str',
                        'required': False,
                    },
                    'fcqronly': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'fepi': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'fldsep': {
                        'type': 'str',
                        'required': False,
                    },
                    'fldstrt': {
                        'type': 'str',
                        'required': False,
                    },
                    'forceqr': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'fsstaff': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'ftimeout': {
                        'type': 'int',
                        'required': False,
                    },
                    'gmtext': {
                        'type': 'str',
                        'required': False,
                    },
                    'gmtran': {
                        'type': 'str',
                        'required': False,
                    },
                    'gntran': {
                        'type': 'str',
                        'required': False,
                    },
                    'grname': {
                        'type': 'str',
                        'required': False,
                    },
                    'grplist': {
                        'type': 'str',
                        'required': False,
                    },
                    'gtftr': {
                        'type': 'str',
                        'required': False,
                        'choices': ['OFF', 'ON'],
                    },
                    'hpo': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'httpserverhdr': {
                        'type': 'str',
                        'required': False,
                    },
                    'httpusragenthdr': {
                        'type': 'str',
                        'required': False,
                    },
                    'icp': {
                        'type': 'str',
                        'choices': ['COLD'],
                        'required': False,
                    },
                    'icv': {
                        'type': 'int',
                        'required': False,
                    },
                    'icvr': {
                        'type': 'int',
                        'required': False,
                    },
                    'icvtsd': {
                        'type': 'int',
                        'required': False,
                    },
                    'infocenter': {
                        'type': 'str',
                        'required': False,
                    },
                    'initparm': {
                        'type': 'str',
                        'required': False,
                    },
                    'inttr': {
                        'type': 'str',
                        'required': False,
                        'choices': ['ON', 'OFF'],
                    },
                    'ircstrt': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'isc': {
                        'type': 'str',
                        'required': False,
                        'choices': ['YES', 'NO'],
                    },
                    'jesdi': {
                        'type': 'int',
                        'required': False,
                    },
                    'jvmprofiledir': {
                        'type': 'str',
                        'required': False,
                    },
                    'kerberosuser': {
                        'type': 'str',
                        'required': False,
                    },
                    'keyring': {
                        'type': 'str',
                        'required': False,
                        'no_log': False,
                    },
                    'lgdfint': {
                        'type': 'int',
                        'required': False,
                    },
                    'lgnmsg': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'llacopy': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES', 'NEWCOPY'],
                    },
                    'localccsid': {
                        'type': 'int',
                        'required': False,
                    },
                    'lpa': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'maxopentcbs': {
                        'type': 'int',
                        'required': False,
                    },
                    'maxsockets': {
                        'type': 'int',
                        'required': False,
                    },
                    'maxssltcbs': {
                        'type': 'int',
                        'required': False,
                    },
                    'maxtlslevel': {
                        'type': 'str',
                        'required': False,
                        'choices': ['TLS11', 'TLS12', 'TLS13'],
                    },
                    'maxxptcbs': {
                        'type': 'int',
                        'required': False,
                    },
                    'mct': {
                        'type': 'str',
                        'required': False,
                    },
                    'mintlslevel': {
                        'type': 'str',
                        'required': False,
                        'choices': ['TLS11', 'TLS12', 'TLS13'],
                    },
                    'mn': {
                        'type': 'str',
                        'required': False,
                        'choices': ['OFF', 'ON'],
                    },
                    'mnconv': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'mnexc': {
                        'type': 'str',
                        'required': False,
                        'choices': ['OFF', 'ON'],
                    },
                    'mnfreq': {
                        'type': 'int',
                        'required': False,
                    },
                    'mnidn': {
                        'type': 'str',
                        'required': False,
                        'choices': ['OFF', 'ON'],
                    },
                    'mnper': {
                        'type': 'str',
                        'required': False,
                        'choices': ['OFF', 'ON'],
                    },
                    'mnres': {
                        'type': 'str',
                        'required': False,
                        'choices': ['OFF', 'ON'],
                    },
                    'mnsync': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'mntime': {
                        'type': 'str',
                        'required': False,
                        'choices': ['GMT', 'LOCAL'],
                    },
                    'mqconn': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'mrobtch': {
                        'type': 'int',
                        'required': False,
                    },
                    'mrofse': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'mrolrm': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'msgcase': {
                        'type': 'str',
                        'required': False,
                        'choices': ['MIXED', 'UPPER'],
                    },
                    'msglvl': {
                        'type': 'int',
                        'required': False,
                        'choices': [1, 0],
                    },
                    'mxt': {
                        'type': 'int',
                        'required': False,
                    },
                    'natlang': {
                        'type': 'str',
                        'required': False,
                        'choices': ['E', 'C', 'K'],
                    },
                    'ncpldft': {
                        'type': 'str',
                        'required': False,
                    },
                    'newsit': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'nistsp800131a': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NOCHECK', 'CHECK'],
                    },
                    'nonrlsrecov': {
                        'type': 'str',
                        'required': False,
                        'choices': ['VSAMCAT', 'FILEDEF'],
                    },
                    'nqrnl': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'offsite': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'opertim': {
                        'type': 'int',
                        'required': False,
                    },
                    'opndlim': {
                        'type': 'int',
                        'required': False,
                    },
                    'parmerr': {
                        'type': 'str',
                        'required': False,
                        'choices': ['INTERACT', 'IGNORE', 'ABEND'],
                    },
                    'pcdsasze': {
                        'type': 'int',
                        'required': False,
                    },
                    'pdi': {
                        'type': 'int',
                        'required': False,
                    },
                    'pdir': {
                        'type': 'str',
                        'required': False,
                    },
                    'pgaictlg': {
                        'type': 'str',
                        'required': False,
                        'choices': ['MODIFY', 'NONE', 'ALL'],
                    },
                    'pgaiexit': {
                        'type': 'str',
                        'required': False,
                    },
                    'pgaipgm': {
                        'type': 'str',
                        'required': False,
                        'choices': ['INACTIVE', 'ACTIVE'],
                    },
                    'pgchain': {
                        'type': 'str',
                        'required': False,
                    },
                    'pgcopy': {
                        'type': 'str',
                        'required': False,
                    },
                    'pgpurge': {
                        'type': 'str',
                        'required': False,
                    },
                    'pgret': {
                        'type': 'str',
                        'required': False,
                    },
                    'pltpi': {
                        'type': 'str',
                        'required': False,
                    },
                    'pltpisec': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NONE', 'CMDSEC', 'RESSEC', 'ALL'],
                    },
                    'pltpiusr': {
                        'type': 'str',
                        'required': False,
                    },
                    'pltsd': {
                        'type': 'str',
                        'required': False,
                    },
                    'prgdlay': {
                        'type': 'int',
                        'required': False,
                    },
                    'print': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES', 'PA1', 'PA2', 'PA3'],
                    },
                    'prtyage': {
                        'type': 'int',
                        'required': False,
                    },
                    'prvmod': {
                        'type': 'str',
                        'required': False,
                    },
                    'psbchk': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'psdint': {
                        'type': 'int',
                        'required': False,
                    },
                    'pstype': {
                        'type': 'str',
                        'required': False,
                        'choices': ['SNPS', 'MNPS', 'NOPS'],
                    },
                    'pudsasze': {
                        'type': 'str',
                        'required': False,
                    },
                    'pvdelay': {
                        'type': 'int',
                        'required': False,
                    },
                    'quiestim': {
                        'type': 'int',
                        'required': False,
                    },
                    'racfsync': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'ramax': {
                        'type': 'int',
                        'required': False,
                    },
                    'rapool': {
                        'type': 'str',
                        'required': False,
                    },
                    'rdsasze': {
                        'type': 'str',
                        'required': False,
                    },
                    'rentpgm': {
                        'type': 'str',
                        'required': False,
                        'choices': ['PROTECT', 'NOPROTECT'],
                    },
                    'resoverrides': {
                        'type': 'str',
                        'required': False,
                    },
                    'resp': {
                        'type': 'str',
                        'required': False,
                        'choices': ['FME', 'RRN'],
                    },
                    'ressec': {
                        'type': 'str',
                        'required': False,
                        'choices': ['ASIS', 'ALWAYS'],
                    },
                    'rls': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'rlstolsr': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'rmtran': {
                        'type': 'str',
                        'required': False,
                    },
                    'rrms': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'rst': {
                        'type': 'str',
                        'required': False,
                    },
                    'rstsignoff': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NOFORCE', 'FORCE'],
                    },
                    'rstsigntime': {
                        'type': 'int',
                        'required': False,
                    },
                    'ruwapool': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'sdsasze': {
                        'type': 'str',
                        'required': False,
                    },
                    'sdtmemlimit': {
                        'type': 'str',
                        'required': False,
                    },
                    'sdtran': {
                        'type': 'str',
                        'required': False,
                    },
                    'sec': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'secprfx': {
                        'type': 'str',
                        'required': False,
                    },
                    'sit': {
                        'type': 'str',
                        'required': False
                    },
                    'skrxxxx': {
                        'type': 'dict',
                        'required': False,
                    },
                    'snpreset': {
                        'type': 'str',
                        'required': False,
                        'choices': ['UNIQUE', 'SHARED'],
                    },
                    'snscope': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NONE', 'CICS', 'MVSIMAGE', 'SYSPLEX'],
                    },
                    'sotuning': {
                        'type': 'str',
                        'required': False,
                        'choices': ['YES', 520],
                    },
                    'spctr': {
                        'type': 'str',
                        'required': False,
                    },
                    'spctrxx': {
                        'type': 'dict',
                        'required': False,
                    },
                    'spool': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'srbsvc': {
                        'type': 'int',
                        'required': False,
                    },
                    'srt': {
                        'type': 'str',
                        'required': False,
                    },
                    'srvercp': {
                        'type': 'str',
                        'required': False,
                    },
                    'sslcache': {
                        'type': 'str',
                        'required': False,
                        'choices': ['CICS', 'SYSPLEX'],
                    },
                    'ssldelay': {
                        'type': 'int',
                        'required': False,
                    },
                    'start': {
                        'type': 'str',
                        'required': False,
                        'choices': ['INITIAL', 'AUTO', 'COLD', 'STANDBY', '(INITIAL, ALL)', '(AUTO, ALL)',
                                    '(COLD, ALL)', '(STANDBY, ALL)'],
                    },
                    'starter': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'stateod': {
                        'type': 'int',
                        'required': False,
                    },
                    'statint': {
                        'type': 'int',
                        'required': False,
                    },
                    'statrcd': {
                        'type': 'str',
                        'required': False,
                        'choices': ['OFF', 'ON'],
                    },
                    'stgprot': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'stgrcvy': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'stntr': {
                        'type': 'str',
                        'required': False,
                    },
                    'stntrxx': {
                        'type': 'dict',
                        'required': False,
                    },
                    'subtsks': {
                        'type': 'int',
                        'required': False,
                        'choices': [0, 1],
                    },
                    'suffix': {
                        'type': 'str',
                        'required': False,
                    },
                    'sydumax': {
                        'type': 'int',
                        'required': False,
                    },
                    'sysidnt': {
                        'type': 'str',
                        'required': False,
                    },
                    'systr': {
                        'type': 'str',
                        'required': False,
                        'choices': ['ON', 'OFF'],
                    },
                    'takeovr': {
                        'type': 'str',
                        'required': False,
                        'choices': ['MANUAL', 'AUTO', 'COMMAND'],
                    },
                    'tbexits': {
                        'type': 'str',
                        'required': False,
                    },
                    'tcp': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'tcpip': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'tcsactn': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NONE', 'UNBIND', 'FORCE'],
                    },
                    'tcswait': {
                        'type': 'str',
                        'required': False,
                    },
                    'tct': {
                        'type': 'str',
                        'required': False,
                    },
                    'tctuakey': {
                        'type': 'str',
                        'required': False,
                        'choices': ['USER', 'CICS'],
                    },
                    'tctualoc': {
                        'type': 'str',
                        'required': False,
                        'choices': ['BELOW', 'ANY'],
                    },
                    'td': {
                        'type': 'str',
                        'required': False,
                    },
                    'tdintra': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NOEMPTY', 'EMPTY'],
                    },
                    'traniso': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'trap': {
                        'type': 'str',
                        'required': False,
                        'choices': ['OFF', 'ON'],
                    },
                    'trdumax': {
                        'type': 'int',
                        'required': False,
                    },
                    'trtabsz': {
                        'type': 'int',
                        'required': False,
                    },
                    'trtransz': {
                        'type': 'int',
                        'required': False,
                    },
                    'trtranty': {
                        'type': 'str',
                        'required': False,
                        'choices': ['TRAN', 'ALL'],
                    },
                    'ts': {
                        'type': 'str',
                        'required': False,
                    },
                    'tsmainlimit': {
                        'type': 'str',
                        'required': False,
                    },
                    'tst': {
                        'type': 'str',
                        'required': False,
                    },
                    'udsasze': {
                        'type': 'str',
                        'required': False,
                    },
                    'uownetql': {
                        'type': 'str',
                        'required': False,
                    },
                    'usertr': {
                        'type': 'str',
                        'required': False,
                        'choices': ['ON', 'OFF'],
                    },
                    'usrdelay': {
                        'type': 'int',
                        'required': False,
                    },
                    'ussconfig': {
                        'type': 'str',
                        'required': False,
                    },
                    'usshome': {
                        'type': 'str',
                        'required': False,
                    },
                    'vtam': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'vtprefix': {
                        'type': 'str',
                        'required': False
                    },
                    'webdelay': {
                        'type': 'str',
                        'required': False,
                    },
                    'wlmhealth': {
                        'type': 'str',
                        'required': False,
                    },
                    'wrkarea': {
                        'type': 'int',
                        'required': False,
                    },
                    'xappc': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'xcfgroup': {
                        'type': 'str',
                        'required': False,
                    },
                    'xcmd': {
                        'type': 'str',
                        'required': False,
                    },
                    'xdb2': {
                        'type': 'str',
                        'required': False,
                    },
                    'xdct': {
                        'type': 'str',
                        'required': False,
                    },
                    'xfct': {
                        'type': 'str',
                        'required': False,
                    },
                    'xhfs': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'xjct': {
                        'type': 'str',
                        'required': False,
                    },
                    'xlt': {
                        'type': 'str',
                        'required': False,
                    },
                    'xpct': {
                        'type': 'str',
                        'required': False,
                    },
                    'xppt': {
                        'type': 'str',
                        'required': False,
                    },
                    'xpsb': {
                        'type': 'str',
                        'required': False,
                    },
                    'xptkt': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'xres': {
                        'type': 'str',
                        'required': False,
                    },
                    'xrf': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES'],
                    },
                    'xtran': {
                        'type': 'str',
                        'required': False,
                    },
                    'xtst': {
                        'type': 'str',
                        'required': False,
                    },
                    'xuser': {
                        'type': 'str',
                        'required': False,
                        'choices': ['NO', 'YES']
                    }
                }
            },
        }


def main():
    AnsibleStartCICSModule().main()


if __name__ == '__main__':
    main()

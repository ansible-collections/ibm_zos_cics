# (c) Copyright IBM Corp. 2020,2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import traceback
import re

ZOS_CORE_IMP_ERR = None

try:
    from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.mvs_cmd import idcams
except ImportError:
    ZOS_CORE_IMP_ERR = traceback.format_exc()


class CatalogSize():

    def __init__(self, unit, primary, secondary, record_count, record_size, control_interval_size):
        self.unit = unit
        self.primary = primary
        self.secondary = secondary
        self.record_count = record_count
        self.record_size = record_size
        self.control_interval_size = control_interval_size

    def to_dict(self):
        return {
            'unit': self.unit,
            'primary': self.primary,
            'secondary': self.secondary,
            'record_count': self.record_count,
            'record_size': self.record_size,
            'control_interval_size': self.control_interval_size,
        }


class GlobalCatalog():

    def __init__(
            self,
            size,
            name,
            sdfhload,
            state,
            autostart_override,
            nextstart,
            exists,
            vsam):
        self.size = size
        self.name = name
        self.sdfhload = sdfhload
        self.state = state
        self.autostart_override = autostart_override
        self.nextstart = nextstart
        self.exists = exists
        self.vsam = vsam

    def to_dict(self):
        return {
            'size': self.size.to_dict(),
            'name': self.name,
            'sdfhload': self.sdfhload,
            'state': self.state,
            'autostart_override': self.autostart_override,
            'nextstart': self.nextstart,
            'exists': self.exists,
            'vsam': self.vsam,
        }


class LocalCatalog():
    def __init__(
            self,
            size,
            name,
            sdfhload,
            state,
            exists,
            vsam):
        self.size = size
        self.name = name
        self.sdfhload = sdfhload
        self.state = state
        self.exists = exists
        self.vsam = vsam

    def to_dict(self):
        return {
            'size': self.size.to_dict(),
            'name': self.name,
            'sdfhload': self.sdfhload,
            'state': self.state,
            'exists': self.exists,
            'vsam': self.vsam,
        }


class CatalogResponse():

    def __init__(self, success, rc, msg):
        self.success = success
        self.rc = rc
        self.msg = msg

    def to_dict(self):
        return {
            'success': self.success,
            'rc': self.rc,
            'msg': self.msg,
        }


class Execution():
    def __init__(self, name, rc, stdout, stderr):
        self.name = name
        self.rc = rc
        self.stdout = stdout
        self.stderr = stderr

    def to_dict(self):
        return {
            "name": self.name,
            "rc": self.rc,
            "stdout": self.stdout,
            "stderr": self.stderr,
        }


def run_idcams(cmd, name):  # type: (str, str) -> Execution
    for x in range(10):
        rc, stdout, stderr = idcams(cmd=cmd, authorized=True)
        if rc == 0 and len(stderr) == 0:
            output = stdout.replace(" ", "").replace("\n", "")
            pattern = ".?IDCAMSSYSTEMSERVICESTIME:\\d{2}:\\d{2}:\\d{2}\\d{2}/\\d{2}/\\d{2}PAGE100IDC0002IIDCAMSPROCESSINGCOMPLETE.MAXIMUMCONDITIONCODEWAS0"
            if re.match(pattern, output) is None:
                break
        else:
            break
    return Execution(
        name="IDCAMS - {0}".format(name),
        rc=rc,
        stderr=stderr,
        stdout=stdout
    )


def update_catalog_props(catalog):  # type: (GlobalCatalog) -> GlobalCatalog

    execu = listcat(catalog=catalog)
    elements = ["{0}".format(element.replace(" ", "").upper())
                for element in execu.stdout.split("\n")]
    filtered = list(filter(lambda x: "TOTAL---" in x, elements))
    value = 0
    if len(filtered) != 0:
        value = filtered[0].replace("-", "").replace("TOTAL", "")

    if execu.rc == 4 or "ENTRY{0}NOTFOUND".format(
        catalog.name.upper()) in execu.stdout.upper().replace(
        " ",
            ""):
        catalog.exists = False
    elif execu.rc == 0:
        catalog.exists = True

        if "{0}".format(value) == "3":
            catalog.vsam = True
        else:
            catalog.vsam = False
    else:
        raise Exception("RC {0} from LISTCAT command".format(execu.rc))

    return catalog


def listcat(catalog):  # type: (GlobalCatalog) -> Execution
    listcat_output = run_idcams(
        cmd=" LISTCAT ENTRIES('{0}')".format(
            catalog.name), name="Retrieve dataset information (if exists)")
    return listcat_output


def get_catalog_size_unit(unit_symbol):  # type: (str) -> str
    return {
        'M': "MEGABYTES",
        'K': "KILOBYTES",
        'CYL': "CYLINDERS",
        'REC': "RECORDS",
        'TRK': "TRACKS"
    }.get(unit_symbol, "MEGABYTES")


def get_idcams_create_cmd(catalog):
    return '''
    DEFINE CLUSTER -
        (NAME({0}) -
        INDEXED                      -
        {1}({2} {3})             -
        SHR(2)              -
        FREESPACE(10 10)              -
        RECORDSIZE({4} {5})       -
        REUSE)              -
        DATA                           -
        (NAME({0}.DATA)  -
        CONTROLINTERVALSIZE({6})    -
        KEYS(52 0))  -
        INDEX                          -
        (NAME({0}.INDEX))
    '''.format(catalog.name,
               get_catalog_size_unit(catalog.size.unit),
               catalog.size.primary,
               catalog.size.secondary,
               catalog.size.record_count,
               catalog.size.record_size,
               catalog.size.control_interval_size)

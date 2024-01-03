# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

from __future__ import absolute_import, division, print_function

from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils.response import _execution
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.zos_mvs_raw import MVSCmdResponse
__metaclass__ = type
from ansible_collections.ibm.ibm_zos_cics.plugins.module_utils import icetool
import pytest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


icetool_stdout = """
    1ICE200I 0 IDENTIFIER FROM CALLING PROGRAM IS 0001
    ICE201I C RECORD TYPE IS F - DATA STARTS IN POSITION 1
    ICE751I 0 C5-I79518 C6-I90068 C7-I76949 C8-I75151 EE-I76949 E9-I77769 C9-NONE   E5-I92416 E7-I76949
    ICE143I 0 BLOCKSET     COPY  TECHNIQUE SELECTED
    ICE250I 0 VISIT http://www.ibm.com/storage/dfsort FOR DFSORT PAPERS, EXAMPLES AND MORE
    ICE000I 0 - CONTROL STATEMENTS FOR 5650-ZOS, Z/OS DFSORT V2R4  - 09:55 ON WED DEC 13, 2023 -
    0          DEBUG NOABEND,ESTAE
    OPTION MSGDDN=DFSMSG,LIST,MSGPRT=ALL,RESINV=0,SORTIN=DD1,COPY,NOCHECK
    MODS E35=(ICE35DU,12288)
    ICE193I 0 ICEAM2 INVOCATION ENVIRONMENT IN EFFECT - ICEAM2 ENVIRONMENT SELECTED
    ICE088I 0 ANSIBIT3.STEP1   .        , INPUT LRECL = 2041, BLKSIZE = 2048, TYPE = F
    ICE093I 0 MAIN STORAGE = (MAX,6291456,6291456)
    ICE156I 0 MAIN STORAGE ABOVE 16MB = (6250480,6234096)
    ICE127I 0 OPTIONS: OVFLO=RC0 ,PAD=RC0 ,TRUNC=RC0 ,SPANINC=RC16,VLSCMP=N,SZERO=Y,RESET=Y,VSAMEMT=Y,DYNSPC=256
    ICE128I 0 OPTIONS: SIZE=6291456,MAXLIM=1048576,MINLIM=450560,EQUALS=N,LIST=Y,ERET=RC16 ,MSGDDN=DFSMSG
    ICE129I 0 OPTIONS: VIO=N,RESDNT=ALL ,SMF=NO   ,WRKSEC=Y,OUTSEC=Y,VERIFY=N,CHALT=N,DYNALOC=N             ,ABCODE=MSG
    ICE130I 0 OPTIONS: RESALL=4096,RESINV=0,SVC=109 ,CHECK=N,WRKREL=Y,OUTREL=Y,CKPT=N,COBEXIT=COB2,ZSORT=N
    ICE131I 0 OPTIONS: TMAXLIM=6291456,ARESALL=0,ARESINV=0,OVERRGN=16384,CINV=Y,CFW=Y,DSA=0
    ICE132I 0 OPTIONS: VLSHRT=N,ZDPRINT=Y,IEXIT=N,TEXIT=N,LISTX=N,EFS=NONE    ,EXITCK=S,PARMDDN=DFSPARM ,FSZEST=N
    ICE133I 0 OPTIONS: HIPRMAX=OPTIMAL,DSPSIZE=MAX ,ODMAXBF=0,SOLRF=Y,VLLONG=N,VSAMIO=N,MOSIZE=MAX
    ICE235I 0 OPTIONS: NULLOUT=RC0
    ICE236I 0 OPTIONS: DYNAPCT=10 ,MOWRK=Y,TUNE=STOR,EXPMAX=MAX    ,EXPOLD=50%    ,EXPRES=10%
    ICE084I 1 VSAM ACCESS METHOD USED FOR DD1
    ICE751I 1 EF-I80637 F0-I90068 E8-I76949
    ICE091I 0 OUTPUT LRECL = 2041, TYPE = F
    ICE055I 0 INSERT 0, DELETE 52
    ICE054I 0 RECORDS - IN: 52, OUT: 0
    ICE267I 0 ZSORT ACCELERATOR PATH NOT USED    RSN=193
    ICE052I 0 END OF DFSORT
    1ICE600I 0 DFSORT ICETOOL UTILITY RUN STARTED

    ICE650I 0 VISIT http://www.ibm.com/storage/dfsort FOR ICETOOL PAPERS, EXAMPLES AND MORE

    ICE632I 0 SOURCE FOR ICETOOL STATEMENTS:  TOOLIN


    ICE630I 0 MODE IN EFFECT:  STOP

    COUNT FROM(DD1)
    ICE627I 0 DFSORT CALL 0001 FOR COPY FROM DD1      TO E35 EXIT COMPLETED
    ICE628I 0 RECORD COUNT:  000000000000052
    ICE602I 0 OPERATION RETURN CODE:  00


    ICE601I 0 DFSORT ICETOOL UTILITY RUN ENDED - RETURN CODE:  00
"""


def test__get_record_count_with_invalid_stdout():
    record_count = icetool._get_record_count("Some invalid STDOUT")
    expected = {
        "record_count": -1
    }
    assert record_count == expected


def test__get_record_count_with_record_count_string():
    record_count = icetool._get_record_count("RECORD COUNT:  000000000000001")
    expected = {
        "record_count": 1
    }
    assert record_count == expected


def test__get_record_count_with_icetool_stdout():
    record_count = icetool._get_record_count(icetool_stdout)
    expected = {
        "record_count": 52
    }
    assert record_count == expected


def test__run_icetool():
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=0, stdout=icetool_stdout, stderr="stderr"))
    executions, record_count = icetool._run_icetool("TEST.REGIONS.LCD")
    expected_record_count = {
        "record_count": 52
    }
    expected_executions = [
        _execution(name="ICETOOL - Get record count", rc=0, stdout=icetool_stdout, stderr="stderr"),
    ]
    assert record_count == expected_record_count
    assert executions == expected_executions


def test__run_icetool_rc_16_no_reason():
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=16, stdout="", stderr="stderr"))
    with pytest.raises(Exception) as e_info:
        icetool._run_icetool("TEST.REGIONS.LCD")

    assert (e_info.value).args[0] == "ICETOOL failed with RC 16"


def test__run_icetool_rc_nonzero():
    icetool._execute_icetool = MagicMock(return_value=MVSCmdResponse(rc=99, stdout="", stderr="stderr"))
    with pytest.raises(Exception) as e_info:
        icetool._run_icetool("TEST.REGIONS.LCD")

    assert (e_info.value).args[0] == "ICETOOL failed with RC 99"

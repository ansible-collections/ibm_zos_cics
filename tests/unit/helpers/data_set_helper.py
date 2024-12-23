# -*- coding: utf-8 -*-

# (c) Copyright IBM Corp. 2023,2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
import json
from textwrap import dedent
from ansible.module_utils.common.text.converters import to_bytes
from ansible.module_utils import basic

PYTHON_LANGUAGE_FEATURES_MESSAGE = "Requires python 3 language features"

default_data_set = {
    "exists": False,
    "name": None,
    "size": {
        "primary": 5,
        "secondary": 1,
        "unit": "M"
    },
    "state": "initial",
    "vsam": False
}


def set_module_args(args):
    basic._ANSIBLE_ARGS = to_bytes(json.dumps({'ANSIBLE_MODULE_ARGS': args}))


def LISTDS_run_name(run):
    return "IKJEFT01 - Get Data Set Status - Run {0}".format(run)


def LISTDS_data_set_doesnt_exist(data_set_name):
    return """
        1READY
            LISTDS '{0}'
           {0}
           DATA SET '{0}' NOT IN CATALOG
           READY
           END
    """.format(data_set_name)


def LISTDS_member_doesnt_exist(base_data_set_name, member_name):
    return """
      1READY
        LISTDS '{0}({1})'
       {0}
       --RECFM-LRECL-BLKSIZE-DSORG
         FB    80    27920   PO
       --VOLUMES--
         P2P117
       DIRECTORY INFORMATION NOT AVAILABLE+
       MEMBER NAME NOT FOUND
       READY
       END
    """.format(base_data_set_name, member_name)


def LISTDS_data_set(data_set_name, dsorg):
    return """
        1READY
          LISTDS '{0}'
         {0}
         --LRECL--DSORG-
           **     {1}
         --VOLUMES-BLKSIZE
                     **
         READY
         END
    """.format(data_set_name, dsorg)


def LISTSDS_member_data_set(base_data_set_name, member_name):
    return """
        1READY
            LISTDS '{0}({1})'
        {0}
        --RECFM-LRECL-BLKSIZE-DSORG
            FB    80    27920   PO
        --VOLUMES--
            P2P117
        --MEMBER---TTR----ALIAS-TTRN-CNT-DATA
            {1}      000110 NO    0    00
        READY
        END
    """.format(base_data_set_name, member_name)


def IDCAMS_run_cmd(data_set_name):
    return """
        DEFINE CLUSTER -
            (NAME({0}) -
            INDEXED                      -
            MEGABYTES(5 1)             -
            SHR(2)              -
            FREESPACE(10 10)              -
            RECORDSIZE(4089 32760)       -
            REUSE)              -
            DATA                           -
            (NAME({0}.DATA)  -
            CONTROLINTERVALSIZE(32768)    -
            KEYS(52 0))  -
            INDEX                          -
            (NAME({0}.INDEX))
    """.format(data_set_name)


def IDCAMS_create_run_name(run, data_set_name):
    return "IDCAMS - Creating {0} data set - Run {1}".format(data_set_name, run)


def IDCAMS_delete_run_name(run, data_set_name):
    return "IDCAMS - {0} - Run {1}".format(data_set_name, run)


def IDCAMS_create_stdout(data_set_name):
    return """
        1IDCAMS  SYSTEM SERVICES                                           TIME: 10:04:57
              06/29/23     PAGE      1
        0
            DEFINE CLUSTER -
                (NAME({0})
        0IDC0508I DATA ALLOCATION STATUS FOR VOLUME P2P0D5 IS 0
        0IDC0509I INDEX ALLOCATION STATUS FOR VOLUME P2P0D5 IS 0
        IDC0181I STORAGECLASS USED IS STANDARD
        IDC0181I MANAGEMENTCLASS USED IS STANDARD
        0IDC0001I FUNCTION COMPLETED, HIGHEST CONDITION CODE WAS 0
        0

        0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 0
    """.format(data_set_name)


def IDCAMS_create_already_exists_stdout(data_set_name):
    return """
        1IDCAMS  SYSTEM SERVICES                                           TIME: 10:04:51
              06/29/23     PAGE      1
        0
            DEFINE CLUSTER -
                (NAME({0})
        0IGD17101I DATA SET {0}
        NOT DEFINED BECAUSE DUPLICATE NAME EXISTS IN CATALOG
        RETURN CODE IS 8 REASON CODE IS 38 IGG0CLEH
        IGD17219I UNABLE TO CONTINUE DEFINE OF DATA SET
        {0}
        0IDC3013I DUPLICATE DATA SET NAME
        IDC3009I ** VSAM CATALOG RETURN CODE IS 8 - REASON CODE IS IGG0CLEH-38
        0IDC3003I FUNCTION TERMINATED. CONDITION CODE IS 12
        0

        0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 12
    """.format(data_set_name)


def IDCAMS_delete(data_set_name):
    return """
        1IDCAMS  SYSTEM SERVICES                                           TIME: 18:54:07        01/29/24     PAGE      1
        0
                 DELETE {0}
        0IDC0550I ENTRY (D) {0}.DATA DELETED
        0IDC0550I ENTRY (I) {0}.INDEX DELETED
        0IDC0550I ENTRY (C) {0} DELETED
        0IDC0001I FUNCTION COMPLETED, HIGHEST CONDITION CODE WAS 0
        0

        0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 0
    """.format(data_set_name)


def IDCAMS_delete_not_found(data_set_name):
    return """
        1IDCAMS  SYSTEM SERVICES                                           TIME: 10:15:24
                06/29/23     PAGE      1
        0
                DELETE {0}
        0IDC3012I ENTRY {0} NOT FOUND
        IDC3009I ** VSAM CATALOG RETURN CODE IS 8 - REASON CODE IS IGG0CLEG-42
        IDC0551I ** ENTRY {0} NOT DELETED
        0IDC0001I FUNCTION COMPLETED, HIGHEST CONDITION CODE WAS 8
        0

        0IDC0002I IDCAMS PROCESSING COMPLETE. MAXIMUM CONDITION CODE WAS 8
    """.format(data_set_name)


def IEFBR14_create_stderr(data_set_name, dd_name):
    return """
        BGYSC0307I Program: <IEFBR14> Arguments: <>
        BGYSC0308I DDNames:
        BGYSC0312I   {1}={0}
        BGYSC0303I Dataset allocation succeeded for {1}={0}
        BGYSC0328I OS Load program IEFBR14
        BGYSC0320I Addressing mode: AMODE24
        BGYSC0327I Attach Exit code: 0 from IEFBR14
        BGYSC0338I Dataset free succeeded for {1}={0}
    """.format(data_set_name, dd_name)


def IEFBR14_get_run_name(run):
    return "IEFBR14 - DFHIEFT - Run {0}".format(run)


def ICETOOL_name(count):
    return "ICETOOL - Get record count - Run {0}".format(count)


def ICETOOL_stdout(count):
    return """
        1ICE200I 0 IDENTIFIER FROM CALLING PROGRAM IS 0001
         ICE201I C RECORD TYPE IS F - DATA STARTS IN POSITION 1
         ICE751I 0 C5-I79518 C6-I90068 C7-I76949 C8-I75151 EE-I76949 E9-I77769 C9-NONE   E5-I92416 E7-I76949
         ICE143I 0 BLOCKSET     COPY  TECHNIQUE SELECTED
         ICE250I 0 VISIT http://www.ibm.com/storage/dfsort FOR DFSORT PAPERS, EXAMPLES AND MORE
         ICE000I 0 - CONTROL STATEMENTS FOR 5650-ZOS, Z/OS DFSORT V2R4  - 18:44 ON MON JAN 29, 2024 -
         0          DEBUG NOABEND,ESTAE
                   OPTION MSGDDN=DFSMSG,LIST,MSGPRT=ALL,RESINV=0,SORTIN=DD1,COPY,NOCHECK
                   MODS E35=(ICE35DU,12288)
         ICE193I 0 ICEAM2 INVOCATION ENVIRONMENT IN EFFECT - ICEAM2 ENVIRONMENT SELECTED
         ICE088I 0 HUGHEA8 .STEP1   .        , INPUT LRECL = 2041, BLKSIZE = 2048, TYPE = F
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
         ICE628I 0 RECORD COUNT:  0000000000000{0}
         ICE602I 0 OPERATION RETURN CODE:  00


         ICE601I 0 DFSORT ICETOOL UTILITY RUN ENDED - RETURN CODE:  00"
    """.format(count)


def ICETOOL_stderr():
    return """
        BGYSC0307I Program: <ICETOOL> Arguments: <>
        BGYSC0308I DDNames:
        BGYSC0312I   TOOLIN=DATA.SET.PATH
        BGYSC0310I   SHOWDEF=*
        BGYSC0310I   DFSMSG=*
        BGYSC0310I   TOOLMSG=*
        BGYSC0312I   DD1=DATA.SET.PATH
        BGYSC0310I   SYSPRINT=*
        BGYSC0303I Dataset allocation succeeded for TOOLIN=DATA.SET.PATH
        BGYSC0304I Dynamic allocation succeeded for SHOWDEF (temporary dataset for console)
        BGYSC0304I Dynamic allocation succeeded for DFSMSG (temporary dataset for console)
        BGYSC0304I Dynamic allocation succeeded for TOOLMSG (temporary dataset for console)
        BGYSC0303I Dataset allocation succeeded for DD1=DATA.SET.PATH
        BGYSC0304I Dynamic allocation succeeded for SYSPRINT (temporary dataset for console)
        BGYSC0328I OS Load program ICETOOL
        BGYSC0320I Addressing mode: AMODE31
        BGYSC0327I Attach Exit code: 0 from ICETOOL
        BGYSC0338I Dataset free succeeded for TOOLIN=DATA.SET.PATH
        BGYSC0356I Console free succeeded for SHOWDEF
        BGYSC0356I Console free succeeded for DFSMSG
        BGYSC0356I Console free succeeded for TOOLMSG
        BGYSC0338I Dataset free succeeded for DD1=DATA.SET.PATH
        BGYSC0356I Console free succeeded for SYSPRINT
    """


def RMUTL_get_run_name(run):
    return "DFHRMUTL - Get current catalog - Run {0}".format(run)


def RMUTL_update_run_name(run):
    return "DFHRMUTL - Updating autostart override - Run {0}".format(run)


def RMUTL_stdout(auto_start, next_start):
    return """
    ===DFHRMUTL CICS RECOVERY MANAGER BATCH UTILITY===

    ---DFHRMUTL:   DFHGCD information
        No recovery manager record found. GCD assumed empty.

    ---DFHRMUTL:   DFHGCD updated information
        Recovery manager auto-start override   : {0}
        Recovery manager next start type       : {1}

    Note: a CICS system that was shutdown warm, and which
    has no indoubt, commit-failed or backout-failed Units
    Of Work keypointed at that time, can safely be restarted
    cold without loss of data integrity.
    """.format(auto_start, next_start)


def RMUTL_stderr(data_set_name):
    return """
        BGYSC0345I STEPLIB set to TEST.CICS.INSTALL.SDFHLOAD
        BGYSC0346I Nested invocation <'mvscmdhelper' '-v' '--pgm=DFHRMUTL' '--dfhgcd={0}' '--sysin=TMP.P3621188.T0403704.C0000000' '--sysprint=*'>
        BGYSC0307I Program: <DFHRMUTL> Arguments: <>
        BGYSC0308I DDNames:
        BGYSC0310I   SYSPRINT=*
        BGYSC0312I   SYSIN=TMP.P3621188.T0403704.C0000000
        BGYSC0312I   DFHGCD={0}
        BGYSC0304I Dynamic allocation succeeded for SYSPRINT (temporary dataset for console)
        BGYSC0303I Dataset allocation succeeded for SYSIN=TMP.P3621188.T0403704.C0000000
        BGYSC0303I Dataset allocation succeeded for DFHGCD={0}
        BGYSC0328I OS Load program DFHRMUTL
        BGYSC0320I Addressing mode: AMODE31
        BGYSC0327I Attach Exit code: 0 from DFHRMUTL
        BGYSC0356I Console free succeeded for SYSPRINT
        BGYSC0338I Dataset free succeeded for SYSIN=TMP.P3621188.T0403704.C0000000
        BGYSC0338I Dataset free succeeded for DFHGCD={0}
    """.format(data_set_name)


def CCUTL_name():
    return "DFHCCUTL - Initialise Local Catalog"


def CCUTL_stderr(data_set_name):
    return """
        BGYSC0345I STEPLIB set to TEST.CICS.INSTALL.SDFHLOAD
        BGYSC0346I Nested invocation <'mvscmdhelper' '-v' '--pgm=DFHCCUTL' '--sysprint=*' '--sysudump=*' '--dfhlcd={0},SHR'>
        BGYSC0307I Program: <DFHCCUTL> Arguments: <>
        BGYSC0308I DDNames:
        BGYSC0312I   DFHLCD={0}
        BGYSC0310I   SYSUDUMP=*
        BGYSC0310I   SYSPRINT=*
        BGYSC0303I Dataset allocation succeeded for DFHLCD={0}
        BGYSC0304I Dynamic allocation succeeded for SYSUDUMP (temporary dataset for console)
        BGYSC0304I Dynamic allocation succeeded for SYSPRINT (temporary dataset for console)
        BGYSC0328I OS Load program DFHCCUTL
        BGYSC0320I Addressing mode: AMODE24
        BGYSC0327I Attach Exit code: 0 from DFHCCUTL
        BGYSC0338I Dataset free succeeded for DFHLCD={0}
        BGYSC0356I Console free succeeded for SYSUDUMP
        BGYSC0356I Console free succeeded for SYSPRINT
    """.format(data_set_name)


def CSDUP_name():
    return "Run DFHCSDUP"


def CSDUP_initialize_stdout(data_set_name):
    return """
        ***************************************************************************
        **  CICS RDO OFF-LINE UTILITY PROGRAM DFHCSDUP RELEASE:0750 PTF:I0602193.**
        ***************************************************************************


        INITIALIZE

        DFH5120 I PRIMARY CSD OPENED;  DDNAME: DFHCSD   - DSNAME: {0}
        DFH5280 I PROCESSING DEFINITIONS FROM LIBRARY MEMBER DFHCURDI
        DFH5131 I LIST DFHLIST  CREATED.
        DFH5135 I GROUP DFHDCTG  ADDED TO LIST
    """.format(data_set_name)


def CSDUP_stderr(data_set_name):
    return """
        BGYSC0345I STEPLIB set to TEST.CICS.INSTALL.SDFHLOAD
        BGYSC0346I Nested invocation <'mvscmdhelper' '-v' '--pgm=DFHCSDUP' '--dfhcsd={0},SHR' '--sysprint=*' '--sysudump=*' '--sysin={0}'>
        BGYSC0307I Program: <DFHCSDUP> Arguments: <>
        BGYSC0308I DDNames:
        BGYSC0312I   SYSIN={0}
        BGYSC0310I   SYSUDUMP=*
        BGYSC0310I   SYSPRINT=*
        BGYSC0312I   DFHCSD={0}
        BGYSC0303I Dataset allocation succeeded for SYSIN={0}
        BGYSC0304I Dynamic allocation succeeded for SYSUDUMP (temporary dataset for console)
        BGYSC0304I Dynamic allocation succeeded for SYSPRINT (temporary dataset for console)
        BGYSC0303I Dataset allocation succeeded for DFHCSD={0}
        BGYSC0328I OS Load program DFHCSDUP
        BGYSC0320I Addressing mode: AMODE24
        BGYSC0327I Attach Exit code: 0 from DFHCSDUP
        BGYSC0338I Dataset free succeeded for SYSIN={0}
        BGYSC0356I Console free succeeded for SYSUDUMP
        BGYSC0356I Console free succeeded for SYSPRINT
        BGYSC0338I Dataset free succeeded for DFHCSD={0}
    """.format(data_set_name)


def CSDUP_add_group_stdout(data_set_name):
    return """
        ***************************************************************************
        **  CICS RDO OFF-LINE UTILITY PROGRAM DFHCSDUP RELEASE:0750 PTF:I1302193.**
        ***************************************************************************

        ADD GROUP(DFHTERMC) LIST(DFHLIST1)

        DFH5120 I PRIMARY CSD OPENED;  DDNAME: DFHCSD   - DSNAME: {0}
        DFH5131 I LIST DFHLIST1 CREATED.
        DFH5135 I GROUP DFHTERMC ADDED TO LIST DFHLIST1
        DFH5101 I ADD COMMAND EXECUTED SUCCESSFULLY.
        DFH5123 I PRIMARY CSD CLOSED;  DDNAME: DFHCSD   - DSNAME: {0}

        DFH5107 I COMMANDS EXECUTED SUCCESSFULLY: 1     COMMANDS GIVING WARNING(S): 0     COMMANDS IN ERROR: 0
        DFH5108 I COMMANDS NOT EXECUTED AFTER ERROR(S): 0
        DFH5109 I END OF DFHCSDUP UTILITY JOB. HIGHEST RETURN CODE WAS: 0
    """.format(data_set_name)


def read_data_set_content_run_name(data_set_name):
    return "Read data set {0}".format(data_set_name)


def get_sample_generated_JCL_args(data_set_name, state):
    return {
        "state": state,
        "applid": "APPLID",
        "region_data_sets": {
            'dfhauxt': {"dsn": "test.dfhauxt"},
            'dfhbuxt': {"dsn": "test.dfhbuxt"},
            'dfhcsd': {"dsn": "test.dfhcsd"},
            'dfhgcd': {"dsn": "test.dfhgcd"},
            'dfhintra': {"dsn": "test.dfhintra"},
            'dfhlcd': {"dsn": "test.dfhlcd"},
            'dfhlrq': {"dsn": "test.dfhlrq"},
            'dfhtemp': {"dsn": "test.dfhtemp"},
            'dfhdmpa': {"dsn": "test.dfhdmpa"},
            'dfhdmpb': {"dsn": "test.dfhdmpb"},
            "dfhstart": {"dsn": data_set_name}
        },
        "cics_data_sets": {
            "sdfhload": "test.sdfhload",
            "sdfhauth": "test.sdfhauth",
            "sdfhlic": "test.sdfhlic",
        },
        "le_data_sets": {
            "sceecics": "test.sceecics",
            "sceerun": "test.sceerun",
            "sceerun2": "test.sceerun2",
        },
        "cpsm_data_sets": {
            "seyuauth": "test.seyuauth",
            "seyuload": "test.seyuload",
        },
        "steplib": {
            "top_data_sets": ["some.top.lib"]
        },
        "dfhrpl": {
            "top_data_sets": ["another.top.lib"]
        },
        "job_parameters": {
            "region": "0M"
        },
        "sit_parameters": {
            "start": "AUTO",
            "tcpip": "NO"
        }
    }


def get_sample_generated_JCL():
    return dedent("""
        //APPLID   JOB REGION=0M
        //         EXEC PGM=DFHSIP,PARM=SI
        //STEPLIB  DD DSN=SOME.TOP.LIB,DISP=SHR
        //         DD DSN=TEST.SDFHAUTH,DISP=SHR
        //         DD DSN=TEST.SDFHLIC,DISP=SHR
        //         DD DSN=TEST.SEYUAUTH,DISP=SHR
        //         DD DSN=TEST.SCEERUN,DISP=SHR
        //         DD DSN=TEST.SCEERUN2,DISP=SHR
        //DFHRPL   DD DSN=ANOTHER.TOP.LIB,DISP=SHR
        //         DD DSN=TEST.SDFHLOAD,DISP=SHR
        //         DD DSN=TEST.SEYULOAD,DISP=SHR
        //         DD DSN=TEST.SCEECICS,DISP=SHR
        //         DD DSN=TEST.SCEERUN,DISP=SHR
        //         DD DSN=TEST.SCEERUN2,DISP=SHR
        //DFHAUXT  DD DSN=TEST.DFHAUXT,DISP=SHR
        //DFHBUXT  DD DSN=TEST.DFHBUXT,DISP=SHR
        //DFHCSD   DD DSN=TEST.DFHCSD,DISP=SHR
        //DFHGCD   DD DSN=TEST.DFHGCD,DISP=SHR
        //DFHINTRA DD DSN=TEST.DFHINTRA,DISP=SHR
        //DFHLCD   DD DSN=TEST.DFHLCD,DISP=SHR
        //DFHLRQ   DD DSN=TEST.DFHLRQ,DISP=SHR
        //DFHTEMP  DD DSN=TEST.DFHTEMP,DISP=SHR
        //DFHDMPA  DD DSN=TEST.DFHDMPA,DISP=SHR
        //DFHDMPB  DD DSN=TEST.DFHDMPB,DISP=SHR
        //CEEMSG   DD SYSOUT=*
        //CEEOUT   DD SYSOUT=*
        //MSGUSR   DD SYSOUT=*
        //SYSPRINT DD SYSOUT=*
        //SYSUDUMP DD SYSOUT=*
        //SYSABEND DD SYSOUT=*
        //SYSOUT   DD SYSOUT=*
        //DFHCXRF  DD SYSOUT=*
        //LOGUSR   DD SYSOUT=*
        //SYSIN    DD *
        START=AUTO
        TCPIP=NO
        APPLID=APPLID
        /*
        //""").lstrip()

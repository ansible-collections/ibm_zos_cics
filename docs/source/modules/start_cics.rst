.. _start_cics_module:


start_cics -- Start a CICS region
=================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Start a CICS® region by providing CICS system data sets and system initialization parameters for CICS startup using the \ :literal:`DFHSIP`\  program.






Parameters
----------

  job_parameters (False, dict, None)
    Specifies various parameters to be applied to the startup job.


    accounting_information (False, dict, None)
      Allows jobs to be grouped into a class.


      pano (False, str, None)
        Specifies the programmer's accounting number. Pano is 1 through 4 alphanumeric characters.


      room (False, str, None)
        Specifies the programmer's room number. Room is 1 through 4 alphanumeric characters.


      time (False, int, None)
        Specifies the estimated execution time in minutes. Time is 1 through 4 decimal numbers. For example, code 30 for 30 minutes. If you omit a time subparameter and a TIME parameter on the JES2 /\*JOBPARM statement, JES2 uses an installation default specified at initialization. If job execution exceeds the time, JES2 sends a message to the operator.


      lines (False, int, None)
        Specifies the estimated line count, in thousands of lines, from this job's sysout data sets. Lines is 1 through 4 decimal numbers. For example, code 5 for 5000 lines. If you omit lines, JES2 uses an installation default specified at initialization.


      cards (False, int, None)
        Specifies the estimated number of cards JES2 is to punch from this job's sysout data sets. Cards is 1 through 4 decimal numbers. If you omit cards, JES2 uses an installation default specified at initialization.


      forms (False, str, None)
        Specifies the forms that JES2 is to use for printing this job's sysout data sets. Forms is 1 through 4 alphanumeric characters. For example, code 5 for 5-part forms. If you omit forms, JES2 uses an installation default specified at initialization.


      copies (False, int, None)
        Specifies the number of times JES2 is to print and/or punch this job's sysout data sets. Copies is 1 through 3 decimal numbers not exceeding an installation-specified limit. The maximum is 255. For example, code 2 for two copies. If you omit copies, JES2 assumes one copy.


      log (False, str, None)
        Specifies whether or not JES2 is to print the job log. Code N to request no job log. If you code any other character or omit this subparameter, JES2 prints the job log. If your installation specified NOLOG for this job's class during JES2 initialization, JES2 will not print a job log.


      linect (False, int, None)
        Specifies the number of lines JES2 is to print per page for this job's sysout data sets. Linect is 1 through 3 decimal numbers. If you omit linect, JES2 uses an installation default specified at initialization. If you code a zero, JES2 does not eject to a new page when the number of lines exceeds the installation default.



    class (False, str, None)
      Allows jobs to be grouped into a class.


    job_name (False, str, None)
      The name of the CICS startup job. The default value is \ :literal:`APPLID`\ .


    memlimit (False, str, None)
      Use the MEMLIMIT parameter to specify the limit on the total size of usable 64-bit z/OS storage in a single address space.


    msglevel (False, dict, None)
      Use the MSGLEVEL parameter to control the listing of the JCL output for the job.


      statements (False, int, None)
        Indicates which job control statements the system is to print in the statement images portion of the JCL output.


      messages (False, int, None)
        Indicates which messages the system is to print in the system messages portion of the JCL output.



    msgclass (False, str, None)
      Use the MSGCLASS parameter to assign the job log to an output class. The job log is a record of job-related information for the programmer.


    programmer_name (False, str, None)
      Use the programmer's name parameter to identify the person or group responsible for a job.


    region (False, str, None)
      Use the REGION parameter to specify the amount of central or virtual storage that the job requires. The system applies the value that you code on REGION to each step of the job.


    user (False, str, None)
      Code the USER parameter to identify to the system the person submitting the job. The user ID is used by RACF®, the system resources manager (SRM), and other system components.



  applid (True, str, None)
    The name of your z/OS Communications Server application identifier for this CICS region.


  submit_jcl (False, bool, False)
    Specify whether or not you want the CICS startup job to be submitted.


  cics_data_sets (True, dict, None)
    The data set names of the \ :literal:`SDFHAUTH`\ , \ :literal:`SDFHLOAD`\  and \ :literal:`SDFHLIC`\  libraries, for example, \ :literal:`CICSTS61.CICS.SDFHAUTH`\  and \ :literal:`CICSTS61.CICS.SDFHLOAD`\ .


    template (False, str, None)
      The templated location of the libraries.


    sdfhauth (False, str, None)
      The location of the \ :literal:`SDFHAUTH`\  librarty to override the template.


    sdfhload (False, str, None)
      The location of the \ :literal:`SDFHLOAD`\  library to override the template.


    sdfhlic (False, str, None)
      The location of the \ :literal:`SDFHLIC`\  library to override the template.



  le_data_sets (True, dict, None)
    The data set names of the \ :literal:`SCEECICS`\ , \ :literal:`SCEERUN`\  and \ :literal:`SCEERUN2`\  libraries, for example, \ :literal:`SCEERUN`\ .


    template (False, str, None)
      The templated location of the Language Enviornment runtime libraries.


    sceecics (False, str, None)
      The location of the \ :literal:`SCEECICS`\  library to override the template.


    sceerun (False, str, None)
      The location of the \ :literal:`SCEERUN`\  library to override the template.


    sceerun2 (False, str, None)
      The location of the \ :literal:`SCEERUN2`\  library to override the template.



  steplib (False, dict, None)
    Any locations of additional \ :literal:`STEPLIB`\  libraries to add, that are not \ :literal:`SDFHAUTH`\ , \ :literal:`SDFHLIC`\ , \ :literal:`SCEERUN`\ , or \ :literal:`SCEERUN2`\ .


    top_libraries (False, list, None)
      The \ :literal:`STEPLIB`\  libraries to be appended to the very top of the statement.


    libraries (False, list, None)
      The \ :literal:`STEPLIB`\  libraries to be appended to the bottom of the library list.



  dfhrpl (False, dict, None)
    Any locations of additional DFHRPL libraries to add, that are not \ :literal:`SDFHLOAD`\ , \ :literal:`SCEECICS`\ , \ :literal:`SCEERUN`\ , or \ :literal:`SCEERUN2`\ .


    top_libraries (False, list, None)
      The DFHRPL libraries to be appended to the very top of the statement.


    libraries (False, list, None)
      The DFHRPL libraries to be appended to the bottom of the list.



  region_data_sets (True, dict, None)
    The location of the region data sets, e.g \ :literal:`REGIONS.ABCD01.DFHAUXT`\ , \ :literal:`REGIONS.ABCD01.DFHCSD`\  and \ :literal:`REGIONS.ABCD01.DFHGCD`\ .


    template (False, str, None)
      The base location of the region data sets to be created using a template, for example, \ :literal:`REGIONS.ABCD0001.\<\< data\_set\_name \>\>`\ . Not required if you provide the data set name (dsn) of all the data sets individually.


    dfhauxt (False, dict, None)
      Overrides the templated location for the auxiliary trace A data set.


      dsn (False, str, None)
        The name of the auxiliary trace A data set to override the template.



    dfhbuxt (False, dict, None)
      Overrides the templated location for the auxiliary trace B data set.


      dsn (False, str, None)
        The name of the auxiliary trace B data set to override the template.



    dfhcsd (False, dict, None)
      Overrides the templated location for the CSD.


      dsn (False, str, None)
        The name of the CSD to override the template.



    dfhdmpa (False, dict, None)
      Overrides the templated location for the dump A data set.


      dsn (False, str, None)
        The name of the dump A data set to override the template.



    dfhdmpb (False, dict, None)
      Overrides the templated location for the dump B data set.


      dsn (False, str, None)
        The name of the dump B data set to override the template.



    dfhlrq (False, dict, None)
      Overrides the templated location for the local request queue data set.


      dsn (False, str, None)
        The data set name of the local request queue to override the template.



    dfhgcd (False, dict, None)
      Overrides the templated location for the global catalog data set.


      dsn (False, str, None)
        The data set name of the global catalog to override the template.



    dfhlcd (False, dict, None)
      Overrides the templated location for the local catalog data set.


      dsn (False, str, None)
        The data set name of the local catalog to override the template.



    dfhintra (False, dict, None)
      Overrides the templated location for the intrapartition data set.


      dsn (False, str, None)
        The name of the intrapartition data set to override the template.



    dfhtemp (False, dict, None)
      Overrides the templated location for the temporary storage data set.


      dsn (False, str, None)
        The data set name of the temporary storage to override the template.




  output_data_sets (False, dict, None)
    The system output data sets such as \ :literal:`CEEMSG`\  and \ :literal:`SYSPRINT`\ , as well as the destination class of the output.


    default_sysout_class (False, str, None)
      The class to be applied as the default for all of the output data sets. If it isn't provided and if no overrides are specified for an individual output data set, \* will be applied.


    ceemsg (False, dict, None)
      Overrides the default class to use a custom class for the \ :literal:`CEEMSG`\  data set. Alternatively, omit the \ :literal:`CEEMSG`\  data set from being added to the job.


      sysout (False, str, None)
        Specify the output class to assign the \ :literal:`CEEMSG`\  data set to.


      omit (False, bool, None)
        Specifies whether \ :literal:`CEEMSG`\  should be excluded from being added to the list of sysout data sets.



    ceeout (False, dict, None)
      Overrides the default class to use a custom class for the \ :literal:`CEEOUT`\  data set. Alternatively, omit the \ :literal:`CEEOUT`\  data set from being added to the job.


      sysout (False, str, None)
        Specify the output class to assign the \ :literal:`CEEOUT`\  data set to.


      omit (False, bool, None)
        Specifies whether \ :literal:`CEEOUT`\  should be excluded from being added to the list of sysout data sets.



    msgusr (False, dict, None)
      Overrides the default class to use a custom class for the \ :literal:`MSGUSR`\  data set. Alternatively, omit the \ :literal:`MSGUSR`\  data set from being added to the job.


      sysout (False, str, None)
        Specify the output class to assign the \ :literal:`MSGUSR`\  data set to.


      omit (False, bool, None)
        Specifies whether \ :literal:`MSGUSR`\  should be excluded from being added to the list of sysout data sets.



    sysprint (False, dict, None)
      Overrides the default class to use a custom class for the \ :literal:`SYSPRINT`\  data set. Alternatively, omit the \ :literal:`SYSPRINT`\  data set from being added to the job.


      sysout (False, str, None)
        Specify the output class to assign the \ :literal:`SYSPRINT`\  data set to.


      omit (False, bool, None)
        Specifies whether \ :literal:`SYSPRINT`\  should be excluded from being added to the list of sysout data sets.



    sysudump (False, dict, None)
      Overrides the default class to use a custom class for the \ :literal:`SYSUDUMP`\  data set. Alternatively, omit the \ :literal:`SYSUDUMP`\  data set from being added to the job.


      sysout (False, str, None)
        Specify the output class to assign the \ :literal:`SYSUDUMP`\  data set to.


      omit (False, bool, None)
        Specifies whether \ :literal:`SYSUDUMP`\  should be excluded from being added to the list of sysout data sets.



    sysabend (False, dict, None)
      Overrides the default class to use a custom class for the \ :literal:`SYSABEND`\  data set. Alternatively, omit the \ :literal:`SYSABEND`\  data set from being added to the job.


      sysout (False, str, None)
        Specify the output class to assign the \ :literal:`SYSABEND`\  data set to.


      omit (False, bool, None)
        Specifies whether \ :literal:`SYSABEND`\  should be excluded from being added to the list of sysout data sets.



    sysout (False, dict, None)
      Overrides the default class to use a custom class for the \ :literal:`SYSOUT`\  data set. Alternatively, omit the \ :literal:`SYSOUT`\  data set from being added to the job.


      sysout (False, str, None)
        Specify the output class to assign the \ :literal:`SYSOUT`\  data set to.


      omit (False, bool, None)
        Specifies whether \ :literal:`SYSOUT`\  should be excluded from being added to the list of sysout data sets.



    dfhcxrf (False, dict, None)
      Overrides the default class to use a custom class for the \ :literal:`DFHCXRF`\  data set. Alternatively, omit the \ :literal:`DFHCXRF`\  data set from being added to the job.


      sysout (False, str, None)
        Specify the output class to assign the \ :literal:`DFHCXRF`\  data set to.


      omit (False, bool, None)
        Specifies whether \ :literal:`DFHCXRF`\  should be excluded from being added to the list of sysout data sets.



    logusr (False, dict, None)
      Overrides the default class to use a custom class for the \ :literal:`LOGUSR`\  data set. Alternatively, omit the \ :literal:`LOGUSR`\  data set from being added to the job.


      sysout (False, str, None)
        Specify the output class to assign the \ :literal:`LOGUSR`\  data set to.


      omit (False, bool, None)
        Specifies whether \ :literal:`LOGUSR`\  should be excluded from being added to the list of sysout data sets.




  sit_parameters (False, dict, None)
    Define the system initalization parameters for the CICS region.


    adi (False, int, None)
      The ADI parameter specifies the alternate delay interval in seconds for an alternate CICS® region when you are running CICS with XRF.


    aibridge (False, str, None)
      The AIBRIDGE parameter specifies whether the autoinstall user replaceable module (URM) is to be called when creating bridge facilities (virtual terminals) used by the 3270 bridge mechanism.

      Specify this parameter only in the bridge router region.


    aicons (False, str, None)
      The AICONS parameter specifies whether you want autoinstall support for consoles.


    aiexit (False, str, None)
      The AIEXIT parameter specifies the name of the autoinstall user-replaceable program that you want CICS® to use when autoinstalling local z/OS® Communications Server terminals, APPC connections, virtual terminals, and shipped terminals and connections.


    aildelay (False, int, None)
      The AILDELAY parameter specifies the delay period that elapses after all sessions between CICS® and an autoinstalled terminal, APPC device, or APPC system are ended, before the terminal or connection entry is deleted.


    aiqmax (False, int, None)
      The AIQMAX parameter specifies the maximum number of z/OS® Communications Server terminals and APPC connections that can be queued concurrently for autoinstall, the limit is the sum of installs and deletes.


    airdelay (False, int, None)
      The AIRDELAY parameter specifies the delay period that elapses after an emergency restart before autoinstalled terminal and APPC connection entries that are not in session are deleted.


    akpfreq (False, int, None)
      The AKPFREQ parameter specifies the number of write requests to the CICS® system log stream output buffer required before CICS writes an activity keypoint.


    autconn (False, int, None)
      The AUTCONN parameter specifies that the reconnection of terminals after an XRF takeover is to be delayed, to allow time for manual switching.


    autodst (False, str, None)
      The AUTODST parameter specifies whether CICS is to activate automatic dynamic storage tuning for application programs.


    autoresettime (False, str, None)
      The AUTORESETTIME parameter specifies the action CICS  takes for automatic time changes.


    auxtr (False, str, None)
      The AUXTR parameter specifies whether the auxiliary trace destination is to be activated at system initialization.


    auxtrsw (False, str, None)
      The AUXTRSW parameter specifies whether you want the auxiliary trace autoswitch facility.


    bms (False, str, None)
      The BMS system initialization parameter specifies which version of basic mapping support you require in CICS.


    brmaxkeeptime (False, int, None)
      The BRMAXKEEPTIME parameter specifies the maximum time (in seconds) that bridge facilities (virtual terminals used by the 3270 bridge) are kept if they are not used.


    cdsasze (False, int, None)
      The CDSASZE system initialization parameter specifies the size of the CDSA.


    chkstrm (False, str, None)
      The CHKSTRM parameter specifies that terminal storage-violation checking is to be activated or deactivated.


    chkstsk (False, str, None)
      The CHKSTSK parameter specifies that task storage-violation checking at startup is to be activated or deactivated.


    cicssvc (False, int, None)
      The CICSSVC parameter  specifies the number that you have assigned to the CICS type 3 SVC.


    cilock (False, str, None)
      The CILOCK parameter specifies whether or not the control interval lock of a non-RLS VSAM file is to be kept after a successful read-for-update request.


    clintcp (False, str, None)
      The CLINTCP parameter specifies the default client code page to be used by the DFHCNV data conversion table, but only if the CLINTCP parameter in the DFHCNV macro is set to SYSDEF.


    clsdstp (False, str, None)
      The CLSDSTP system initialization parameter specifies the notification required for an EXEC CICS ISSUE PASS command.


    clt (False, str, None)
      The CLT parameter specifies the suffix for the command list table (CLT), if this SIT is used by an alternate XRF system.


    cmdprot (False, str, None)
      The CMDPROT parameter specifies whether to allow or inhibit CICS validation of start addresses of storage referenced as output parameters on EXEC CICS commands.


    cmdsec (False, str, None)
      The CMDSEC parameter specifies whether or not you want CICS to honor the CMDSEC option specified on a transaction's resource definition.


    confdata (False, str, None)
      The CONFDATA parameter specifies whether CICS is to redact sensitive data that might otherwise appear in CICS trace entries or in dumps.


    conftxt (False, str, None)
      The CONFTXT system initialization parameter specifies whether CICS is to prevent z/OS Communications Server from tracing user data.


    cpsmconn (False, str, None)
      The CPSMCONN parameter specifies whether you want CICS to invoke the specified  component during initialization of the region.


    crlprofile (False, str, None)
      The CRLPROFILE parameter specifies the name of the profile that is used to authorize CICS to access the certification revocation lists (CRLs) that are stored in an LDAP server.


    csdacc (False, str, None)
      The CSDACC parameter specifies the type of access to the CSD to be permitted to this CICS region.


    csdbkup (False, str, None)
      The CSDBKUP parameter specifies whether or not the CSD is eligible for BWO.


    csdbufnd (False, int, None)
      The CSDBUFND parameter specifies the number of buffers to be used for CSD data.


    csdbufni (False, int, None)
      The CSDBUFNI parameter specifies the number of buffers to be used for the CSD index.


    csddisp (False, str, None)
      The CSDDISP parameter specifies the disposition of the data set to be allocated to the CSD.


    csddsn (False, str, None)
      The CSDDSN parameter specifies the 1-44 character JCL data set name (DSNAME) to be used for the CSD.


    csdfrlog (False, int, None)
      The CSDFRLOG parameter specifies a number that corresponds to the journal name that CICS uses to identify the forward recovery log stream for the CSD.


    csdinteg (False, str, None)
      The CSDINTEG parameter specifies the level of read integrity for the CSD if it is accessed in RLS mode.


    csdjid (False, str, None)
      The CSDJID parameter specifies the journal identifier of the journal that you want CICS to use for automatic journaling of file requests against the CSD.


    csdlsrno (False, str, None)
      The CSDLSRNO system initialization parameter specifies whether the CSD is to be associated with a local shared resource (LSR) pool.


    csdrecov (False, str, None)
      The CSDRECOVsystem initialization parameter specifies whether the CSD is a recoverable file.


    csdrls (False, str, None)
      The CSDRLS system initialization parameter specifies whether CICS is to access the CSD in RLS mode.


    csdstrno (False, int, None)
      The CSDSTRNO system initialization parameter specifies the number of concurrent requests that can be processed against the CSD.


    cwakey (False, str, None)
      The CWAKEY system initialization parameter specifies the storage key for the common work area (CWA) if you are operating CICS with storage protection (STGPROT=YES).


    dae (False, str, None)
      The DAE system initialization parameter specifies the default DAE action when new system dump table entries are created.


    datform (False, str, None)
      The DATFORM system initialization parameter specifies the external date display standard that you want to use for CICS date displays.


    db2conn (False, str, None)
      The DB2CONN system initialization parameter specifies whether you want CICS to start the  connection automatically during initialization.


    dbctlcon (False, str, None)
      The DBCTLCON system initialization parameter specifies whether you want CICS to start the DBCTL connection automatically during initialization.


    debugtool (False, str, None)
      The DEBUGTOOL system initialization parameter specifies whether you want to use debugging profiles to select the programs that will run under the control of a debugging tool.


    dfltuser (False, str, None)
      The DFLTUSER system initialization parameter specifies the RACF userid of the default user; that is, the user whose security attributes are used to protect CICS resources in the absence of other, more specific, user identification.


    dip (False, str, None)
      The DIP system initialization parameter specifies whether the batch data interchange program, DFHDIP, is to be included.


    dismacp (False, str, None)
      The DISMACP system initialization parameter specifies whether CICS is to disable any transaction that terminates abnormally with an ASRD or ASRE abend.


    doccodepage (False, str, None)
      The DOCCODEPAGE system initialization parameter specifies the default host code page to be used by the document domain.


    dsalim (False, str, None)
      The DSALIM system initialization parameter specifies the upper limit of the total amount of storage within which CICS® can allocate the individual dynamic storage areas (DSAs) that reside in 24-bit storage.


    dshipidl (False, int, None)
      The DSHIPIDL system initialization parameter specifies the minimum time, in hours, minutes, and seconds, that an inactive shipped terminal definition must remain installed in this region.


    dshipint (False, int, None)
      The DSHIPINT system initialization parameter specifies the interval between invocations of the timeout delete mechanism.


    dsrtpgm (False, str, None)
      The DSRTPGM system initialization parameter specifies the name of a distributed routing program. The distributed routing program must be specified in the DSRTPGM parameter for all routing and potential target regions.


    dtrpgm (False, str, None)
      The DTRPGM system initialization parameter specifies the name of a dynamic routing program.


    dtrtran (False, str, None)
      The DTRTRAN system initialization parameter specifies the name of the transaction definition that you want CICS to use for dynamic transaction routing.


    dump (False, str, None)
      The DUMP system initialization parameter specifies whether the CICS dump domain is to take SDUMPs.


    dumpds (False, str, None)
      The DUMPDS system initialization parameter specifies the transaction dump data set that is to be opened during CICS initialization.


    dumpsw (False, str, None)
      The DUMPSW system initialization parameter specifies whether you want CICS to switch automatically to the next dump data set when the first is full.


    duretry (False, int, None)
      The DURETRY system initialization parameter specifies, in seconds, the total time that CICS is to continue trying to obtain a system dump using the SDUMP macro.


    ecdsasze (False, str, None)
      The ECDSASZE system initialization parameter specifies the size of the ECDSA.


    edsalim (False, str, None)
      The EDSALIM system initialization parameter specifies the upper limit of the total amount of storage within which CICS® can allocate the individual extended dynamic storage areas (ExxDSAs) that reside in 31-bit (above-the-line) storage; that is, above 16 MB but below 2 GB.


    eodi (False, str, None)
      The EODI system initialization parameter specifies the end-of-data indicator for input from sequential devices.


    erdsasze (False, str, None)
      The ERDSASZE system initialization parameter specifies the size of the ERDSA.


    esdsasze (False, str, None)
      The ESDSASZE system initialization parameter specifies the size of the ESDSA.


    esmexits (False, str, None)
      The ESMEXITS system initialization parameter specifies whether installation data is to be passed through the RACROUTE interface to the external security manager (ESM) for use in exits written for the ESM.


    eudsasze (False, str, None)
      The EUDSASZE system initialization parameter specifies the size of the EUDSA.


    fcqronly (False, str, None)
      The FCQRONLY system initialization parameter specifies whether you want CICS to force all file control requests to run under the CICS QR TCB. This parameter applies to file control requests that access VSAM RLS files and local VSAM LSR files.


    fct (False, str, None)
      The FCT system initialization parameter specifies the suffix of the file control table to be used.


    fepi (False, str, None)
      The FEPI system initialization parameter specifies whether or not you want to use the Front End Programming Interface feature (FEPI).


    fldsep (False, str, None)
      The FLDSEP system initialization parameter specifies 'ON'e through four field-separator characters, each of which indicates end of field in the terminal input data.


    fldstrt (False, str, None)
      The FLDSTRT system initialization parameter specifies a single character to be the field-name-start character for free-form input for built-in functions.


    forceqr (False, str, None)
      The FORCEQR system initialization parameter specifies whether you want CICS to force all CICS API user application programs that are specified as threadsafe to run under the CICS QR TCB, as if they were specified as quasi-reentrant programs.


    fsstaff (False, str, None)
      The FSSTAFF system initialization parameter prevents transactions initiated by function-shipped EXEC CICS START requests being started against incorrect terminals.


    ftimeout (False, int, None)
      The FTIMEOUT system initialization parameter specifies a timeout interval for requests made on files that are opened in RLS mode.


    gmtext (False, str, None)
      The GMTEXT system initialization parameter specifies whether the default logon message text (WELCOME TO CICS) or your own message text is to be displayed on the screen.


    gmtran (False, str, None)
      The GMTRAN system initialization parameter specifies the ID of a transaction.


    gntran (False, str, None)
      The GNTRAN system initialization parameter specifies the transaction that you want CICS to invoke when a user's terminal-timeout period expires, and instructs CICS whether to keep a pseudo-conversation in use at a terminal that is the subject of a timeout sign-off.


    grname (False, str, None)
      The GRNAME system initialization parameter specifies the z/OS Communications Server generic resource name, as 1 through 8 characters, under which a group of CICS terminal-owning regions in a CICSplex register to z/OS Communications Server.


    grplist (False, str, None)
      The GRPLIST system initialization parameter specifies the names of up to four lists of resource definition groups on the CICS system definition file (CSD). The resource definitions in all the groups in the specified lists are loaded during initialization when CICS performs a cold start. If a warm or emergency start is performed, the resource definitions are derived from the global catalog, and the GRPLIST parameter is ignored.


    gtftr (False, str, None)
      The GTFTR system initialization parameter specifies whether CICS can use the MVS generalized trace facility (GTF) as a destination for trace data.


    hpo (False, str, None)
      The HPO system initialization parameter specifies whether you want to use the z/OS Communications Server authorized path feature of the high performance option (HPO).


    httpserverhdr (False, str, None)
      The HTTPSERVERHDR system initialization parameter specifies the value (up to 64 characters) that CICS sets in the server header of HTTP responses.


    httpusragenthdr (False, str, None)
      The HTTPUSRAGENTHDR system initialization parameter specifies the value (up to 64 characters) that CICS sets in the user-agent header of HTTP requests.


    icp (False, str, None)
      The ICP system initialization parameter specifies that you want to perform a cold start for interval control program.


    icv (False, int, None)
      The ICV system initialization parameter specifies the region exit time interval in milliseconds.


    icvr (False, int, None)
      The ICVR system initialization parameter specifies the default runaway task time interval in milliseconds as a decimal number.


    icvtsd (False, int, None)
      The ICVTSD system initialization parameter specifies the terminal scan delay value.


    infocenter (False, str, None)
      The INFOCENTER system initialization parameter specifies the location of the online . If you add this parameter to the Web User Interface (WUI) CICS startup JCL, a link labeled Information Center is displayed on WUI views and menus. If you do not code this parameter, CICS does not construct links to IBM Documentation. .


    initparm (False, str, None)
      The INITPARM system initialization parameter specifies parameters that are to be passed to application programs that use the ASSIGN INITPARM command.


    inttr (False, str, None)
      The INTTR system initialization parameter specifies whether the internal CICS trace destination is to be activated at system initialization.


    ircstrt (False, str, None)
      The IRCSTRT system initialization parameter specifies whether IRC is to be started up at system initialization.


    isc (False, str, None)
      The ISC system initialization parameter specifies whether the CICS programs required for multiregion operation (MRO) and  are to be included.


    jesdi (False, int, None)
      The JESDI system initialization parameter specifies, in a SIT for an alternate XRF system, the JES delay interval.


    jvmprofiledir (False, str, None)
      The JVMPROFILEDIR system initialization parameter specifies the name (up to 240 characters long) of a z/OS UNIX directory that contains the JVM profiles for CICS. CICS searches this directory for the profiles it needs to configure JVMs.


    kerberosuser (False, str, None)
      The KERBEROSUSER system initialization parameter specifies the user ID that is associated with the Kerberos service principal for the CICS region.


    keyring (False, str, None)
      The KEYRING system initialization parameter specifies the fully qualified name of the key ring, within the RACF database, that contains the keys and X.509 certificates used by CICS support for the Secure Sockets Layer (SSL) and for web services security. The region user ID that will use the key ring must either own the key ring or have the authority to use the key ring if it is owned by a different region user ID. You can create an initial key ring with the DFH$RING exec in .CICS.SDFHSAMP.


    lgdfint (False, int, None)
      The LGDFINT system initialization parameter specifies the log defer interval to be used by CICS® log manager when determining how long to delay a forced journal write request before invoking the MVS™ system logger.


    lgnmsg (False, str, None)
      The LGNMSG system initialization parameter specifies whether z/OS Communications Server logon data is to be made available to an application program.


    llacopy (False, str, None)
      The LLACOPY system initialization parameter specifies the situations where CICS uses either the LLACOPY macro or the BLDL macro when locating modules in the DFHRPL or dynamic LIBRARY concatenation.


    localccsid (False, int, None)
      The LOCALCCSID system initialization parameter specifies the default CCSID for the local region.


    lpa (False, str, None)
      The LPA system initialization parameter specifies whether CICS and user modules can be used from the link pack areas.


    maxopentcbs (False, int, None)
      The MAXOPENTCBS system initialization parameter specifies the maximum number, in the range 32 through 4032, of open task control blocks (open TCBs) CICS® can create in the pool of L8 and L9 mode TCBs.


    maxsockets (False, int, None)
      The MAXSOCKETS system initialization parameter specifies the maximum number of IP sockets that can be managed by the CICS sockets domain.


    maxssltcbs (False, int, None)
      The MAXSSLTCBS system initialization parameter specifies the maximum number of S8 TCBs that can run in the SSL pool.


    maxxptcbs (False, int, None)
      The MAXXPTCBS system initialization parameter specifies the maximum number, in the range 1 through 2000, of open X8 and X9 TCBs that can exist concurrently in the CICS region.


    mct (False, str, None)
      The MCT system initialization parameter specifies the monitoring control table suffix.


    mintlslevel (False, str, None)
      The MINTLSLEVEL system initialization parameter specifies the minimum TLS protocol that CICS uses for secure TCP/IP connections.


    mn (False, str, None)
      The MN system initialization parameter specifies whether monitoring is to be switched 'ON' or 'OFF' at initialization.


    mnconv (False, str, None)
      The MNCONV system initialization parameter specifies whether conversational tasks have separate performance class records produced for each pair of terminal control I/O requests.


    mnexc (False, str, None)
      The MNEXC system initialization parameter specifies whether the monitoring exception class is to be made active during initialization.


    mnfreq (False, int, None)
      The MNFREQ system initialization parameter specifies the interval for which CICS automatically produces a transaction performance class record for any long-running transaction.


    mnidn (False, str, None)
      The MNIDN system initialization parameter specifies whether the monitoring identity class is to be made active during CICS initialization.


    mnper (False, str, None)
      The MNPER system initialization parameter specifies whether the monitoring performance class is to be made active during CICS initialization.


    mnres (False, str, None)
      The MNRES system initialization parameter specifies whether transaction resource monitoring is to be made active during CICS initialization.


    mnsync (False, str, None)
      The MNSYNC system initialization parameter specifies whether you want CICS to produce a transaction performance class record when a transaction takes an implicit or explicit syncpoint (unit-of-work).


    mntime (False, str, None)
      The MNTIME system initialization parameter specifies whether you want the time stamp fields in the performance class monitoring data to be returned to an application using the EXEC CICS COLLECT STATISTICS MONITOR(taskno) command in either GMT or local time.


    mqconn (False, str, None)
      The MQCONN system initialization parameter specifies whether you want CICS to start a connection to automatically during initialization.


    mrobtch (False, int, None)
      The MROBTCH system initialization parameter specifies the number of events that must occur before CICS is posted for dispatch because of the batching mechanism.


    mrofse (False, str, None)
      The MROFSE system initialization parameter specifies whether you want to extend the lifetime of the long-running mirror to keep it allocated until the end of the task rather than after a user syncpoint for function shipping applications.


    mrolrm (False, str, None)
      The MROLRM system initialization parameter specifies whether you want to establish an MRO long-running mirror task.


    msgcase (False, str, None)
      The MSGCASE system initialization parameter specifies how you want the message domains to display mixed case messages.


    msglvl (False, int, None)
      The MSGLVL system initialization parameter specifies the message level that controls the generation of messages to the console and JES message log.


    mxt (False, int, None)
      The MXT system initialization parameter specifies the maximum number, in the range 10 through 2000, of user tasks that can exist in a CICS system at the same time. The MXT value does not include CICS system tasks.


    natlang (False, str, None)
      The NATLANG system initialization parameter specifies the single-character code for the language to be supported in this CICS run.


    ncpldft (False, str, None)
      The NCPLDFT system initialization parameter specifies the name of the default named counter pool to be used by the CICS region 'ON' calls it makes to a named counter server.


    newsit (False, str, None)
      The NEWSIT system initialization parameter specifies whether CICS is to load the specified SIT, and enforce the use of all system initialization parameters, modified by any system initialization parameters provided by PARM, SYSIN, or the system console, even in a warm start.


    nistsp800131a (False, str, None)
      The NISTSP800131A system initialization parameter specifies whether the CICS region is to check for conformance to the NIST SP800-131A standard.


    nonrlsrecov (False, str, None)
      The NONRLSRECOV system initialization parameter specifies whether VSAM catalog recovery options should override those specified on the CICS FILE resource definition for all non-RLS files. Default behavior, with NONRLSRECOV=VSAMCAT, will take recovery attributes from the catalog if they are present, and from the file definition otherwise. RLS files must always specify recovery options on the catalog.


    nqrnl (False, str, None)
      The NQRNL system initialization parameter controls resource name list (RNL) processing by z/OS global resource serialization, which can cause the scope value of a resource to change. CICS uses z/OS global resource serialization to provide sysplex-wide protection of application resources.


    offsite (False, str, None)
      The 'OFF'SITE system initialization parameter specifies whether CICS is to restart in 'OFF'-site recovery mode; that is, a restart is taking place at a remote site.


    opertim (False, int, None)
      The OPERTIM system initialization parameter specifies the write-to-operator timeout value, in the range 0 through 86400 seconds (24 hours).


    opndlim (False, int, None)
      The OPNDLIM system initialization parameter specifies the destination and close destination request limit.


    parmerr (False, str, None)
      The PARMERR system initialization parameter specifies what action you want to follow if CICS detects incorrect system initialization parameter overrides during initialization.


    pdi (False, int, None)
      The PDI system initialization parameter specifies the XRF primary delay interval, in seconds, in a SIT for an active CICS region.


    pdir (False, str, None)
      The PDIR system initialization parameter specifies a suffix for the PDIR list.


    pgaictlg (False, str, None)
      The PGAICTLG system initialization parameter specifies whether autoinstalled program definitions should be cataloged.


    pgaiexit (False, str, None)
      The PGAIEXIT system initialization parameter specifies the name of the program autoinstall exit program.


    pgaipgm (False, str, None)
      The PGAIPGM system initialization parameter specifies the state of the program autoinstall function at initialization.


    pgchain (False, str, None)
      The PGCHAIN system initialization parameter specifies the character string that is identified by terminal control as a BMS terminal page-chaining command.


    pgcopy (False, str, None)
      The PGCOPY system initialization parameter specifies the character string that is identified by terminal control as a BMS command to copy output from one terminal to another.


    pgpurge (False, str, None)
      The PGPURGE system initialization parameter specifies the character string that is identified by terminal control as a BMS terminal page-purge command.


    pgret (False, str, None)
      The PGRET system initialization parameter specifies the character string that is recognized by terminal control as a BMS terminal page-retrieval command.


    pltpi (False, str, None)
      The PLTPI system initialization parameter specifies the suffix for, or the full name of, a program list table that contains a list of programs to be run in the final stages of system initialization.


    pltpisec (False, str, None)
      The PLTPISEC system initialization parameter specifies whether you want CICS to perform command security or resource security checking for PLT programs during CICS initialization.


    pltpiusr (False, str, None)
      The PLTPIUSR system initialization parameter specifies the user ID that CICS uses for security checking for PLT programs that run during CICS initialization.


    pltsd (False, str, None)
      The PLTSD system initialization parameter specifies the suffix for, or full name of, a program list table that contains a list of programs to be run during system termination.


    prgdlay (False, int, None)
      The PRGDLAY system initialization parameter specifies the BMS purge delay time interval that is added t the specified delivery time to determine when a message is to be considered undeliverable and therefore purged.


    print (False, str, None)
      The PRINT system initialization parameter specifies the method of requesting printout of the contents of a 3270 screen.


    prtyage (False, int, None)
      The PRTYAGE system initialization parameter specifies the number of milliseconds to be used in the priority aging algorithm that is used to increment the priority of a task.


    prvmod (False, str, None)
      The PRVMOD system initialization parameter specifies the names of those modules that are not to be used from the LPA.


    psbchk (False, str, None)
      The PSBCHK system initialization parameter specifies whether CICS is to perform PSB authorization checks for remote terminal users who use transaction routing to initiate a transaction in this CICS region to access an attached IMS system.


    psdint (False, int, None)
      The PSDINT system initialization parameter specifies the persistent session delay interval, which states if, and for how long, z/OS CommunicationsServer holds sessions in a recovery-pending state.


    pstype (False, str, None)
      The PSTYPE system initialization parameter specifies whether CICS uses z/OS Communications Server single-node persistent sessions (SNPS), multinode persistent sessions (MNPS), or does not use z/OS Communications Server persistent sessions support (NOPS).


    pvdelay (False, int, None)
      The PVDELAY system initialization parameter specifies the persistent verification delay as a value in the range 0 through 10080 minutes (up to 7 days).


    quiestim (False, int, None)
      The QUIESTIM system initialization parameter specifies a timeout value for data set quiesce requests.


    racfsync (False, str, None)
      The RACFSYNC system initialization parameter specifies whether CICS listens for type 71 ENF events and refreshes user security.


    ramax (False, int, None)
      The RAMAX system initialization parameter specifies the size in bytes of the I/O area allocated for each RECEIVE ANY issued by CICS, in the range 0 through 32767 bytes.


    rapool (False, str, None)
      The RAPOOL system initialization parameter specifies the number of concurrent receive-any requests that CICS is to process from the z/OS Communications Server for SNA.


    rdsasze (False, str, None)
      The RDSASZE system initialization parameter specifies the size of the RDSA.


    rentpgm (False, str, None)
      The RENTPGM system initialization parameter specifies whether you want CICS to allocate the read-only DSAs from read-only key-0 protected storage.


    resoverrides (False, str, None)
      The RESOVERRIDES system initialization parameter specifies the 1-64 character name of the resource overrides file. For more information, see .


    resp (False, str, None)
      The RESP system initialization parameter specifies the type of request that CICS terminal control receives from logical units.


    ressec (False, str, None)
      The RESSEC system initialization parameter specifies whether you want CICS to honor the RESSEC option specified on a transaction's resource definition.


    rls (False, str, None)
      The RLS system initialization parameter specifies whether CICS is to support VSAM record-level sharing (RLS).


    rlstolsr (False, str, None)
      The RLSTOLSR system initialization parameter specifies whether CICS is to include files that are to be opened in RLS mode when calculating the number of buffers, strings, and other resources for an LSR pool.


    rmtran (False, str, None)
      The RMTRAN system initialization parameter specifies the name of the transaction that you want an alternate CICS to initiate when logged-on class 1 terminals, which are defined with the attribute RECOVNOTIFY(TRANSACTION) specified, are switched following a takeover.


    rrms (False, str, None)
      The RRMS system initialization parameter specifies whether CICS is to register as a resource manager with recoverable resource management services (RRMS).


    rst (False, str, None)
      The RST system initialization parameter specifies a recoverable service table suffix.


    rstsignoff (False, str, None)
      The RSTSIGNOFF system initialization parameter specifies whether all users signed-on to the active CICS region are to remain signed-on following a persistent sessions restart or an XRF takeover.


    rstsigntime (False, int, None)
      The RSTSIGNTIME parameter specifies the timeout delay interval for signon retention during a persistent sessions restart or an XRF takeover.


    ruwapool (False, str, None)
      The RUWAPOOL parameter specifies the option for allocating a storage pool the first time a program invoked by Language Environment runs in a task.


    sdsasze (False, str, None)
      The SDSASZE system initialization parameter specifies the size of the SDSA.


    sdtran (False, str, None)
      The SDTRAN system initialization parameter specifies the name of the shutdown transaction to be started at the beginning of normal and immediate shutdown.


    sec (False, str, None)
      The SEC system initialization parameter specifies what level of external security you want CICS to use.


    secprfx (False, str, None)
      The SECPRFX system initialization parameter specifies whether CICS prefixes the resource names in any authorization requests to RACF.


    sit (False, str, None)
      The SIT system initialization parameter specifies the suffix, if any, of the system initialization table that you want CICS to load at the start of initialization.


    skrxxxx (False, dict, None)
      The SKRxxxx system initialization parameter specifies that a single-keystroke-retrieval operation is required.


    snpreset (False, str, None)
      The SNPRESET system initialization parameter specifies whether preset userid terminals share a single access control environment element (ACEE) that is associated with the userid, or a unique ACEE for every terminal.


    snscope (False, str, None)
      The SNSCOPE system initialization parameter specifies whether a userid can be signed on to CICS more than once, within the scope of a single CICS region, a single MVS image, and a sysplex.


    sotuning (False, str, None)
      The SOTUNING system initialization parameter specifies whether performance tuning for HTTP connections will occur to protect CICS from unconstrained resource demand.


    spctr (False, str, None)
      The SPCTR system initialization parameter specifies the level of special tracing required for CICS as a whole.


    spctrxx (False, dict, None)
      The SPCTRxx system initialization parameter specifies the level of special tracing for a particular CICS component used by a transaction, terminal, or both.


    spool (False, str, None)
      The SPOOL system initialization parameter specifies whether the system spooling interface is required.


    srbsvc (False, int, None)
      The SRBSVC system initialization parameter specifies the number that you have assigned to the CICS type 6 SVC.


    srt (False, str, None)
      The SRT system initialization parameter specifies the system recovery table suffix.


    srvercp (False, str, None)
      The SRVERCP system initialization parameter specifies the default server code page to be used by the DFHCNV data conversion table but only if the SRVERCP parameter in the DFHCNV macro is set to SYSDEF.


    sslcache (False, str, None)
      The SSLCACHE system initialization parameter specifies whether session IDs for SSL sessions are to be cached locally or at sysplex level for reuse by the CICS® region. The SSL cache allows CICS to perform abbreviated handshakes with clients that it has previously authenticated.


    ssldelay (False, int, None)
      The SSLDELAY system initialization parameter specifies the length of time in seconds for which CICS retains session ids for secure socket connections.


    start (False, str, None)
      The START system initialization parameter specifies the type of start for the system initialization program.


    starter (False, str, None)
      The STARTER system initialization parameter specifies whether the generation of starter system modules (with $ and


    stateod (False, int, None)
      The STATEOD system initialization parameter specifies the end-of-day time in the format hhmmss.


    statint (False, int, None)
      The STATINT system initialization parameter specifies the recording interval for system statistics in the format hhmmss.


    statrcd (False, str, None)
      The STATRCD system initialization parameter specifies the interval statistics recording status at CICS initialization.


    stgprot (False, str, None)
      The STGPROT system initialization parameter specifies whether you want storage protection to operate in the CICS region.


    stgrcvy (False, str, None)
      The STGRCVY system initialization parameter specifies whether CICS should try to recover from a storage violation.


    stntr (False, str, None)
      The STNTR system initialization parameter specifies the level of standard tracing required for CICS as a whole.


    stntrxx (False, dict, None)
      The STNTRxx system initialization parameter specifies the level of standard tracing you require for a particular CICS component. Specify the final two characters as the dictionary key


    subtsks (False, int, None)
      The SUBTSKS system initialization parameter specifies the number of task control blocks (TCBs) you want CICS to use for running tasks in concurrent mode.


    suffix (False, str, None)
      The SUFFIX system initialization parameter specifies the last two characters of the name of this system initialization table.


    sysidnt (False, str, None)
      The SYSIDNT system initialization parameter specifies a 1- to 4-character name that is known only to your CICS region.


    systr (False, str, None)
      The SYSTR system initialization parameter specifies the setting of the main system trace flag.


    sydumax (False, int, None)
      The SYDUMAX system initialization parameter specifies the limit on the number of system dumps that can be taken per dump table entry.


    takeovr (False, str, None)
      The TAKEOVR system initialization parameter specifies the action to be taken by the alternate CICS region, following the apparent loss of the surveillance signal in the active CICS region.


    tbexits (False, str, None)
      The TBEXITS system initialization parameter specifies the names of your backout exit programs for use during emergency restart backout processing.


    tcp (False, str, None)
      The TCP system initialization parameter specifies whether the pregenerated non-z/OS Communications Server terminal control program, DFHTCP, is to be included.


    tcpip (False, str, None)
      The TCPIP system initialization parameter specifies whether CICS TCP/IP services are to be activated at CICS startup.


    tcsactn (False, str, None)
      The TCSACTN system initialization parameter specifies the required action that CICS terminal control should take if the terminal control shutdown wait threshold expires.


    tcswait (False, str, None)
      The TCSWAIT system initialization parameter specifies the required CICS terminal control shutdown wait threshold.


    tct (False, str, None)
      The TCT system initialization parameter specifies which terminal control table, if any, is to be loaded.


    tctuakey (False, str, None)
      The TCTUAKEY system initialization parameter specifies the storage key for the terminal control table user areas (TCTUAs) if you are operating CICS with storage protection (STGPROT=YES).


    tctualoc (False, str, None)
      The TCTUALOC system initialization parameter specifies where terminal user areas (TCTUAs) are to be stored.


    td (False, str, None)
      The TD system initialization parameter specifies the number of VSAM buffers and strings to be used for intrapartition transient data (TD).


    tdintra (False, str, None)
      The TDINTRA system initialization parameter specifies whether CICS is to initialize with empty intrapartition TD queues.


    traniso (False, str, None)
      The TRANISO system initialization parameter specifies, together with the STGPROT system initialization parameter, whether you want transaction isolation in the CICS region.


    trap (False, str, None)
      The TRAP system initialization parameter specifies whether the FE global trap exit is to be activated at system initialization.


    trdumax (False, int, None)
      The TRDUMAX system initialization parameter specifies the limit on the number of transaction dumps that may be taken per Dump Table entry.


    trtabsz (False, int, None)
      The TRTABSZ system initialization parameter specifies the size, in kilobytes, of the internal trace table.


    trtransz (False, int, None)
      The TRTRANSZ system initialization parameter specifies the size, in kilobytes, of the transaction dump trace table.


    trtranty (False, str, None)
      The TRTRANTY system initialization parameter specifies which trace entries should be copied from the internal trace table to the transaction dump trace table.


    ts (False, str, None)
      The TS system initialization parameter specifies whether you want to perform a cold start for temporary storage, as well as the number of VSAM buffers and strings to be used for auxiliary temporary storage.


    tsmainlimit (False, str, None)
      The TSMAINLIMIT system initialization parameter specifies a limit for the storage that is available for main temporary storage queues to use. You can specify an amount of storage in the range 1 - 32768 MB (32 GB), but this amount must not be greater than 25% of the value of the z/OS parameter MEMLIMIT. The default is 64 MB.


    tst (False, str, None)
      The TST system initialization parameter specifies the temporary storage table suffix.


    udsasze (False, str, None)
      The UDSASZE system initialization parameter specifies the size of the UDSA.


    uownetql (False, str, None)
      The UOWNETQL system initialization parameter specifies a qualifier for the NETUOWID for units of work initiated on the local CICS region.


    usertr (False, str, None)
      The USERTR system initialization parameter specifies whether the main user trace flag is to be set on or off.


    usrdelay (False, int, None)
      The USRDELAY system initialization parameter specifies the maximum time, in the range 0 - 10080 minutes (up to seven days), that an eligible user ID and its associated attributes are cached in the CICS region after use. A user ID that is retained in the user table can be reused.


    ussconfig (False, str, None)
      The USSCONFIG system initialization parameter specifies the name and path of the root directory for configuration files on z/OS UNIX.


    usshome (False, str, None)
      The USSHOME system initialization parameter specifies the name and path of the root directory for files on z/OS UNIX.


    vtam (False, str, None)
      The VTAM system initialization parameter specifies whether the z/OS Communications Server access method is to be used.


    vtprefix (False, str, None)
      The VTPREFIX system initialization parameter specifies the first character to be used for the terminal identifiers (termids) of autoinstalled virtual terminals.


    webdelay (False, str, None)
      The WEBDELAY system initialization parameter specifies two Web delay periods.


    wlmhealth (False, str, None)
      The WLMHEALTH system initialization parameter specifies the time interval and the health adjustment value to be used by CICS® on z/OS® Workload Manager Health API (IWM4HLTH) calls, which CICS makes to inform z/OS WLM about the health state of a CICS region.


    wrkarea (False, int, None)
      The WRKAREA system initialization parameter specifies the number of bytes to be allocated to the common work area (CWA).


    xappc (False, str, None)
      The XAPPC system initialization parameter specifies whether RACF session security can be used when establishing APPC sessions.


    xcfgroup (False, str, None)
      The XCFGROUP system initialization parameter specifies the name of the cross-system coupling facility (XCF) group to be joined by this region.


    xcmd (False, str, None)
      The XCMD system initialization parameter specifies whether you want CICS to perform command security checking, and optionally the RACF resource class name in which you have defined the command security profiles.


    xdb2 (False, str, None)
      The XDB2 system initialization parameter specifies whether you want CICS to perform DB2ENTRY security checking.


    xdct (False, str, None)
      The XDCT system initialization parameter specifies whether you want CICS to perform resource security checking for transient data queues.


    xfct (False, str, None)
      The XFCT system initialization parameter specifies whether you want CICS to perform file resource security checking, and optionally specifies the RACF resource class name in which you have defined the file resource security profiles.


    xhfs (False, str, None)
      The XHFS system initialization parameter specifies whether CICS is to check the transaction user's ability to access files in the z/OS UNIX System Services file system.


    xjct (False, str, None)
      The XJCT system initialization parameter specifies whether you want CICS to perform journal resource security checking.


    xlt (False, str, None)
      The XLT system initialization parameter specifies a suffix for the transaction list table.


    xpct (False, str, None)
      The XPCT system initialization parameter specifies whether you want CICS to perform started transaction resource security checking, and optionally specifies the name of the RACF resource class name in which you have defined the started task security profiles.


    xppt (False, str, None)
      The XPPT system initialization parameter specifies that CICS is to perform application program resource security checks and optionally specifies the RACF resource class name in which you have defined the program resource security profiles.


    xpsb (False, str, None)
      The XPSB system initialization parameter specifies whether you want CICS to perform program specification block (PSB) security checking and optionally specifies the RACF resource class name in which you have defined the PSB security profiles.


    xptkt (False, str, None)
      The XPTKT system initialization parameter specifies whether CICS checks if a user can generate a PassTicket for the user's userid using the EXEC CICS REQUEST PASSTICKET command, the EXEC CICS REQUEST ENCRYPTPTKT command, or the EXEC FEPI REQUEST PASSTICKET command.


    xres (False, str, None)
      The XRES system initialization parameter specifies whether you want CICS to perform resource security checking for particular CICS resources and optionally specifies the general resource class name in which you have defined the resource security profiles.


    xrf (False, str, None)
      The XRF system initialization parameter specifies whether XRF support is to be included in the CICS region.


    xtran (False, str, None)
      The XTRAN system initialization parameter specifies whether you want CICS to perform transaction security checking and optionally specifies the RACF resource class name in which you have defined the transaction security profiles.


    xtst (False, str, None)
      The XTST system initialization parameter specifies whether you want CICS to perform security checking for temporary storage queues and optionally specifies the RACF resource class name in which you have defined the temporary storage security profiles.


    xuser (False, str, None)
      The XUSER system initialization parameter specifies whether CICS is to perform surrogate user checks.


    epcdsasze (False, str, None)
      The EPCDSASZE parameter specifies the size of the EPCDSA dynamic storage area. Message DFHSM0136I at initialization shows the value that is set.


    epudsasze (False, str, None)
      The EPUDSASZE parameter specifies the size of the EPUDSA dynamic storage area. Message DFHSM0136I at initialization shows the value that is set.


    maxtlslevel (False, str, None)
      The MAXTLSLEVEL system initialization parameter specifies the maximum TLS protocol that CICS uses for secure TCP/IP connections.


    pcdsasze (False, int, None)
      The PCDSASZE parameter specifies the size of the PCDSA dynamic storage area. Message DFHSM0136I at initialization shows the value that is set.


    pudsasze (False, str, None)
      The PUDSASZE parameter specifies the size of the PUDSA dynamic storage area. Message DFHSM0136I at initialization shows the value that is set.


    sdtmemlimit (False, str, None)
      The SDTMEMLIMIT system initialization parameter specifies a limit to the amount of storage above the bar that is available for shared data tables to use for control information (entry descriptors, backout elements, and index nodes). The default is 4 GB. When you set this parameter, check your current setting for the z/OS MEMLIMIT parameter.








See Also
--------

.. seealso::

   :ref:`stop_cics_module`
      The official documentation on the **stop_cics** module.


Examples
--------

.. code-block:: yaml+jinja

    
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
    - name: Start CICS with more customisation
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



Return Values
-------------

changed (always, bool, )
  True if the CICS startup JCL was submitted, otherwise False.


failed (always, bool, )
  True if the query job failed, otherwise False.


jcl (always, list, )
  The CICS startup JCL that is built during module execution.


err (always, str, )
  The error message returned when building the JCL.


executions (always, list, )
  A list of program executions performed during the Ansible task.


  name (always, str, )
    A human-readable name for the program execution.


  rc (always, int, )
    The return code for the program execution.


  stdout (always, str, )
    The standard out stream returned by the program execution.


  stderr (always, str, )
    The standard error stream returned from the program execution.






Status
------





Authors
~~~~~~~

- Kiera Bennett (@KieraBennett)


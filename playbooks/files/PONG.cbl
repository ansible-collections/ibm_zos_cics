       IDENTIFICATION DIVISION.
       PROGRAM-ID.   PONG.
       AUTHOR.       WILL YATES.

       ENVIRONMENT DIVISION.

       DATA DIVISION.

       WORKING-STORAGE SECTION.

       01  BALL-SPEED                  PIC X(4).

       LINKAGE SECTION.

       01  DFHCOMMAREA.
           02 SPEED                    PIC X(4).

       PROCEDURE DIVISION.
           MOVE "200"      TO BALL-SPEED.
           MOVE BALL-SPEED TO DFHCOMMAREA.
           EXEC CICS RETURN END-EXEC.

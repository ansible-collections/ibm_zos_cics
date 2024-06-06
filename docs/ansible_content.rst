.. ...........................................................................
.. © Copyright IBM Corporation 2020,2024                                     .
.. ...........................................................................

=========
z/OS CICS
=========

The **IBM® z/OS® CICS® collection**, also represented as
ibm_zos_cics in this document, is part of the broader
initiative to bring Ansible® Automation to IBM Z® through the offering
**Red Hat® Ansible Certified Content for IBM Z**.

The **IBM® z/OS® CICS® collection** provides modules for automation tasks that
perform operations on CICS and CICSPlex SM resources and definitions, for example,
creating and installing a PROGRAM definition, then updating or deleting the definition.
These modules interact with the `CMCI REST API`_ of the CICS® management client
interface (CMCI) for system management.

The **IBM® z/OS® CICS® collection** also provides modules for provisioning and managing
CICS TS data sets and utilities. You can use these Ansible modules to create automation
tasks that provision or deprovision a CICS region and tasks for CICS startup and
shutdown.

The Ansible modules in this collection are written in Python.

.. _CMCI REST API:
   https://www.ibm.com/docs/en/cics-ts/latest?topic=cmci-how-it-works-rest-api

.. toctree::
   :maxdepth: 1
   :caption: Collection Content

   source/modules

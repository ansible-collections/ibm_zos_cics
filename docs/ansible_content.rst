.. ...........................................................................
.. © Copyright IBM Corporation 2020,2021                                     .
.. ...........................................................................

=========
z/OS CICS
=========

The **IBM® z/OS® CICS® collection**, also represented as
ibm_zos_cics in this document, is  part of the broader
initiative to bring Ansible® Automation to IBM Z® through the offering
**Red Hat® Ansible Certified Content for IBM Z**.

The **IBM® z/OS® CICS® collection** supports automation tasks that can
define, install, and perform actions on CICS definitions and resources such as
creating a PROGRAM definition, installing and updating it, and deleting the
definition.

The Ansible modules in this collection are written in Python and interact with
the `CMCI REST API`_ of the CICS® management client interface (CMCI) for system
management.

.. _CMCI REST API:
   https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/fundamentals/cpsm/cpsm-cmci-restfulapi-overview.html

.. toctree::
   :maxdepth: 1
   :caption: Collection Content

   source/modules

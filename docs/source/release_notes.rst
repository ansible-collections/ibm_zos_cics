.. ...............................................................................
.. © Copyright IBM Corporation 2020                                              .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

========
Releases
========

Version 1.0.0
=============

What's New
-------------------
Initial release of the **IBM z/OS CICS collection**, also referred to as **ibm_zos_cics**, which is part of the broader offering **Red Hat® Ansible Certified Content for IBM Z®**.

This collection can manage CICS resources and definitions by calling the `CMCI REST API`_, which can be configured in a CICSplex or in a stand-alone region.

* Modules

  * ``cmci_create`` - Create definitional CICS and CICSPlex® SM resources in CICS regions, using the CMCI REST API.
  * ``cmci_delete`` - Delete installed and definitional CICS and CICSPlex® SM resources from CICS regions, using the CMCI REST API.
  * ``cmci_get`` - Get information about installed and definitional CICS and CICSPlex® SM resources from CICS regions, using the CMCI REST API.
  * ``cmci_install`` - Install CICS and CICSPlex® SM resources into CICS regions from definitions, using the CMCI REST API.
  * ``cmci_update`` - Make changes to CICS and CICSPlex® SM resources in CICS regions using the CMCI REST API.


* Documentation

  * Generic documentation is available at `the documentation site`_, covering guidance on installation, modules, and other reference.

  * Documentation related to playbook configuration is provided with sample playbooks at the `samples repository`_. Each playbook contains a README that explains what configurations must be made to run a sample playbook.


* Playbooks

  * Sample playbooks are available at the `samples repository`_. Each playbook contains a README that explains what configurations must be made to run a sample playbook.

.. _samples repository:
   https://github.com/IBM/z_ansible_collections_samples/blob/master/README.md

.. _CMCI REST API:
   https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/fundamentals/cpsm/cpsm-cmci-restfulapi-overview.html

.. _the documentation site:
   https://ansible-collections.github.io/ibm_zos_cics/

Availability
------------

* `Galaxy`_
* `GitHub`_

.. _GitHub:
   https://github.com/ansible-collections/ibm_zos_cics

.. _Galaxy:
   https://galaxy.ansible.com/ibm/ibm_zos_cics


Reference
---------

* Supported by IBM CICS V4.2 or later


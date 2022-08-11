.. ...............................................................................
.. © Copyright IBM Corporation 2020,2021                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

========
Releases
========

Version 1.0.3
=============

What's New
-------------------
* Updated timeout support on requests to be configurable via the ``timeout`` option. The default value is 30 seconds if not specified

* Improve sanitisation and validation of parameters.

* Added support for CMCI Feedback on failed CMCI Requests.


Version 1.0.1
=============

What's New
-------------------

Initial release of the **IBM® z/OS® CICS® collection**, also referred to as **ibm_zos_cics**, which is part of the broader offering **Red Hat® Ansible® Certified Content for IBM Z®**.

This collection can manage CICS and CICSPlex® SM resources and definitions by calling the `CMCI REST API`_, which can be configured in a CICSplex or in a stand-alone region.

* Modules

  * ``cmci_create`` - Create definitional CICS and CICSPlex SM resources in CICS regions, by initiating POST requests via the CMCI REST API.
  * ``cmci_delete`` - Remove or discard definitional and installed CICS and CICSPlex SM resources from CICS regions, by initiating DELETE requests via the CMCI REST API.
  * ``cmci_get`` - Retrieve information about installed and definitional CICS and CICSPlex SM resources from CICS regions, by initiating GET requests via the CMCI REST API.
  * ``cmci_action`` - Install CICS and CICSPlex SM resources into CICS regions from definitions, by initiating PUT requests via the CMCI REST API.
  * ``cmci_update`` - Make changes to CICS and CICSPlex SM resources in CICS regions, by initiating PUT requests via the CMCI REST API.


* Documentation

  * Generic documentation is available at `the documentation site`_, covering guidance on installation, modules, and other reference.

  * Documentation related to playbook configuration is provided with sample playbooks at the `samples repository`_. Each playbook contains a README that explains what configurations must be made to run a sample playbook.


* Playbooks

  * Sample playbooks are available at the `samples repository`_. Each playbook contains a README that explains what configurations must be made to run a sample playbook.

.. _samples repository:
   https://github.com/IBM/z_ansible_collections_samples/tree/master/zos_subsystems/cics

.. _CMCI REST API:
   https://www.ibm.com/docs/en/cics-ts/latest?topic=cmci-how-it-works-rest-api

.. _the documentation site:
   https://ibm.github.io/z_ansible_collections_doc/ibm_zos_cics/docs/ansible_content.html

Availability
------------

* `Automation Hub`_
* `Galaxy`_
* `GitHub`_

.. _GitHub:
   https://github.com/ansible-collections/ibm_zos_cics

.. _Galaxy:
   https://galaxy.ansible.com/ibm/ibm_zos_cics

.. _Automation Hub:
   https://www.ansible.com/products/automation-hub


Reference
---------

* Supported by IBM CICS V4.2 or later

.. ...............................................................................
.. © Copyright IBM Corporation 2020,2024                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

========
Releases
========

Version 2.1.0
=============
What's New
-------------------

**New modules**

**General Availability of CICS provisioning modules.** You can use these Ansible modules to create automation tasks that provision or deprovision, and start or stop
a CICS region. Sample playbooks show you how to do this with the latest version of the Ansible IBM z/OS CICS collection.

You can use the following modules to provision and manage CICS TS data sets:

* ``aux_temp_storage`` can be used to create or remove the CICS auxiliary temporary storage data set.
* ``aux_trace`` can be used to allocate the CICS auxiliary trace data sets.
* ``csd`` can be used to create, manage, or remove the CICS system definition data set.
* ``global_catalog`` can be used to create, manage, or remove the CICS global catalog data set.
* ``local_request_queue`` can be used to create, manage, or remove the CICS local request queue data set.
* ``td_intrapartition`` can be used to create or remove the CICS transient data intrapartition data set.
* ``transaction_dump`` can be used to allocate the CICS transaction dump data sets.

You can use the following modules for CICS startup and shutdown operations:

* ``region_jcl`` can be used to create a CICS startup JCL data set.
* ``stop_region`` can be used to stop a CICS region.

The group name for the CICS provisioning modules is ``region``.

CICS provisioning modules provide support for all in-service CICS TS releases including the latest CICS TS 6.2.

**Changed modules**

The group name for the CMCI modules is changed to ``cmci`` instead of ``cmci_group``. ``cmci_group`` is deprecated.

**New playbooks**

Sample playbooks are available at the `samples repository`_. The CICS provisioning playbook samples demonstrate how to configure and allocate the required
data sets to provision and start a CICS region, with or without SMSS support. The deprovisioning sample shows how to stop a running region and delete all
the associated data sets.

Version 2.0.0
=============
What's New
-------------------

* **Removed support for Python 2.7.** Python 2.7 is no longer supported as the managed node runtime.

Version 1.0.6
=============
What's New
-------------------
* Bug fix that allows the CICSPlex SM Scope and Context to contain special characters '$', '@', and '#'.


Version 1.0.5
=============
What's New
-------------------
* Bug fix that includes the ``requirements.txt`` file in the built collection.


Version 1.0.4
=============
What's New
-------------------
* Provide variables for all modules in one go using Ansible's `group module defaults`_ support. The group name for the CMCI modules is ``cmci_group``.

* Prevent ``cmci_get`` from failing if no records are found via the ``fail_on_nodata`` option. The default value is true if not specified.

.. _group module defaults:
   https://docs.ansible.com/ansible/2.8/user_guide/playbooks_module_defaults.html#module-defaults-groups


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

**Modules**

* ``cmci_create`` - Create definitional CICS and CICSPlex SM resources in CICS regions, by initiating POST requests via the CMCI REST API.
* ``cmci_delete`` - Remove or discard definitional and installed CICS and CICSPlex SM resources from CICS regions, by initiating DELETE requests via the CMCI REST API.
* ``cmci_get`` - Retrieve information about installed and definitional CICS and CICSPlex SM resources from CICS regions, by initiating GET requests via the CMCI REST API.
* ``cmci_action`` - Install CICS and CICSPlex SM resources into CICS regions from definitions, by initiating PUT requests via the CMCI REST API.
* ``cmci_update`` - Make changes to CICS and CICSPlex SM resources in CICS regions, by initiating PUT requests via the CMCI REST API.


**Documentation**

* Generic documentation is available at `the documentation site`_, covering guidance on installation, modules, and other reference.

* Documentation related to playbook configuration is provided with sample playbooks at the `samples repository`_. Each playbook contains a README that explains what configurations must be made to run a sample playbook.


**Playbooks**

* Sample playbooks are available at the `samples repository`_. Each playbook contains a README that explains what configurations must be made to run a sample playbook.

.. _samples repository:
   https://github.com/IBM/z_ansible_collections_samples/tree/main/zos_subsystems/cics

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

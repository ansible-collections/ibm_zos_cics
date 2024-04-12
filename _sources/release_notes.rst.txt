.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

========
Releases
========

Version 1.1.0-beta.5
=============
What's New
-------------------

**New modules**

* ``start_cics`` - Start a CICS region.
* ``stop_cics`` - Stop a CICS region.

**Changed modules**

* ``csd`` - A new ``state`` option, ``script`` is introduced so that you can now supply a script that contains ``CSDUP`` commands to update an existing CSD. The script can be either a data set or a z/OS UNIX file.
* All modules for CICS region data sets - New option ``space_secondary`` is introduced so that you can specify the size of the secondary extent.
* All modules for CICS region data sets - Return values now use ``data_set_organization`` to indicate the organization of the data set. The ``vsam`` field has been removed from the return structure.


Version 1.1.0-beta.4
=============
What's New
-------------------

**New modules**

* ``auxiliary_temp`` - Create and remove the CICS auxiliary temporary storage data set.
* ``csd`` - Create, remove, and manage the CICS system definition data set.
* ``intrapartition`` - Create and remove the CICS transient data intrapartition data set.
* ``trace`` - Allocate the CICS auxiliary trace data sets.
* ``transaction_dump`` - Allocate the CICS transaction dump data sets.

**Changed modules**

* ``local_request_queue`` -  New option ``warm`` added to the ``state`` input parameter.

**Bugfixes**

* ``local_request_queue`` and ``local_request_queue`` - The behavior of these modules with ``state`` set to ``initial`` is updated to match documentation.

Version 1.1.0-beta.3
=============
What's New
-------------------

**New modules**

* ``local_request_queue`` - Create and remove the CICS local request queue data set.

**Changed modules**

* ``global_catalog`` and ``local_catalog`` - Added support for the ``region_data_sets`` and ``cics_data_sets`` defaults groups. This enhancement changes the way you specify the data set location for these modules.

Version 1.1.0-beta.2
=============
What's New
-------------------

**New modules**

* ``local_catalog`` - Create, initialize, and manage the CICS local catalog data set.

**Changed modules**

* ``global_catalog`` - Added return values ``start_state``, ``end_state``, and ``executions``.

**Bugfixes**

* ``global_catalog`` - Fixed an issue that when input parameters were lowercase, the module failed. Now these input parameters are not case sensitive.
* ``global_catalog`` - Fixed an issue that was found in the ``changed`` flag. Now the ``changed`` flag corresponds with the actions taken during the ``global_catalog`` execution.


Version 1.1.0-beta.1
=============
What's New
-------------------

**New modules**

* ``global_catalog`` - Create, initialize, and manage the CICS global catalog data set.


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

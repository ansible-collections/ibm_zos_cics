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
a CICS region. Sample playbooks show you how to do this with the latest version of the Ansible IBM z/OS CICS collection. All modules were initially released
with Version 1.1.0-beta as noted below. Subsequent Version 1.1.0-beta releases may include enhancements and bugfixes for these modules. Refer to the What's new
of Version 1.1.0-beta releases for details.

You can use the following modules for provisioning and managing CICS TS data sets:

* ``aux_temp_storage`` for the CICS auxiliary temporary storage data set. This module was initially
  released as ``auxiliary_temp`` with Version 1.1.0-beta.4. The module is changed to ``aux_temp_storage`` in Version 2.1.0.
* ``aux_trace`` for the CICS auxiliary trace data sets. This module was initially released as ``trace`` with Version 1.1.0-beta.4.
  The module is changed to ``aux_trace`` in Version 2.1.0.
* ``csd`` for the CICS system definition data set. This module was initially released with Version 1.1.0-beta.4.
* ``global_catalog`` for the CICS global catalog data set. This module was initially released with Version 1.1.0-beta.4.
* ``local_request_queue`` for the CICS local request queue data set. This module was initially released with Version 1.1.0-beta.3.
* ``td_intrapartition`` for the CICS transient data intrapartition data set. This module was initially released as ``intrapartition`` with
  Version 1.1.0-beta.4. The module is changed to ``td_intrapartition`` in Version 2.1.0.
* ``transaction_dump`` for the CICS transaction dump data sets. This module was initially released with Version 1.1.0-beta.4.

You can use the following modules for CICS startup and shutdown operations:

* ``region_jcl`` - Create a CICS startup JCL data set. This module replaces ``start_cics``, which was released with Version 1.1.0-beta.5.
  ``region_jcl`` is significantly different from ``start_cics`` in function. ``region_jcl`` creates a data set that contains the startup JCL, but
  doesn't perform the actual startup processing. ``region_jcl`` also supports definition and allocation of user data sets with the ``user_data_sets`` parameter.
* ``stop_region`` - Stop a CICS region. This module was initially released as ``stop_cics`` with Version 1.1.0-beta.5. The module is changed to ``stop_region``
  in Version 2.1.0. In Version 2.1.0, ``stop_region`` supports a new input parameter, ``job_name`` so that you can use the job name, which is typically the CICS's
  APPLID, to identify a running CICS region.

The group name for the CICS provisioning modules is ``region``. However, in the Version 1.1.0-beta releases, the group name was ``region_group``.

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

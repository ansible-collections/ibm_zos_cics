==============================
ibm.ibm_zos_cics Release Notes
==============================

.. contents:: Topics


v1.1.0-beta.5
=============

Release Summary
---------------

This release contains new modules for starting and stopping standalone CICS regions. The ``csd`` module now supports executing a ``CSDUP`` script against an existing ``CSD`` data set.

Major Changes
-------------

- A new ``state`` option for the ``csd`` module that alllows a user to supply a script as either a data set or a z/OS Unix file containing ``CSDUP`` commands
- Data set modules now support a ``space_secondary`` option to specify size of the secondary extent
- Return values for all data set modules now use ``data_set_organization`` to indicate the organization of the data set. The ``vsam`` field has been removed from the return structure.

New Modules
-----------

- ibm.ibm_zos_cics.start_cics - Start a CICS region
- ibm.ibm_zos_cics.stop_cics - Stop a CICS Region

v1.1.0-beta.4
=============

Release Summary
---------------

This release delivers new modules for provisioning the CICS auxiliary temporary storage data set, the CICS system definition data set, the CICS transient data intrapartition data set, the CICS auxiliary trace data sets and the CICS transaction dump data sets. This release also contains fixes to the CICS local request queue data set module and the CICS local catalog data set module.

Bugfixes
--------

- Additional ``state`` input parameter option ``warm`` added to ``local_request_queue`` module
- Behaviour of ``local_catalog`` and ``local_request_queue`` module with ``state`` set to ``initial`` updated to match documentation

New Modules
-----------

- ibm.ibm_zos_cics.auxiliary_temp - Create and remove the CICS auxiliary temporary storage data set
- ibm.ibm_zos_cics.csd - Create, remove, and manage the CICS CSD
- ibm.ibm_zos_cics.intrapartition - Create and remove the CICS transient data intrapartition data set
- ibm.ibm_zos_cics.trace - Allocate auxiliary trace data sets
- ibm.ibm_zos_cics.transaction_dump - Allocate transaction dump data sets

v1.1.0-beta.3
=============

Release Summary
---------------

This release introduces changes to the global and local catalog modules by adding support for the ``region_data_sets`` and ``cics_data_sets`` defaults groups. This changes the way you specifiy the data set location for these modules. A new ``local_request_queue`` module is also included to support provisioning a local request queue data set. 

Breaking Changes / Porting Guide
--------------------------------

- Introduction of ``region_data_sets`` and ``cics_data_sets`` defaults group

New Modules
-----------

- ibm.ibm_zos_cics.local_request_queue - Create and remove the CICS local request queue

v1.1.0-beta.2
=============

Release Summary
---------------

This release improves the return values for the ``global_catalog`` module, fixes bugs related to its input parameters, and includes a new ``local_catalog`` module for provisioning a local catalog data set.

Minor Changes
-------------

- Return values for ``global_catalog`` - changes the values returned to include ``start_state``, ``end_state``, and ``executions``.

Bugfixes
--------

- Input parameters for ``global_catalog`` failed when lowercase. Now these parameters are not case sensitive.
- The ``changed`` flag did not always correspond with actions taken during the ``global_catalog`` execution. Now this flag represents if changes were made.

New Modules
-----------

- ibm.ibm_zos_cics.local_catalog - Create, remove, and manage the CICS local catalog

v1.1.0-beta.1
=============

Release Summary
---------------

This release contains a new Global Catalog module

New Modules
-----------

- ibm.ibm_zos_cics.global_catalog - Create and initialize CICS global catalog.

v1.0.5
======

Release Summary
---------------

This release contains one bug fix

Bugfixes
--------

- Missing requirements.txt - requirements.txt was not included in the built collection. Fix removes this from the build_ignore section of the galaxy.yml.

v1.0.4
======

Release Summary
---------------

This release contains a number of new features and bug fixes.

Minor Changes
-------------

- Provide variables for all modules in one go using Ansible's `group module defaults <https://docs.ansible.com/ansible/2.8/user_guide/playbooks_module_defaults.html#module-defaults-groups>`_ support. The group name for the CMCI modules is ``cmci_group``.

Bugfixes
--------

- cmci_get - prevent ``cmci_get`` from failing if no records are found via the ``fail_on_nodata`` option. The default value is ``true`` if not specified.

v1.0.3
======

Release Summary
---------------

This release contains a number of new features and bug fixes.

Minor Changes
-------------

- Added support for CMCI feedback on failed CMCI requests.
- Updated timeout support on requests to be configurable via the timeout option. The default value is 30 seconds if not specified.

Bugfixes
--------

- Improve sanitisation and validation of parameters.

v1.0.1
======

Release Summary
---------------

Fix some documentation issues on Hub, and include some missing documentation about requirements.

v1.0.0
======

Release Summary
---------------

Initial release of the IBM® z/OS® CICS® collection, also referred to as ibm_zos_cics, which is part of the broader offering Red Hat® Ansible® Certified Content for IBM Z®.

This collection can manage CICS and CICSPlex® SM resources and definitions by calling the CMCI REST API, which can be configured in a CICSplex or in a stand-alone region.

New Modules
-----------

- ibm.ibm_zos_cics.cmci_action - Perform actions on CICS and CICSPlex SM resources
- ibm.ibm_zos_cics.cmci_create - Create CICS and CICSPlex SM definitions
- ibm.ibm_zos_cics.cmci_delete - Delete CICS and CICSPlex SM resources
- ibm.ibm_zos_cics.cmci_get - Query CICS and CICSPlex SM resources and definitions
- ibm.ibm_zos_cics.cmci_update - Update CICS and CICSPlex resources and definitions

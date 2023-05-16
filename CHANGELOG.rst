==============================
ibm.ibm_zos_cics Release Notes
==============================

.. contents:: Topics


v1.0.5
======

Release Summary
---------------

This release contains one bug fix.

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

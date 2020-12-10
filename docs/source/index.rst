.. ...........................................................................
.. © Copyright IBM Corporation 2020                                          .
.. ...........................................................................

IBM z/OS CICS collection
========================

The **IBM z/OS CICS collection**, also represented as **ibm\_zos\_cics**
in this document, provides tasks to define, install, and perform actions on CICS resources such as NEWCOPY a program or CLOSE a file, and to perform actions in the region such as request a dump or to shut down.

The **IBM z/OS CICS collection** can work independently from other IBM z/OS modules on Ansible to perform tasks in CICS. You can, however, to use it in conjunction with the `IBM z/OS core collection`_ to achieve more automation on z/OS. If you do that, always refer to their documentation for extra configuration needed.

.. _IBM z/OS core collection:
   https://github.com/ansible-collections/ibm_zos_core

Included content
================

The IBM z/OS CICS collection includes modules, sample playbooks, and ansible-doc to automate tasks against CICS resources and definitions.

Modules
-------

A table containing all modules, descriptions and their links.

Sample playbooks
----------------

A table containing all sample playbooks, descriptions and their links.


.. _action plugins:
   https://github.com/ansible-collections/ibm_zos_cics/tree/master/plugins/action/
.. _modules:
    https://github.com/ansible-collections/ibm_zos_cics/tree/master/plugins/modules/
.. _sample playbooks:
    https://github.com/ansible-collections/ibm_zos_cics/tree/master/playbooks/


Red Hat Ansible Certified Content for IBM Z
===========================================

**Red Hat® Ansible Certified Content for IBM Z** provides the ability to
connect IBM Z® to clients' wider enterprise automation strategy through the
Ansible Automation Platform ecosystem. This enables development and operations
automation on Z through a seamless, unified workflow orchestration with
configuration management, provisioning, and application deployment in one
easy-to-use platform.

**The IBM z/OS CICS collection**, as part of the broader offering
**Red Hat® Ansible Certified Content for IBM Z**, is available on Galaxy as 
community supported.



Copyright
=========

© Copyright IBM Corporation 2020

License
=======

This collection is licensed under `Apache License, Version 2.0`_.

.. _Apache License, Version 2.0:
    https://opensource.org/licenses/Apache-2.0

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   installation

.. toctree::
   :maxdepth: 3
   :caption: Reference

   modules
   playbooks

.. toctree::
   :maxdepth: 1
   :caption: Community guides

   community_guides

.. toctree::
   :maxdepth: 1
   :caption: Requirements

   requirements

.. toctree::
   :maxdepth: 1
   :caption: Appendices

   release_notes

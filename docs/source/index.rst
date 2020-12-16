.. ...............................................................................
.. © Copyright IBM Corporation 2020                                              .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

IBM z/OS CICS collection
========================
Collections are a distribution format for prepackaged Ansible content including playbooks, modules, and so on that enable you to quickly set up your automation project.

The **IBM z/OS CICS collection**, also represented as **ibm\_zos\_cics**
in this document, provides tasks to define, install, and perform actions on CICS definitions and resources such as creating a PROGRAM definition, installing and updating it, and deleting the definition.

This CICS collection can work independently from other IBM z/OS modules on Ansible to perform tasks in CICS. You can, however, to use it in conjunction with the `IBM z/OS core collection`_ to achieve more automation on z/OS. If you do that, always refer to their documentation for extra configuration needed.

.. _IBM z/OS core collection:
   https://github.com/ansible-collections/ibm_zos_core

Included content
================

The IBM z/OS CICS collection includes `modules`_, `sample playbooks`_, and ansible-doc to automate tasks against CICS resources and definitions.



.. _modules:
    https://github.com/ansible-collections/ibm_zos_cics/tree/master/plugins/modules/
.. _sample playbooks:
    https://github.com/ansible-collections/ibm_zos_cics/tree/master/playbooks/

Contributing
============

Thank you for contributing to this project.

We welcome bug reports and discussions about new function in the issue tracker, and we also welcome proposed new features or bug fixes via pull requests.

For contribution guidelines, see `How to contribute`_.

.. _How to contribute:
   https://github.com/ansible-collections/ibm_zos_cics/tree/master/CONTRIBUTING.md


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
   :caption: Requirements

   requirements

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
   :caption: Appendices

   release_notes

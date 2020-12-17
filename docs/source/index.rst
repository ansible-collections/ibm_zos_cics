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


Red Hat Ansible Certified Content for IBM Z
===========================================

**Red Hat® Ansible Certified Content for IBM Z** provides the ability to
connect IBM Z® to clients' wider enterprise automation strategy through the
Ansible Automation Platform ecosystem. This enables development and operations
automation on Z through a seamless, unified workflow orchestration with
configuration management, provisioning, and application deployment in one
easy-to-use platform.

The **The IBM z/OS CICS collection** is following the **Red Hat Ansible Certified Content for IBM Z** method of distributing content. Collections will be developed in the open, and when content is ready for use it is released to `Ansible Galaxy`_ for community adoption. Once contributors review community usage, feedback, and are satisfied with the content published, the collection will then be released to `Ansible Automation Hub`_ as certified and IBM supported for Red Hat® Ansible Automation Platform subscribers.

.. _Ansible Galaxy:
   https://galaxy.ansible.com/search?keywords=zos_&order_by=-relevance&deprecated=false&type=collection&page=1

.. _Ansible Automation Hub:
   https://www.ansible.com/products/automation-hub

Features
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

   requirements
   installation
   playbooks

.. toctree::
   :maxdepth: 1
   :caption: Ansible Content

   modules


.. toctree::
   :maxdepth: 1
   :caption: Release Notes

   release_notes


.. toctree::
   :maxdepth: 1
   :caption: Reference

   community_guides

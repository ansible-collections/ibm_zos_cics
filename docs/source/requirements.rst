.. ...............................................................................
.. © Copyright IBM Corporation 2020                                              .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

Requirements
============

The nodes listed below require these specific versions of software:

Control node
------------

A control node is any machine with Ansible installed. From the control node,
you can run commands and playbooks from a laptop, desktop, or server.

.. note:: The IBM z/OS CICS collection cannot run on a Windows system.

* `Ansible version`_: 2.9 or later
* `Python`_: 2.7 or later
* `OpenSSH`_

.. _Ansible version:
   https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
.. _Python:
   https://www.python.org/downloads/release/latest
.. _OpenSSH:
   https://www.openssh.com/


Managed node
------------

Ansible needs not be installed on a managed node, but SSH must be enabled. The CICS collection also requires a CMCI connection to either a CICSPlex SM or a stand-alone CICS region. For detailed requirements, see :doc:`requirements_managed`.


.. toctree::
   :maxdepth: 3

   requirements_managed
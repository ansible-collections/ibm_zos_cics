.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

Requirements
============

The nodes listed below require these specific versions of software:

Control node
------------

A control node is any machine with Ansible® installed. You can run commands and playbooks from a control node, be it a laptop, desktop, or server.

.. note:: The IBM® z/OS® CICS® collection cannot run on a Windows system.

The following software must be installed on the control node:

* `Ansible version`_ 2.15 or later
* `Python`_ 3.9 or later
* z/OS core collection 1.5.0 or later, if you want to use the provisioning tasks provided by the **IBM® z/OS® CICS® collection**


.. _Ansible version:
   https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
.. _Python:
   https://www.python.org/downloads/release/latest
.. _OpenSSH:
   https://www.openssh.com/
.. _CMCI REST API:
   https://www.ibm.com/docs/en/cics-ts/latest?topic=cmci-how-it-works-rest-api


Managed node
------------

For detailed requirements, see :doc:`requirements_managed`.


.. toctree::
   :maxdepth: 3

   requirements_managed
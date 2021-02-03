.. ...............................................................................
.. © Copyright IBM Corporation 2020                                              .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

Requirements
============

The nodes listed below require these specific versions of software:

Control node
------------

A control node is any machine with Ansible® installed. You can run commands and playbooks from a control noede, be it a laptop, desktop, or server. The following software must be installed on the control node.

.. note:: The IBM® z/OS® CICS® collection cannot run on a Windows system.

* `Ansible version`_: 2.9 or later
* `Python`_: 2.7 or later


.. _Ansible version:
   https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html
.. _Python:
   https://www.python.org/downloads/release/latest
.. _OpenSSH:
   https://www.openssh.com/
.. _CMCI REST API:
   https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/fundamentals/cpsm/cpsm-cmci-restfulapi-overview.html


Managed node
------------

The CMCI tasks in the IBM z/OS CICS collection interact with the managed node over an HTTP connection by leveraging the `CMCI REST API`_. Therefore, an SSH connection is not necessary. Instead, you can delegate the CMCI tasks to run on the control node directly, for example, by specifying ``delegate_to: 'localhost'`` for the tasks in the playbook. For detailed requirements, see :doc:`requirements_managed`.


.. toctree::
   :maxdepth: 3

   requirements_managed
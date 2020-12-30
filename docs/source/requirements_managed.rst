.. ...........................................................................
.. © Copyright IBM Corporation 2020                                          .
.. ...........................................................................

Requirements of managed nodes
=============================

The managed node is the host that is managed by Ansible, as identified in the Ansible inventory.

The IBM® z/OS® CICS® collection interacts with the managed node by sending HTTP requests via the `CMCI REST API`_ using a CMCI connection. Therefore, no SSH connection or Python is required on the managed node. You need, however, to delegate Ansible tasks to run on the local control node, for example, by specifying ``delegate_to: 'localhost'`` for the task in the playbook. For more ways of delegating tasks, see `Controlling where tasks run`_.

The managed node must follow these requirements to use the CICS collection:

* IBM CICS V4.2 or later
* A `CMCI connection`_ must be set up in either a CICSplex or a stand-alone CICS region

If you want to use the CICS collection in conjunction with other IBM z/OS collections, you must follow their specific requirements, for example, `IBM z/OS core managed node requirements`_.

.. _z/OS OpenSSH:
   https://www.ibm.com/support/knowledgecenter/SSLTBW_2.2.0/com.ibm.zos.v2r2.e0za100/ch1openssh.htm

.. _CMCI connection:
   https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/configuring/cmci/clientapi_setup.html

.. _CMCI REST API:
   https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/fundamentals/cpsm/cpsm-cmci-restfulapi-overview.html

.. _IBM z/OS core managed node requirements:
   https://ibm.github.io/z_ansible_collections_doc/ibm_zos_core/docs/source/requirements_managed.html
.. _Controlling where tasks run:
   https://docs.ansible.com/ansible/latest/user_guide/playbooks_delegation.html#delegating-tasks

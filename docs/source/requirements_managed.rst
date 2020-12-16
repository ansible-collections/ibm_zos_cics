.. ...........................................................................
.. © Copyright IBM Corporation 2020                                          .
.. ...........................................................................

Requirements of managed nodes
=============================

The managed z/OS node is the host that is managed by Ansible, as identified in the Ansible inventory.

The IBM z/OS CICS collection calls the `CMCI REST API`_ of CICS to perform tasks in CICS. Therefore, it doesn't require Python to be installed on the managed node when used alone.

* `z/OS OpenSSH`_
* IBM CICS V4.2 or later
* `CMCI connection`_ must be set up in either a CICSPlex SM or a stand-alone CICS region

If you want to use the CICS collection in conjunction with other IBM z/OS collections, you must follow their specific requirements, for example, `IBM z/OS core managed node requirements`_.

.. _z/OS OpenSSH:
   https://www.ibm.com/support/knowledgecenter/SSLTBW_2.2.0/com.ibm.zos.v2r2.e0za100/ch1openssh.htm

.. _CMCI connection:
   https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/configuring/cmci/clientapi_setup.html

.. _CMCI REST API:
   https://www.ibm.com/support/knowledgecenter/SSGMCP_5.6.0/fundamentals/cpsm/cpsm-cmci-restfulapi-overview.html

.. _IBM z/OS core managed node requirements:
   https://ibm.github.io/z_ansible_collections_doc/ibm_zos_core/docs/source/requirements_managed.html

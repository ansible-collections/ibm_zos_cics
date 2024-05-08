.. ...........................................................................
.. © Copyright IBM Corporation 2020,2024                                     .
.. ...........................................................................

Requirements of managed nodes
=============================

The tasks in the **IBM® z/OS® CICS® collection** can be classified into two types,
**CMCI tasks** and **provisioning tasks**, that have different requirements of the managed
node.

CMCI tasks
----------

The CMCI tasks in the **IBM® z/OS® CICS® collection** interact
with the managed node over an HTTP connection by leveraging the `CMCI REST API`_.
Therefore, an SSH connection is not required. Instead, you can delegate
Ansible tasks to run on the control node, for example, by specifying
``delegate_to: 'localhost'`` for the task in the playbook. In this case, you
install dependencies on your localhost instead of the managed node.
For more ways of delegating tasks, see `Controlling where tasks run`_.

The requirements of the managed node are as follows:

* z/OS Version 2.3 or later
* All IBM CICS TS releases that are in service
* A `CMCI connection`_ must be set up in either a CICSplex or a stand-alone CICS region
* Python module dependencies:

  * `requests`_
  * `xmltodict`_

  If you delegate the tasks to run on your localhost, the Python module dependencies
  need to be installed on your localhost instead.

  You can install them from the CLI by using the following command:

  .. code-block:: sh

     pip install requests xmltodict

  You can also install them using the playbook. For example, this `CICS
  sample playbook`_ shows how you can ensure that the prerequisites are installed before the module is executed.

.. _requests:
   https://pypi.org/project/requests/

.. _xmltodict:
   https://pypi.org/project/xmltodict/
.. _CICS sample playbook:
   https://github.com/IBM/z_ansible_collections_samples/tree/main/zos_subsystems/cics/cmci/reporting

If you use the CMCI tasks in the CICS collection but don't delegate the CMCI tasks to your localhost, your
managed node must also follow the `IBM z/OS core managed node requirements`_ except that IBM Z Open Automation Utilities (ZOAU) is not required.

.. _z/OS OpenSSH:
   https://www.ibm.com/docs/en/zos/latest?topic=descriptions-zos-openssh

.. _CMCI connection:
   https://www.ibm.com/docs/en/cics-ts/latest?topic=configuring-setting-up-cmci

.. _CMCI REST API:
   https://www.ibm.com/docs/en/cics-ts/latest?topic=cmci-how-it-works-rest-api

.. _IBM z/OS core managed node requirements:
   https://ibm.github.io/z_ansible_collections_doc/ibm_zos_core/docs/source/requirements_managed.html
.. _Controlling where tasks run:
   https://docs.ansible.com/ansible/latest/user_guide/playbooks_delegation.html#delegating-tasks


Provisioning tasks
------------------

The provisioning tasks in the **IBM® z/OS® CICS® collection** interact with a
z/OS managed node over SSH, and therefore have different requirements to the
CMCI tasks. The provisioning modules follow the requirements of the other z/OS
collections as documented in `IBM z/OS core managed node requirements`_. These
requirements include installation of the following components:

* z/OS Version 2.3 or later
* z/OS OpenSSH
* IBM Open Enterprise SDK for Python (previously IBM Open Enterprise Python for z/OS)
* IBM Z Open Automation Utilities (ZOAU) 1.2.x
* The z/OS shell

For specific versions of these dependencies and additional information, review
the `IBM z/OS core managed node requirements`_ page.

Note that you must have z/OS core collection 1.5.0 or later installed in the control node
if you want to run the provisioning tasks.

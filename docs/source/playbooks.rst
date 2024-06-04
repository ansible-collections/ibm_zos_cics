.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

Playbooks
=========

There are sample playbooks that demonstrate the **IBM z/OS CICS collection**
functionality in the `samples repository`_.

The sample playbooks fall into two categories:

- Operations on CICS and CICSPlex SM resources and definitions. The sample playbooks use the CMCI modules to achieve various real-life use cases.
- CICS provisioning. The sample playbook demonstrates how a set of modules for provisioning and managing CICS TS data sets and utilities can be used to provision, start, stop, and deprovision a CICS region.

.. _samples repository:
   https://github.com/IBM/z_ansible_collections_samples



Playbook Documentation
----------------------

An `Ansible playbook`_ consists of organized instructions that define work for
a managed node (host) to be managed with Ansible.

`Samples`_ that contains multiple example playbooks are included in the
`Ansible Z playbook repository`_. The sample playbooks are for reference and can be run
with the ``ansible-playbook`` command with some modification to their **inventory**,
**ansible.cfg** and **group_vars** as well as updates to their module parameters
to reference your CICS artifacts and configuration.

You can find the playbook content that is included with the collection in the
same location where the collection is installed. For more information, refer to
the `installation documentation`_. In the following examples, this document
refers to the installation path as ``~/.ansible/collections/ibm/ibm_zos_cics``.


.. _Ansible playbook:
   https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#playbooks-intro
.. _Samples:
   https://github.com/IBM/z_ansible_collections_samples/tree/main/zos_subsystems/cics
.. _Ansible Z playbook repository:
   https://github.com/IBM/z_ansible_collections_samples
.. _installation documentation:
   installation.html



Sample Configuration and Setup
------------------------------
Each release of Ansible provides options in addition to the ones identified in
the sample configurations that are included with this collection. These options
allow you to customize how Ansible operates in your environment. Ansible
supports several sources to configure its behavior and all sources follow the
Ansible `precedence rules`_.

The Ansible configuration file ``ansible.cfg`` can override almost all
``ansible-playbook`` configurations.

You can specify the SSH port used by Ansible and instruct Ansible where to
write the temporary files on the target. This can be easily done by adding the
options to your inventory or ``ansible.cfg``.

An example of adding these options to ``ansible.cfg`` is shown below.

.. code-block:: yaml

   [defaults]
   forks = 25
   remote_tmp = /u/ansible/tmp
   remote_port = 2022

For more information about available configurations for ``ansible.cfg``, read
the Ansible documentation on `Ansible configuration settings`_.

.. _Ansible configuration settings:
   https://docs.ansible.com/ansible/latest/reference_appendices/config.html#ansible-configuration-settings-locations
.. _precedence rules:
   https://docs.ansible.com/ansible/latest/reference_appendices/general_precedence.html#general-precedence-rules



Inventory
---------

Ansible works with multiple managed nodes (hosts) at the same time, using a
list or group of lists known as an `inventory`_. After the inventory is defined,
you can use `patterns`_ to select the hosts or groups that you want Ansible to
run against.

Included in the CICS `deploy program sample`_ is an example `inventory file`_,
which shows how host information is supplied to Ansible. Code that defines a host
is shown below:

.. code-block:: yaml

   source_system:
     hosts:
       zos_host:
         ansible_host: zos_target_address
         ansible_user: zos_target_username
         ansible_python_interpreter: path_to_python_interpreter_binary_on_zos_target

A host is defined by the following properties:

- **ansible_host**: The value of this property identifies the hostname of the managed node. For example: ``ansible_host: example.com``
- **zos_target_username**: The value of this property identifies the user name to use when connecting to the host. For example: ``ansible_user: ibmuser``
- **ansible_python_interpreter**: The value of this property specifies the Python path for the target host. For example: ``ansible_python_interpreter: /usr/lpp/rsusr/python39/bin/python``
  This is useful for systems with more than one Python installation, or when Python is not installed in the default location **/usr/bin/python**.

For more information about the Python configuration requirements on z/OS, see the Ansible `FAQ`_.

For behavioral inventory parameters such as ``ansible_port`` which allows you to set the port for a host, see `behavioral inventory parameters`_.

.. _inventory:
   https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html
.. _patterns:
   https://docs.ansible.com/ansible/latest/user_guide/intro_patterns.html#intro-patterns
.. _deploy program sample:
   https://github.com/IBM/z_ansible_collections_samples/blob/main/zos_subsystems/cics/cmci/deploy_program
.. _inventory file:
   https://github.com/IBM/z_ansible_collections_samples/blob/main/zos_subsystems/cics/cmci/deploy_program/inventory.yml
.. _FAQ:
   https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#running-on-z-os
.. _behavioral inventory parameters:
   https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#connecting-to-hosts-behavioral-inventory-parameters



Group_vars
----------

Although you can store variables in the inventory file, storing separate host
and group variables files may help you organize your variable values more
easily. An example of one of these variable files is the `zos_host.yml`_
file included with the `deploy_program sample`_, which is used to provide the
required environment variables. Another such example is the `variables.yml`_ file
included with the `CICS provisioning`_ playbook.

The properties that define the environment variables are as follows:

- **BPXK_AUTOCVT**: The value must be ``ON``.
- **ZOAU_HOME**: The value of this property identifies the ZOA Utilities install root path. For example: ``/usr/lpp/IBM/zoautil``
- **PYTHONPATH**: The value of this property identifies the ZOA Utilities Python library path. For example: ``/usr/lpp/IBM/zoautil/lib/``
- **LIBPATH**: The value of this property specifies both the path to the Python libraries on the target and the ZOA Utilities Python library path, separated by colons ``:``. For example: ``/usr/lpp/IBM/zoautil/lib/:/usr/lpp/rsusr/python39/lib:/lib:/usr/lib:.``
- **PATH**: The value of this property identifies the ZOA utilities BIN path and the Python interpreter path, separated by colons ``:``. For example: ``/usr/lpp/IBM/zoautil/bin:/usr/lpp/rsusr/python39/bin/python:/bin``

.. code-block:: yaml

   environment_vars:
      _BPXK_AUTOCVT: ON
      ZOAU_HOME: '/usr/lpp/IBM/zoautil'
      PYTHONPATH: '/usr/lpp/IBM/zoautil/lib'
      LIBPATH: '/usr/lpp/IBM/zoautil/lib/:/usr/lpp/rsusr/python39/lib:/usr/lib:/lib:.'
      PATH: '/usr/lpp/IBM/zoautil/bin:/usr/lpp/rsusr/python39/bin/python:/bin'

.. note::
   In ZOAU 1.0.2 and later, the property **ZOAU_ROOT** is no longer supported
   and can be replaced with the property **ZOAU_HOME**. If you are using ZOAU
   version 1.0.1 or lower, you must continue to use the property
   **ZOAU_ROOT** which is the ZOA Utilities install root path required for
   ZOAU; for example, ``/usr/lpp/IBM/zoautil``.

.. _zos_host.yml:
   https://github.com/IBM/z_ansible_collections_samples/blob/main/zos_subsystems/cics/cmci/deploy_program/host_vars/zos_host.yml
.. _deploy_program sample:
   https://github.com/IBM/z_ansible_collections_samples/blob/main/zos_subsystems/cics/cmci/deploy_program
.. _variables.yml:
   https://github.com/IBM/z_ansible_collections_samples/blob/main/zos_subsystems/cics/provisioning/host_vars/variables.yml
.. _CICS provisioning:
   https://github.com/IBM/z_ansible_collections_samples/tree/main/zos_subsystems/cics/provisioning



Module Defaults
---------------

Ansible has a module defaults feature to use the same values during every use of
a module, rather than repeating them everytime.

For example, when using CMCI modules to manage CICS and CICSPlex SM resources and definitions, you can set the host url and
credentials of the **cmci_get** module to be the same throughout the playbook.

.. code-block:: yaml

   module_defaults:
     ibm.ibm_zos_cics.cmci_get:
       cmci_host: "{{ cmci_host }}"
       cmci_user: "{{ cmci_user }}"
       cmci_password: "{{ cmci_password }}"


If you want to use the same values in **all** CMCI modules, you can assign them
to the group called **cmci_group**.

.. code-block:: yaml

   module_defaults:
     group/ibm.ibm_zos_cics.cmci_group:
       cmci_host: "my.system.host"
       cmci_port: "system.port.number"
       cmci_user: "my.username"
       cmci_password: "my.password"


Likewise, you can easily apply a default set of CICS TS data sets and utilities for the provisioning or de-provisioning of CICS regions.
If you want to use the same values in **all** CICS TS data set provisioning modules, you can assign them to the group called **region_group**.
For example, the following **module_defaults** example indicates that the SDFHLOAD library of the CICS installation is created by default using the templated location of
``CTS610.CICS740.<< data_set_name >>``, and the region data sets are to be created by using the templated location of ``{{ansible_user}}.REGIONS.{{applid}}.<< data_set_name >>``.

.. code-block:: yaml

   module_defaults:
     group/ibm.ibm_zos_cics.region_group:
       state: initial
       cics_data_sets:
         template: "CTS610.CICS740.<< data_set_name >>"
       region_data_sets:
         template: "{{ansible_user}}.REGIONS.{{applid}}.<< data_set_name >>"


.. note::
   Group module defaults are only available in ``ansible-core`` 2.12 or later. If
   this syntax is used with ``ansible-core`` 2.11 or earlier, the values are
   perceived as not present, and a 'missing required arguments' error is thrown.



Run the playbook
----------------

Access the `collection samples repository`_ and ensure you have navigated to
the directory containing the playbook you want to run. For example:
``zos_subsystems/cics/cmci/deploy_program/``.

Use the Ansible command ``ansible-playbook`` to run the sample playbook.  The
command syntax is ``ansible-playbook -i <inventory> <playbook>`` which, using
the example above of ``deploy_program``, is
``ansible-playbook -i inventory deploy_program.yaml``.

This command assumes that the controller's public SSH key has been shared with
the managed node. If you want to avoid entering a username and password each
time, copy the SSH public key to the managed node using the ``ssh-copy-id``
command; for example, ``ssh-copy-id -i ~/.ssh/mykey.pub user@<hostname>``.

Alternatively, you can use the ``--ask-pass`` option to be prompted for the
user's password each time a playbook is run; for example,
``ansible-playbook -i inventory deploy_program.yaml --ask-pass``.

.. note::
   * Using ``--ask-pass`` is not recommended because it will hinder performance.
   * Using ``--ask-pass`` requires ``sshpass`` be installed on the controller.
     For further reference, see the `ask-pass documentation`_.

Optionally, you can configure the console logging verbosity during playbook
execution. This is helpful in situations where communication is failing and
you want to obtain more details. To adjust the logging verbosity, append more
letter `v`'s; for example, `-v`, `-vv`, `-vvv`, or `-vvvv`. Each letter `v`
increases logging verbosity similar to traditional logging levels INFO, WARN,
ERROR, DEBUG.

.. note::
   It is a good practice to review the playbook samples before executing them.
   It will help you understand what requirements in terms of space, location,
   names, authority, and artifacts will be created and cleaned up. Although
   samples are always written to operate without the need for the user's
   configuration, flexibility is written into the samples because it is not
   easy to determine if a sample has access to the host's resources.
   Review the playbook notes sections for additional details and
   configuration.

   Playbooks often submit JCL that is included in the samples repository
   under the `files directory`_. Review the sample JCL for necessary edits to
   allow for submission on the target system. The most common changes are to
   add a CLASS parameter and change the NOTIFY user parameter. For more details,
   see the JCL notes section included in the collection.

.. _ask-pass documentation:
   https://linux.die.net/man/1/sshpass
.. _collection samples repository:
   https://github.com/IBM/z_ansible_collections_samples
.. _files directory:
   https://github.com/IBM/z_ansible_collections_samples/tree/main/zos_basics/constructs/files

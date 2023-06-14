.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

Playbooks
=========

There are sample playbooks that demonstrate the **IBM z/OS CICS collection**
functionality in the `samples repository`_.

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
the `installation documentation`_. In the following examples, this document will
refer to the installation path as ``~/.ansible/collections/ibm/ibm_zos_cics``.


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
list or group of lists known as an `inventory`_. Once the inventory is defined,
you can use `patterns`_ to select the hosts or groups that you want Ansible to
run against.

Included in the CICS `deploy program sample`_ is an example `inventory file`_
which shows how host information is supplied to Ansible. It looks like the 
following:

.. code-block:: yaml

   source_system:
     hosts:
       zos_host:
         ansible_host: zos_target_address
         ansible_user: zos_target_username
         ansible_python_interpreter: path_to_python_interpreter_binary_on_zos_target


The value for the property **ansible_host** is the hostname of the managed node;
for example, ``ansible_host: ec33017A.vmec.svl.ibm.com``

The value for the property **zos_target_username** is the user name to use when
connecting to the host; for example, ``ansible_user: omvsadm``.

The value for the property **ansible_python_interpreter** is the target host
Python path. This is useful for systems with more than one Python installation,
or when Python is not installed in the default location **/usr/bin/python**;
for example, ``ansible_python_interpreter: /usr/lpp/rsusr/python36/bin/python``

For more information on Python configuration requirements on z/OS, refer to
Ansible `FAQ`_.

Behavioral inventory parameters such as ``ansible_port`` which allows you
to set the port for a host can be reviewed in the
`behavioral inventory parameters`_.

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
required environment variables.

The value for the property **BPXK_AUTOCVT** must be configured to ``ON``.

The value for the property **ZOAU_HOME** is the ZOA Utilities install root path;
for example, ``/usr/lpp/IBM/zoautil``.

The value for the property **PYTHONPATH** is the ZOA Utilities Python library
path; for example, ``/usr/lpp/IBM/zoautil/lib/``.

The value for the property **LIBPATH** is both the path to the Python libraries
on the target and the ZOA Utilities Python library path separated by
colons ``:``; for example,
``/usr/lpp/IBM/zoautil/lib/:/usr/lpp/rsusr/python36/lib:/lib:/usr/lib:.``.

The value for the property **PATH** is the ZOA utilities BIN path and the Python
interpreter path; for example,
``/usr/lpp/IBM/zoautil/bin:/usr/lpp/rsusr/python36/bin/python:/bin``.

The included sample variables file (zos_host.yml) contains variables specific to
the playbook as well as the following:

.. code-block:: yaml

   environment_vars:
      _BPXK_AUTOCVT: ON
      ZOAU_HOME: '/usr/lpp/IBM/zoautil'
      PYTHONPATH: '/usr/lpp/IBM/zoautil/lib'
      LIBPATH: '/usr/lpp/IBM/zoautil/lib/:/usr/lpp/rsusr/python36/lib:/usr/lib:/lib:.'
      PATH: '/usr/lpp/IBM/zoautil/bin:/usr/lpp/rsusr/python36/bin/python:/bin'

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



Module Defaults
---------------

Ansible has a module defaults feature to use the same values during every use of
a module, rather than repeating them everytime. Here we can set the host url and
credentials of the **cmci_get** module to be the same throughout the playbook.

.. code-block:: yaml

   module_defaults:
     ibm.ibm_zos_cics.cmci_get:
       cmci_host: "{{ cmci_host }}"
       cmci_user: "{{ cmci_user }}"
       cmci_password: "{{ cmci_password }}"


If you wish to use the same values in **all** CMCI modules, you can assign them
to the group called **cmci_group**.

.. code-block:: yaml

   module_defaults:
     group/ibm.ibm_zos_cics.cmci_group:
       cmci_host: "my.system.host"
       cmci_port: "system.port.number"
       cmci_user: "my.username"
       cmci_password: "my.password"

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

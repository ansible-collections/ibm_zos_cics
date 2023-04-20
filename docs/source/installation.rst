.. ...............................................................................
.. © Copyright IBM Corporation 2020,2023                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

Installation
============
Always check that your control node has fulfilled the :doc:`requirements` before installing the **IBM® z/OS® CICS® collection**.

Then, follow the guidance to install the collection from Ansible® Galaxy or a custom Galaxy server. More ways to install an Ansible collection are documented at `installing collections`_.


Installing from Ansible Galaxy
------------------------------
This is the quickest way to install the CICS collection. From your CLI, enter:

.. code-block:: sh

   $ ansible-galaxy collection install ibm.ibm_zos_cics


..
   Comment: Will need to add something about overwriting previous versions when we have multiple versions. If you have installed a prior version, overwrite the existing collection with the ``--force`` (or ``-f``) option. Also, how to install a previous version, including beta.

By default, collections are installed in ``~/.ansible/collections``. After installation, the collection content will resemble this hierarchy: :

.. code-block:: sh

   ├── collections/
   │  ├── ansible_collections/
   │      ├── ibm/
   │          ├── ibm_zos_cics/
   │              ├── docs/
   │              ├── plugins/
   │                  ├── action/
   │                  ├── module_utils/
   │                  ├── modules/



To install with customization, such as specifying another installation path or using a playbook, see `installing collections`_.

.. _installing collections:
   https://docs.ansible.com/ansible/latest/user_guide/collections_using.html#installing-collections-with-ansible-galaxy


Installing from a custom Galaxy server
----------------------------------------
By default, the ``ansible-galaxy`` command is configured to access
`https://galaxy.ansible.com`_ as the server when you install a
collection. The ``ansible-galaxy`` client can be configured to point to other servers, such as a privately running Galaxy server, by configuring the server list in the ``ansible.cfg`` file.

Ansible searches for ``ansible.cfg`` in the following locations in this order:

   * ANSIBLE_CONFIG (environment variable if set)
   * ansible.cfg (in the current directory)
   * ~/.ansible.cfg (in the home directory)
   * /etc/ansible/ansible.cfg

Instructions on how to configure the server list in ``ansible.cfg`` can be found at `configuring the ansible-galaxy client`_. Available options in the Ansible configuration file can be found at `Ansible Configuration Settings`_.

.. note:: When hosting a private Galaxy server, available content is not always consistent with what is available on the community Galaxy server.

.. _https://galaxy.ansible.com:
   https://galaxy.ansible.com

.. _configuring the ansible-galaxy client:
   https://docs.ansible.com/ansible/latest/user_guide/collections_using.html#configuring-the-ansible-galaxy-client

.. _Ansible configuration Settings:
   https://docs.ansible.com/ansible/latest/reference_appendices/config.html



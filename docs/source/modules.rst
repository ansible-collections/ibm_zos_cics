.. ...............................................................................
.. © Copyright IBM Corporation 2020,2021                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

Modules
=======

Modules can be used in a playbook to automate tasks. Ansible® executes each
module on the target node and returns the result back to the controller.

The **IBM® z/OS® CICS® collection** provides two categories of modules:

* Modules for working with CICS and CICSPlex SM resources and definitions.
  These modules interact with CMCI over an HTTP connection by leveraging
  the `CMCI REST API`_. These modules are collectively referred to as
  **CMCI modules** in documentation.
* Modules for provisioning and deprovisioning of CICS TS regions and for
  CICS startup and shutdown operations. These modules are collectively
  referred to as CICS **provisioning modules** in documentation.

These modules have different requirements of the managed node. For details, see :doc:`requirements_managed`.

.. _CMCI REST API:
   https://www.ibm.com/docs/en/cics-ts/latest?topic=cmci-how-it-works-rest-api


Using Defaults Groups in CICS Provisioning Modules
---------------

The CICS provisioning modules use several defaults groups. In particular, these two defaults groups are used for specific purposes:

* ``cics_data_sets`` can be used to specify the location of a CICS installation.
* ``region_data_sets`` can be used to specify a high level qualifier for the data sets used by a single CICS region.

The example below shows how to use these default groups within the **global_catalog** module.

.. code-block:: yaml+jinja


    - name: Initialize a global catalog
      ibm.ibm_zos_cics.global_catalog:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        state: "initial"


In the above example, the global catalog is created at the data set location of ``REGIONS.ABCD0001.DFHGCD``,
and the CICS load libraries can be found at ``CICSTS61.CICS``, which means that the SDFHLOAD library can be
found at ``CICSTS61.CICS.SDFHLOAD``.

These groups can be placed in a `module_defaults`_ section, which means that all 
the CICS provisioning modules use the same high level qualifier for the 
region data sets, and the location of the CICS installation only has to be 
declared once for all the modules.

To override the data set location or name for a specific task, you can provide an 
additional parameter to the ``region_data_sets`` group as shown in the example 
for a global catalog data set below.

N.B. There is a known limitation with ansible-core version 2.15.0 and 2.15.1, where the custom templating may fail.

.. code-block:: yaml+jinja


    - name: Initialize a global catalog with a custom name
      ibm.ibm_zos_cics.global_catalog:
        region_data_sets:
          dfhgcd:
            dsn: "MY.CICS.GLOBAL.CATALOG"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        state: "initial"


.. _module_defaults:
    https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_module_defaults.html


Module Reference
---------------

The **IBM® z/OS® CICS® collection** contains these modules. For each module,
the accepted parameters, return values, and examples are provided in the
documentation.

.. toctree::
   :maxdepth: 1
   :glob:

   modules/*

.. ...............................................................................
.. © Copyright IBM Corporation 2020,2021                                         .
.. Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)  .
.. ...............................................................................

Modules
=======

Modules can be used in a playbook to automate tasks. Ansible® executes each
module on the target node and returns the result back to the controller.

The **IBM® z/OS® CICS® collection** provides modules for interacting with CMCI 
over an HTTP connection by leveraging the `CMCI REST API`_, as well as modules
to automate provisioning of a CICS TS region. These modules have different 
requirements of the managed node. For more detail see :doc:`requirements_managed`.

.. _CMCI REST API:
   https://www.ibm.com/docs/en/cics-ts/latest?topic=cmci-how-it-works-rest-api

The region provisioning modules make use of two defaults groups that allow a 
user to specify the location of a CICS installation and a high level qualifier 
for all region data sets to be created under. The example below shows how to 
use these default groups within the *cics_global_catalog* module.

.. code-block:: yaml+jinja


    - name: Initialize a global catalog
      ibm.ibm_zos_cics.global_catalog:
        region_data_sets:
          template: "REGIONS.ABCD0001.<< data_set_name >>"
        cics_data_sets:
          template: "CICSTS61.CICS.<< lib_name >>"
        state: "initial"


In the above example the global catalog will be created at the data set location 
*REGIONS.ABCD0001.DFHGCD* and the CICS load libraries can be found at the 
location *CICSTS61.CICS*, meaning the library SDFHLOAD could be found at 
*CICSTS61.CICS.SDFHLOAD*.

These groups can be placed in a `module_defaults`_ section meaning all 
the CICS provisioning modules will use the same high level qualifier for the 
regions data sets, and the location of the CICS installation only has to be 
declared once for all the modules.

To override a specific task's data set location and/or name you can provide an
additional parameter to the ``region_data_sets`` group as shown in the example 
for a global catalog data set below.

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

The **IBM® z/OS® CICS® collection** contains these modules. For each module,
the accepted parameters, return values, and examples are provided in the
documentation.

.. toctree::
   :maxdepth: 1
   :glob:

   modules/*

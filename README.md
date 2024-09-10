# IBM z/OS CICS collection

The **IBM® z/OS® CICS® collection**, also represented as **ibm\_zos\_cics**
in this document, is part of the broader initiative to bring Ansible Automation to IBM Z® through the offering
**Red Hat® Ansible Certified Content for IBM Z®**. The **IBM z/OS CICS collection** supports management of CICS
resources and definitions through the CMCI REST API provided by CICS as well as provisioning of standalone CICS regions.

This CICS collection works in conjunction with other Ansible collections for IBM Z,
such as the [IBM z/OS core collection](https://github.com/ansible-collections/ibm_zos_core).
It is also possible to use it independently to perform automation tasks solely in CICS.


## Red Hat Ansible Certified Content for IBM Z

**Red Hat® Ansible Certified Content for IBM Z** provides the ability to
connect IBM Z® to clients' wider enterprise automation strategy through the
Ansible Automation Platform ecosystem. This enables development and operations
automation on Z through a seamless, unified workflow orchestration with
configuration management, provisioning, and application deployment in
one easy-to-use platform.

The **IBM z/OS CICS collection** is following the
**Red Hat® Ansible Certified Content for IBM Z®** method of distributing
content. Collections will be developed in the open, and when content is ready
for use it is released to
[Ansible Galaxy](https://galaxy.ansible.com/search?keywords=zos_&order_by=-relevance&deprecated=false&type=collection&page=1)
for community adoption. Once contributors review community usage, feedback,
and are satisfied with the content published, the collection will then be
released to [Ansible Automation Hub](https://www.ansible.com/products/automation-hub)
as **certified** and **IBM supported** for
**Red Hat® Ansible Automation Platform subscribers**. 


For guides and reference, please review the [documentation](https://ibm.github.io/z_ansible_collections_doc/index.html).

## Features

The IBM CICS collection includes
[modules](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_cics/docs/source/modules.html),
[sample playbooks](https://github.com/IBM/z_ansible_collections_samples),
and ansible-doc to:

- Automate tasks in CICS.
- Provision or deprovision CICS regions.
- Start or stop a CICS region.

## Requirements

The tasks in the IBM® z/OS® CICS® collection can be classified into two types, CMCI tasks and provisioning tasks, that have different requirements of the managed node.

The CMCI tasks in the IBM® z/OS® CICS® collection interact with the managed node over an HTTP connection by leveraging the CMCI REST API. Therefore, an SSH connection is not required. Instead, you can delegate Ansible tasks to run on the control node, for example, by specifying delegate_to: 'localhost' for the task in the playbook. In this case, you install dependencies on your localhost instead of the managed node.

The requirements of the managed node for **CMCI tasks** are as follows:

 * z/OS Version 2.3 or later

 * All IBM CICS TS releases that are in service

 * A CMCI connection must be set up in either a CICSplex or a stand-alone CICS region

 * Python module dependencies:

   * requests

   * xmltodict


The **provisioning tasks** in the IBM® z/OS® CICS® collection interact with a z/OS managed node over SSH, and therefore have different requirements to the CMCI tasks. 
The requirements include installation of the following components

 * z/OS Version 2.3 or later

 * z/OS OpenSSH

 * IBM Open Enterprise SDK for Python (previously IBM Open Enterprise Python for z/OS)

 * IBM Z Open Automation Utilities (ZOAU) 1.2.x

 * The z/OS shell
   
Note that you must have z/OS core collection 1.5.0 to 1.9.2 installed in the control node if you want to run the provisioning tasks.

For more details on the different requirements, please see [here](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_cics/docs/source/requirements_managed.html).


  
## Installation

You can install this collection with the Ansible Galaxy command-line tool:
```sh
ansible-galaxy collection install ibm.ibm_zos_cics
```


You can also include it in a requirements.yml file and install it with ansible-galaxy collection install -r requirements.yml, using the format:
```sh
collections:
  - name: ibm.ibm_zos_cics
```


To install a specific version of the collection or upgrade an an existing installation to a specific version, for example installing 2.1.0, use the following syntax:
```sh
ansible-galaxy collection install ibm.ibm_zos_cics:2.1.0
```


If you want to upgrade the collection to the latest version, you can run:
```sh
ansible-galaxy collection install ibm.ibm_zos_cics --upgrade
```

As part of the installation, the collection requirements must be made available to Ansible through the use of environment variables. The preferred configuration is to place the environment variables in group_vars and host_vars. An example of the variables file can be seen here:


```sh
pyz: "path_to_python_installation_on_zos_target"
zoau: "path_to_zoau_installation_on_zos_target"

environment_vars:
  _BPXK_AUTOCVT: "ON"
  ZOAU_HOME: "{{ zoau }}"
  PYTHONPATH: "{{ zoau }}/lib"
  LIBPATH: "{{ zoau }}/lib:{{ pyz }}/lib:/lib:/usr/lib:."
  PATH: "{{ zoau }}/bin:{{ pyz }}/bin:/bin:/var/bin"
  _CEE_RUNOPTS: "FILETAG(AUTOCVT,AUTOTAG) POSIX(ON)"
  _TAG_REDIR_ERR: "txt"
  _TAG_REDIR_IN: "txt"
  _TAG_REDIR_OUT: "txt"
  LANG: "C"
```

## Use Cases

* Use Case Name: Provision a standalone CICS region 
  * Actors:
    * System Programmer
  * Description:
    * A system programmer can provision a set of region data sets and start up a standalone CICS region.
  * Flow:
    * Create and activate a VTAM node to ensure user had a valid applid
    * Create region data sets
    * Update the CSD data set with a CSDUP script
    * Create CICS startup JCL data set
    * Submit the CICS startup JCL data set as a job using zoau's jsub.
* Use Case Name: Deprovision a standalone CICS region
  * Actors:
    * System Programmer
  * Description:
    * A system programmer can stop a standalone cics region and delete the region data sets.
  * Flow:
    * Stop the CICS region
    * Check the CICS region has been shut down
    * If it has not stopped, shut the region down with state "immediate" or cancel the job.
    * Delete the region data sets
    * Delete the CICS startup JCL data set
* Use Case Name: Provision an SMSS CICS region
  * Actors:
    * System Programmer
  * Description:
    * A system programmer can start a SMSS CICS region.
  * Flow:
    * Create and activate a VTAM node to ensure user had a valid applid
    * Ensure user has an allocated/free port available
    * Create region data sets
    * Update the CSD data with a CSDUP script which also alters the TCPIP service
    * Create CICS startup JCL data set
    * Submit the CICS startup JCL data set as a job using zoau's jsub task
 * Use Case Name: Install a bundle in a CICS region
  * Actors:
    * Application Developer
  * Description:
    * An application developer can install a CICS bundle into a CICS region
  * Flow:
    * Find if the CICS bundle already exists in target region
    * Disable and discard existing CICS bundle
    * Install bundle definition into target region
    * Wait for bundle to reach enabled status
 * Use Case Name: Deploy a program to a CICS region
  * Actors:
    * Application Developer
  * Description:
    * An application developer can deploy a program to a CICS region
  * Flow:
    * Copy load module to load library
    * Use NEWCOPY PROGRAM to deploy program into CICS

## Release Notes and Roadmap

The collection's cumulative release notes can be reviewed [here](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_cics/docs/source/release_notes.html).

<br/>The collection's changelogs can be reviewed in the following table.

| Version  | Status         | Release notes | Changelogs |
|----------|----------------|---------------|------------|
| 2.1.1  | In development | unreleased    | unreleased |
| 2.1.0   | Released       | [Release notes](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_cics/docs/source/release_notes.html#version-2-1-0)    | [Changelogs](https://github.com/ansible-collections/ibm_zos_cics/blob/v2.1.0/CHANGELOG.rst)  |
| 2.0.x    | Released       | [Release notes](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_cics/docs/source/release_notes.html#version-2-0-0)    | [Changelogs](https://github.com/ansible-collections/ibm_zos_cics/blob/v2.0.0/CHANGELOG.rst)  |
| 1.0.x    | Released       | [Release notes](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_cics/docs/source/release_notes.html#version-1-0-6)    | [Changelogs](https://github.com/ansible-collections/ibm_zos_cics/blob/v1.0.6/CHANGELOG.rst)  |


## Related Information 

Example playbooks and use cases can be be found in the [z/OS playbook repository](https://github.com/IBM/z_ansible_collections_samples).
Supplemental content on getting started with Ansible, architecture and use cases is available [here](https://ibm.github.io/z_ansible_collections_doc/reference/helpful_links.html).

## Contributing

We welcome contributions! Find out how in our [contribution guide](https://github.com/ansible-collections/ibm_zos_cics/blob/main/CONTRIBUTING.md).

## Copyright 

© Copyright IBM Corporation 2021, 2024.

## License

This collection is licensed under the [Apache License,
Version 2.0](https://opensource.org/licenses/Apache-2.0).

IBM z/OS CICS collection
========================

The **IBM z/OS CICS collection**, also represented as **ibm\_zos\_cics**
in this document, is part of the broader offering **Red Hat® Ansible
Certified Content for IBM Z**. The IBM z/OS CICS collection supports tasks
such as operating cics resources, operating cics csd, initialize cics catalog,
process cics catalog.

The **IBM z/OS CICS collection** works closely with offerings such as the 
[IBM z/OS core collection](https://github.com/ansible-collections/ibm_zos_core) 
to deliver a solution that will enable you to automate tasks on z/OS.

Red Hat Ansible Certified Content for IBM Z
===========================================

**Red Hat® Ansible Certified Content for IBM Z** provides the ability to
connect IBM Z® to clients\' wider enterprise automation strategy through
the Ansible Automation Platform ecosystem. This enables development and
operations automation on Z through a seamless, unified workflow
orchestration with configuration management, provisioning, and
application deployment in one easy-to-use platform.

**The IBM z/OS CICS collection**, as part of the broader offering
**Red Hat® Ansible Certified Content for IBM Z**, is available on Galaxy as 
community supported.

For **guides** and **reference**, please visit [the documentation
site](https://ansible-collections.github.io/ibm_zos_cics/).

Features
========

The IBM CICS collection includes
[modules](https://github.com/ansible-collections/ibm_zos_cics/tree/master/plugins/modules/),
[sample playbooks](https://github.com/ansible-collections/ibm_zos_cics/tree/master/playbooks/),
and ansible-doc to automate tasks on CICS.

Copyright
=========

© Copyright IBM Corporation 2020

License
=======

This collection is licensed under [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0).

```
# Create a new venv called env
python3 -m venv env

# Activate env
source env/bin/activate

# Install requirements
pip install -r requirements.txt`
```

```
# Run unit tests
pytest tests/unit
```

```
Integration tests
You have to clone into {...}/ansible_collections/ibm/ibm_zos_cics to be able to run the test using ansible-test
See this issue: https://github.com/ansible/ansible/issues/60215

ansible-test integration cics_cmci --python=3.8
```
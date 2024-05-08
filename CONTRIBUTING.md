# (c) Copyright IBM Corp. 2020,2023
# Developer guide

### Licensing

All code must have an Apache-2.0 header.

### Signing your contribution

You must declare that you wrote the code that you contribute, or that you have the right to contribute someone else's code. To do so, you must sign the [Developer Certificate of Origin](https://developercertificate.org) (DCO):

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
1 Letterman Drive
Suite D4700
San Francisco, CA, 94129

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```


If you can certify the above, then sign off each Git commit at the bottom of the commit message with the following:

```
Signed-off-by: My Name <my.name@example.com>
```

You must use your real name and email address.

To save you having to type the above for every commit, Git can add the `Signed-off-by` line. When committing, add the `-s` option to your `git commit` command.

If you haven't signed each commit, then the pull request will fail to pass all checks.

# Development Environment Set-Up Instructions
=============================================

This repository contains an Ansible collection, which is tested using `ansible-test`.  This combination of development
tooling requires you to clone the repository to a pretty specific path.  As an example, clone the repository to:

```
.../ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics
```

`ansible-test` requires your project to exist in a FQCN-compatible folder structure following the Ansible Collections
conventions.  For details, see [this issue](https://github.com/ansible/ansible/issues/60215).

### Create a new virtual environment

Create a virtual environment in the checked out repository.  The dir `venv3` is gitignored, and the rest of this
documentation assumes you'll be using that as the name for your virtual environment:

```bash
# Create a new venv called venv3
python3 -m venv venv3

# Activate venv3
source venv3/bin/activate

# Install dev-requirements
pip install -r dev-requirements.txt
```

#### Running the unit tests

You can use the `ansible-test` command to run all of the unit tests:
```bash
# Run unit tests
ansible-test units --python=3.8
```

#### Run Integration Tests

You can also use the `ansible-test` command to run all of the integration tests:

```bash
# Run integration tests
ansible-test integration --python=3.8
```

### PyCharm set-up instructions

If you're planning on using a development environment such as PyCharm to develop `ibm_zos_cics`, you will need to
load the bolded folder in the sample checkout path, in order that your development environment is able to resolve
references to FQCN imports:

<code>.../<b>ibm_zos_cics</b>/ansible_collections/ibm/ibm_zos_cics</code>

#### Make your virtual environment the default Python interpreter for the project

Add the virtual environment as an existing Python interpreter:

 - `Preferences > Project: cics-ansible > Python Interpreter > Cog menu > Add.. > {project_root}/ansible_collections/ibm/ibm_zos_cics/env/bin/python`

Set the virtual environment as the default Python interpreter:

 - `Preferences > Project: cics-ansible > Python Interpreter > Top dropdown box > Select interpreter you just imported > Apply`

#### Python 2 support

The CMCI modules support running on Python 2.7.  To ensure we maintain python 2.7 compatibility, you will also want to
configure a Python 2.7 virtualenv:

```bash
# Ensure virtualenv is installed
python2.7 -m pip install virtualenv
 
# Create a new virtualenv called venv2
python2.7 -m virtualenv venv2

# Activate venv2
source venv2/bin/activate

# Install dev-requirements
pip install -r dev-requirements.txt
```

Note that a slightly different set of dev requirements is installed for python 2.7, as most of the static analysis tools in
the automated build are run in python 3.8, so are not dev requirements for the python 2.7 environment.

#### Running the build, tests and static analysis locally

A bash script is provided to automate running the static analysis, and tests in both python 2.7 and python 3.8
environments.  You will need to have set up `venv`s as described above, with the dev-requirements pre-installed.  You will 
then be able to run the build, passing the locations of the python 2.7 and python 3.8 `venv`s as environment variables:

```bash
CMCI_PYTHON_38=./venv3 CMCI_PYTHON_27=./venv2 ./build.sh
```

If you are running on Windows, you will need to run the automated build in a docker container produced by building the `Dockerfile` in this repository

#### Configure PyCharm to be able to run Ansible collection unit tests

First, add the `ansible_pytest_collections` plugin to `PYTHONPATH` for your python interpreter.  This will be in your
venv if you installed the dependencies using the dev requirements file:

 - `Preferences > Project: cics-ansible > Python Interpreter > Cog menu > Show all > 
   Select your interpreter > Show paths for the selected interpreter (at the bottom) > Plus > 
   add the path to the 'ansible_test' 'pytest' plugin in your python environment`

   - For the sample path:
     `.../ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics/venv3/lib/python3.8/site-packages/ansible_test/_data/pytest/plugins`

Next, you'll need to set some default environment variables for pytest launches, to enable the
`ansible_pytest_collections` plugin, and successfully resolve the `ibm_zos_cics` collection locally.

Go to `Run Config Menu > Edit Configurations... > Templates > Python tests > pytest > Environment variables button`
 
- Set `PYTEST_PLUGINS` to `ansible_pytest_collections`

- Set `ANSIBLE_COLLECTIONS_PATHS` to your project root, i.e. the directory that contains `ansible_collections`.  For the
  example configuration, that's set to `.../ibm_zos_cics`.
     
*(You may need to delete existing test configurations in `Python Tests` as they won't have been created with the new
template)*

You should be able to launch the unit tests in `tests/unit/modules` by clicking the play button.

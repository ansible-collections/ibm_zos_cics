# How to contribute

Thank you for contributing to this project.

We welcome bug reports and discussions about new function in the issue tracker, and we also welcome proposed new features or bug fixes via pull requests.

You should read these guidelines to help you contribute.

## Reporting a bug

Please raise bugs via the issue tracker. First, check whether an issue for your problem already exists.

When raising bugs, try to give a good indication of the exact circumstances that provoked the bug. What were you doing? What did you expect to happen? What actually happened? What logs or other material can you provide to show the problem?

## Requesting new features

Please request new features via the issue tracker. When requesting features, try to show why you want the feature you're requesting.

## Contributing code

### Before you start...

If you're thinking of fixing a bug or adding new features, be sure to open an issue first. This gives us a place to have a discussion about the work.

### Licensing

All code must have an ASL v2.0 header

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

Development Environment Set-Up Instructions
===================

This repository contains an Ansible collection, which is tested using `ansible-test`.  This combination of development
tooling requires you to clone the repository to a pretty specific path.  As an example, clone the repository to:

```
.../ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics
```

`ansible-test` requires your project to exist in a FQCN-compatible folder structure following the Ansible Collections
conventions.  For details, see [this issue](https://github.com/ansible/ansible/issues/60215) 

### Create a new virtual environment

Create a virtual environment in the checked out repository.  The dir `env` is gitignored, and the rest of this
documentation assumes you'll be using that as the name for your virtual environment:

```
# Create a new venv called env
python3 -m venv env

# Activate env
source env/bin/activate

# Install requirements
pip install -r requirements.txt
```

#### Running the unit tests

You can use the `ansible-test` command to run all of the unit tests
```
# Run unit tests
ansible-test units --python=3.8
```

#### Run Integration Tests

You can also use the `ansible-test` command to run all of the integration tests:

```
# Run integration tests
ansible-test integration --python=3.8
```

### PyCharm set-up instructions

If you're planning on using a development environment such as PyCharm to develop `ibm_zos_cics`, you will need to
load the bolded folder in the sample checkout path, in order that your development environment is able to resolve
references to FQCN imports:

<code>.../<b>ibm_zos_cics</b>/ansible_collections/ibm/ibm_zos_cics</code>

#### Make your virtual environment the default Python interpreter for the project

Add the virtual environment as an existing Python interpreter

 - `Preferences > Project: cics-ansible > Python Interpreter > Cog menu > Add.. > {project_root}/ansible_collections/ibm/ibm_zos_cics/env/bin/python`

Set the virtual environment as the default Python interpreter

 - `Preferences > Project: cics-ansible > Python Interpreter > Top dropdown box > Select interpreter you just imported > Apply`

#### Configure PyCharm to be able to run Ansible collection unit tests

First, add the `ansible_pytest_collections` plugin to `PYTHONPATH` for your python interpreter.  This will be in your
venv if you installed the dependencies using the requirements file:

 - `Preferences > Project: cics-ansible > Python Interpreter > Cog menu > Show all > 
   Select your interpreter > Show paths for the selected interpreter (at the bottom) > Plus > 
   add the path to the 'ansible_test' 'pytest' plugin in your python environment`

   - For the sample path:
     `.../ibm_zos_cics/ansible_collections/ibm/ibm_zos_cics/env/lib/python3.8/site-packages/ansible_test/_data/pytest/plugins`

Next, you'll need to set some default environment variables for pytest launches, to enable the
`ansible_pytest_collections` plugin, and successfully resolve the `ibm_zos_cics` collection locally.

Go to `Run Config Menu > Edit Configurations... > Templates > Python tests > pytest > Environment variables button`
 
- Set `PYTEST_PLUGINS` to `ansible_pytest_collections`

- Set `ANSIBLE_COLLECTIONS_PATHS` to your project root, i.e. the directory that contains `ansible_collections`.  For the
  example configuration, that's set to `.../ibm_zos_cics`.
     
*(You may need to delete existing test configurations in `Python Tests` as they won't have been created with the new
template)*

You should be able to launch the unit tests in `tests/unit/modules` by clicking the play button.
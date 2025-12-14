# IBM z/OS CICS Collection - Developer Guide

Welcome to the IBM z/OS CICS Ansible Collection! This guide will help you set up your development environment and start contributing to this open-source project.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Started with Dev Container (Recommended)](#getting-started-with-dev-container-recommended)
3. [Manual Setup (Alternative)](#manual-setup-alternative)
4. [Project Structure](#project-structure)
5. [Development Workflow](#development-workflow)
6. [Testing](#testing)
7. [Code Quality](#code-quality)
8. [Contributing Guidelines](#contributing-guidelines)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

### For Dev Container Setup (Recommended)
- **Visual Studio Code** with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- **Docker Desktop** or compatible container runtime
- **Git** for version control
- **SSH keys** configured for z/OS access (if testing against real systems)

### For Manual Setup
- **Python 3.9+** (Python 3.12 recommended)
- **Ansible Core 2.15+** (2.16 recommended)
- **Git** for version control
- **pip** for Python package management

## Getting Started with Dev Container (Recommended)

The dev container provides a pre-configured development environment with all dependencies installed automatically.

### Step 1: Clone the Repository

```bash
git clone https://github.com/ansible-collections/ibm_zos_cics.git
cd ibm_zos_cics
```

### Step 2: Open in VS Code

```bash
code .
```

### Step 3: Reopen in Container

When VS Code opens, you'll see a notification asking if you want to reopen the folder in a container. Click **"Reopen in Container"**.

Alternatively, you can:
1. Press `F1` or `Ctrl+Shift+P` (Windows/Linux) / `Cmd+Shift+P` (Mac)
2. Type "Dev Containers: Reopen in Container"
3. Press Enter

### Step 4: Wait for Container Setup

The container will:
- Pull the Python 3.12 base image
- Install Ansible Core 2.16
- Install required Ansible collections (`ibm.ibm_zos_core`, `community.general`)
- Install Python dependencies from [`dev-requirements.txt`](dev-requirements.txt)
- Configure your SSH keys for z/OS access
- Set up shell history persistence
- Configure VS Code extensions (Ansible, Python, GitLens)

This process takes 2-5 minutes on first run. Subsequent starts are much faster.

### Step 5: Verify Setup

Once the container is ready, open a terminal in VS Code and verify:

```bash
# Check Ansible version
ansible --version

# Check Python version
python --version

# Check installed collections
ansible-galaxy collection list

# Verify you're in the correct directory
pwd
# Should output: /workspace/collections/ansible_collections/ibm/ibm_zos_cics
```

### What's Included in the Dev Container?

The dev container ([`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json)) provides:

**Base Image:**
- Python 3.12 on Debian Bullseye
- Git and common utilities

**Installed Tools:**
- Ansible Core 2.16
- Required Ansible collections
- All Python dependencies for development and testing
- Linting tools (pylint, ansible-lint, yamllint, shellcheck)
- Testing frameworks (pytest, mock)
- Documentation tools (rstcheck)

**VS Code Extensions:**
- Red Hat Ansible extension
- Python extension
- GitLens for Git integration
- Live Share for collaboration

**Configuration:**
- SSH keys mounted from your host machine
- Shell history persistence across container restarts
- Ansible configured with YAML output callback
- Collection paths pre-configured

## Manual Setup (Alternative)

If you prefer not to use the dev container:

### Step 1: Clone and Navigate

```bash
git clone https://github.com/ansible-collections/ibm_zos_cics.git
cd ibm_zos_cics
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Ansible

```bash
pip install ansible-core==2.16
```

### Step 4: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
pip install -r dev-requirements.txt
pip install -r doc-requirements.txt

# Install required Ansible collections
ansible-galaxy collection install ibm.ibm_zos_core:==1.10.0
ansible-galaxy collection install community.general
```

### Step 5: Configure Ansible

Create `~/.ansible.cfg`:

```ini
[defaults]
stdout_callback=community.general.yaml
collections_paths=./
```

## Project Structure

Understanding the project layout:

```
ibm_zos_cics/
├── .devcontainer/          # Dev container configuration
│   ├── devcontainer.json   # Container settings
│   └── setup.sh            # Post-creation setup script
├── plugins/
│   ├── modules/            # Ansible modules (user-facing)
│   │   ├── cmci_*.py       # CMCI REST API modules
│   │   ├── *_catalog.py    # Catalog management modules
│   │   ├── aux_*.py        # Auxiliary data set modules
│   │   ├── csd.py          # CSD management
│   │   ├── region_jcl.py   # JCL generation
│   │   └── stop_region.py  # Region lifecycle
│   ├── module_utils/       # Shared utility code
│   │   ├── cmci.py         # CMCI base class
│   │   ├── _data_set.py    # Data set base class
│   │   └── _*.py           # Specialized utilities
│   ├── action/             # Action plugins
│   ├── doc_fragments/      # Reusable documentation
│   └── plugin_utils/       # Plugin utilities
├── docs/                   # Documentation source
├── tests/
│   ├── integration/        # Integration tests
│   └── unit/              # Unit tests
├── requirements.txt        # Runtime dependencies
├── dev-requirements.txt    # Development dependencies
├── doc-requirements.txt    # Documentation dependencies
├── CONTRIBUTING.md         # Contribution guidelines
└── galaxy.yml             # Collection metadata
```

More information about the project internals can be found in the [architecture guide](Architecture.md).

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-new-feature
```

### 2. Make Your Changes

Edit the relevant files in [`plugins/modules/`](plugins/modules/) or [`plugins/module_utils/`](plugins/module_utils/).

### 3. Add Tests

- **Unit tests**: Add to [`tests/unit/`](tests/unit/)
- **Integration tests**: Add to [`tests/integration/targets/`](tests/integration/targets/)

### 4. Run Code Quality Checks

```bash
# Run ansible-lint
ansible-lint

# Run sanity tests (includes pylint, yamllint, etc.)
ansible-test sanity

# Or run specific sanity tests:
ansible-test sanity --test pylint
ansible-test sanity --test yamllint
ansible-test sanity --test validate-modules
```

### 5. Run Tests

```bash
# Run unit tests
ansible-test units

# Run specific unit test
ansible-test units cmci_get

# Run unit tests with Python 3.9
ansible-test units --python 3.9

```

### 6. Update Documentation

If you've added or modified modules:
- Update module docstrings (DOCUMENTATION, EXAMPLES, RETURN)
- Generate RST documentation from modules:
  ```bash
  cd docs
  python ansible-doc-extractor-collections.py
  ```
- Build HTML documentation:
  ```bash
  make html
  ```
- View documentation locally:
  ```bash
  make view-html
  ```
- Review generated docs in [`docs/build/html/`](docs/build/html/)

### 7. Commit Your Changes

**Important**: All commits must be signed off (DCO):

```bash
git add .
git commit -s -m "Add new feature: description"
```

The `-s` flag adds the required `Signed-off-by` line.

### 8. Push and Create Pull Request

```bash
git push origin feature/my-new-feature
```

Then create a pull request on GitHub.

## Testing

### Unit Tests

Unit tests validate individual functions and classes without external dependencies.

```bash
# Run all unit tests
ansible-test units

# Run with verbose output
ansible-test units -v

# Run specific unit test module
ansible-test units cmci_get

# Run unit tests for specific Python version
ansible-test units --python 3.9
ansible-test units --python 3.10
ansible-test units --python 3.11


# Run with coverage
ansible-test units --coverage
ansible-test coverage report
```

### Integration Tests

Integration tests validate end-to-end functionality against real or mocked systems.

```bash
# Run integration tests (requires z/OS access)
ansible-test integration

# Run specific integration test target
ansible-test integration cics_cmci
ansible-test integration cics_csd


# Run with verbose output
ansible-test integration cics_cmci -v
```

**Note**: Integration tests require:
- Access to a z/OS system with CICS
- SSH connectivity to the target system
- tests/integration/inventory_zos.yml setup. Use the [template file](tests/integration/template.inventory_zos.yml) for guidance

### Sanity Tests

Ansible's built-in sanity tests validate code quality and compatibility:

```bash
# Run all sanity tests
ansible-test sanity

# Run specific sanity test
ansible-test sanity --test validate-modules
ansible-test sanity --test pylint
ansible-test sanity --test pep8
ansible-test sanity --test yamllint

# Run sanity tests for specific Python version
ansible-test sanity --python 3.9

# List available sanity tests
ansible-test sanity --list-tests
```

## Code Quality

### Linting Tools

The project uses multiple linters to maintain code quality:

#### Ansible Lint
Validates Ansible-specific best practices:

```bash
ansible-lint
```

Configuration: [`.ansible-lint`](.ansible-lint)

#### Ansible Test Sanity
Comprehensive validation including pylint, yamllint, and more:

```bash
# Run all sanity tests
ansible-test sanity

# Run specific tests
ansible-test sanity --test pylint
ansible-test sanity --test yamllint
ansible-test sanity --test pep8
```

#### Bandit
Security vulnerability scanner:

```bash
bandit -r plugins/
```

## Contributing Guidelines

### Before You Start

1. **Read** [`CONTRIBUTING.md`](CONTRIBUTING.md) for detailed guidelines
2. **Check** existing issues and pull requests to avoid duplicates
3. **Discuss** major changes in an issue first

### Code Requirements

✅ **Must Have:**
- Signed-off commits (DCO)
- Unit tests for new functionality
- Updated documentation
- Passing linter checks

❌ **Avoid:**
- Committing sensitive data (credentials, IPs)
- Large binary files
- Unrelated changes in the same PR
- Breaking existing functionality

### Pull Request Process

1. **Title**: Use clear, descriptive titles
   - Good: "Add support for CICS bundles in cmci_create"
   - Bad: "Fix bug"

2. **Description**: Include:
   - What changed and why
   - Related issue numbers
   - Testing performed
   - Breaking changes (if any)

3. **Review**: Address reviewer feedback promptly

4. **Merge**: Maintainers will merge once approved


## Additional Resources

### Documentation
- [Architecture Guide](Architecture.md) - Detailed architecture overview
- [CICS Ansible Collection Documentation](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_cics/docs/source/modules.html)
- [CICS Documentation](https://www.ibm.com/docs/en/cics-ts/latest)
- [CMCI REST API Reference](https://www.ibm.com/docs/en/cics-ts/6.x?topic=reference-cmci-rest-api)

### Community
- [GitHub Issues](https://github.com/ansible-collections/ibm_zos_cics/issues)
- [GitHub Discussions](https://github.com/ansible-collections/ibm_zos_cics/discussions)
- [Sample Playbooks](https://github.com/IBM/z_ansible_collections_samples)

### Related Projects
- [IBM z/OS Core Collection](https://github.com/ansible-collections/ibm_zos_core)
- [Ansible Documentation](https://docs.ansible.com/)
- [Z Open Automation Utilities (ZOAU)](https://www.ibm.com/docs/en/zoau/latest)

## Getting Help

If you encounter issues:

1. **Check** this guide and the [Architecture document](Architecture.md)
2. **Search** existing [GitHub issues](https://github.com/ansible-collections/ibm_zos_cics/issues)
3. **Ask** in [GitHub Discussions](https://github.com/ansible-collections/ibm_zos_cics/discussions)
4. **Create** a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Environment details (OS, Python version, Ansible version)
   - Relevant logs or error messages

## License

This collection is licensed under the [Apache License, Version 2.0](LICENSE.txt).

All contributions must include the Apache 2.0 license header and be signed off according to the [Developer Certificate of Origin](https://developercertificate.org).

---

**Happy Contributing! 🚀**

Thank you for helping improve the IBM z/OS CICS Ansible Collection!

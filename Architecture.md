# IBM z/OS CICS Collection Architecture

## Overview

The **IBM z/OS CICS collection** (`ibm.ibm_zos_cics`) is an Ansible collection that provides automation capabilities for managing CICS (Customer Information Control System) resources and regions on IBM z/OS. The collection supports two primary use cases:

1. **CICS Resource Management** - Managing CICS resources through the CMCI REST API
2. **CICS Region Provisioning** - Provisioning and managing standalone CICS regions

## Collection Structure

```
ibm_zos_cics/
├── plugins/
│   ├── modules/           # Ansible modules (user-facing)
│   ├── module_utils/      # Shared utility code
│   ├── action/            # Action plugins for module execution
│   ├── doc_fragments/     # Reusable documentation
│   └── plugin_utils/      # Plugin utilities
├── docs/                  # Documentation
├── tests/                 # Integration and unit tests
└── meta/                  # Collection metadata
```

## Architecture Components

### 1. Module Categories

The collection's modules are organized into two main categories:

#### A. CMCI Modules (Resource Management)

These modules interact with the CICS Management Client Interface (CMCI) REST API to manage CICS resources:

- [`cmci_get`](plugins/modules/cmci_get.py) - Query CICS resources and definitions
- [`cmci_create`](plugins/modules/cmci_create.py) - Create new CICS resources and definitions
- [`cmci_update`](plugins/modules/cmci_update.py) - Update existing CICS resources and definitions
- [`cmci_delete`](plugins/modules/cmci_delete.py) - Delete CICS resources and definitions
- [`cmci_action`](plugins/modules/cmci_action.py) - Perform actions on CICS resources (e.g., NEWCOPY, INSTALL)

**Key Characteristics:**
- Use HTTP/HTTPS to communicate with CMCI
- Support both basic authentication and certificate-based authentication
- Work with CICSPlex SM or standalone SMSS regions
- Return structured data about CICS resources

#### B. Provisioning Modules (Region Management)

These modules manage CICS region data sets and lifecycle:

**Data Set Management:**
- [`csd`](plugins/modules/csd.py) - CICS System Definition (CSD) data set
- [`local_catalog`](plugins/modules/local_catalog.py) - Local catalog data set
- [`global_catalog`](plugins/modules/global_catalog.py) - Global catalog data set
- [`aux_temp_storage`](plugins/modules/aux_temp_storage.py) - Auxiliary temporary storage
- [`aux_trace`](plugins/modules/aux_trace.py) - Auxiliary trace data sets
- [`local_request_queue`](plugins/modules/local_request_queue.py) - Local request queue
- [`td_intrapartition`](plugins/modules/td_intrapartition.py) - Transient data intrapartition
- [`transaction_dump`](plugins/modules/transaction_dump.py) - Transaction dump data sets

**Region Lifecycle:**
- [`region_jcl`](plugins/modules/region_jcl.py) - Generate CICS startup JCL
- [`stop_region`](plugins/modules/stop_region.py) - Stop a running CICS region

**Key Characteristics:**
- Create, initialize, and manage VSAM and sequential data sets
- Support templated data set naming conventions
- Provide state management (absent, initial, warm)
- Execute z/OS utilities directly via ZOAU CLI tools (IDCAMS, DFHCSDUP, DFHCCUTL, etc.)

### 2. Module Utilities Layer

The [`module_utils`](plugins/module_utils/) directory contains shared code used by multiple modules:

#### Core Utilities

- [`cmci.py`](plugins/module_utils/cmci.py) - Base class for all CMCI modules
  - Handles HTTP communication with CMCI REST API
  - Manages authentication (basic and certificate)
  - Parses XML responses using xmltodict
  - Provides filter and parameter handling
  - Validates CMCI responses and error handling

- [`_data_set.py`](plugins/module_utils/_data_set.py) - Base class for data set modules
  - Common data set operations (create, delete, initialize)
  - State management (absent, initial, warm)
  - Parameter validation using BetterArgParser
  - VSAM and sequential data set handling

#### Specialized Utilities

- [`_data_set_utils.py`](plugins/module_utils/_data_set_utils.py) - Data set operations
  - IDCAMS command building and execution via `mvscmdauth`
  - LISTDS operations for data set inspection via `mvscmdauth IKJEFT01`
  - Sequential data set allocation via `dtouch`
  - Data set content reading via `dcat`

- [`_dd_statement.py`](plugins/module_utils/_dd_statement.py) - DD statement definitions
  - `DatasetDefinition`, `StdinDefinition`, `StdoutDefinition`, `InputDefinition`, `OutputDefinition`, `DDStatement`
  - Represent DD allocations passed to `_mvscmd_builder` for command construction

- [`_mvscmd_builder.py`](plugins/module_utils/_mvscmd_builder.py) - MVS command construction
  - Builds `mvscmd` and `mvscmdauth` shell commands from a program name and list of `DDStatement` objects
  - Manages temporary datasets for stdin content, cleaning them up after execution
  - Provides `_write_to_dataset()` for writing content to a temporary MVS dataset via `dtouch`/`decho`

- [`_arg_parser.py`](plugins/module_utils/_arg_parser.py) - Argument parsing
  - `BetterArgParser` for z/OS-specific argument validation (dataset names, volume serials, members)

- [`_csd.py`](plugins/module_utils/_csd.py) - CSD-specific operations
  - DFHCSDUP command execution via `mvscmd`
  - CSD initialization scripts

- [`_local_catalog.py`](plugins/module_utils/_local_catalog.py) - Local catalog operations
  - DFHCCUTL utility execution via `mvscmd`

- [`_global_catalog.py`](plugins/module_utils/_global_catalog.py) - Global catalog operations
  - DFHRMUTL utility execution via `mvscmd`

- [`_jcl_helper.py`](plugins/module_utils/_jcl_helper.py) - JCL generation
  - Builds CICS startup JCL
  - Handles DD statements and parameters
  - Manages SIT (System Initialization Table) parameters

- [`_icetool.py`](plugins/module_utils/_icetool.py) - ICETOOL operations
  - Record counting for VSAM data sets via `mvscmd`

- [`_response.py`](plugins/module_utils/_response.py) - Response handling
  - `_execution()` — builds the standard `{name, rc, stdout, stderr}` dict appended to every module's `executions` list
  - `MVSCmdResponse` — holds `rc`, `stdout`, `stderr` from a subprocess invocation
  - `MVSExecutionException` — wraps failures with the accumulated executions list
  - `_execute_subprocess()` — runs a shell command via `subprocess.run` and returns `(rc, stdout, stderr)`
  - `_cleanup_temp_items()` — removes temporary Unix files and MVS datasets created during execution

- [`_zoau_version_checker.py`](plugins/module_utils/_zoau_version_checker.py) - ZOAU validation
  - Invokes `zoaversion` CLI at runtime to determine the installed ZOAU version
  - Raises `ImportError` if ZOAU is absent or below the minimum supported version (1.3.0.0)

### 3. Action Plugins

Action plugins in [`plugins/action/`](plugins/action/) provide custom execution logic for specific modules:
The collection includes 10 action plugins for provisioning modules. **CMCI modules do not have custom action plugins** but support `module_defaults` via action_groups defined in `meta/runtime.yml`.

**Data Set Action Plugins** (8 plugins extending `_DataSetActionPlugin`):
- [`aux_temp_storage.py`](plugins/action/aux_temp_storage.py), [`aux_trace.py`](plugins/action/aux_trace.py), [`csd.py`](plugins/action/csd.py), [`global_catalog.py`](plugins/action/global_catalog.py), [`local_catalog.py`](plugins/action/local_catalog.py), [`local_request_queue.py`](plugins/action/local_request_queue.py), [`td_intrapartition.py`](plugins/action/td_intrapartition.py), [`transaction_dump.py`](plugins/action/transaction_dump.py)
- Run on controller to expand templated data set names (e.g., `<< data_set_name >>` → `DFHCSD`)
- Validate parameters and resolve library references before sending to modules
- `csd.py` reads local DFHCSDUP scripts; `aux_trace.py` and `transaction_dump.py` select A/B destinations

**Region JCL Action Plugin**:
- [`region_jcl.py`](plugins/action/region_jcl.py) - Processes all region data sets and library templates for JCL generation

**Stop Region Action Plugin**:
- [`stop_region.py`](plugins/action/stop_region.py) - Orchestrates multi-step CICS shutdown with job status polling

### 4. Documentation Fragments

Reusable documentation in [`plugins/doc_fragments/`](plugins/doc_fragments/) provides consistent parameter documentation across related modules:

- `cmci.py` - Common CMCI parameters (host, port, authentication)
- `csd.py` - CSD module parameters
- `local_catalog.py` - Local catalog parameters
- `region_jcl.py` - Region JCL parameters
- And others for each data set type

## Data Flow Architecture

### CMCI Module Flow

```mermaid
flowchart TD
    A[User Playbook] --> B[Ansible Module<br/>e.g., cmci_get]
    B --> C[AnsibleCMCIModule<br/>cmci.py]
    C --> D[HTTP Request]
    D --> E[CMCI REST API]
    E --> F[CICS Region /<br/>CICSPlex SM]
    F --> G[XML Response]
    G --> H[Parse with xmltodict]
    H --> I[Return structured data to user]
```

### Provisioning Module Flow

```mermaid
flowchart TD
    A[User Playbook] --> B[Action Plugin<br/>e.g., csd.py<br/>Controller]
    B --> |Expand templates<br/>Validate parameters<br/>Read local files| C[Ansible Module<br/>e.g., csd<br/>Managed Node]
    C --> D[DataSet Base Class<br/>_data_set.py]
    D --> E[Specialized Module Utils<br/>e.g., _csd.py]
    E --> F[_mvscmd_builder.py<br/>Build CLI command]
    F --> G[ZOAU CLI Tools<br/>mvscmd / mvscmdauth<br/>dtouch / dcat / decho]
    G --> H[z/OS System<br/>IDCAMS, DFHCSDUP, etc.]
    H --> I[Return execution results to user]
```

## Key Design Patterns

### 1. Inheritance Hierarchy

**CMCI Modules:**
```
AnsibleCMCIModule (base)
    ├── AnsibleCMCIGetModule
    ├── AnsibleCMCICreateModule
    ├── AnsibleCMCIUpdateModule
    ├── AnsibleCMCIDeleteModule
    └── AnsibleCMCIInstallModule (cmci_action)
```

**Data Set Modules:**
```
DataSet (base)
    ├── AnsibleCSDModule
    ├── AnsibleLocalCatalogModule
    ├── AnsibleGlobalCatalogModule
    ├── AnsibleAuxiliaryTempModule
    ├── AnsibleAuxiliaryTraceModule
    ├── AnsibleLocalRequestQueueModule
    ├── AnsibleTDIntraModule
    └── AnsibleTransactionDumpModule
```

### 2. State Management

Data set modules implement a state-based approach:

- **`absent`** - Ensure data set does not exist (delete if present)
- **`initial`** - Create new or reinitialize existing data set (empty)
- **`warm`** - Ensure data set exists with current content preserved
- **`cold`** - Cold start the global catalog (global_catalog only)
- **`changed`** - Apply changes to existing data set (csd only)

### 3. Template-Based Configuration

Modules support templated data set names for consistency:

```yaml
region_data_sets:
  template: "REGIONS.ABCD0001.<< data_set_name >>"
```

This expands to:
- `REGIONS.ABCD0001.DFHCSD`
- `REGIONS.ABCD0001.DFHLCD`
- `REGIONS.ABCD0001.DFHTEMP`
- etc.

### 4. Execution Tracking

All provisioning modules return an `executions` list. Each entry is produced by `_execution()` in `_response.py` and has the same four fields regardless of which program ran:

```python
executions = [
    {
        "name": "IDCAMS - Creating DFHCSD data set - Run 1",
        "rc": 0,
        "stdout": "...",   # raw stdout from the CLI tool
        "stderr": "..."    # raw stderr from the CLI tool
    }
]
```

The `stop_region` action plugin uses a different execution shape, reflecting the shell commands it issues (`jls`, `opercmd`, `jcan`):

```python
executions = [
    {
        "name": "Checking status of job MYJOB(JOB12345)",
        "rc": 0,
        "return": {        # raw result dict from the command action plugin
            "rc": 0,
            "stdout": "...",
            "stderr": "...",
            "cmd": "jls -j '/*/{job_name}'"
        }
    }
]
```

Both formats provide full transparency for debugging.

## Dependencies

### External Dependencies

1. **ZOAU (Z Open Automation Utilities)** - Required for provisioning modules
   - CLI tools (`mvscmd`, `mvscmdauth`, `dtouch`, `dcat`, `decho`, `drm`, `jls`, `jcan`, `opercmd`, `zoaversion`) must be present on the managed node
   - Minimum version 1.3.0.0 is verified at runtime by invoking `zoaversion`

2. **xmltodict** - Required for CMCI modules
   - Parses XML responses from CMCI REST API

### z/OS Requirements

**For CMCI Modules:**
- CMCI REST API enabled in CICSPlex SM or SMSS
- Network connectivity to CMCI host
- Valid credentials or certificates

**For Provisioning Modules:**
- ZOAU 1.3.0.0 or later installed on the managed node
- CICS libraries (SDFHLOAD, etc.)
- Language Environment libraries
- Appropriate z/OS authorizations

## Error Handling

### CMCI Modules

- HTTP errors are caught and reported with status codes
- CMCI response codes are validated against expected values
- Feedback records provide detailed error information
- XML parsing errors are handled gracefully

### Provisioning Modules

- `MVSExecutionException` wraps z/OS utility failures, carrying the full `executions` list at the point of failure
- Return codes from subprocess invocations are checked; non-zero RC raises an exception
- Execution history is preserved in the module return value for debugging
- Data set state is validated before and after operations via LISTDS
- `_cleanup_temp_items()` ensures temporary datasets and Unix files created during command construction are always removed, even on failure

## Security Considerations

### Authentication

**CMCI Modules:**
- Support basic authentication (username/password)
- Support certificate-based authentication (cert/key)
- Credentials can be provided via environment variables
- Passwords and certificates are marked as `no_log`

**Provisioning Modules:**
- Rely on SSH authentication to managed node
- Execute with user's z/OS credentials
- Require appropriate data set and utility authorizations

## Performance Considerations

### CMCI Modules

- Single HTTP request per module invocation
- Configurable timeout (default 30 seconds)
- Support for filtering to reduce data transfer
- Connection reuse within session

### Provisioning Modules

- Data set operations can be time-consuming
- Large data sets may require significant space
- VSAM operations are synchronous
- Multiple modules can run in parallel (different data sets)

## Extensibility

### Adding New CMCI Modules

1. Extend `AnsibleCMCIModule` base class
2. Implement required methods:
   - `init_argument_spec()` - Define parameters
   - `init_body()` - Build request body (if needed)
   - `init_request_params()` - Build URL parameters

### Adding New Data Set Modules

1. Extend `DataSet` base class from [`_data_set.py`](plugins/module_utils/_data_set.py)
2. Implement required methods:
   - `_get_arg_spec()` - Define parameters
   - `create_data_set()` - Data set creation logic; use `build_vsam_data_set()` for VSAM or `build_seq_data_set()` for sequential
   - `execute_target_state()` - State-specific logic (optional)
3. Create a corresponding module_utils helper (e.g., `_new_dataset.py`) that builds DD statements using types from `_dd_statement.py` and executes them via `_mvscmd_builder.build_mvscmd_command()`

## Testing Strategy

### Integration Tests

Located in [`tests/integration/targets/`](tests/integration/):
- Test against real CICS regions
- Validate end-to-end workflows
- Cover error scenarios

### Unit Tests

Located in [`tests/unit/`](tests/unit/):
- Test individual functions and classes
- Mock external dependencies
- Validate parameter parsing and validation

## Version Compatibility

- **Ansible**: Requires >= 2.15.0
- **Python**: Compatible with Python 3.6+
- **CICS**: Supports CICS TS 5.6 and later
- **z/OS**: Tested on z/OS 2.4 and later
- **ZOAU**: Version checked at runtime

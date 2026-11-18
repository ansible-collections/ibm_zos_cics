# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Commands

The repo is an Ansible collection and must live at `.../ansible_collections/ibm/ibm_zos_cics` (already true here); `ansible-test` only works from that path. Dependencies: `pip install -r dev-requirements.txt`; `ibm.ibm_zos_core` and `community.general` collections must be installed.

- All unit tests: `ansible-test units --python 3.12`
- Single unit test file: `ansible-test units --python 3.12 tests/unit/modules/test_csd.py`
- Single test case: `ansible-test units --python 3.12 tests/unit/modules/test_csd.py -k test_name` (plain `pytest` also works since `pytest` is in dev-requirements, but `ansible-test` sets up the collection import path)
- Sanity (pylint/pep8/validate-modules/etc.): `ansible-test sanity --test validate-modules` (or `pylint`, `pep8`, `yamllint`)
- Lint: `ansible-lint`, `yamllint -c yamllint.yaml .`, `./bandit.sh` (uses `.bandit.baseline`; tests excluded)
- Integration tests (`tests/integration/targets/cics_*`) need a real z/OS + CICS; copy `tests/integration/template.inventory_zos.yml` to `inventory_zos.yml`.
- Docs: `cd docs && python ansible-doc-extractor-collections.py && make html`
- All commits need DCO sign-off: `git commit -s`.

## Architecture (non-obvious bits)

- Two unrelated module families:
  - `cmci_*` modules (`plugins/module_utils/cmci.py`, class `AnsibleCMCIModule`) are REST/XML (needs `xmltodict`), no action plugins.
  - Provisioning modules (`csd`, `*_catalog`, `aux_*`, `td_intrapartition`, `transaction_dump`, `local_request_queue`, `region_jcl`, `stop_region`) run on z/OS via ZOAU and `ibm.ibm_zos_core`.
- Each provisioning module has FOUR coupled files: `plugins/modules/X.py`, `plugins/action/X.py`, `plugins/doc_fragments/X.py` (parameter docs live here, not in the module's `DOCUMENTATION`), `plugins/module_utils/_X.py`. Adding a module also requires: adding to `action_groups` in `meta/runtime.yml`, an entry in `tests/sanity/ignore-2.*.txt` for `validate-modules:missing-gplv3-license` (code is Apache-2.0), and unit tests.
- Action plugins run on the controller (expand `<< data_set_name >>` templates, read local files) and extend `_DataSetActionPlugin` via `plugin_utils/_module_action_plugin.py`; the module then runs on the managed node. Don't put controller-only logic in the module.
- Data set modules extend `DataSet` in `module_utils/_data_set.py`; subclasses implement `_get_arg_spec()`, `create_data_set()`, optionally `execute_target_state()`. States: `absent`, `initial`, `warm` (+ `cold` for global_catalog, `changed` for csd).
- z/OS utility calls (IDCAMS, LISTDS, IEFBR14, ICETOOL, DFHCSDUP, DFHCCUTL, DFHRMUTL) go through helpers in `_data_set_utils.py`/`_icetool.py` and every call is recorded with `_execution(name, rc, stdout, stderr)` from `_response.py`; failures raise `MVSExecutionException(message, executions)` so the full execution history is returned to the user. Follow this instead of calling `module.run_command`.
- `_check_zoau_version()` (min ZOAU 1.3.0.0) is called in the `DataSet` constructor (and in `stop_region`); the `zoautil_py` import in `_zoau_version_checker.py` is wrapped via `ZOAUImportError` so sanity/unit tests pass without ZOAU. Never import `zoautil_py` directly elsewhere.
- Arg validation uses `BetterArgParser` (from `ibm.ibm_zos_core`) in `get_arg_defs()`/`validate_parameters()`, in addition to the `AnsibleModule` argument_spec.

## Code style

Formatting and module boilerplate are enforced by `ansible-test sanity` and `ansible-lint`; run them instead of restating their rules. Not covered by either:

- New files carry the `# (c) Copyright IBM Corp. <years>` + Apache-2.0 header (not GPL, hence the `missing-gplv3-license` sanity ignores).
- Helpers in `module_utils/` are underscore-prefixed (`_data_set.py`); `cmci.py` is the only public util. Parameter names/values are module-level constants (`STATE`, `ABSENT`), not literals.
- Type hints are comment-style (`# type: (str, int) -> dict`).
- Unit tests: `pytest` + `MagicMock`; use `set_module_args` and canned z/OS output from `tests/unit/helpers/data_set_helper.py` (e.g. `LISTDS_*`, `IDCAMS_*`) and `cmci_helper.py`; mark py2-incompatible tests with `@pytest.mark.skipif(sys.version_info.major < 3, reason=PYTHON_LANGUAGE_FEATURES_MESSAGE)`. Test dirs mirror plugin dirs (`tests/unit/{modules,module_utils,action,plugin_utils}`).
- Changelog: uses antsibull-changelog (`changelogs/config.yaml`, fragments in `changelogs/fragments/`, which is currently absent—create it when needed).

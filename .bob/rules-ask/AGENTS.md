# Documentation Rules (Non-Obvious Only)

- Module parameter docs live in `plugins/doc_fragments/<module>.py` (pulled in via `extends_documentation_fragment`), not in `plugins/modules/<module>.py`.
- `plugins/module_utils/` files prefixed with `_` are internal-only; `cmci.py` is the only public util.
- `docs/source/modules/*.rst` are generated from module docstrings by `docs/ansible-doc-extractor-collections.py`; other `docs/source/*.rst` are hand-written.

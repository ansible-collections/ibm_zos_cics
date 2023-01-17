#!/usr/bin/env bash

ansible-lint
ansible-test sanity --python "$PYTHON_VERSION_SET"
ansible-test units --python "$PYTHON_VERSION_SET"

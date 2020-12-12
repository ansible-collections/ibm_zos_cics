#!/usr/bin/env bash

ansible-playbook -e "@cmci-variables.yml" playbooks/cics_cmci.yml
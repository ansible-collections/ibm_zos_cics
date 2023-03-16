#!/usr/bin/env bash

A="A"
B="B"
star="*"

TRAVIS_NO_DOT="${TRAVIS_JOB_NUMBER//./D}"

program_name_1="A$TRAVIS_NO_DOT$A"
program_name_2="A$TRAVIS_NO_DOT$B"
program_filter="A$TRAVIS_NO_DOT$star"

echo ""
echo "################ Job-Specific Variables ################"
echo "## Program 1 Name: $program_name_1"
echo "## Program 2 Name: $program_name_2"
echo "## Program Filter: $program_filter"
echo ""

echo "############# Creating cmci-variables.yml #############"
touch "$TRAVIS_BUILD_DIR"/tests/integration/targets/cics_cmci/cmci-variables.yml
{
    echo cmci_host: "$CMCI_HOST"
    echo cmci_port: "$CMCI_PORT"
    echo cmci_secure_port: "$CMCI_SECURE_PORT"
    echo cmci_user: "$CMCI_USER"
    echo cmci_password: "$CMCI_PASSWORD"
    echo cmci_context: "$CMCI_CONTEXT"
    echo cmci_scope: "$CMCI_SCOPE"
    echo cmci_scope_region_1: "$CMCI_SCOPE_REGION_1"
    echo cmci_scope_region_2: "$CMCI_SCOPE_REGION_2"
    echo cmci_program_name_1: "$program_name_1"
    echo cmci_program_name_2: "$program_name_2"
    echo cmci_program_filter: "$program_filter"
} >>"$TRAVIS_BUILD_DIR"/tests/integration/targets/cics_cmci/cmci-variables.yml

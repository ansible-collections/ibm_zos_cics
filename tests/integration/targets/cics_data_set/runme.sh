#!/usr/bin/env bash
# (c) Copyright IBM Corp. 2024
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

set -eux

VAR_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/provisioning.yml"
INV_PATH="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/inventory_zos.yml"
ZOS_ENV="$ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/integration/variables/zos.yml"

# These tests use a base "template" test that is run for each data set in turn, with parameters passed in 
# to tailor the test. Where possible, parameters are passed in on the ansible-playbook command, but there 
# are some things in ansible playbooks that can't have variables in (such module names). For these, the sed 
# command is instead used to do a find and replace on the template file to insert the required value.

sed -e "s/MODULE_NAME/auxiliary_temp/g"      playbooks/initial_absent_template.yml > playbooks/initial_absent_auxiliary_temp.yml
sed -e "s/MODULE_NAME/csd/g"                 playbooks/initial_absent_template.yml > playbooks/initial_absent_csd.yml
sed -e "s/MODULE_NAME/global_catalog/g"      playbooks/initial_absent_template.yml > playbooks/initial_absent_global_catalog.yml
sed -e "s/MODULE_NAME/intrapartition/g"      playbooks/initial_absent_template.yml > playbooks/initial_absent_intrapartition.yml
sed -e "s/MODULE_NAME/local_catalog/g"       playbooks/initial_absent_template.yml > playbooks/initial_absent_local_catalog.yml
sed -e "s/MODULE_NAME/local_request_queue/g" playbooks/initial_absent_template.yml > playbooks/initial_absent_local_request_queue.yml
sed -e "s/MODULE_NAME/trace/g"               playbooks/initial_absent_template.yml > playbooks/initial_absent_trace.yml
sed -e "s/MODULE_NAME/transaction_dump/g"    playbooks/initial_absent_template.yml > playbooks/initial_absent_transaction_dump.yml

sed -e "s/MODULE_NAME/auxiliary_temp/g"      playbooks/warm_template.yml > playbooks/warm_auxiliary_temp.yml
sed -e "s/MODULE_NAME/csd/g"                 playbooks/warm_template.yml > playbooks/warm_csd.yml
sed -e "s/MODULE_NAME/global_catalog/g"      playbooks/warm_template.yml > playbooks/warm_global_catalog.yml
sed -e "s/MODULE_NAME/intrapartition/g"      playbooks/warm_template.yml > playbooks/warm_intrapartition.yml
sed -e "s/MODULE_NAME/local_catalog/g"       playbooks/warm_template.yml > playbooks/warm_local_catalog.yml
sed -e "s/MODULE_NAME/local_request_queue/g" playbooks/warm_template.yml > playbooks/warm_local_request_queue.yml
sed -e "s/MODULE_NAME/trace/g"               playbooks/warm_template.yml > playbooks/warm_trace.yml
sed -e "s/MODULE_NAME/transaction_dump/g"    playbooks/warm_template.yml > playbooks/warm_transaction_dump.yml

sed -e "s/MODULE_NAME/auxiliary_temp/g"      -e "s/DATA_SET_NAME_LOWER/dfhtemp/g"  playbooks/validation_template.yml > playbooks/validation_auxiliary_temp.yml
sed -e "s/MODULE_NAME/csd/g"                 -e "s/DATA_SET_NAME_LOWER/dfhcsd/g"   playbooks/validation_template.yml > playbooks/validation_csd.yml
sed -e "s/MODULE_NAME/global_catalog/g"      -e "s/DATA_SET_NAME_LOWER/dfhgcd/g"   playbooks/validation_template.yml > playbooks/validation_global_catalog.yml
sed -e "s/MODULE_NAME/intrapartition/g"      -e "s/DATA_SET_NAME_LOWER/dfhintra/g" playbooks/validation_template.yml > playbooks/validation_intrapartition.yml
sed -e "s/MODULE_NAME/local_catalog/g"       -e "s/DATA_SET_NAME_LOWER/dfhlcd/g"   playbooks/validation_template.yml > playbooks/validation_local_catalog.yml
sed -e "s/MODULE_NAME/local_request_queue/g" -e "s/DATA_SET_NAME_LOWER/dfhlrq/g"   playbooks/validation_template.yml > playbooks/validation_local_request_queue.yml
sed -e "s/MODULE_NAME/trace/g"               -e "s/DATA_SET_NAME_LOWER/dfhauxt/g"  playbooks/validation_template.yml > playbooks/validation_trace.yml
sed -e "s/MODULE_NAME/transaction_dump/g"    -e "s/DATA_SET_NAME_LOWER/dfhdmpa/g"  playbooks/validation_template.yml > playbooks/validation_transaction_dump.yml

sed -e "s/MODULE_NAME/trace/g"            -e "s/DATA_SET_NAME_LOWER_A/dfhauxt/g" -e "s/DATA_SET_NAME_LOWER_B/dfhbuxt/g" playbooks/destination_template.yml > playbooks/destination_trace.yml
sed -e "s/MODULE_NAME/transaction_dump/g" -e "s/DATA_SET_NAME_LOWER_A/dfhdmpa/g" -e "s/DATA_SET_NAME_LOWER_B/dfhdmpb/g" playbooks/destination_template.yml > playbooks/destination_transaction_dump.yml

sed -e "s/MODULE_NAME/auxiliary_temp/g"      playbooks/region_group_template.yml > playbooks/region_group_auxiliary_temp.yml
sed -e "s/MODULE_NAME/csd/g"                 playbooks/region_group_template.yml > playbooks/region_group_csd.yml
sed -e "s/MODULE_NAME/global_catalog/g"      playbooks/region_group_template.yml > playbooks/region_group_global_catalog.yml
sed -e "s/MODULE_NAME/intrapartition/g"      playbooks/region_group_template.yml > playbooks/region_group_intrapartition.yml
sed -e "s/MODULE_NAME/local_catalog/g"       playbooks/region_group_template.yml > playbooks/region_group_local_catalog.yml
sed -e "s/MODULE_NAME/local_request_queue/g" playbooks/region_group_template.yml > playbooks/region_group_local_request_queue.yml
sed -e "s/MODULE_NAME/trace/g"               playbooks/region_group_template.yml > playbooks/region_group_trace.yml
sed -e "s/MODULE_NAME/transaction_dump/g"    playbooks/region_group_template.yml > playbooks/region_group_transaction_dump.yml

sed -e "s/MODULE_NAME/auxiliary_temp/g"      -e "s/DATA_SET_NAME_LOWER/dfhtemp/g"  playbooks/template_override_template.yml > playbooks/template_override_auxiliary_temp.yml
sed -e "s/MODULE_NAME/csd/g"                 -e "s/DATA_SET_NAME_LOWER/dfhcsd/g"   playbooks/template_override_template.yml > playbooks/template_override_csd.yml
sed -e "s/MODULE_NAME/global_catalog/g"      -e "s/DATA_SET_NAME_LOWER/dfhgcd/g"   playbooks/template_override_template.yml > playbooks/template_override_global_catalog.yml
sed -e "s/MODULE_NAME/intrapartition/g"      -e "s/DATA_SET_NAME_LOWER/dfhintra/g" playbooks/template_override_template.yml > playbooks/template_override_intrapartition.yml
sed -e "s/MODULE_NAME/local_catalog/g"       -e "s/DATA_SET_NAME_LOWER/dfhlcd/g"   playbooks/template_override_template.yml > playbooks/template_override_local_catalog.yml
sed -e "s/MODULE_NAME/local_request_queue/g" -e "s/DATA_SET_NAME_LOWER/dfhlrq/g"   playbooks/template_override_template.yml > playbooks/template_override_local_request_queue.yml
sed -e "s/MODULE_NAME/trace/g"               -e "s/DATA_SET_NAME_LOWER/dfhauxt/g"  playbooks/template_override_template.yml > playbooks/template_override_trace.yml
sed -e "s/MODULE_NAME/transaction_dump/g"    -e "s/DATA_SET_NAME_LOWER/dfhdmpa/g"  playbooks/template_override_template.yml > playbooks/template_override_transaction_dump.yml

# For debug, uncomment this to save the generated playbooks to the output directory if you want to see the effect of the sed commands
# cp -r playbooks $ANSIBLE_COLLECTIONS_PATH/ansible_collections/ibm/ibm_zos_cics/tests/output/templates

ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHTEMP, vsam: true}"                playbooks/initial_absent_auxiliary_temp.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHCSD, vsam: true, recreate: true}" playbooks/initial_absent_csd.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHGCD, vsam: true, start: true}"    playbooks/initial_absent_global_catalog.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHINTRA, vsam: true}"               playbooks/initial_absent_intrapartition.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHLCD, vsam: true, recreate: true}" playbooks/initial_absent_local_catalog.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHLRQ, vsam: true}"                 playbooks/initial_absent_local_request_queue.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHAUXT}"                            playbooks/initial_absent_trace.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHDMPA}"                            playbooks/initial_absent_transaction_dump.yml

ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHTEMP, vsam: true}"                     playbooks/warm_auxiliary_temp.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHCSD, vsam: true, empty_allowed: true}" playbooks/warm_csd.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHGCD, vsam: true}"                      playbooks/warm_global_catalog.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHINTRA, vsam: true}"                    playbooks/warm_intrapartition.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHLCD, vsam: true, empty_allowed: true}" playbooks/warm_local_catalog.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHLRQ, vsam: true}"                      playbooks/warm_local_request_queue.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHAUXT}"                                 playbooks/warm_trace.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHDMPA}"                                 playbooks/warm_transaction_dump.yml

ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHTEMP}"  playbooks/validation_auxiliary_temp.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHCSD}"   playbooks/validation_csd.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHGCD}"   playbooks/validation_global_catalog.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHINTRA}" playbooks/validation_intrapartition.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHLCD}"   playbooks/validation_local_catalog.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHLRQ}"   playbooks/validation_local_request_queue.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHAUXT}"  playbooks/validation_trace.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHDMPA}"  playbooks/validation_transaction_dump.yml

ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name_A: DFHAUXT, data_set_name_B: DFHBUXT}" playbooks/destination_trace.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name_A: DFHDMPA, data_set_name_B: DFHDMPB}" playbooks/destination_transaction_dump.yml

ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHTEMP}"  playbooks/region_group_auxiliary_temp.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHCSD}"   playbooks/region_group_csd.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHGCD}"   playbooks/region_group_global_catalog.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHINTRA}" playbooks/region_group_intrapartition.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHLCD}"   playbooks/region_group_local_catalog.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHLRQ}"   playbooks/region_group_local_request_queue.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHAUXT}"  playbooks/region_group_trace.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHDMPA}"  playbooks/region_group_transaction_dump.yml

ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHTEMP}"  playbooks/template_override_auxiliary_temp.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHCSD}"   playbooks/template_override_csd.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHGCD}"   playbooks/template_override_global_catalog.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHINTRA}" playbooks/template_override_intrapartition.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHLCD}"   playbooks/template_override_local_catalog.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHLRQ}"   playbooks/template_override_local_request_queue.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHAUXT}"  playbooks/template_override_trace.yml
ansible-playbook -i "$INV_PATH" -e "@$VAR_PATH" -e "@$ZOS_ENV" -e "{data_set_name: DFHDMPA}"  playbooks/template_override_transaction_dump.yml

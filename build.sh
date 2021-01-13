#!/usr/bin/env bash
trap "exit" INT
set -e
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
echo "/* -------------------------------------------------------------------------- */"
echo "/*                          Unit tests Python 3.8                             */"
echo "/* -------------------------------------------------------------------------- */"
source "$CMCI_PYTHON_38/bin/activate"
pip install -r requirements.txt
ansible-test units --python 3.8
ansible-test sanity 2>&1 --python 3.8
ansible-test integration --python 3.8
ansible-lint --python 3.8
deactivate


# echo "/* -------------------------------------------------------------------------- */"
# echo "/*                          Unit tests Python 2.7                             */"
# echo "/* -------------------------------------------------------------------------- */"
# source $CMCI_PYTHON_27/bin/activate
# pip install -r requirements.txt
# ansible-test units --python 2.7
# deactivate


echo "/* -------------------------------------------------------------------------- */"
echo "/*                              Linting Tests                                 */"
echo "/* -------------------------------------------------------------------------- */"

python3 -m yamllint -c yamllint.yaml .

#checkForAnsibleLintErrors(out)

for i in plugins/modules/*.py; do
    [ -f "$i" ] || break # handle empty directory
    echo "Checking if $i is an Ansible module"
    if grep -q AnsibleModule "$i"; then
      echo "$i is an Ansible module"
      ansible-doc -j -M . "$i"
    fi
    # checkForAnsibleDocErrors(out)
done

echo "/* -------------------------------------------------------------------------- */"
echo "/*                   Test Collection Build and Install                        */"
echo "/* -------------------------------------------------------------------------- */"
ansible-galaxy collection build . --force
ansible-galaxy collection install ibm-ibm_zos_cics* --force

echo "/* -------------------------------------------------------------------------- */"
echo "/*                           ansible-test Sanity Tests                        */"
echo "/* -------------------------------------------------------------------------- */"
# ansible-test sanity 2>&1 || true
# checkForAnsibleTestErrors(out)

echo "/* -------------------------------------------------------------------------- */"
echo "/*                          Unit and Functional Test                          */"
echo "/* -------------------------------------------------------------------------- */"
#    dir("${git_repo_name}") {
#        dir("playbooks") {
#            writeFile(file: "ansible.cfg", text: ANSIBLE_CONFIG_CONTENTS)
#        }
#        writeFile(file: "configuration.yml", text: generateYmlConfig(TARGET_HOST, USERNAME, PYTHON_PATH, ENVIRONMENT))
#    }
#
#    ansibleTestingImage.inside("-u jenkins\
#    -e TARGET_HOST=${TARGET_HOST}\
#    -e ANSIBLE_LIBRARY=${rootDir}/plugins/modules\
#    -e ANSIBLE_ACTION_PLUGINS=${rootDir}/plugins/action\
#    -e ANSIBLE_CONFIG=${rootDir}/playbooks/ansible.cfg\
#    -e ANSIBLE_CONNECTION_PLUGINS=${rootDir}/plugins/connection\
#    -e ANSIBLE_MODULE_UTILS=${rootDir}/plugins/module_utils") {
#
#        dir(params.git_repo_name) {
#            // Install collection so module_utils imports will be valid in modules
#            // Attempt to build the collection
#            sh script: "ansible-galaxy collection build . --force"
#            // Install the built collection
#            sh script: "ansible-galaxy collection install ibm-${params.git_repo_name}* --force"
#
#            dir("tests") {
#                if (env.git_ssh_ref == 'feature/1972/cics_cmci') {
#                    def out = sh script: "python3 -m pytest --host-pattern=localhost || true ", returnStdout: true
#                    echo out
#                    checkForPytestFails(out)
#                } else {
#                    def out = sh script: "python3 -m pytest --host-pattern=all -Z=${env.WORKSPACE}/${git_repo_name}/tests/test_config.yml || true", returnStdout: true
#                    echo out
#                    checkForPytestFails(out)
#                }
#            }
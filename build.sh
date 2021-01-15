#!/usr/bin/env bash
trap "exit" INT
set -e
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

source "$CMCI_PYTHON_38/bin/activate"
(set -x; pip install -r requirements.txt)

(set -x; ANSIBLE_COLLECTIONS_PATHS=../../.. ansible-lint)
(set -x; python3 -m yamllint -c yamllint.yaml .)

echo "/* -------------------------------------------------------------------------- */"
echo "/*                           ansible-test Sanity Tests                        */"
echo "/* -------------------------------------------------------------------------- */"
(set -x; ansible-test sanity 2>&1 --python 3.8)

echo "/* -------------------------------------------------------------------------- */"
echo "/*                          Unit tests Python 3.8                             */"
echo "/* -------------------------------------------------------------------------- */"
(set -x; ansible-test units --python 3.8)

echo "/* -------------------------------------------------------------------------- */"
echo "/*                          Integration tests Python 3.8                      */"
echo "/* -------------------------------------------------------------------------- */"
(set -x; ansible-test integration --python 3.8)
deactivate


# echo "/* -------------------------------------------------------------------------- */"
# echo "/*                          Unit tests Python 2.7                             */"
# echo "/* -------------------------------------------------------------------------- */"
# source $CMCI_PYTHON_27/bin/activate
# pip install -r requirements.txt
# ansible-test units --python 2.7
# deactivate
#
#for i in plugins/modules/*.py; do
#    [ -f "$i" ] || break # handle empty directory
#    echo "Checking if $i is an Ansible module"
#    if grep -q AnsibleCMCIModule "$i"; then
#      echo "$i is an Ansible module.  Running ansible-doc against it"
#
#      unset t_std t_err t_ret
#      # shellcheck disable=SC2030
#      eval "$( (ANSIBLE_COLLECTIONS_PATHS=../../.. ansible-doc -j ibm.ibm_zos_cics."$(basename "$i" .py)") \
#              2> >(t_err=$(cat); typeset -p t_err) \
#               > >(t_std=$(cat); typeset -p t_std); t_ret=$?; typeset -p t_ret )"
#
#      # shellcheck disable=SC2031
#      printf "stderr:\n%s\n" "$t_err"
#      # shellcheck disable=SC2031
#      printf "stdout:\n%s\n" "$t_std"
#
#      # shellcheck disable=SC2031
#      if [[ "${t_ret}" -ne 0 ]]; then
#        echo "ansible-doc returned a non-zero return code: ${t_ret}"
#        exit 1
#      elif [[ ! -z $t_err ]]; then
#        echo "ansible-doc wrote to std err which we're assuming was an error or warning"
#        exit 1
#      elif [[ ${t_std} =~ ^{}$ ]]; then
#        echo "No documentation"
#        exit 1
#      fi
#    fi
#done

echo "/* -------------------------------------------------------------------------- */"
echo "/*                   Collection Build and Install                             */"
echo "/* -------------------------------------------------------------------------- */"
(set -x; ansible-galaxy collection build . --force)
#(set -x; ansible-galaxy collection install ibm-ibm_zos_cics* --force)
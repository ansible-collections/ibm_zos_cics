#!/usr/bin/env bash
# Copy contents to the .ssh directory
cp -r /root/.ssh-local/. /root/.ssh
if [ -e  /root/.ssh/config ]; then
    # If config file exists
    mv ~/.ssh/config ~/.ssh/config-local
    touch ~/.ssh/config
    cat ~/.ssh/config-local > ~/.ssh/config
    rm ~/.ssh/config-local
fi

eval "$(ssh-agent)"
ssh-add

python_ver=$(python -c 'import platform; major, minor, patch = platform.python_version_tuple(); print("{0}.{1}".format(major,minor))')

ansible-galaxy collection install ibm.ibm_zos_core:==1.9.1 -p /workspace/collections
ansible-galaxy collection install community.general -p /workspace/collections

echo -e "[defaults]\nstdout_callback=community.general.yaml\nCOLLECTIONS_PATHS=/workspace/collections" > ~/.ansible.cfg

pip install -r /workspace/collections/ansible_collections/ibm/ibm_zos_cics/dev-requirements.txt
pip install -r /workspace/collections/ansible_collections/ibm/ibm_zos_cics/doc-requirements.txt

# Remove additional pythons from bin so we can use shorthand ansible commands
find /usr/bin/python* -type f -not -name python"${python_ver}" -exec rm -v {} +

mkdir -p /commandhistory
touch /commandhistory/.zsh_history
chown -R root /commandhistory
echo "export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.zsh_history" >> "/root/.zshrc"

# .zshrc file configuration - Use default zsh_theme
sed -i '/^ZSH_THEME/c\ZSH_THEME="robbyrussell"' ~/.zshrc

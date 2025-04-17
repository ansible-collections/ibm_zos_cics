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

python3 -m pip install --user ansible-core==2.16

ansible-galaxy collection install ibm.ibm_zos_core:==1.10.0 -p /workspace/collections
ansible-galaxy collection install community.general -p /workspace/collections

echo -e "[defaults]\nstdout_callback=community.general.yaml\nCOLLECTIONS_PATHS=/workspace/collections" > ~/.ansible.cfg

pip install -r /workspace/collections/ansible_collections/ibm/ibm_zos_cics/dev-requirements.txt
pip install -r /workspace/collections/ansible_collections/ibm/ibm_zos_cics/doc-requirements.txt

mkdir -p /commandhistory
touch /commandhistory/.zsh_history
chown -R root /commandhistory

{
    # Add history to zsh shell
    echo "export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.zsh_history"

    # Make this ansible_cics_collection repo the default repo when opening a new zsh terminal
    echo "cd /workspace/collections/ansible_collections/ibm/ibm_zos_cics/"
    echo "git config --global --add safe.directory /workspaces/collections/ansible_collections/ibm/ibm_zos_cics"
}  >> "/root/.zshrc"



# .zshrc file configuration - Use default zsh_theme
sed -i '/^ZSH_THEME/c\ZSH_THEME="robbyrussell"' ~/.zshrc

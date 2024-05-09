Docs generated under source/modules are automatically generated.
Other .rst files have to be manually updated
If you are running in a devcontainer, you can run 'update-docs.py' to generate updates to the modules .rst documents
Otherwise, you will need to run 'pip install -r /workspace/collections/ansible_collections/ibm/ibm_zos_cics/doc-requirements.txt'
Then run, 'apt-get updates' followed by 'apt-get install make' before you can run 'update-docs.py'
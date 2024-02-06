import os

# Run doc extractor to update .rst files in modules
os.system('ansible-doc-extractor ./docs/source/modules ./plugins/modules/*.py')

# Generate html source from .rst files
os.system('make html')

# Open html source to verify it's correct
os.system('make view html')

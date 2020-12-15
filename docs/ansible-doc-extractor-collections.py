# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
import re
import sys
from ansible_doc_extractor.cli import main
from ansible.utils.collection_loader import AnsibleCollectionLoader

if __name__ == '__main__':
    # allow doc-extractor to import code from collections so doc_fragment plugins work
    sys.meta_path.insert(0, AnsibleCollectionLoader())
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())

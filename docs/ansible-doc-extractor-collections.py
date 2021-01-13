# Copyright (c) IBM Corporation 2020
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

import sys
import os

# This needs to be set before the imports get evaluated!
os.environ['ANSIBLE_COLLECTIONS_PATHS'] = os.path.abspath('../../../..')

from ansible_doc_extractor.cli import render_docs

if __name__ == '__main__':
    relpath = '../plugins/modules'
    modules = list(
        map(
            lambda x: relpath + '/' + x,
            filter(
                lambda x: "__init__.py" != x,
                os.listdir(relpath)
            )
        )
    )
    sys.exit(render_docs('source/modules', modules, open('templates/module.rst.j2')))

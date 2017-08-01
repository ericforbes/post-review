#!/usr/bin/env python

from future import standard_library
standard_library.install_aliases()

import sys
import os

if os.environ.get('LC_CTYPE', '') == 'UTF-8':
    os.environ['LC_CTYPE'] = 'en_US.UTF-8'
import cli

def main():
    return cli.main()

if __name__ == '__main__':
    sys.exit(main())
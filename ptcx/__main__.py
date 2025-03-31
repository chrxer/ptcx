import argparse
import os
import sys
from ptcx import patch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    prog='ptcx',
    description='A format for modularized AST-based patching of arbitary code')
    
    parser.add_argument('path', nargs="?", default=os.getcwd())
    args = parser.parse_args()
    patch.path(_path=os.path.abspath(args.path))

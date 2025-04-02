import argparse
from pathlib import Path
from ptcx import patch

if __name__ == "__main__":
    parser = argparse.ArgumentParser( prog='python -m ptcx', description='A format for modularized AST-based patching of arbitary code')
    CWD = Path.cwd()
    parser.add_argument('path', nargs="?",type=Path, default="", help="Relative path from patchroot to patch")
    parser.add_argument('--srcroot',"--src",nargs="?",type=Path, default=CWD.joinpath("src"), help="Source code directory to patch")
    parser.add_argument("--patchroot","--patch",nargs="?",type=Path, default=CWD.joinpath("patch"), help="directory where patches are placed.")
    parser.add_argument("--reset",action="store_true", help="Resevert all uncommited changes within git repository in src")
    args = parser.parse_args()
    if args.reset is True:
        patch.reset(srcroot=args.srcroot)
    else:
        patch.path(args.path, srcroot=args.srcroot, patchroot=args.patchroot)

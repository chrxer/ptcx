import argparse
from pathlib import Path
from ptcx import patch

if __name__ == "__main__":
    parser = argparse.ArgumentParser( prog='python -m ptcx', description='A format for modularized AST-based patching of arbitary code')
    CWD = Path.cwd()
    parser.add_argument('path', nargs="?",type=Path, default="", help="Relative path from patchroot to patch")
    parser.add_argument('--srcroot',"--src",nargs="?",type=Path, default=CWD.joinpath("src"), help="Source code directory to patch")
    parser.add_argument("--patchroot","--patch",nargs="?",type=Path, default=CWD.joinpath("patch"), help="directory where patches are placed.")
    parser.add_argument("--reset",nargs="?", type=bool)
    args = parser.parse_args()
    if args.reset is True:
        raise NotImplementedError("Resetting the source directory isn't implemented yet")
    if args.path.is_file():
        patch.file(args.path, srcroot=args.srcroot, patchroot=args.patchroot)
    else:
        patch.path(args.path, srcroot=args.srcroot, patchroot=args.patchroot)

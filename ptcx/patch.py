from os import PathLike
import shutil
from pathlib import Path
from typing import List, Callable, Union
import time
import re

from ptcx.utils.imprt import fileimport
from ptcx.utils.wrap import exc
from ptcx import BasePTC

def ensure_is_git_repo(srcroot:Path):
    if not srcroot.joinpath(".git").exists():
        exc("git", "init", cwd=srcroot)
        exc("git", "add", "*", cwd=srcroot)
        exc("git", "commit", "-m", "Initial commit created by ptcx", cwd=srcroot)
        time.sleep(1)

def path(_path:PathLike="", srcroot:PathLike="./src",patchroot:PathLike="./patch"):
    """
    Apply patch to src
    """
    srcroot=Path(srcroot).absolute()
    patchroot=Path(patchroot).absolute()

    ensure_is_git_repo(srcroot)
    _path = Path(patchroot).joinpath(_path)
    cpr(patchroot, srcroot)

def reset(srcroot:PathLike="./src"):
    """
    Resevert all uncommited changes within git repository in src
    """
    srcroot=Path(srcroot).absolute()
    if not srcroot.joinpath(".git").exists():
        raise EnvironmentError("Resevert all uncommited changes within git repository in src ist only possible if it is a git repository")
    exc("git", "clean", "-d", "--force", cwd=srcroot)
    exc("git","reset", "--hard", "--recurse-submodules", cwd=srcroot)

def _patch_file(_path:PathLike,srcroot:Path=Path.cwd().joinpath("src"),patchroot:Path=Path.cwd().joinpath("patch")):
    rel_path = Path(str(_path)[:-5]).relative_to(patchroot)
    dstpath = srcroot.joinpath(rel_path)
    ptcxmod = fileimport(_path)
    PTC = ptcxmod.PTC
    if issubclass(PTC, BasePTC):
        ptcinst = PTC(file=dstpath, srcroot=srcroot, patchroot=patchroot)
        ptcinst._patch() # pylint: disable=protected-access
    else:
        raise ValueError(f"Expected class PTC (parent class of BasePTC), but got {PTC} at {rel_path}")
    

def _logpath(_path:str, names:List[str], patchroot:Path, srcroot:Path):
    ignores = []
    for name in names:
        __path = Path(_path).joinpath(name).absolute()
        if not __path.is_dir():
            _rel = __path.relative_to(patchroot)
            _str = str(__path)
            if len(_str)>4 and _str[-4:]=="ptcx":
                ignores.append(name)
                print(f"\033[92m[patch] {_rel}\033[0m")
                _patch_file(__path, srcroot=srcroot, patchroot=patchroot)
            else:
                print(f"\033[92m[cp] {_rel}\033[0m")
        elif name == "__pycache__":
            ignores.append(name)
                
    return ignores

def cpr(src:PathLike, dst:PathLike):
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=lambda *a, **b:_logpath(*a, **b, srcroot=dst, patchroot=src))

def search_and_insert(text:str, pattern:str, insert_func:Callable[[str], str]):
        """
        finds match & replaces inserts string at
        """
        match = re.search(pattern, text, flags=re.MULTILINE)

        if not match:
            raise ValueError(f"Pattern '{pattern}' not found in the text.")

        start, end = match.span(1)
        matched_text = text[start:end]
        modified_text = insert_func(matched_text)
        updated_text = text[:start] + modified_text + text[end:]

        return updated_text

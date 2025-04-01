from os import PathLike
from os.path import abspath
import shutil
from pathlib import Path
from typing import List, Callable

from ptcx.utils.imprt import fileimport
from ptcx import BasePTC

def path(_path:PathLike=Path.cwd(), srcroot:PathLike=Path.cwd().joinpath("src"),patchroot:PathLike=Path.cwd().joinpath("patch")):
    _path = Path(patchroot).joinpath(_path)
    cpr(patchroot, srcroot)

def file(_path:PathLike,srcroot:Path=Path.cwd().joinpath("src"),patchroot:Path=Path.cwd().joinpath("patch")):
    
    rel_path = Path(str(_path)[:-4]).relative_to(patchroot)
    dstpath = srcroot.joinpath(rel_path)
    ptcxmod = fileimport(_path)
    PTC = ptcxmod.PTC
    if issubclass(PTC, BasePTC):
        ptcinst = PTC(file=dstpath, srcroot=srcroot, patchroot=patchroot)
        ptcinst._patch()
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
                file(__path, srcroot=srcroot, patchroot=patchroot)
            else:
                print(f"\033[92m[cp] {_rel}\033[0m")
        elif name == "__pycache__":
            ignores.append(name)
                
    return ignores

def cpr(src:PathLike, dst:PathLike):
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=lambda *a, **b:_logpath(*a, **b, srcroot=dst, patchroot=src))
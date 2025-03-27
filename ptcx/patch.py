from os import PathLike, getcwd
from os.path import abspath
from ptcx.utils.wrap import exc
import shutil
from pathlib import Path

WRK=Path.cwd()
PATCH=WRK.joinpath("patch")
SRC=WRK.joinpath("SRC")

def path(path:PathLike=getcwd()):
    path = Path(abspath(path))
    cpr(PATCH, SRC)
    pass

def file(path:PathLike=getcwd()):
    path = Path(abspath(path))
    pass

def _logpath(path, names):
    for name in names:
        _path = Path(path).joinpath(name).absolute()
        if not _path.is_dir():
            _rel = _path.relative_to(PATCH)
            _str = str(_path)
            if len(_str)>4 and _str[-4:]=="ptcx":
                print(f"\033[92m[patch] {_rel}\033[0m")
                file(_path)
            else:
                print(f"\033[92m[cp] {_rel}\033[0m")
                
    return []   # nothing will be ignored

def cpr(src, dst):
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=_logpath)
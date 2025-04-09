""""""  # pylint: disable=empty-docstring

from typing import Iterable, Union, Dict
from os import PathLike, getcwd
from os.path import relpath
from pathlib import Path

import subprocess
import traceback
import sys
import os
import shlex
import shutil
import datetime
import logging

import psutil

class CommandFailed(Exception):
    """
    Process returned with exit-code!=0
    """
    def __init__(self, code:int, cmd:Iterable[str]):
        super().__init__(f"Command: {shlex.join(cmd)} failed with exit code {code}")

def fmtpath(path:PathLike, base=getcwd(), _relpath=False) -> str:
    """
    Format path in a readable way
    """
    try:
        if _relpath is True:
            return relpath(str(path), str(base))
        return "./"+str(Path(path).relative_to(base))
    except ValueError:
        return str(path)

def exists_in_PATH(target:str):  # pylint: disable=invalid-name
    """
    if target is a command or exists in path
    """
    # Check if target is a command
    if shutil.which(target):
        return True

    # Check if target is a directory in PATH
    paths = os.environ.get("PATH", "").split(os.pathsep)
    return any(os.path.abspath(target) == os.path.abspath(p) for p in paths)

def exc(*cmd:Iterable[str],dbg:bool=True, _bytes:bool=False,timeout:float=None,
        cwd:PathLike=getcwd(), env:Dict[str, str]=None, _pidx:int=0) -> Union[bytes, str]:
    """
    Executes a process
    """
    if env is None:
        env=os.environ
    stamp = datetime.datetime.now().strftime("%m-%d %H:%M:%S")

    hcmd = list(cmd).copy()

    for i in range(0, _pidx):
        hcmd[i] = fmtpath(hcmd[i],base=cwd, _relpath=False)

    if dbg:
        print(f"\033[94m[EXC {stamp}]\033[0m {shlex.join(hcmd)}")
        stdout = sys.stdout
    else:
        stdout = subprocess.PIPE
    proc = subprocess.Popen(cmd, stdout=stdout, stdin=sys.stdin,
                            stderr=sys.stderr, cwd=cwd, env=env)
    proc.wait(timeout=timeout)
    if proc.returncode != 0:

        raise CommandFailed(proc.returncode, hcmd)
    if proc.stdout:
        if _bytes:
            return proc.stdout.read()
        return proc.stdout.read().decode("utf-8")

def pyexc(*cmd:Iterable[str],dbg:bool=True, _bytes:bool=False,timeout:float=None,
          cwd:PathLike=getcwd(), _pidx:int=0) -> Union[bytes, str]:
    """
    Executes a python file
    """
    return exc(sys.executable, *cmd, dbg=dbg, _bytes=_bytes,
               timeout=timeout, cwd=cwd, _pidx=_pidx+1)

def kill_processes_by_port(port):
    """
    Kills a process by used ports
    """
    killed_any = False

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            conns = proc.net_connections()
        except (PermissionError, psutil.AccessDenied):
            pass
        else:
            for conn in conns:
                if conn.laddr.port == port:
                    try:
                        print(f"Found process with PID {proc.pid} and name {proc.info['name']}")

                        if proc.info['name'].startswith("docker"):
                            print("Found Docker. You might need to stop the container manually")

                        kill_process_and_children(proc)
                        killed_any = True

                    except (PermissionError, psutil.AccessDenied):
                        print(f"Unable to kill process: {proc.name} at {proc.pid}."
                            "The process might be running as "
                            "another user or root. Try again with sudo")
                        print(traceback.format_exc())

                    except Exception: # pylint: disable=broad-exception-caught
                        print(f"Error killing process {proc.pid}:\n"+traceback.format_exc())

    return killed_any

def kill_process_and_children(proc:psutil.Process):
    """
    Kill process and all childred
    """
    children = proc.children(recursive=True)
    for child in children:
        try:
            child.kill()
        except Exception: # pylint: disable=broad-exception-caught
            logging.error(traceback.print_exc())

    proc.kill()

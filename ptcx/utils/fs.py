from pathlib import Path

def readf(_path:Path) -> bytes:
    with open(_path, "a+b") as f:
        f.seek(0)
        return f.read()

def reads(_path:Path) -> str:
    return readf(_path).decode("utf-8")

def writef(content:bytes, _path:Path) -> None:
    with open(_path, "wb") as f:
        return f.write(content)

def writes(content:str, _path:Path) -> None:
    writef(content.encode("utf-8"), _path)

from abc import ABC, abstractmethod
from pathlib import Path

from ptcx.utils.fs import readf, reads, writef, writes

class BasePTC(ABC):
    srcroot:Path
    patchroot:Path
    file:Path

    def __init__(self, file:Path, srcroot:Path, patchroot:Path):
        self.srcroot=srcroot
        self.patchroot=patchroot
        self.file=file

    def _patch(self) -> None:
        self.patch()

    @abstractmethod
    def patch(self) -> None:
        pass

class FPTC(BasePTC):

    content:bytes

    def _patch(self) -> None:
        self.content = readf(self.file)
        super()._patch()
        writef(self.content, self.file)
    
    @abstractmethod
    def patch(self) -> None:
        pass

class SPTC(BasePTC):

    content:str

    def _patch(self) -> None:
        self.content = reads(self.file)
        super()._patch()
        writes(self.content, self.file)
    
    @abstractmethod
    def patch(self) -> None:
        pass

"""""" # pylint: disable=empty-docstring
from abc import ABC, abstractmethod
from pathlib import Path

from ptcx.utils.fs import readf, reads, writef, writes

__str__ = str # pylint: disable=invalid-name
__bytes__ = bytes # pylint: disable=invalid-name

class BasePTC(ABC):
    """
    Example configuration

    .. literalinclude:: ../patch/main.py.ptcx
        :language: python
    """
    srcroot:Path
    """source root directory to patch"""
    patchroot:Path
    """patch root directory, used for specifying patches"""
    file:Path
    """absolute path of the file to patch"""

    _bytes:__bytes__=None
    _str:__str__=None

    def __init__(self, file:Path, srcroot:Path, patchroot:Path):
        self.srcroot=srcroot
        self.patchroot=patchroot
        self.file=file
    
    @property
    def bytes(self) -> bytes:
        """
        content of the file to patch
        """
        if self._str is None:
            if self._bytes is None:
                self._bytes = readf(self.file)
        else:
            self._bytes = self._str.encode("utf-8")
        return self._bytes

    @bytes.setter
    def bytes(self, value):
        self.bytes  # pylint: disable=pointless-statement
        self._bytes = value
    
    @property
    def str(self) -> str:
        """
        file to patch as str
        """
        if self._str is None:
            self._str = self.bytes.decode("utf-8")
            self._bytes = None
        return self._str
    
    @str.setter
    def str(self, value):
        self.str  # pylint: disable=pointless-statement
        self._str = value

    def _patch(self) -> None:
        self.prepatch()
        self.patch()
        self.postpatch()
        writef(self.bytes, self.file)
    
    def prepatch(self):
        """
        Optional prepatch override
        """

    @abstractmethod
    def patch(self) -> None:
        """
        function to impelement for patching
        """

    def postpatch(self):
        """
        optional postpatch override
        """

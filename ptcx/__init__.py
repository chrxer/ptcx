"""""" # pylint: disable=empty-docstring
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Callable
from os import PathLike
import re
from re import Match

from ptcx.utils.fs import readf, writef
from ptcx.utils import langs
from tree_sitter import Parser, Tree

__str__ = str # pylint: disable=invalid-name
__bytes__ = bytes # pylint: disable=invalid-name

class BasePTC(ABC):
    """"""
    srcroot:Path
    """source root directory to patch"""
    patchroot:Path
    """patch root directory, used for specifying patches"""
    file:Path
    """absolute path of the file to patch"""

    _bytes:__bytes__=None
    _lang:__str__=None
    _parser:Parser=None
    _tree:Tree=None

    def __init__(self, file:Path, srcroot:Path, patchroot:Path):
        self.srcroot=srcroot
        self.patchroot=patchroot
        self.file=file
    
    @property
    def bytes(self) -> __bytes__:
        """
        File to patch as bytes based on :py:func:`ptcx.BasePTC.file`.
        Setting it to str will automatically convert it to bytes (utf-8 encoded)
        """
        if self._bytes is None:
            self._bytes = readf(self.file)
        return self._bytes

    @bytes.setter
    def bytes(self, value:Union[__bytes__, str]):
        if isinstance(value, str):
            value = value.encode("utf-8")
        self.bytes  # pylint: disable=pointless-statement
        self._bytes = value

        # indicate that tree has changed
        self._tree = None
    
    @property
    def lang(self):
        """
        (programming) Language of the file to patch based on :py:func:`ptcx.BasePTC.file` and based on :py:func:`ptcx.BasePTC.bytes`.
        """
        if self._lang is None:
            self.lang = self.file
        return self._lang

    @lang.setter
    def lang(self, value:PathLike):
        self._lang = langs.guess(value)
    
    @property
    def parser(self) -> Parser:
        """"
        :py:class:`tree_sitter.Parser` based on :py:func:`ptcx.BasePTC.lang`
        """
        if self._parser is None:
            self._parser = langs.get_parser(self.lang)
        return self._parser
    
    @parser.setter
    def parser(self, value:Parser) -> str:
        assert isinstance(value, Parser)
        self._parser = value
    
    @property
    def tree(self)->Tree:
        """"
        :py:class:`tree_sitter.Tree` based on :py:func:`ptcx.BasePTC.parser`
        """
        if self._tree is None:
            self._tree = self.parser.parse(self.bytes)
        return self._tree

    def _patch(self) -> None:
        self.patch()
        writef(self.bytes, self.file)

    @abstractmethod
    def patch(self):
        """
        function to implement for patching
        """
    
    def insert(self,pattern:Union[str, __bytes__], insert_func:Callable[[Union[__bytes__]], Union[str, __bytes__]]):
        """
        Wraps :py:func:`ptcx.utils.langs.search_and_insert` for :py:func:`ptcx.BasePTC.bytes`.
        """
        self.bytes = langs.search_and_insert(self.bytes, pattern, insert_func)

    def sub(self,pattern:Union[str, __bytes__],repl:Union[str, bytes], **kwargs):
        """
        :py:func:`re.sub` on :py:func:`ptcx.BasePTC.bytes`
        """
        if isinstance(pattern, str):
            pattern = pattern.encode("utf-8")
        if isinstance(repl, str):
            repl=repl.encode("utf-8")
        self.bytes = re.sub(pattern, repl, self.bytes, **kwargs)

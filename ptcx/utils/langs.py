"""
various algorithms//utils for modifying bytes
"""
from os import PathLike
from pathlib import Path
from typing import get_origin, get_args, Annotated, Callable, Union, List
from importlib import import_module
import re

import orjson.orjson
import sourcetypes
from tree_sitter import Parser, Language
import orjson
import pyjson5

# name has to be consistent with https://github.com/chrxer/python-inline-source-3/blob/main/languages.json
LANGFNS={
    "cpp":"tree_sitter_cpp.language",
    "python":"tree_sitter_python.language"
}

def get_parser(lang:str) -> Parser:
    """
    :py:class:`tree_sitter.Parser` based on ``lang``
    """
    mod_path = LANGFNS.get(guess(lang))
    parts = mod_path.split(".")
    module = ".".join(parts[:-1])
    module = import_module(module)
    func = None
    try:
        func = getattr(module, parts[-1])
    except AttributeError:
        pass
    assert callable(func), f"Expected function at: {mod_path}"
    return Parser(Language(func()))

def guess(path:PathLike, content:str=None) -> str:
    """
    guesses the sourcetypes language based on the ``path`` and optionally file ``content``
    """
    extension = str(path).rsplit(".", maxsplit=1)[-1]
    path = Path(path)
    lang = sourcetypes.__dict__.get(extension)
    if get_origin(lang) is not Annotated:
        raise ValueError(f"Language for file: {path.name} not identified")
    
    lang_str = get_args(lang)[2]
    assert isinstance(lang_str, str)
    return lang_str

def search_and_insert(text:bytes, pattern:Union[str, bytes], insert_func:Callable[[Union[bytes]], Union[str, bytes]]) -> bytes:
    """
    finds match & replaces inserts string at first group in pattern.

    :param text: text to insert into
    :param patter: pattern including group to match
    :param insert_func: function with signature ``def insert(_content:bytes) -> str:`` to which the matched section is passed
    """
    if isinstance(pattern, str):
        pattern = pattern.encode("utf-8")
    match = re.search(pattern, text, flags=re.MULTILINE)

    if not match:
        raise ValueError(f"Pattern '{pattern}' not found in the text.")

    start, end = match.span(1)
    matched_text = text[start:end]
    modified_text = insert_func(matched_text)

    if isinstance(modified_text, str):
        modified_text = modified_text.encode("utf-8")
    assert isinstance(modified_text, bytes)
    updated_text = text[:start] + modified_text + text[end:]

    return updated_text

def array_add(matched_text:Union[str, bytes], to_add:List[Union[str, bytes]]) -> bytes:
    """
    extend array inside string. Accepts json5, returns json (with indent_2 and newlines)
    """
    if isinstance(matched_text, bytes):
        matched_text = matched_text.decode("utf-8")
    _list = pyjson5.decode(matched_text) # pylint: disable=no-member
    assert isinstance(_list, list)
    for i,item in enumerate(to_add):
        if isinstance(item, bytes):
            to_add[i]=item.decode("utf-8")

    _list.extend(to_add)
    return orjson.dumps(_list, option=orjson.OPT_APPEND_NEWLINE|orjson.OPT_INDENT_2) # pylint: disable=no-member
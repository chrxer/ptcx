"""
Utils for ast-based patching.

.. warning::
    This only supports C++ with 
    `tree-sitter-cpp <https://github.com/tree-sitter/tree-sitter-cpp>`_ yet
"""
import re
from typing import Dict, List
from tree_sitter import Node, Query, Parser, Tree

from sourcetypes import trs

from ptcx.utils.langs import get_parser



CppFnSignQuery:trs = b"""
[
  (function_definition
    type:( ;; return type
      [
        (primitive_type) @ret_type
        (qualified_identifier
          name:(_) @ret_type
        )
      ]
    ) 
    declarator:(_;; function name
      [
        declarator:(qualified_identifier) @name
        declarator:(identifier) @name
        declarator:(field_identifier) @name
      ]
      parameters: (parameter_list ;; parameters
        (parameter_declaration
          type:(
              [
                (primitive_type) @param_type
                (qualified_identifier
                  name:(_) @param_type
                )
              ]
          )
          declarator:(_) @param_name
        )
      )?
    ) @sign
    body: (compound_statement)? @body
  ) @function
  (declaration
    type:( ;; return type
      [
        (primitive_type) @ret_type
        (qualified_identifier
          name:(_) @ret_type
        )
      ]
    ) 
    declarator:(_;; function name
      [
        declarator:(qualified_identifier) @name
        declarator:(identifier) @name
        declarator:(field_identifier) @name
      ]
      parameters: (parameter_list ;; parameters
        (parameter_declaration
          type:( 
              [
                (primitive_type) @param_type
                (qualified_identifier
                  name:(_) @param_type
                )
              ]
          )
          declarator:(_) @param_name
        )
      )?
    ) @sign
    body: (compound_statement)? @body
  ) @declaration
]
"""

def _get_one(captures:Dict[str, List[Node]], name:str, no_ok:bool=True)->bytes:
    values = captures.get(name)
    if values is None:
        if no_ok:
            return
        raise ValueError(f"{name} not found")
    if len(values)>1:
        raise ValueError(f"More than one {name} found in captures")
    return values[0].text

SignQueries={
    "cpp":CppFnSignQuery
}

class FuncSign():
    """
    Signature of a Cpp function or declaration
    """
    parser:Parser
    """language-specific parser used"""
    query:Query
    """Query which matches any function with this signature"""
    lang_str:str
    """
    language as str, has to be valid for 
    `sourcetypes3 <https://github.com/chrxer/python-inline-source-3>`_
    """
    source:bytes
    """Source code this signature is based on"""
    is_declaration:bool=False
    """If provide source is a declaration, not in fact function"""

    tree:Tree
    """
    AST tree of source
    """

    ret_type:bytes
    """
    Return type of function (excluding scope)
    """
    name:bytes
    """
    Function name (including scope)
    """

    body:bytes
    """
    Body of function provided in source
    """
    _params:List[List[bytes]]=None
    _captures:Dict[str, List[Node]]=None

    def __init__(self,source: bytes, lang_str:str, query_str:str=None):
        if query_str is None:
            query_str = SignQueries[lang_str]
        self.query_str= query_str
        self.parser = get_parser(lang_str)
        self.source = source
        self.lang_str=lang_str
        self.query = Query(self.parser.language, self.query_str)
        self.tree = self.parser.parse(self.source)

        # analyze signaure of provided function in source
        self._captures = self.query.captures(self.tree.root_node)
        if len(self._captures) < 1:
            raise ValueError("No captures found, does the following contain a function in"
                             f" {lang_str}?: {self.source.decode('utf-8', errors='replace')}")

        self.name = _get_one(self._captures,"name")
        self.ret_type = _get_one(self._captures,"ret_type")
        sign= _get_one(self._captures, "sign")

        self.body= _get_one(self._captures, "body", no_ok=True)
        if self.body is None:
            self.body = b''
        else:
            self.body = self.body[1:-1]

        self.source = _get_one(self._captures,"function", no_ok=True)
        if self.source is None:
            self.source = _get_one(self._captures, "declaration")
            self.is_declaration = True

        # create new tree-sitter query for signature
        raw_sign = re.escape(sign)

        # \s => \s*
        re_sign=re.sub(rb"\\\s+", rb"\\s*", raw_sign)

        # spaces around ","
        re_sign=re.sub(rb",", rb"\\s*,\\s*", re_sign)

        # spaces around "(" or ")"
        re_sign=re.sub(rb"\\\(", rb"\\s*\\(\\s*", re_sign)
        re_sign=re.sub(rb"\\\)", rb"\\s*\\)\\s*", re_sign)

        # escape for " quotes
        re_sign=re.sub(rb'([\\"])', rb'\\\1', re_sign)
        ret_type=re.sub(rb'([\\"])', rb'\\\1', self.ret_type)

        # place match statement in query
        statement=b'\n(#match? @sign "'+re_sign+b'")\n(#match? @ret_type "'+ret_type+b'")\n'

        # inject match statement into query
        query_str=self.query_str
        matches = list(re.finditer(rb'(\)\s+(@declaration|@function)\s+)', query_str))
        # Reverse to avoid changing indices while modifying the string
        for match in reversed(matches):
            before_match = query_str[:match.start(1)]
            after_match = query_str[match.end(1):]
            query_str = before_match + match.group(1) + statement + after_match

        self.query = Query(self.parser.language, query_str)

    @property
    def params(self) -> List[List[bytes]]:
        """
        Parameters in the form

        .. code-block: python
            [
                [type_name, name],
                ...
            ]
        """
        if self._params is None:
            self._params = []
            for args in zip(
                    self._captures.get("param_type",[]),
                    self._captures.get("raw_param_name", [])
                ):
                args = tuple(arg.text for arg in args)

                self._params.append(args)
        return self._params

    def rplace(self, node:Node):
        """
        Place :py:attr:`ptcx.FuncSign.ast.body` in other node at same or similar function signature.
        """
        new_body = self.body
        body = self.query.captures(node)["body"]
        assert len(body) == 1
        body = body[0]
        start, end = body.start_byte, body.end_byte
        return node.text[:start] + b"{\n" + new_body + b"\n}" + node.text[end:]

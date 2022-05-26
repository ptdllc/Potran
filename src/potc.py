import sys
from typing import List
from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta
this_module = sys.modules[__name__]
if len(sys.argv) != 2: print("Usage: python3 compiler.py <file>"); exit()
fileExtensions = [".p22", ".p", ".ptrn", ".pt"]
validFileExtension = False
for i in fileExtensions: 
    if sys.argv[1].endswith(i): validFileExtension = True 
if not validFileExtension: print("Valid file extensions: .p22 | .p | .ptrn | .pt"); exit()
class _Ast(ast_utils.Ast): pass
class _Statement(_Ast): pass
@dataclass
class Value(_Ast, ast_utils.WithMeta): "Uses WithMeta to include line-number metadata in the meta attribute"; meta: Meta; value: object
@dataclass
class Print(_Statement): value: Value
class ToAst(Transformer):
    def STRING(self, s): return s[1:-1]
    def DEC_NUMBER(self, n): return int(n)
    @v_args(inline=True)
    def start(self, x): return x
parser = Lark(r'''
    start: code_block
    code_block: statement+
    ?statement: program | function | outputline | return
    type: "Integer8" | "Integer16" | "Integer32" | "Integer64" 
        | "Unsigned8" | "Unsigned16" | "Unsigned32" | "Unsigned64"
        | "String" | "Char" |
        | "Boolean"
    value: NAME | STRING | DEC_NUMBER
    params: WORD "," params

    program: "Program" NAME "{" code_block "};"
    function: WORD type "::" "Function" NAME "(" params? ")" "{" code_block "};"
    outputline: "OutputLine" value ";"
    return: "Return" value ";"

    %import python (NAME, STRING, DEC_NUMBER)
    %import common (WS, WORD)
    %ignore WS
''', parser="lalr")
transformer = ast_utils.create_transformer(this_module, ToAst())
def parse(text):
    tree = parser.parse(text)
    return transformer.transform(tree)
contents = str()
with open(sys.argv[1]) as file:
    for line in file.readlines():
        contents += line 
print(parse(contents))
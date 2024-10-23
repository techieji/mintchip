import lark
from lark.visitors import Transformer

grammar = '''
start : stmt (NEWLINE+ stmt)*
stmt : "(" stmt ")"      -> paren
     | NUMBER            -> num
     | NAME                    -> get_var
     | stmt "^" stmt     -> exp
     | stmt "*" stmt     -> mul
     | stmt "/" stmt     -> div
     | stmt "+" stmt     -> add
     | stmt "-" stmt     -> sub
     | NAME (":" | "=") stmt   -> set_var
     | NAME "(" [ stmt ("," stmt)* ] ")" (":" | "=") stmt -> set_fn
     | NAME "(" [ stmt ("," stmt)* ] ")"                  -> func_call
     | stmt*  -> stmt_list

%import common.CNAME     -> NAME
%import common.WS_INLINE -> WS_INLINE
%import common.NEWLINE   -> NEWLINE
%import common.NUMBER    -> NUMBER
%ignore WS_INLINE
'''.strip()

parser = lark.Lark(grammar)

print(parser.parse("sin (x + y)\nx").pretty())

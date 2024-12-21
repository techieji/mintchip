import re
from functools import wraps
from collections import namedtuple
import base64 as b64

chip = namedtuple('chip', 'regex fn color')

def to_re(s):
    s = r'\s*'.join(map(re.escape, s.split()))
    s = re.sub(r'(?<!<)<([a-z]+)>', r'(?P<\1>(?:[+-]?([0-9]*[.])?[0-9]+)|<~.*~>|@)', s)
    s = re.sub(r'<<([a-z]+)>>', r'(?P<\1>.+)', s)
    return r'({})'.format(s)

rules = []

def add_chip(regex, fn, color=''):
    rules.insert(0, chip(regex, fn, color))

def to_number(s):
    try: r = int(s)
    except: r = float(s)
    return r

def register(regex, macro=False, color='\033[31m'):
    def dec(f):
        @wraps(f)
        def fn(m):
            return str(f(**{k: (str.strip if macro else to_number)(v) for k, v in m.groupdict().items()}))
        fn.macro = macro
        rules.append(chip(to_re(regex), fn, color))
        return fn
    return dec

@register('<<l>> = <<r>>', macro=True)
def assign(l, r):
    if l.strip():
        add_chip(to_re(l), lambda m: evaluate(r, [chip(*x, '') for x in m.groupdict().items()] + rules))

# Actual mathematical functions
import math
import inspect
for x in [x for x in dir(math) if x[0] != '_']:
    if x in ['e']: continue
    fn = getattr(math, x)
    try:
        if callable(fn):
            #nargs = len(inspect.signature(fn).params)
            args = inspect.signature(fn).parameters.keys()
            css = ', '.join(map('<{}>'.format, args))
            css2 = ', '.join(args)
            register(x + '(' + css + ')')(eval(f'lambda {css2}, fn=fn: fn({css2})'))
            #register(x + '(<<args>>)')(lambda args, fn=fn: fn(*map(float, args.split(','))))
        else:
            register(x)(lambda fn=fn: fn)
    except:
        print('no', x)

@register('( <l> )')
def paren(l): return l
@register('<l> ^ <r>', color='\033[31m')
def mul(l, r): return l ** r
@register('<l> * <r>', color='\033[31m')
def mul(l, r): return l * r
@register('<l> / <r>', color='\033[31m')
def div(l, r): return l / r
@register('<l> + <r>', color='\033[33m')
def add(l, r): return l + r
@register('<l> - <r>', color='\033[33m')
def add(l, r): return l - r


def evaluate(s, rules, syntax=False):
    n = 1
    while n != 0:
        for c in rules:
            if syntax:
                s, n = re.subn(c.regex, '@', s)
            else:
                s, n = re.subn(c.regex, c.fn, s)
            if n != 0: break
        #print(n, s)
    return s

def eval_drop_in(s, syntax=False):
    return evaluate(s, rules, syntax=syntax)

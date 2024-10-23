import re
from functools import wraps
from collections import namedtuple
import base64 as b64

chip = namedtuple('chip', 'regex fn color')

def to_re(s):
    s = r'\s*'.join(map(re.escape, s.split()))
    # re.findall(r'\033\[.+?m.*\033\[.+?m', s)
    s = re.sub(r'(?<!<)<([a-z]+)>', r'(?P<\1>[0-9]+|<~.*~>)', s)
    s = re.sub(r'<<([a-z]+)>>', r'(?P<\1>.+)', s)
    # print(s)
    return r'({})'.format(s)

rules = []

def add_chip(regex, fn, color=''):
    #for i, c in enumerate(rules):
    #    if c.regex == regex:
    #        del rules[i]
    #        break
    rules.insert(0, chip(regex, fn, color))

def register(regex, macro=False, color='\033[31m'):
    def dec(f):
        @wraps(f)
        def fn(m):
            return str(f(**{k: (str.strip if macro else int)(v) for k, v in m.groupdict().items()}))
        fn.macro = macro
        rules.append(chip(to_re(regex), fn, color))
        return fn
    return dec

@register('<<l>> = <<r>>', macro=True)
def assign(l, r):
    if l.strip():
        add_chip(to_re(l), lambda m: evaluate(r, [chip(*x, '') for x in m.groupdict().items()] + rules))

@register('( <l> )')
def paren(l): return l
@register('<l> * <r>', color='\033[31m')
def mul(l, r): return l * r
@register('<l> + <r>', color='\033[33m')
def add(l, r): return l + r

def evaluate(s, rules, syntax=False):
    n = 1
    while n != 0:
        for c in rules:
            if syntax:
                n = 0
                if not c.fn.macro:
                    s, n = re.subn(c.regex, lambda m, c=c.color: '<~' + b64.b32encode(f'{c}{m.group(1)}\033[0m'.encode()).decode() + '~>', s)
            else:
                s, n = re.subn(c.regex, c.fn, s)
            if n != 0: break
        #print(n, s)
    return s

def eval_drop_in(s):
    return evaluate(s, rules)

#s = evaluate('inc <a> = (a + 1)', reversed(rules), syntax=True)
#s = evaluate('inc <a> = inc a', (rules))
#print(s)
#n = 1
#while n != 0:
#    s, n = re.subn('<~(.*)~>', lambda m: b64.b32decode(m.group(1).encode()).decode(), s)
#print(s)

if __name__ == '__main__':
    print(evaluate('a = 1', rules))
    print(evaluate('', rules))
    print(evaluate('a', rules))

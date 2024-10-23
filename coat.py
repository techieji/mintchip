import curses
import itertools as it
import lark

class box:
    def __init__(self):
        self.s = [[]]
        self.cursor = [0, 0]
    @property
    def lengths(self): return list(it.accumulate(map(len, self.s)))
    @property
    def cursorn(self): return sum(self.lengths[:self.cursor[0]]) + self.cursor[1]
    @cursorn.setter
    def cursorn(self, n):
        l = list(it.takewhile(lambda x: x <= n, self.lengths))
        self.cursor = [len(l), n - l[-1]]
    def ins(self, c):
        self.s[self.cursor[0]].insert(self.cursor[1], c)
        self.move(0, 1)
    def move(self, y, x):
        self.cursor[0] = max(min(self.cursor[0] + y, len(self.s) - 1), 0)
        self.cursor[1] += x
        if y == 0:
            if self.cursor[1] < 0:
                self.cursor[0] = max(min(self.cursor[0] - 1, len(self.s) - 1), 0)
                self.cursor[1] = len(self.s[self.cursor[0]])
                return
            elif self.cursor[1] > len(self.s[self.cursor[0]]):
                self.cursor[0] = max(min(self.cursor[0] + 1, len(self.s) - 1), 0)
                self.cursor[1] = 0
                return
        self.cursor[1] = max(min(self.cursor[1], len(self.s[self.cursor[0]])), 0)
    def delete(self):
        try:
            if self.cursor[1] >= len(self.s[self.cursor[0]]):
                self.s[self.cursor[0]].extend(self.s[self.cursor[0] + 1])
                del self.s[self.cursor[0] + 1]
            else:
                del self.s[self.cursor[0]][self.cursor[1]]
        except IndexError: pass
    def backspace(self):
        self.move(0, -1)
        self.delete()
    def enter(self):
        self.ins('\n')
        self.s = [list(x) for x in '\n'.join(map(''.join, self.s)).split('\n')]
        self.cursor[0] += 1
        self.cursor[1] = 0
    def to_string(self):
        return '\n'.join(map(''.join, self.s))
    def evaluate(self):
        def _eval(s):
            try:
                return str(eval(s))
            except:
                return ''
        l = list(map(_eval, map(''.join, self.s)))
        m = max(map(len, l))
        return [x.rjust(m) for x in l]

def main(stdscr):
    b = box()
    while True:
        c = stdscr.getkey()
        if c == 'KEY_BACKSPACE': b.backspace()
        elif c == 'KEY_LEFT': b.move(0, -1)
        elif c == 'KEY_RIGHT': b.move(0, 1)
        elif c == 'KEY_UP': b.move(-1, 0)
        elif c == 'KEY_DOWN': b.move(1, 0)
        elif c == 'KEY_HOME': b.cursor[1] = 0
        elif c == 'KEY_END': b.cursor[1] = len(b.s[b.cursor[0]])
        elif c.startswith('KEY_'): pass
        elif c == '\n': b.enter()
        else: b.ins(c)
        stdscr.erase()
        stdscr.addstr(0, 0, b.to_string())         # TODO support color codes
        l = b.evaluate()
        for i, line in enumerate(l):
            stdscr.addstr(i, stdscr.getmaxyx()[1] - len(l[0]) - 5, line)
        stdscr.move(*b.cursor)

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass

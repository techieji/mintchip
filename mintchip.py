#!/usr/bin/python
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label, Rule, TextArea, Static
from textual.reactive import reactive
from difflib import SequenceMatcher
import itertools as it

import lang2
from lang2 import eval_drop_in

r = lang2.rules

def safe_eval(s, syntax=False):
    try:
        res = eval_drop_in(s, syntax=syntax)
        if str(res) == 'None': return s
        else: return str(res)
    except:
        return ''

def highlight(original, calc):
    l = SequenceMatcher(lambda x: x in ' \n\t', original, calc).get_matching_blocks()
    matching = [calc[m.b:m.b+m.size] for m in l]
    nonmatching = [calc[m1.b+m1.size:m2.b] for m1, m2 in zip(l, l[1:])]
    return ''.join(it.chain.from_iterable(zip(matching, it.repeat('[red]'), nonmatching, it.repeat('[/]'))))

class Evaluation(Static):
    text = reactive("")

    def on_mount(self) -> None:
        self.set_interval(1/60, self.update_text)

    def update_text(self) -> None:
        global ta
        lang2.rules = r.copy()
        t1 = (safe_eval(x, syntax=0) for x in ta.text.split('\n'))
        t2 = (safe_eval(x, syntax=1) for x in ta.text.split('\n'))
        self.text = '\n'.join(highlight(' ' + x2, ' ' + x1)[1:] for x1, x2 in zip(t1, t2))

    def watch_text(self, text: str) -> None:
        self.update(text)

class Coat(App):
    CSS_PATH = "style.css"
    BINDINGS = [('escape', 'done()', 'Save and quit'), ('^s', 'save()', 'Save')]

    def compose(self) -> ComposeResult:
        global ta
        try:
            with open('scratchpad') as f:
                s = f.read()
        except FileNotFoundError:
            s = ''
        with Horizontal():
            # ta = TextArea.code_editor('', language='python')
            ta = TextArea(s)
            # ta.show_line_numbers = False
            yield ta
            yield Rule(orientation="vertical", line_style="double")
            yield Evaluation()

    def action_save(self):
        with open('scratchpad', 'w') as f:
            f.write(ta.text)

    def action_done(self):
        self.action_save()
        exit(0)

if __name__ == "__main__":
    app = Coat()
    app.run()

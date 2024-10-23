from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label, Rule, TextArea, Static
from textual.reactive import reactive
from pprint import pprint
import copy

import lang2
from lang2 import eval_drop_in

r = lang2.rules

def safe_eval(s):
    try:
        res = eval_drop_in(s)
        if res != None: return str(res)
        else: return ''
    except:
        return ''

class Evaluation(Static):
    text = reactive("")

    def on_mount(self) -> None:
        self.set_interval(1/60, self.update_text)

    def update_text(self) -> None:
        global ta
        lang2.rules = r.copy()
        self.text = '\n'.join(map(safe_eval, ta.text.split('\n')))

    def watch_text(self, text: str) -> None:
        self.update(text)

class Coat(App):
    CSS_PATH = "style.css"
    def compose(self) -> ComposeResult:
        global ta
        with Horizontal():
            # ta = TextArea.code_editor('', language='python')
            ta = TextArea('')
            # ta.show_line_numbers = False
            yield ta
            yield Rule(orientation="vertical", line_style="double")
            yield Evaluation()

if __name__ == "__main__":
    app = Coat()
    app.run()

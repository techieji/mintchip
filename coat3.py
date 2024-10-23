import curses
from curses.textpad import Textbox
from time import sleep

def main(stdscr):
    scr = stdscr.subwin(0, 0)
    txt = Textbox(scr)
    txt.edit()

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass

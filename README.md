# Mintchip

So basically this is like Numi, which I wanted, but couldn't install. In the process,
I made this app which has some interesting capabilities.

## Features

- Calculator: it's a damn calculator, bro. It does math.
- Regex-based language: uses term rewriting. Upshot: it's insanely flexible.
- Easily extensible: you can just add a function to `lang2.py` and it should work.

## Usage

Obviously, this is not the interface: the answers are highlighted in red.

```
1 + 1           # => 2
a = 1 + 1       # => a = 1 + 1
a               # => 2
a * 10          # => 20
fn <i> = 2*i    # => fn <i> = 2*i
fn a            # => 4
```

And so on.

The scratchpad is persistent, so exiting with the escape key or saving with Ctrl-S
and leaving however should allow you to access the stuff in the scratchpad the next
time you open up the calculator.

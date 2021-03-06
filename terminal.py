"""
terminal.py: Responsible for GUI and input handling
Contributors: Andrew Combs
"""

import os
import sys
from datetime import datetime
import time
import random


# might remove the D in front of all the names but for now it helps with making it not generic
class DTheme(object):
    def __init__(self, default: tuple, log: tuple, error: tuple):
        self.default = default  # (input symbol, input text, default text)
        self.log = log  # (brackets, info, message)
        self.error = error  # (header, main message, secondary)
        return


# Pain
class DColors(object):
    black = u"\u001b[30m"
    bblack = u"\u001b[30;1m"
    bg_black = u"\u001b[40m"
    bg_bblack = u"\u001b[40;1m"

    red = u"\u001b[31m"
    bred = u"\u001b[31;1m"
    bg_red = u"\u001b[41m"
    bg_bred = u"\u001b[41;1m"

    green = u"\u001b[32m"
    bgreen = u"\u001b[32;1m"
    bg_green = u"\u001b[42m"
    bg_bgreen = u"\u001b[42;1m"

    yellow = u"\u001b[33m"
    byellow = u"\u001b[33;1m"
    bg_yellow = u"\u001b[43m"
    bg_byellow = u"\u001b[43;1m"

    blue = u"\u001b[34m"
    bblue = u"\u001b[34;1m"
    bg_blue = u"\u001b[44m"
    bg_bblue = u"\u001b[44;1m"

    magenta = u"\u001b[35m"
    bmagenta = u"\u001b[35;1m"
    bg_magenta = u"\u001b[45m"
    bg_bmagenta = u"\u001b[45;1m"

    cyan = u"\u001b[36m"
    bcyan = u"\u001b[36;1m"
    bg_cyan = u"\u001b[46m"
    bg_bcyan = u"\u001b[46;1m"

    white = u"\u001b[37m"
    bwhite = u"\u001b[37;1m"
    bg_white = u"\u001b[47m"
    bg_bwhite = u"\u001b[47;1m"

    bold = u"\u001b[1m"
    underline = u"\u001b[4m"
    reverse = u"\u001b[7m"
    reset = u"\u001b[0m"

    def rgb(r, g, b, bg=False) -> str:
        color = (f"\033[48;2;{r};{g};{b}m" if bg else f"\033[38;2;{r};{g};{b}m")
        return color


# TODO: actually code, better function explanations
class DTerminal(object):

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def __init__(self, theme: DTheme):
        self.theme = theme

        self.buffer = []

        # for windows this is required to get escape codes to work
        self.clear()

        return

    def cloc(self, x: int, y: int) -> str:
        """
        Changes cursor location.
        """
        return f"\033[{y};{x}H"

    # Prompts user input
    def prompt(self) -> str:
        # TODO: put long references into local variables
        dft = self.theme.default
        rst = DColors.reset
        inp = input(f"{rst + dft[0]}>{rst + dft[1]} ")
        print(DColors.reset)
        return inp

    # Prints at a location
    # TODO: UPDATE ALL THE OTHER FUNCTIONS SO THAT DEFAULT PARAMETERS AND FUNCTIONS ARE THERE
    def disp(self, title: str, message: str):
        dft = self.theme.default
        rst = DColors.reset
        if str != "": print(f"{dft[2]}{DColors.reverse}{title}{rst}")
        print(f"{dft[2]}{message}{rst}")
        return

    # Logs using vital info
    def log(self, message: str):
        log = self.theme.log
        rst = DColors.reset
        now = datetime.now()
        # TODO: find a better way of doing this
        print(
            f"{rst + log[0]}[{rst + log[1]}{now.hour}:{now.minute}:{now.second}{rst + log[0]}]{rst}{log[2]}: {message + rst}")
        return

    def error(self, message: str, secondary: str=""):
        err = self.theme.error
        rst = DColors.reset
        print(f"{rst + err[0]}ERROR:{rst + err[1]} {message + rst}")
        print(f"{rst + err[2] + str(secondary) + rst}\n")
        return

    # Draws a sprite at a location
    def sprite_draw(self, x: int, y: int, sprite: list, style: str=""):
        for i, line in enumerate(sprite):
            print(style + self.cloc(x=x, y=(y + i)) + line)
        return

    # Puts a header at the top of the screen
    def header(self, header: str, formatting: str):
        print(f"{formatting}{self.cloc(0, 0)}{header}{self.cloc(0, 1)}{DColors.reset}\n")

    def startup(self):
        """
        Purely visual thing, just because it looks cool (MAY BECOME LEGACY)
        """
        load = "Loading..."
        print(DColors.bgreen + DColors.bold)
        for i, c in enumerate(load):
            print(self.cloc(1 + i, 0) + c)
            time.sleep(.02)

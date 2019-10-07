#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et:
"""
This is documentation for the *module* (the whole file)
"""


def main(args):
    """
    main() Needs more stuff here, in real life.
    """
    # Prints a sentence in a centered "box" of correct width

    screen_width = getTerminalSize()[0]
    print(getTerminalSize()[0])
    sentence = input("Sentence: ")
    text_width = len(sentence)
    box_width = text_width + 6
    left_margin = (screen_width - box_width) // 2
    print()
    print(" " * left_margin + "+" + "-" * (box_width - 4) + "+")
    print(" " * left_margin + "| " + " " * text_width + " |")
    print(" " * left_margin + "| " + sentence + " |")
    print(" " * left_margin + "| " + " " * text_width + " |")
    print(" " * left_margin + "+" + "-" * (box_width - 4) + "+")
    print()
    return 0


def getTerminalSize():
    import os

    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os

            cr = struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234"))
        except:
            return
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get("LINES", 25), env.get("COLUMNS", 80))

        ### Use get(key[, default]) instead of a try/catch
        # try:
        #    cr = (env['LINES'], env['COLUMNS'])
        # except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
    sys.exit(0)

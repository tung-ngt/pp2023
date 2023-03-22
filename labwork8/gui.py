import curses

#init gui

STDSCR = None
TERM_WIDTH = 0
TERM_HEIGHT = 0
GREEN = None
WHITE_ON_BLACK = None
BLACK_ON_WHITE = None

def __init_gui():
    """Init curses module"""
    global STDSCR
    global TERM_HEIGHT
    global TERM_WIDTH
    global BLACK_ON_WHITE
    global WHITE_ON_BLACK
    global GREEN
    STDSCR = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    TERM_WIDTH = curses.COLS
    TERM_HEIGHT = curses.LINES
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    BLACK_ON_WHITE = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN = curses.color_pair(2)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    WHITE_ON_BLACK = curses.color_pair(3)

__init_gui()

def deintialize_gui():
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def refresh(win = None):
    """Refresh a window
    
    Parameters
    ----------
    win : optional the window to refresh (default stdscr)
    """
    
    if win:
        win.refresh()
    else:
        STDSCR.refresh()

def clear_screen(win = None):
    """Clear the screen of a window
    
    Parameters
    ----------
    win : optional the window to clear screen (default stdscr)
    """

    if win:
        win.clear()
    else:
        STDSCR.clear()

def clear_win(win):
    """Delete the window
    
    Parameters
    ---------
    win : the window to delete
    """
    del win
    STDSCR.touchwin()
    STDSCR.refresh()
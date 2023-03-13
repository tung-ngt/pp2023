from curses.textpad import rectangle, Textbox
import curses
from output import *
from gui import *

def move_cursor(y, x):
    """Move the cursor to y, x cordinates"""
    curses.setsyx(y, x)

def box(prompt, y, x, height, width, parent_y = 0, parent_x = 0, next_y_reference=[0]):
    """Display a input box
    
    Parameters
    ----------
    prompt : the text prompt
    y : y position of the box
    x : x position of the box
    height : height of the the box
    width : width of the box
    parent_y : if specified set y orgin to parent_y (default 0)
    parent_x : if specified set x orgin to parent_x (default 0)
    next_y_reference : optional the list [y] reference

    Return (text, clear_box)
    ---------
    text : the input the user entered
    clear : function to delelte the box
    """

    clear_text = fixed_text("Ctrl + G to exit any text box", TERM_HEIGHT - 1, 0)     
    box_win = curses.newwin(height + 4, max(len(prompt), width) + 3, y + parent_y, x + parent_x)
    box_win.addstr(prompt)
    rectangle(box_win, 1, 0, height + 2, width + 2)
    textbox_win = box_win.subwin(height, width + 1, 2 + y + parent_y , 1 + x + parent_x)
    textbox = Textbox(textbox_win)
    STDSCR.refresh()
    box_win.refresh()
    textbox.edit()
    
    next_y_reference[0] += height+4

    def clear():
        clear_text()
        clear_win(box_win)

    return textbox.gather(), clear

def wait():
    """Wait for a key and return it"""
    return STDSCR.getkey()
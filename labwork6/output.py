from curses.textpad import rectangle, Textbox
import curses
from gui import *

def row(cells, next_y_reference):
    """Print a table row
    
    Parameters:
    cells : [(text, width),] list contain tupples of text and width
    next_y_reference : y reference to list [y] cordinate of the row

    Return next_row_y
    """
    i = 0
    for cell in cells:
        print_text(str(cell[0]), cords=(next_y_reference[0]+1,i+1))
        rectangle(STDSCR, next_y_reference[0], i, 2 + next_y_reference[0], cell[1] + i)
        i += cell[1]

    refresh()
    next_y_reference[0] += 2


def description_box(title, description, cords=(0,0)):
    """Print a description box with title
    
    Parameters
    ----------
    title : the title string
    description : the desciption in the box
    cords : (y,x) cords of the box (default: 0, 0)
    """

    des_text = description.splitlines()[1:]
    height = len(des_text)
    width = max([len(line) for line in des_text])
    des_win = curses.newwin(height + 4, width + 4, cords[0], cords[1])
    print_text(title + "\n", color=GREEN, parent=des_win)
    
    for index, line in enumerate(des_text):
        print_text(line, cords=(index+2, 2), parent=des_win)

    rectangle(des_win, 1, 0, height + 2, width + 3)
    refresh(des_win)
    def clear():
        clear_win(des_win)

    return clear


def print_text(text, parent = None, cords = None, color = None):
    """Print a string to the screen
    
    Parameters
    ----------
    text : the string to print
    parent : if specified the screen to print on (default stdscr)
    cords : tupple (y, x) if specified the cords to print on (default: append)
    color : color of the text (default: white)
    """
    screen = None
    if not parent:
        screen = STDSCR
    else:
        screen = parent
    
    text_color = color if color else WHITE_ON_BLACK
    if cords:
        screen.addstr(cords[0], cords[1], text, text_color)
    else:
        screen.addstr(text, text_color)
    refresh(screen)

def fixed_text(text, y, x):
    """Display a input box
    Parameters
    ----------
    text : the text string
    y : y position of the text
    x : x position of the text
    Return (clear)
    ---------
    clear : clear the text
    """

    win = curses.newwin(1, len(text) + 2, y, x)
    refresh()
    win.addstr(text)
    refresh(win)

    def clear():
        clear_win(win)

    return clear 
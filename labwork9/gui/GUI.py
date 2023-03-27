import tkinter as tk
from tkinter.font import Font as tkFont
import os
from .Screen import Screen
from .Navbar import Navbar
from .Label import Label
class GUI(tk.Tk):
    """GUI app class"""
    def __init__(self, 
            title, 
            geometry="800x600", 
            resizable=(True, True),
            fullscreen=False,
            min_size=(0,0), 
            icon=None,
            fonts = {},
            on_close=None
        ):
        """Init gui
        
        Parameters
        ----------
        title : title of the window
        geometry : initial geometry of the window string "{width}x{height}" default "800x600"
        resizable : if the window can change size (width, height) default (False, False)
        fullscreen : bool if the app is fullscreen (default False)
        min_size : (width: int, height: int)
        icon : path to icon default None
        fonts : fonts that is used in the app
        on_close : None
        """
        super().__init__()
        self.title(title)

        if fullscreen:
            self.state("zoomed")
            self.resizable(True, True)
        else:
            self.geometry(geometry)
            self.resizable(resizable[0], resizable[1])
            self.minsize(min_size[0], min_size[0])

        if os.path.isfile(icon):
            self.iconphoto(True, tk.PhotoImage(file=icon))
        
        if on_close != None:
             self.protocol("WM_DELETE_WINDOW", lambda: self.on_exit(on_close))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=150)
        self.grid_columnconfigure(1, weight=20)
        self.screens: dict[str, Screen] = {}
        self.current_screen: str = None
    def on_exit(self, fun):
        """On close window
        
        Parameter
        ---------
        Fun : function to run when close
        """
        fun()
        self.destroy()

    def init_navbar(self, navbar: Navbar):
        """Add navbar and place it in root window"""    
        self.navbar = navbar
        self.navbar.grid(row=0,column=0, sticky=tk.NSEW)

    def add_screen(self, screen_name: str, screen: Screen):
        """Add screen to the app
        
        Parameters
        ----------
        screen_name : name of the screen,
        screen : the screen
        """
        self.screens[screen_name] = screen

    def change_screen(self, screen_name: str):
        """Change screen to a specified screen"""
        self.hide_screen(self.current_screen)
        self.show_screen(screen_name)

    def hide_screen(self, screen_name: str):
        """Hide a screen"""
        self.screens[screen_name].grid_forget()
    
    def show_screen(self, screen_name: str):
        """Show a screen"""
        self.screens[screen_name].grid(row=0, column=1, sticky=tk.NSEW)
        self.current_screen = screen_name
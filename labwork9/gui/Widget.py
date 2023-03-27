import tkinter as tk

class Widget():
    def __init__(self, widget) -> None:
        """Initialize the widget
        
        Every widget subclass must have a root_widget

        Parameters
        ----------
        root_widget : the root widget
        """
        self.root_widget = widget


    
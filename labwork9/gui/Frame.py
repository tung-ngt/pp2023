from tkinter import Frame as tkFrame
from .Widget import Widget

class Frame(tkFrame):
    """Wrapper around tkFrame"""
    def __init__(self,
            master,
            width: int = 400,
            height: int = 400,
            background = "white"
        ):
        """Init the frame
        
        Parameters
        ----------
        master : master widget
        width : int default 400
        height : int default 400
        background : background color default white
        """
        super().__init__(
            master,
            width=width,
            height=height,
            background=background
        )
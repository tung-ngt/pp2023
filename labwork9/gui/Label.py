from tkinter import Label as tkLabel
from tkinter.font import Font
class Label(tkLabel):
    """Custom Label"""
    def __init__(self,
            master,
            text: str="",
            foreground="black",
            background="white",
            image= None
        ):
        """Init the label
        
        Parameters
        ----------
        master : master widget,
        text : str text
        foreground : text color (default black)
        background : background color (default white)
        justify : text align (left, center, right) (default center)
        """
        if image:
            super().__init__(
                master,
                image=image,
                background=background,
            )
        else:
            super().__init__(
                master,
                text=text,
                background=background,
                foreground=foreground,
            )
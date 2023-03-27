from gui import Screen, Label
from constants import COLORS
from tkinter import PhotoImage

class MainScreen(Screen):
    def __init__(self, master):
        """Init screen"""
        super().__init__(master, COLORS.WHITE)

        self.logo_image = PhotoImage(file="./images/graduation.png")
        self.image_label = Label(self, image=self.logo_image, background=COLORS.WHITE)
        self.image_label.pack()
        self.app_name = Label(self, "Student Mark Management App", background=COLORS.WHITE)
        self.app_name.pack()
        

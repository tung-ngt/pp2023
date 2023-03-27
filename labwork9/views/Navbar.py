from labwork9.gui import Navbar as guiNav
from labwork9.constants import COLORS

class Navbar(guiNav):
    def __init__(self, master, links: list[tuple[str, str]], redirect_funtion):
        super().__init__(master, COLORS.BLACK, links, COLORS.WHITE, redirect_funtion)
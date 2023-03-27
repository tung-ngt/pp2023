from gui import GUI
from views import MainScreen, Navbar, StudentScreen, CourseScreen, MarkScreen
from constants import COLORS
from controllers import StudentMarkController
class ManagementApp(GUI):
    def __init__(self):
        """Initialize GUi"""
        self.studentMarkController = StudentMarkController()
        super().__init__(
            "Student mark management system",
            resizable=(True, True), 
            geometry="1200x900",
            icon="./images/graduation.png",
            on_close=self.studentMarkController.quit
        )

        self.init_navbar(Navbar(self, 
            [
                ("home", "Home"), 
                ("student", "Student"),
                ("course", "Course"),
                ("mark", "Mark")
            ],
            self.change_screen
        ))
        self.add_screen("home", MainScreen(self))
        self.add_screen("student", StudentScreen(self, self.studentMarkController))
        self.add_screen("course", CourseScreen(self, self.studentMarkController))
        self.add_screen("mark", MarkScreen(self, self.studentMarkController))

        self.show_screen("home")

        
if __name__ == "__main__":
    m = ManagementApp()
    m.mainloop()
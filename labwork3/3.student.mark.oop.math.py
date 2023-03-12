from math import floor
import numpy as np
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from time import sleep

class InputAndListable:
    """Abstract class that can input and list"""

    def input(self, reserved_ids = [], reserved_names = [], **kwargs):
        print("can input")

    def list(self):
        print(self)

class Student(InputAndListable):
    """Represent student object
    
    Attributes
    ----------
    id, name, dob
    """

    def __init__(self):
        self.id = ""
        self.name = ""
        self.dob = ""
        self.marks = Mark()

    def __str__(self):
        return f"Student (id: {self.id}) {self.name}, dob: {self.dob}"
    
    def input(self, reserved_ids = [], reserved_names=[], **kwargs):
        id = ""
        box = None
        if "box" in kwargs.keys():
            box = kwargs["box"]
            clear_id = None
            while True:

                id, clear_id = box("ID:", 0, 0, 1, 10, 4, 0)

                if id not in reserved_ids:
                    break
                else:
                    clear_id()
            self.id = id
            self.name, clear_name = box("Name:", 4, 0, 1, 20, 4, 0)
            self.dob, clear_dob = box("DoB:", 8, 0, 1, 10, 4, 0)
            clear_id()
            clear_name()
            clear_dob()
        else:
            while True:
                id = input("ID: ")
                if id not in reserved_ids:
                    break
            self.id = id
            self.name = input("Name: ")
            self.dob = input("DoB: ")

        return id
    
    def list(self, print_function = None, next_row_y = [0]):
        if print_function:
            print_function([(self.id, 10), (self.name, 20), (self.dob, 12)], next_row_y)
        else:
            print(self)

    def gpa(self, courses):
        marks = np.array([self.marks.get_mark(course.id) for course in courses])
        ects = np.array([course.ects for course in courses])
        gpa = np.dot(marks, ects.T) / sum(ects)
        return floor(gpa*100)/100


class Course(InputAndListable):
    """Represent course object
    
    Attributes
    ----------
    id, name
    """
     
    def __init__(self):
        self.id = ""
        self.name = ""
        self.ects = 0

    def __str__(self):
        return f"Course (id: {self.id}) {self.name}: {self.ects} ECTS"
    
    def input(self, reserved_ids = [], reserved_names=[], **kwargs):
        id = ""
        name = ""

        box = None
        if "box" in kwargs.keys():
            box = kwargs["box"]
            clear_id = None
            clear_name = None
            while True:
                id, clear_id = box("ID:", 0, 0, 1, 10, 4, 0)
                if id not in reserved_ids:
                    break
                else:
                    clear_id()
            self.id = id

            while True:
                name, clear_name = box("Name:", 4, 0, 1, 20, 4, 0)
                if name not in reserved_names:
                    break
                else:
                    clear_name()
            self.name = name

            ects, clear_ects = box("ECTS:", 8, 0, 1, 10, 4, 0)
            self.ects = int(ects)
            clear_id()
            clear_name()
            clear_ects()
        else:
            while True:
                id = input("ID: ")
                if id not in reserved_ids:
                    break
            self.id = id

            while True:
                name = input("Name: ")
                if name not in reserved_names:
                    break
            self.name = name

            self.ects = int(input("ECTS: "))

        return id, name
    
    def list(self, print_function = None, next_row_y = [0]):
        if print_function:
            print_function([(self.id, 10), (self.name, 20), (self.ects, 6)], next_row_y)
        else:
            print(self)
        
        
class Mark:
    """Represent student object
    
    Methods
    ----------
    get_mark, set_mark
    """

    def __init__(self):
        self.__marks = {}
    
    def get_mark(self, course_id):
        """Return mark of course with course_id"""
        return self.__marks[course_id]
    
    def set_mark(self, course_id, mark):
        """Set mark of course with course_id 
        
        Round down mark to 1 decimalplace
        """
        self.__marks[course_id] = floor(mark*10)/10

class InputOutput():
    def __init__(self):
        self.__init_curser()

    def __init_curser(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        if curses.has_colors():
            curses.start_color()
        self.TERM_WIDTH = curses.COLS
        self.TERM_HEIGHT = curses.LINES
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.BLACK_ON_WHITE = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.GREEN = curses.color_pair(2)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.WHITE_ON_BLACK = curses.color_pair(3)
        self.COLORS = [self.BLACK_ON_WHITE, self.GREEN, self.WHITE_ON_BLACK]
    
    def move_cursor(self, y, x):
        """Move the cursor to y, x cordinates"""
        curses.setsyx(y, x)

    def row(self, cells, next_y_reference):
        """Print a table row
        
        Parameters:
        cells : [(text, width),] list contain tupples of text and width
        next_y_reference : y reference to list [y] cordinate of the row

        Return next_row_y
        """
        i = 0
        for cell in cells:
            self.print(str(cell[0]), cords=(next_y_reference[0]+1,i+1))
            rectangle(self.stdscr, next_y_reference[0], i, 2 + next_y_reference[0], cell[1] + i)
            i += cell[1]

        self.refresh()

        next_y_reference[0] += 2

    def refresh(self, win = None):
        """Refresh a window
        
        Parameters
        ----------
        win : optional the window to refresh (default stdscr)
        """
        
        if win:
            win.refresh()
        else:
            self.stdscr.refresh()

    def clear_screen(self, win = None):
        """Clear the screen of a window
        
        Parameters
        ----------
        win : optional the window to clear screen (default stdscr)
        """

        if win:
            win.clear()
        else:
            self.stdscr.clear()

    def description_box(self, title, description, cords=(0,0)):
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
        self.print(title + "\n", color=self.GREEN, parent=des_win)
        
        for index, line in enumerate(des_text):
            self.print(line, cords=(index+2, 2), parent=des_win)

        rectangle(des_win, 1, 0, height + 2, width + 3)
        des_win.refresh()
        def clear():
            self.clear_win(des_win)

        return clear


    def print(self, text, parent = None, cords = None, color = None):
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
            screen = self.stdscr
        else:
            screen = parent
        
        text_color = self.WHITE_ON_BLACK if color not in self.COLORS else color
        if cords:
            screen.addstr(cords[0], cords[1], text, text_color)
        else:
            screen.addstr(text, text_color)
        self.refresh()

    def wait(self):
        """Wait for a key and return it"""
        return self.stdscr.getkey()
        
    def box(self, prompt, y, x, height, width, parent_y = 0, parent_x = 0, next_y_reference=[0]):
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

        clear_text = self.fixed_text("Ctrl + G to exit any text box", self.TERM_HEIGHT - 1, 0)     
        box_win = curses.newwin(height + 4, max(len(prompt), width) + 3, y + parent_y, x + parent_x)
        box_win.addstr(prompt)
        rectangle(box_win, 1, 0, height + 2, width + 2)
        textbox_win = box_win.subwin(height, width + 1, 2 + y + parent_y , 1 + x + parent_x)
        textbox = Textbox(textbox_win)
        self.stdscr.refresh()
        box_win.refresh()
        textbox.edit()
        
        next_y_reference[0] += height+4

        def clear():
            clear_text()
            self.clear_win(box_win)

        return textbox.gather(), clear

    def fixed_text(self, text, y, x):
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
        self.stdscr.refresh()
        win.addstr(text)
        win.refresh()

        def clear():
            self.clear_win(win)

        return clear 
    
    def clear_win(self, win):
        """Delete the window
        
        Parameters
        ---------
        win : the window to delete
        """
        del win
        self.stdscr.touchwin()
        self.stdscr.refresh()


    def deintialize(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

class StudentMarkManagement:
    """Student mark management system"""

    def __init__(self):
        self.students = []
        self.courses = []
        self.no_students = 0
        self.no_courses = 0
        self.input_output = InputOutput()
        self.init_students()
        self.init_courses()

    def main(self):
        """Main loop of the program
        
        Wait for a command and execute it
        """

        while True:
            self.input_output.clear_screen()
            self.input_output.refresh()
            clear_commands = self.print_commands()
            key = self.input_output.wait()
            
            if key == "q":
                print("Exited")
                break
            if key == "i":
                clear_commands()
                self.insert_mark()
            if key == "s":
                clear_commands()
                self.list_students()
            if key == "c":
                clear_commands()
                self.list_courses()
            if key == "m":
                clear_commands()
                self.list_marks()
            if key == "g":
                clear_commands()
                self.list_gpa()
            if key == "d":
                clear_commands()
                self.sort_gpa()
      
    def insert_mark(self):
        """Insert mark of students in a course"""
        self.input_output.print("INSERTING MARK",)
        self.input_output.refresh()
        # Get course_id
        course = None
        while True:
            course = self.get_course_id()
            if course != -1:
                break
        self.input_output.print("\n"+str(course), color=self.input_output.GREEN)
        # Insert mark of student to marks of the course with id
        next_y = [2]
        clear_functions = []
        for student in self.students:       
            mark, clear = self.input_output.box(str(student), next_y[0], 0, 1, 5, 0, 0, next_y)
            student.marks.set_mark(course.id, float(mark))
            clear_functions.append(clear)

        for clear_function in clear_functions:
            clear_function()
        print()


    def init_students(self):
        """Add student to the system"""
        self.input_output.print("Insert students:\n")       
        no_students, clear_no_students = self.input_output.box("Number of students:", 2, 0, 1, 10)
        self.no_students = int(no_students)
        clear_no_students()
        self.input_output.refresh()

        reserved_ids = []
        for i in range(self.no_students):
            self.input_output.fixed_text(f"Student {i + 1}:", 2, 0)
            student = Student()
            reserved_ids.append(student.input(reserved_ids, box=self.input_output.box))
            clear_info = self.input_output.fixed_text("Added: " + str(student), y=2, x=0)
            self.input_output.wait()
            clear_info()
            self.students.append(student)

        self.input_output.clear_screen()
        self.input_output.refresh()
        self.list_students()

    def init_courses(self):
        """Add course to the system"""
        self.input_output.print("Insert courses:\n")       
        no_courses, clear_no_courses = self.input_output.box("Number of courses:", 2, 0, 1, 10)
        self.no_courses = int(no_courses)
        clear_no_courses()
        self.input_output.refresh()

        reserved_ids = []
        reserved_names = []
        for i in range(self.no_courses):
            self.input_output.fixed_text(f"Course {i + 1}:", 2, 0)
            course = Course()
            id, name = course.input(reserved_ids, reserved_names, box=self.input_output.box)
            reserved_ids.append(id)
            reserved_names.append(name)
            clear_info = self.input_output.fixed_text("Added: " + str(course), y=2, x=0)
            self.input_output.wait()
            clear_info()
            self.courses.append(course)
            print()

        self.input_output.clear_screen()
        self.input_output.refresh()
        self.list_courses()

    def print_commands(self):
        """List the commands that are available"""
        return self.input_output.description_box("Student mark management system", 
"""
q (quit) : quit the program
i (insert) : insert marks of students in a course
s (students) : list the students
c (courses) : list the courses
m (marks) : list the marks of students in a course
g (gpa): list students' gpas
d (decending sort) : sort students' gpas in decending order
""")
    
    def list_students(self):
        self.input_output.print("Students:\n")
        next_row_y = [1]
        self.input_output.row([("ID", 10), ("Name", 20), ("DOB", 12)], next_row_y)
        for student in self.students:
            student.list(self.input_output.row, next_row_y)
        self.input_output.wait()
        self.input_output.clear_screen()
        self.input_output.refresh()
    
    def list_courses(self):
        self.input_output.print("Courses:\n")
        next_row_y = [1]
        self.input_output.row([("ID", 10), ("Name", 20), ("ECTS", 6)], next_row_y)
        for course in self.courses:
            course.list(self.input_output.row, next_row_y)
        self.input_output.wait()
        self.input_output.clear_screen()
        self.input_output.refresh()

    def list_marks(self):
        self.input_output.print("MARKS",)
        # Get course_id
        course = None
        while True:
            course = self.get_course_id()
            if course != -1:
                break
      
        self.input_output.print("\n"+str(course), color=self.input_output.GREEN)
        next_row_y = [2]
        self.input_output.row([("ID", 10), ("Name", 20), ("DOB", 12), ("Mark", 6)], next_row_y)

        for student in self.students:
            self.input_output.row([(student.id, 10), (student.name, 20), (student.dob, 12), (student.marks.get_mark(course.id), 6)], next_row_y)

        self.input_output.wait()

    def list_gpa(self):
        self.input_output.print("GPA", color=self.input_output.BLACK_ON_WHITE)
        next_row_y = [1]
        self.input_output.row([("ID", 10), ("Name", 20), ("DOB", 12), ("GPA", 6)], next_row_y)
        for student in self.students:
            self.input_output.row([(student.id, 10), (student.name, 20), (student.dob, 12), (student.gpa(self.courses), 6)], next_row_y)
        self.input_output.wait()

    def sort_gpa(self):
        self.students.sort(reverse=True, key=(lambda student: student.gpa(self.courses)))
        self.list_gpa()

    def get_course_id(self):
        """Get the course that the user want
        
        Return a course
        """

        return_course = None
        # Search couse by ID or NAME
        search_type, clear_search = self.input_output.box("Search course by ID or Name", 1, 0, 1, 6, 0, 0)
        clear_name = None
        clear_a = None
        option = search_type.lower().strip() 
        try:
            if option.lower() not in ["id", "name"]:
                raise Exception("invalid search_type")
            elif option == "name":
                name, clear_name = self.input_output.box("Course name: ", 5, 0, 1, 20, 0, 0)
                # Loop through the courses to find the id 
                for course in self.courses:
                    if course.name == name:
                        return_course = course
                        break
                else:
                    raise Exception("Cannot find course name: " + name)
            else:
                a, clear_a = self.input_output.box("Course ID: ", 5, 0, 1, 10, 0, 0)
                # Loop through the courses to check if the id exists 
                for course in self.courses:
                    if course.id == a:
                        return_course = course
                        break
                else:
                    raise Exception("Cannot find course id: " + a)

        except Exception as e:
            # An exception ocurred
            print(e)
            return -1
        else:
            # No error, found the id
            return return_course
        finally:
            # clear the boxes
            clear_search()
            if clear_name:
                clear_name()
            if clear_a:
                clear_a()

    def __del__(self):
        self.input_output.deintialize()
        


        
management = StudentMarkManagement()
management.main()
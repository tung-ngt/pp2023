from math import floor
import numpy as np
import curses
from curses.textpad import Textbox, rectangle

class InputAndListable:
    """Abstract class that can input and list"""

    def input(self):
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

    def __str__(self):
        return f"Student (id: {self.id}) {self.name}, dob: {self.dob}"
    
    def input(self, data={}):
        """Input the data of student
        
        Parameters
        ----------
        input : a dict with id, name, dob keys and values

        Return id
        """
        self.id = data["id"]
        self.name = data["name"]
        self.dob = data["dob"]
        return self.id

class Course(InputAndListable):
    """Represent course object
    
    Attributes
    ----------
    id, name, ects
    """
     
    def __init__(self):
        self.id = ""
        self.name = ""
        self.ects = 0

    def __str__(self):
        return f"Course (id: {self.id}) {self.name}: {self.ects} ECTS"
    
    def input(self, data):
        """Input the data of course
        
        Parameters
        ----------
        input : a dict with id, name, ects keys and values

        Return id, name
        """

        self.id = data["id"]
        self.name = data["name"]
        self.ects = data["ects"]

        return self.id, self.name
        
class Marks:
    """Represent marks object
    
    Methods
    ----------
    get_mark, set_mark
    """

    def __init__(self):
        self.__marks = {}

    def get_mark(self, course_id, student_id):
        """Return mark of course with course_id and student_id"""
        if student_id not in self.__marks[course_id].keys():
            return -1
        return self.__marks[course_id][student_id]
    
    def set_mark(self, course_id, student_id, mark):
        """Set mark of course with course_id and student_id"""
        self.__marks[course_id][student_id] = floor(mark*10)/10

    def add_course(self, course_id):
        """Add course with course_id to the table of marks"""
        if course_id not in self.__marks.keys():
            self.__marks[course_id] = {}
    
    def get_course_marks(self, course_id):
        """Return marks of student in course with course_id
        
        Return [(student_id, mark)]
        """
        if course_id in self.__marks.keys():
            return list(self.__marks[course_id].items())
        return []

# init gui

STDSCR = None
TERM_WIDTH = 0
TERM_HEIGHT = 0
GREEN = None
WHITE_ON_BLACK = None
BLACK_ON_WHITE = None

def __init_gui():
    """Init curses module"""
    global STDSCR
    global TERM_HEIGHT
    global TERM_WIDTH
    global BLACK_ON_WHITE
    global WHITE_ON_BLACK
    global GREEN
    STDSCR = curses.initscr()
    curses.noecho()
    curses.cbreak()
    if curses.has_colors():
        curses.start_color()
    TERM_WIDTH = curses.COLS
    TERM_HEIGHT = curses.LINES
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    BLACK_ON_WHITE = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN = curses.color_pair(2)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    WHITE_ON_BLACK = curses.color_pair(3)

__init_gui()

def deintialize_gui():
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def refresh(win = None):
    """Refresh a window
    
    Parameters
    ----------
    win : optional the window to refresh (default stdscr)
    """
    
    if win:
        win.refresh()
    else:
        STDSCR.refresh()

def clear_screen(win = None):
    """Clear the screen of a window
    
    Parameters
    ----------
    win : optional the window to clear screen (default stdscr)
    """

    if win:
        win.clear()
    else:
        STDSCR.clear()

def clear_win(win):
    """Delete the window
    
    Parameters
    ---------
    win : the window to delete
    """
    del win
    STDSCR.touchwin()
    STDSCR.refresh()

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

def input_student(reserved_ids):
    """Input a valid students and return it
    
    Parameters
    ----------
    reserved_ids : list of reserved ids

    Return {id: string, name: string, dob: string}
    """

    # Make sure the student's id is unique
    id = ""
    clear_id = None
    while True:
        id, clear_id = box("ID:", 0, 0, 1, 10, 4, 0)
        if id not in reserved_ids:
            reserved_ids.append(id)
            break
        else:
            clear_id()

    name, clear_name = box("Name:", 4, 0, 1, 20, 4, 0)
    dob, clear_dob = box("DoB:", 8, 0, 1, 10, 4, 0)
    clear_id()
    clear_name()
    clear_dob()
    
    return {"id": id, "name": name, "dob": dob}

def input_course(reserved_ids, reserved_names):
    """Input a valid students and return it
    
    Parameters
    ----------
    reserved_ids : list of reserved ids
    reserved_names : list of reserved names

    Return {id: string, name: string, ects: int}
    """
     
    id = ""
    name = ""
    clear_id = None
    clear_name = None

    # Make sure the course's id is unique
    while True:
        id, clear_id = box("ID:", 0, 0, 1, 10, 4, 0)
        if id not in reserved_ids:
            reserved_ids.append(id)
            break
        else:
            clear_id()

    # Make sure the course's name is unique
    while True:
        name, clear_name = box("Name:", 4, 0, 1, 20, 4, 0)
        if name not in reserved_names:
            reserved_names.append(name)
            break
        else:
            clear_name()

    ects, clear_ects = box("ECTS:", 8, 0, 1, 10, 4, 0)
    ects = int(ects)
    clear_id()
    clear_name()
    clear_ects()
    return {"id": id, "name": name, "ects": ects}

class StudentMarkManagement:
    """Student mark management system"""

    def __init__(self):
        self.no_students = 0
        self.no_courses = 0

        self.students = []
        self.courses = []
        self.marks = Marks()

        self.init_students()
        self.init_courses()

    def init_students(self):
        """Add student to the system"""

        print_text("Insert students:\n")       
        no_students, clear_no_students = box("Number of students:", 2, 0, 1, 10)
        self.no_students = int(no_students)
        clear_no_students()
        refresh()

        reserved_ids = []
        for i in range(self.no_students):
            fixed_text(f"Student {i + 1}:", 2, 0)
            student = Student()
            student.input(input_student(reserved_ids))
            clear_info = fixed_text("Added: " + str(student), y=1, x=0)
            wait()
            clear_info()
            self.students.append(student)

        clear_screen()
        refresh()
        self.list_students()

    def init_courses(self):
        """Add course to the system"""

        print_text("Insert courses:\n")       
        no_courses, clear_no_courses = box("Number of courses:", 2, 0, 1, 10)
        self.no_courses = int(no_courses)
        clear_no_courses()
        refresh()

        reserved_ids = []
        reserved_names = []
        for i in range(self.no_courses):
            fixed_text(f"Course {i + 1}:", 2, 0)
            course = Course()
            course.input(input_course(reserved_ids, reserved_names))
            clear_info = fixed_text("Added: " + str(course), y=1, x=0)
            wait()
            clear_info()
            self.courses.append(course)
            self.marks.add_course(course.id)

        clear_screen()
        refresh()
        self.list_courses()

    def insert_mark(self):
        """Insert mark of students in a course"""

        # Get course_id
        course = None
        while True:
            print_text("INSERTING MARK")
            course = self.get_course_id()
            if course != -1:
                break
        print_text("\n"+str(course), color=GREEN)
        print_text("\nEnter -1 for student not in course", color=BLACK_ON_WHITE)
        # Insert mark of student to marks of the course with id
        next_y = [3]
        clear_functions = []
        for student in self.students:       
            m, clear = box(str(student), next_y[0], 0, 1, 5, 0, 0, next_y)
            m = float(m)
            if m == -1:
                continue
            self.marks.set_mark(course.id, student.id, m)
            clear_functions.append(clear)

        for clear_function in clear_functions:
            clear_function()

    def print_commands(self):
        """List the commands that are available"""
        return description_box("Student mark management system", 
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
        print_text("Students:\n")
        next_row_y = [1]
        row([("ID", 10), ("Name", 20), ("DOB", 12)], next_row_y)
        for student in self.students:
            row([(student.id, 10), (student.name, 20), (student.dob, 12)], next_row_y)
        wait()
        clear_screen()
        refresh()

    def list_courses(self):
        print_text("Courses:\n")
        next_row_y = [1]
        row([("ID", 10), ("Name", 20), ("ECTS", 6)], next_row_y)
        for course in self.courses:
            row([(course.id, 10), (course.name, 20), (course.ects, 6)], next_row_y)
        wait()
        clear_screen()
        refresh()

    def list_marks(self):
        print_text("MARKS")
        # Get course_id
        course = None
        while True:
            course = self.get_course_id()
            if course != -1:
                break
      
        print_text("\n"+str(course), color=GREEN)
        next_row_y = [2]
        row([("ID", 10), ("Name", 20), ("DOB", 12), ("Mark", 6)], next_row_y)

        for student_id, mark in self.marks.get_course_marks(course.id):
            student = None
            for s in self.students:
                if s.id == student_id:
                    student = s
            row([(student.id, 10), (student.name, 20), (student.dob, 12), (mark, 6)], next_row_y)

        wait()
        clear_screen()
        refresh()

    def get_gpa(self, student_id):
        """Return the gpa of a student with student_id"""
        marks = []
        ects = []
        for course in self.courses:
            m = self.marks.get_mark(course.id, student_id)
            if m == -1:
                continue
            
            marks.append(m)
            ects.append(course.ects)

        gpa = np.dot(np.array(marks), np.array([ects]).T) / sum(ects)
        return floor(gpa*100)/100

    def list_gpa(self):
        print_text("GPA", color=BLACK_ON_WHITE)
        next_row_y = [1]
        row([("ID", 10), ("Name", 20), ("DOB", 12), ("GPA", 6)], next_row_y)
        for student in self.students:
            row([(student.id, 10), (student.name, 20), (student.dob, 12), (self.get_gpa(student.id), 6)], next_row_y)
        wait()
        clear_screen()
        refresh()

    def sort_gpa(self):
        self.students.sort(reverse=True, key=(lambda student: self.get_gpa(student.id)))
        self.list_gpa()

    def get_course_id(self):
        """Get the course that the user want
        
        Return a course
        """

        return_course = None
        # Search couse by ID or NAME
        search_type, clear_search = box("Search course by ID or Name", 1, 0, 1, 6, 0, 0)
        clear_name = None
        clear_a = None
        option = search_type.lower().strip() 
        try:
            if option.lower() not in ["id", "name"]:
                raise Exception("invalid search_type")
            elif option == "name":
                name, clear_name = box("Course name: ", 5, 0, 1, 20, 0, 0)
                # Loop through the courses to find the id 
                for course in self.courses:
                    if course.name == name:
                        return_course = course
                        break
                else:
                    raise Exception("Cannot find course name: " + name)
            else:
                a, clear_a = box("Course ID: ", 5, 0, 1, 10, 0, 0)
                # Loop through the courses to check if the id exists 
                for course in self.courses:
                    if course.id == a:
                        return_course = course
                        break
                else:
                    raise Exception("Cannot find course id: " + a)

        except Exception as e:
            # An exception ocurred
            clear_screen()
            refresh()
            print_text(str(e))
            wait()
            clear_screen()
            refresh()
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
        deintialize_gui()

    def main(self):
        """Main loop of the program
        
        Wait for a command and execute it
        """

        while True:
            clear_screen()
            refresh()
            clear_commands = self.print_commands()
            key = wait()
            
            if key == "q":
                print_text("Exited")
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
   
management = StudentMarkManagement()
management.main()
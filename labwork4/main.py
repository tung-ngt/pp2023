from domains import Student, Course
from gui import *
from input import *
from output import *

def input_student(reserved_ids):
    id = ""
    clear_id = None
    while True:
        id, clear_id = box("ID:", 0, 0, 1, 10, 4, 0)
        if id not in reserved_ids:
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
    id = ""
    name = ""
    clear_id = None
    clear_name = None

    while True:
        id, clear_id = box("ID:", 0, 0, 1, 10, 4, 0)
        if id not in reserved_ids:
            break
        else:
            clear_id()

    while True:
        name, clear_name = box("Name:", 4, 0, 1, 20, 4, 0)
        if name not in reserved_names:
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
        self.students = []
        self.courses = []
        self.no_students = 0
        self.no_courses = 0
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
            reserved_ids.append(student.input(input_student(reserved_ids)))
            clear_info = fixed_text("Added: " + str(student), y=2, x=0)
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
            id, name = course.input(input_course(reserved_ids, reserved_names))
            reserved_ids.append(id)
            reserved_names.append(name)
            clear_info = fixed_text("Added: " + str(course), y=2, x=0)
            wait()
            clear_info()
            self.courses.append(course)

        clear_screen()
        refresh()
        self.list_courses()

    def insert_mark(self):
        """Insert mark of students in a course"""

        print_text("INSERTING MARK")
        refresh()
        # Get course_id
        course = None
        while True:
            course = self.get_course_id()
            if course != -1:
                break
        print_text("\n"+str(course), color=GREEN)
        # Insert mark of student to marks of the course with id
        next_y = [2]
        clear_functions = []
        for student in self.students:       
            mark, clear = box(str(student), next_y[0], 0, 1, 5, 0, 0, next_y)
            student.marks.set_mark(course.id, float(mark))
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
        print_text("MARKS",)
        # Get course_id
        course = None
        while True:
            course = self.get_course_id()
            if course != -1:
                break
      
        print_text("\n"+str(course), color=GREEN)
        next_row_y = [2]
        row([("ID", 10), ("Name", 20), ("DOB", 12), ("Mark", 6)], next_row_y)

        for student in self.students:
            row([(student.id, 10), (student.name, 20), (student.dob, 12), (student.marks.get_mark(course.id), 6)], next_row_y)

        wait()
        clear_screen()
        refresh()

    def list_gpa(self):
        print_text("GPA", color=BLACK_ON_WHITE)
        next_row_y = [1]
        row([("ID", 10), ("Name", 20), ("DOB", 12), ("GPA", 6)], next_row_y)
        for student in self.students:
            row([(student.id, 10), (student.name, 20), (student.dob, 12), (student.gpa(self.courses), 6)], next_row_y)
        wait()
        clear_screen()
        refresh()

    def sort_gpa(self):
        self.students.sort(reverse=True, key=(lambda student: student.gpa(self.courses)))
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

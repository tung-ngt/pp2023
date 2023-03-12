class InputAndListable:
    """Abstract class that can input and list"""

    def input(self, reserved_ids = [], reserved_names = []):
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
    
    def input(self, reserved_ids = [], reserved_names=[]):
        id = ""
        while True:
            id = input("ID: ")
            if id not in reserved_ids:
                break
        self.id = id
        self.name = input("Name: ")
        self.dob = input("DoB: ")
        return id

class Course(InputAndListable):
    """Represent course object
    
    Attributes
    ----------
    id, name
    """
     
    def __init__(self):
        self.id = ""
        self.name = ""

    def __str__(self):
        return f"Course (id: {self.id}) {self.name}"
    
    def input(self, reserved_ids = [], reserved_names=[]):
        id = ""
        while True:
            id = input("ID: ")
            if id not in reserved_ids:
                break
        self.id = id

        name = ""
        while True:
            name = input("Name: ")
            if name not in reserved_names:
                break
        self.name = name

        return id, name
        
        
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
        """Set mark of course with course_id"""
        self.__marks[course_id] = mark

class StudentMarkManagement:
    """Student mark management system"""

    def __init__(self):
        self.students = []
        self.courses = []
        self.no_students = 0
        self.no_courses = 0
        self.init_students()
        self.init_courses()
    
    def main(self):
        """Main loop of the program
        
        Wait for a command and execute it
        """
        
        self.print_commands()
        while True:
            print(">", end=" ")
    
            # Get command from user
            command = input("").lower() 
            if command in ["q", "quit"]:
                # Quit the program
                print("quitting")
                break
            elif command in ["h", "help"]:
                self.print_commands()
            elif command in ["i", "insert"]:
               self.insert_mark()
            elif command in ["s", "students"]:
                self.list_students()
            elif command in ["c", "courses"]:
                self.list_courses()
            elif command in ["m", "marks"]:
                self.print_marks()
            else:
                print("Invalid command!")

        print()
    
    def insert_mark(self):
        """Insert mark of students in a course"""

        # Get course_id
        course_id = self.get_course_id()
        if course_id == -1:
            return
        # Insert mark of student to marks of the course with id
        for student in self.students:
            student.marks.set_mark(course_id, float(input(str(student) + ": ")))
        print()


    def init_students(self):
        """Add student to the system"""
        no_students = 0
        while True:
            try:
                no_students = int(input("Number of students: "))
                if no_students < 1:
                    raise Exception("Invalid number of students!")
            except Exception as e:
                print(e)
                print("Please re-enter")
            else:
                self.no_students = no_students
                break

        reserved_ids = []
        for i in range(self.no_students):
            student = Student()
            reserved_ids.append(student.input(reserved_ids))
            self.students.append(student)
            print()

    def init_courses(self):
        """Add course to the system"""
        no_courses = 0
        while True:
            try:
                no_courses = int(input("Number of courses: "))
                if no_courses < 1:
                    raise Exception("Invalid number of courses!")
            except Exception as e:
                print(e)
                print("Please re-enter")
            else:
                self.no_courses = no_courses
                break
        reserved_ids = []
        reserved_names = []
        for i in range(self.no_courses):
            course = Course()
            id, name = course.input(reserved_ids, reserved_names)
            reserved_ids.append(id)
            reserved_names.append(name)
            self.courses.append(course)
            print()

    def print_commands(self):
        """List the commands that are available"""

        print(
"""
q (quit) : quit the program
h (help) : list the commands
i (insert) : insert marks of students in a course
s (students) : list the students
c (courses) : list the courses
m (marks) : list the marks of students in a course\n
"""
        )
    
    def list_students(self):
        for student in self.students:
            student.list()
        print()
    
    def list_courses(self):
        for course in self.courses:
            course.list()
        print()

    def print_marks(self):
        course_id = self.get_course_id()
        
        if course_id == -1:
            return

        for student in self.students:
            print(student, end=": ")
            print(student.marks.get_mark(course_id))

    def get_course_id(self):
        """Get the id of the course that the user want"""

        id = ""
        # Search couse by ID or NAME
        search_type = input("Find course by ID or NAME: ").lower()

        try:
            if search_type not in ["id", "name"]:
                raise Exception("invalid search_type")
            elif search_type == "name":
                name = input("Course name: ")
                # Loop through the courses to find the id 
                for course in self.courses:
                    if course.name == name:
                        id = course.id
                        break
                else:
                    raise Exception("Cannot find course name: " + name)
            else:
                a = input("Course ID: ")
                # Loop through the courses to check if the id exists 
                for course in self.courses:
                    if course.id == a:
                        id = course.id
                        break
                else: 
                    raise Exception("Cannot find course id: " + a)

        except Exception as e:
            # An exception ocurred
            return str(e)
        else:
            # Found the id
            return id


        
management = StudentMarkManagement()
management.main()
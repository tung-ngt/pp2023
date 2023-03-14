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
        return self.id, self.name

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
    
    def input(self, data):
        """Input the data of course
        
        Parameters
        ----------
        input : a dict with id, name keys and values

        Return id, name
        """
        self.id = data["id"]
        self.name = data["name"]
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
        self.__marks[course_id][student_id] = mark

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



def input_student(reserved_ids):
    """Input a valid students and return it
    
    Parameters
    ----------
    reserved_ids : list of reserved ids

    Return {id: string, name: string, dob: string}
    """

    # Make sure the student's id is unique
    id = ""
    while True:
        id = input("ID: ")
        if id not in reserved_ids:
            reserved_ids.append(id)
            break
        else:
            print("The id already exist, please re-enter")

    name = input("Name: ")
    dob = input("DoB: ") 
    return {"id": id, "name": name, "dob": dob}

def input_course(reserved_ids, reserved_names):
    """Input a valid students and return it
    
    Parameters
    ----------
    reserved_ids : list of reserved ids
    reserved_names : list of reserved names

    Return {id: string, name: string}
    """

    # Make sure the student's id is unique
    id = ""
    while True:
        id = input("ID: ")
        if id not in reserved_ids:
            reserved_ids.append(id)
            break
        else:
            print("The id already exist, please re-enter")

    # Make sure the course's name is unique
    name = ""
    while True:
        name = input("Name: ")
        if name not in reserved_names:
            reserved_names.append(name)
            break
        else:
            print("The name already exist, please re-enter")

    return {"id": id, "name": name}

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
            student.input(input_student(reserved_ids))
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
            course.input(input_course(reserved_ids, reserved_names))
            self.courses.append(course)
            self.marks.add_course(course.id)
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

    def insert_mark(self):
        """Insert mark of students in a course"""

        # Get course_id
        course_id = self.get_course_id()
        if course_id == -1:
            return
        # Insert mark of student to marks of the course with id
        for student in self.students:
            print("enter -1 for student not in course")
            m = float(input(str(student) + ": "))
            if m == -1:
                continue
            self.marks.set_mark(course_id, student.id, m)
        print()
    
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
        for student_id, mark in self.marks.get_course_marks(course_id):
            print(f"({student_id}) {mark:.2f}")

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
            print(e)
            return -1
        else:
            # Found the id
            return id
        
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

management = StudentMarkManagement()
management.main()
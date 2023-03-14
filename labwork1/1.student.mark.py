def print_commands():
    """List the commands that are available"""

    print(
"""
q (quit) : quit the program
h (help) : list the commands
i (insert) : insert marks of students in a course
s (students) : list the students
c (courses) : list the courses
m (marks) : list the marks of students in a course\n\n
"""
    )

def get_course_id(courses):
    """Get the id of the course that the user want
    
    Parameters
    ----------
    courses : the list of courses to choose from
    """

    id = ""
    # Search couse by ID or NAME
    search_type = input("Find course by ID or NAME: ").lower()

    try:
        if search_type not in ["id", "name"]:
            raise Exception("invalid search_type")
        elif search_type == "name":
            name = input("Course name: ")
            # Loop through the courses to find the id 
            for course in courses:
                if course["name"] == name:
                    id = course["id"]
                    break
            else:
                raise Exception("Cannot find course name: " + name)
        else:
            a = input("Course ID: ")
            # Loop through the courses to check if the id exists 
            for course in courses:
                if course["id"] == a:
                    id = course["id"]
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
    
def input_students(reserved_ids):
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

def init_students():
    """Insert the student to the course
    
    return the list of students
    """

    students = []
    no_students = 0

    # Make sure the no_students is valid
    while True:
        try:
            no_students = int(input("Number of students: "))
            if no_students < 1:
                raise Exception("Invalid number of students!")
        except Exception as e:
            print(e)
            print("Please re-enter")
        else:
            break
        
    reserved_ids = []
    for i in range(no_students):
        students.append(input_students(reserved_ids))
        print()
        
    return students

def input_courses(reserved_ids, reserved_names):
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

def init_courses():
    """Insert courses to the system
    
    return the list of courses
    """

    courses = []
    no_courses = 0

    # Make sure the no_courses is valid
    while True:
        try:
            no_courses = int(input("Number of courses: "))
            if no_courses < 1:
                raise Exception("Invalid number of courses!")
        except Exception as e:
            print(e)
            print("Please re-enter")
        else:
            break
    
    reserved_ids = []
    reserved_names = []
    for i in range(no_courses):
        courses.append(input_courses(reserved_ids, reserved_names))
        print()
    
    return courses

def init_marks(courses):
    """Init the marks
    
    return the marks dict
    """

    marks = {}
    for course in courses:
        # Initialize marks of students in a course to be -1
        marks[course["id"]] = {}

    return marks

def main():
    """Main function"""

    # Init students, courses and marks
    students = init_students()
    no_students = len(students)
    courses = init_courses()
    marks = init_marks(courses)

    # Insert courses and marks
    print_commands()

    # Main loop
    while True:
        print(">", end=" ")

        # Get command from user
        command = input("").lower() 
        
        if command in ["q", "quit"]:
            # Quit the program
            print("quitting")
            break
        
        elif command in ["h", "help"]:
            print_commands()

        elif command in ["i", "insert"]:
            # Insert marks
            id = get_course_id(courses)
            if id != -1:
                # Insert mark of student to marks of the course with id
                for student in students:
                    print("enter -1 for student not in course")
                    m = float(input(f"({student['id']}) {student['name']}: "))
                    if m == -1:
                        continue
                    marks[id][student['id']] = m

        elif command in ["s", "students"]:
            # Loop through the students and print them
            for student in students:
                print(f"({student['id']}) {student['name']}, {student['dob']}")
        
        elif command in ["c", "courses"]:
            # Loop through the courses and print them
            for course in courses:
                print(f"({course['id']}) {course['name']}")
        
        elif command in ["m", "marks"]:
            # Print the marks of student in a course
            course_id = get_course_id(courses)
            if course_id != -1:
                course_marks = marks[course_id]
                for student_id in course_marks.keys():
                    print(f"({student_id}) {course_marks[student_id]:.2f}")
        
        else:
            print("Invalid command!")

        print()    

main()
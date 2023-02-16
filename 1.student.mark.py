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

def insert_students():
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
        student = {}
        id = ""

        # Make sure the student's id is unique
        while True:
            id = input("ID: ")
            if id not in reserved_ids:
                reserved_ids.append(id)
                break

        student["id"] = id
        student["name"] = input("Name: ")
        student["dob"] = input("DoB: ") 
        students.append(student)
        print()

    return students


def insert_courses():
    """Insert courses to the system
    
    return the list of courses
    """

    courses = []

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
        course = {}
        id = ""
        # Make sure the course's id is unique
        while True:
            id = input("ID: ")
            if id not in reserved_ids:
                reserved_ids.append(id)
                break
            else:
                print("The id already exist, please re-enter")

        course["id"] = id
        name = ""

        # Make sure the course's name is unique
        while True:
            name = input("Name: ")
            if name not in reserved_names:
                reserved_names.append(name)
                break
            else:
                print("The name already exist, please re-enter")

        course["name"] = name
        courses.append(course)
        print()
    
    return courses

def init_marks(courses, no_students):
    """Init the marks
    
    return the marks dict
    """

    marks = {}
    for course in courses:
        # Initialize marks of students in a course to be -1
        marks[course["id"]] = [-1 for n in range(no_students)]

    return marks

def main():
    """Main function"""

    # Init students, courses and marks
    students = insert_students()
    no_students = len(students)
    courses = insert_courses()
    marks = init_marks(courses, no_students)

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
                for s in range(no_students):
                    marks[id][s] = float(input(f"({students[s]['id']}) {students[s]['name']}: "))

        elif command in ["s", "students"]:
            # Loop through the students and print them
            for s in students:
                print(f"({s['id']}) {s['name']}, {s['dob']}")
        
        elif command in ["c", "courses"]:
            # Loop through the courses and print them
            for c in courses:
                print(f"({c['id']}) {c['name']}")
        
        elif command in ["m", "marks"]:
            # Print the marks of student in a course
            id = get_course_id(courses)
            if id != -1:
                for s in range(no_students):
                    print(f"({students[s]['id']}) {students[s]['name']} : {marks[id][s]:.2f}")
        
        else:
            print("Invalid command!")

        print()    

main()
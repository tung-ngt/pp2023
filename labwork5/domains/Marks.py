from math import floor

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
    
    def write_to_file(self, file):
        """Write marks to a file
        
        marks will be represented as lines with format:
        course_id|student_id:marks,student_id:marks,...
        course_id|student_id:marks,student_id:marks,...
        """
        for course_id, course_mark in list(self.__marks.items()):
            file.write(f"{course_id}|")
            for student_id, mark in list(course_mark.items()):
                file.write(f"{student_id}:{mark},")
            file.write("\n")
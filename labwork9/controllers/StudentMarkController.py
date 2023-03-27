import sys
sys.path.append('..')
from labwork9.domains import Student, Course, Marks
import numpy as np
from math import floor
from .file_utils import *
import pickle
import os

class StudentMarkController:
    """Student mark management system"""

    def __init__(self):
        self.no_students = 0
        self.no_courses = 0

        self.students = []
        self.courses = []
        self.marks = Marks()

        self.load_data()
      
    def load_data(self):
        """Load data into the system
        
        Try to load data about students, courses and marks from students.dat 
        else input the data
        """
        try:
            # Check if the data file exist
            if os.path.exists("./data/students.dat"):
                # File exist, decompressing the file, the output will be stored in ./data/ folder
                decompress("./data/students.dat")
                try:
                    # Open students file
                    with open("./data/students.txt", "rb") as students_file:
                        self.students = pickle.load(students_file)
                except Exception:
                    # Init students list to empty if students file does not exist
                    self.students = []

                try:
                    # Open courses file
                    with open("./data/courses.txt", "rb") as courses_file:
                        self.courses = pickle.load(courses_file)
                except Exception:
                    # Init courses list to empty if no courses file does not exist
                    self.courses = []

                try:
                    # Open marks file and read marks
                    with open("./data/marks.txt", "rb") as marks_file:
                        self.marks = pickle.load(marks_file)
                except:
                    # Input students if no courses file does not exist
                    self.marks = Marks()
                    for course in self.courses:
                        self.marks.add_course(course.id)
            else:
                raise FileNotFoundError()
        except FileNotFoundError:
            self.students = []
            self.courses = []

    def add_student(self, student_data):
        """Add a student to the system
        
        Parameters
        ----------
        student_data : {id: str, name: str, dob: str}
        """
        if self.check_unique_student(student_data["id"]):
            student = Student()
            student.input(student_data)
            self.students.append(student)
        else:
            raise Exception("ID already exist")
        
    def remove_student(self, id):
        """Remove_student with student_id"""
        delete_index = None
        for index, student in enumerate(self.students):
            if student.id == id:
                delete_index = index
                break

        if delete_index != None:
            self.students.pop(delete_index)

    def check_unique_student(self, id):
        """Check if a student is unique base on their id"""
        for student in self.students:
            if student.id == id:
                return 0
        return 1

    def save_students(self):
        try:
            write_with_thread(self.students, "./data/students.txt")
            return 1
        except Exception as e:
            print(e)
            return 0

    def add_course(self, course_data):
        """Add course to the system
        
        Parameters
        ----------
        course_data : {id: str, name: str, ects: int}
        """
        if self.check_unique_course(course_data["id"], course_data["name"]):
            course = Course()
            course.input(course_data)
            self.courses.append(course)
            self.marks.add_course(course.id)
    
    def remove_course(self, id):
        """Remove_student with course_id"""
        delete_index = None
        for index, course in enumerate(self.courses):
            if course.id == id:
                delete_index = index
                break

        if delete_index != None:
            self.courses.pop(delete_index)

    def check_unique_course(self, id, name):
        """Check if a course is unique base on their id and name"""
        for course in self.courses:
            if course.id == id or course.name == name:
                return 0
        return 1

    def save_courses(self):
        try:
            write_with_thread(self.courses, "./data/courses.txt")
            return 1
        except Exception as e:
            print(e)
            return 0

    def insert_mark(self, data):
        """Insert mark of a student in a course
        
        Parameters
        ----------
        data : {course_id: str, student_id: str, mark: float}
        """
        self.marks.set_mark(data["course_id"], data["student_id"], data["mark"])

    def save_marks(self):
        try:
            write_with_thread(self.marks, "./data/marks.txt")
            return 1
        except Exception as e:
            print(e)
            return 0

    def get_students_list(self):
        students_data = []
        for student in self.students:
            students_data.append((student.id, student.name, student.dob))
        return students_data

    def get_courses_list(self):
        courses_data = []
        for course in self.courses:
            courses_data.append((course.id, course.name, str(course.ects)))
        return courses_data

    def get_marks_list(self, course_id):
        if not self.course_exist(course_id):
            raise Exception(f"Course (id: {course_id}) does not exist")
        
        marks_data = []
        for student_id, mark in self.marks.get_course_marks(course_id):
            student = None
            for s in self.students:
                if s.id == student_id:
                    student = s
            marks_data.append((student.id, student.name, student.dob, mark))
        return marks_data

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
        gpa_data = []
        for student in self.students:
            gpa_data.append((student.id, student.name, student.dob, self.get_gpa(student.id)))
        return gpa_data
    
    def sort_gpa(self):
        self.students.sort(reverse=True, key=(lambda student: self.get_gpa(student.id)))
        self.list_gpa()

    def course_exist(self, id):
        """Check if the course exist base on id
        
        Return 1 if exist, 0 if not
        """
        # Loop through the courses to check if the id exists 
        for course in self.courses:
            if course.id == id:
                return 1
        
        return 0
    
    def quit(self):
        data_files = ["./data/students.txt", "./data/courses.txt", "./data/marks.txt"]
        compress(data_files, "./data/students.dat")
        for file in data_files:
            os.remove(file)
        print("Exited")
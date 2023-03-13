from .InputAndListable import InputAndListable
from .Mark import Mark
import numpy as np
from math import floor

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

    def gpa(self, courses):
        marks = np.array([self.marks.get_mark(course.id) for course in courses])
        ects = np.array([course.ects for course in courses])
        gpa = np.dot(marks, ects.T) / sum(ects)
        return floor(gpa*100)/100
from .InputAndListable import InputAndListable
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
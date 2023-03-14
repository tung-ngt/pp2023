from .InputAndListable import InputAndListable

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
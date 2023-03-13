from math import floor

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
        """Set mark of course with course_id 
        
        Round down mark to 1 decimalplace
        """
        self.__marks[course_id] = floor(mark*10)/10
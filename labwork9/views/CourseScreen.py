import sys
sys.path.append('..')
from labwork9.gui import Screen, Label, Frame, Button
from labwork9.constants import COLORS
from tkinter import PhotoImage, ttk, Toplevel, Entry, messagebox
class CourseScreen(Screen):
    def __init__(self, master, studentMarkController):
        """Init screen"""
        super().__init__(master, COLORS.WHITE)

        self.logo_image = PhotoImage(file="./images/graduation.png")
        self.image_label = Label(self, image=self.logo_image, background=COLORS.WHITE)
        self.image_label.pack()
        self.app_name = Label(self, "STUDENTS", background=COLORS.WHITE)
        self.app_name.pack()
        self.studentMarkController = studentMarkController
        self.create_course_table()
        
    def create_course_table(self):
        """Create the student table view"""
        self.course_table_frame = Frame(self, width=500, height=400, background=COLORS.WHITE)
        self.course_table_frame.pack()
        self.course_table_frame.pack_propagate(False)
        self.course_table = ttk.Treeview(self.course_table_frame)
        self.course_table["columns"] = ("id", "name", "ects")
        self.course_table.column("#0", width=0, stretch=False)
        self.course_table.column("id", width=80)
        self.course_table.column("name", width=200)
        self.course_table.column("ects", width=80)

        # Create headings
        self.course_table.heading("#0", text="")
        self.course_table.heading("id", text="ID", anchor="w")
        self.course_table.heading("name", text="Name", anchor="w")
        self.course_table.heading("ects", text="ECTS", anchor="w")
        self.course_table.pack(fill="x", expand=True)

        self.latest_id = 0
        self.get_list()
        
        self.add_button = Button(self,
            self.add_course_popup,
            "ADD +", 
            width=10,
            height=2,
            background="black",
            foreground="white",
            activebackground="black",
            activeforeground="white"
        )
        self.remove_button = Button(self,
            self.delete_course,
            "REMOVE x", 
            width=10,
            height=2,
            background="black",
            foreground="white",
            activebackground="black",
            activeforeground="white"
        )
        self.save_button = Button(self,
            self.save,
            "SAVE CHANGES", 
            width=10,
            height=2,
            background="black",
            foreground="white",
            activebackground="black",
            activeforeground="white"
        )
        self.add_button.pack()
        self.remove_button.pack(pady=5)
        self.save_button.pack()

    def save(self):
        self.studentMarkController.save_courses()

    def delete_course(self):
        course_id_to_delete = self.course_table.selection()
        for course_id in course_id_to_delete:
            self.studentMarkController.remove_course(self.course_table.item(course_id)["values"][0])
        self.get_list()

    def clear_all(self):
        self.latest_id = 0
        for s in self.course_table.get_children():
            self.course_table.delete(s)

    def get_list(self):
        self.clear_all()
        for course in self.studentMarkController.get_courses_list():
            self.course_table.insert(parent="", index="end", iid=self.latest_id, text="", values=course)
            self.latest_id += 1
        
    def add_course_popup(self):
        self.add_course_window = Toplevel()
        self.add_course_window.title("Add a course")
        self.add_course_window.geometry("500x300")
        self.add_course_window.resizable(False, False)
        self.add_course_window.grab_set()
        
        self.add_course_window.grid_columnconfigure(0, weight=1)
        self.add_course_window.grid_columnconfigure(1, weight=4)
        self.add_course_window.grid_rowconfigure(0, weight=1)
        self.add_course_window.grid_rowconfigure(1, weight=1)
        self.add_course_window.grid_rowconfigure(2, weight=1)
        self.add_course_window.grid_rowconfigure(3, weight=1)
        self.add_course_window.grid_rowconfigure(4, weight=1)
        
        id_label = Label(self.add_course_window, "ID:", background=COLORS.WHITE)
        name_label = Label(self.add_course_window, "Name:", background=COLORS.WHITE)
        ects_label = Label(self.add_course_window, "ECTS:", background=COLORS.WHITE)

        id_label.grid(row=0, column=0, sticky="nsw")
        name_label.grid(row=1, column=0, sticky="nsw")
        ects_label.grid(row=2, column=0, sticky="nsw")

        id_entry = Entry(self.add_course_window)
        name_entry = Entry(self.add_course_window)
        ects_entry = Entry(self.add_course_window)

        id_entry.grid(row=0, column=1, sticky="nsew")
        name_entry.grid(row=1, column=1, sticky="nsew")
        ects_entry.grid(row=2, column=1, sticky="nsew")

        def save_course():
            try:
                student_data = {
                    "id": id_entry.get(),
                    "name": name_entry.get(),
                    "ects": int(ects_entry.get())
                }
                self.studentMarkController.add_course(student_data)
                self.add_course_window.destroy()
                self.get_list()
            except Exception as e:
                messagebox.showerror("Failed to add student", str(e))

        save_button = Button(self.add_course_window,
            save_course,
            "SAVE", 
            background="black",
            foreground="white",
            activebackground="black",
            activeforeground="white"                 
        )
        cancel_button = Button(self.add_course_window,
            lambda: self.add_course_window.destroy(),
            "cancel", 
            background="black",
            foreground="white",
            activebackground="black",
            activeforeground="white"                 
        )

        save_button.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5)
        cancel_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

    
    
from gui import Screen, Label, Frame, Button
from constants import COLORS
from tkinter import PhotoImage, ttk, Toplevel, Entry, messagebox
class StudentScreen(Screen):
    def __init__(self, master, studentMarkController):
        """Init screen"""
        super().__init__(master, COLORS.WHITE)

        self.logo_image = PhotoImage(file="./images/graduation.png")
        self.image_label = Label(self, image=self.logo_image, background=COLORS.WHITE)
        self.image_label.pack()
        self.app_name = Label(self, "STUDENTS", background=COLORS.WHITE)
        self.app_name.pack()
        self.studentMarkController = studentMarkController
        self.create_student_table()
        
    def create_student_table(self):
        """Create the student table view"""
        self.student_table_frame = Frame(self, width=500, height=400, background=COLORS.WHITE)
        self.student_table_frame.pack()
        self.student_table_frame.pack_propagate(False)
        self.student_table = ttk.Treeview(self.student_table_frame)
        self.student_table["columns"] = ("id", "name", "dob")
        self.student_table.column("#0", width=0, stretch=False)
        self.student_table.column("id", width=80)
        self.student_table.column("name", width=200)
        self.student_table.column("dob", width=80)

        # Create headings
        self.student_table.heading("#0", text="")
        self.student_table.heading("id", text="ID", anchor="w")
        self.student_table.heading("name", text="Name", anchor="w")
        self.student_table.heading("dob", text="DOB", anchor="w")
        self.student_table.pack(fill="x", expand=True)

        self.latest_id = 0
        self.get_list()
        
        self.add_button = Button(self,
            self.add_student_popup,
            "ADD +", 
            width=10,
            height=2,
            background="black",
            foreground="white",
            activebackground="black",
            activeforeground="white"
        )
        self.remove_button = Button(self,
            self.delete_student,
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
        self.studentMarkController.save_students()

    def delete_student(self):
        student_id_to_delete = self.student_table.selection()
        for student_id in student_id_to_delete:
            self.studentMarkController.remove_student(self.student_table.item(student_id)["values"][0])
        self.get_list()

    def clear_all(self):
        self.latest_id = 0
        for s in self.student_table.get_children():
            self.student_table.delete(s)

    def get_list(self):
        self.clear_all()
        for student in self.studentMarkController.get_students_list():
            self.student_table.insert(parent="", index="end", iid=self.latest_id, text="", values=student)
            self.latest_id += 1
        
    def add_student_popup(self):
        self.add_student_window = Toplevel()
        self.add_student_window.title("Add a student")
        self.add_student_window.geometry("500x300")
        self.add_student_window.resizable(False, False)
        self.add_student_window.grab_set()
        
        self.add_student_window.grid_columnconfigure(0, weight=1)
        self.add_student_window.grid_columnconfigure(1, weight=4)
        self.add_student_window.grid_rowconfigure(0, weight=1)
        self.add_student_window.grid_rowconfigure(1, weight=1)
        self.add_student_window.grid_rowconfigure(2, weight=1)
        self.add_student_window.grid_rowconfigure(3, weight=1)
        self.add_student_window.grid_rowconfigure(4, weight=1)
        
        id_label = Label(self.add_student_window, "ID:", background=COLORS.WHITE)
        name_label = Label(self.add_student_window, "Name:", background=COLORS.WHITE)
        dob_label = Label(self.add_student_window, "DOB:", background=COLORS.WHITE)

        id_label.grid(row=0, column=0, sticky="nsw")
        name_label.grid(row=1, column=0, sticky="nsw")
        dob_label.grid(row=2, column=0, sticky="nsw")

        id_entry = Entry(self.add_student_window)
        name_entry = Entry(self.add_student_window)
        dob_entry = Entry(self.add_student_window)

        id_entry.grid(row=0, column=1, sticky="nsew")
        name_entry.grid(row=1, column=1, sticky="nsew")
        dob_entry.grid(row=2, column=1, sticky="nsew")

        def save_student():
            student_data = {
                "id": id_entry.get(),
                "name": name_entry.get(),
                "dob": dob_entry.get()
            }
            try:
                self.studentMarkController.add_student(student_data)
                self.add_student_window.destroy()
                self.get_list()
            except Exception as e:
                messagebox.showerror("Failed to add student", str(e))

        save_button = Button(self.add_student_window,
            save_student,
            "SAVE", 
            background="black",
            foreground="white",
            activebackground="black",
            activeforeground="white"                 
        )
        cancel_button = Button(self.add_student_window,
            lambda: self.add_student_window.destroy(),
            "cancel", 
            background="black",
            foreground="white",
            activebackground="black",
            activeforeground="white"                 
        )

        save_button.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5)
        cancel_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

    
    
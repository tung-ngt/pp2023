from gui import Screen, Label, Frame, Button
from constants import COLORS
from tkinter import PhotoImage, ttk, Toplevel, Entry, messagebox, Scrollbar, END as tkEND
class MarkScreen(Screen):
    def __init__(self, master, studentMarkController):
        """Init screen"""
        super().__init__(master, COLORS.WHITE)

        self.logo_image = PhotoImage(file="./images/graduation.png")
        self.image_label = Label(self, image=self.logo_image, background=COLORS.WHITE)
        self.image_label.pack()
        self.app_name = Label(self, "STUDENTS", background=COLORS.WHITE)
        self.app_name.pack()
        self.studentMarkController = studentMarkController
        self.create_mark_table()
        
    def create_mark_table(self):
        """Create the student table view"""
        self.mark_table_frame = Frame(self, width=500, height=400, background=COLORS.WHITE)
        self.mark_table_frame.pack()
        self.mark_table_frame.pack_propagate(False)
        self.mark_table = ttk.Treeview(self.mark_table_frame)
        self.mark_table["columns"] = ("id", "name", "dob", "mark")
        self.mark_table.column("#0", width=0, stretch=False)
        self.mark_table.column("id", width=80)
        self.mark_table.column("name", width=200)
        self.mark_table.column("dob", width=80)
        self.mark_table.column("mark", width=40)

        # Create headings
        self.mark_table.heading("#0", text="")
        self.mark_table.heading("id", text="ID", anchor="w")
        self.mark_table.heading("name", text="Name", anchor="w")
        self.mark_table.heading("dob", text="DOB", anchor="w")
        self.mark_table.heading("mark", text="Mark", anchor="w")
        self.mark_table.pack(fill="x", expand=True)

        self.latest_id = 0

        self.course_id_input_frame = Frame(self)
        self.course_id_input_frame.pack()
        self.course_id_label = Label(self.course_id_input_frame, "Course id:  ", background=COLORS.WHITE)
        self.course_id_label.pack(side="left")
        self.course_id_input = Entry(self.course_id_input_frame)
        self.course_id_input.pack(side="left")

        self.find_button = Button(self,
            self.get_list,
            "FIND", 
            width=12,
            height=2,
            background="black",
            foreground="white",
            activebackground="black",
            activeforeground="white"
        )
        self.change_mark_button = Button(self,
            self.insert_mark_popup,
            "INSERT MARK", 
            width=12,
            height=2,
            background="black",
            foreground="white",
            activebackground="black",
            activeforeground="white"
        )
        self.save_button = Button(self,
            self.save,
            "SAVE CHANGES", 
            width=12,
            height=2,
            background="black",
            foreground="white",
            activebackground="black",
            activeforeground="white"
        )
        self.find_button.pack()
        self.change_mark_button.pack(pady=5)
        self.save_button.pack()

    def save(self):
        self.studentMarkController.save_marks()

    def clear_all(self):
        self.latest_id = 0
        for s in self.mark_table.get_children():
            self.mark_table.delete(s)

    def get_list(self):
        self.clear_all()
        try:
            marks = self.studentMarkController.get_marks_list(self.course_id_input.get())
            for mark in marks:
                self.mark_table.insert(parent="", index="end", iid=self.latest_id, text="", values=mark)
                self.latest_id += 1
        except Exception as e:
            messagebox.showwarning("Failed", str(e))

    def insert_mark_popup(self):
        def create_mark_sheet():
            self.current_edit_course_id = self.id_entry.get()
            for s in self.marks_edit_view.get_children():
                self.marks_edit_view.delete(s)
            try:
                marks = self.studentMarkController.get_marks_list(self.current_edit_course_id)
                for mark in marks:
                    self.marks_edit_view.insert(parent="", index="end", text="", values=mark)
            except Exception as e:
                messagebox.showwarning("Failed", str(e))

        def double_click(event):
            region = self.marks_edit_view.identify_region(event.x, event.y)
            
            if region != "cell":
                return
            
            column = self.marks_edit_view.identify_column(event.x)
            column_index = int(column[1]) - 1

            if column_index != 3:
                return
            

            selected_iid = self.marks_edit_view.focus()
            selected_mark = self.marks_edit_view.item(selected_iid)["values"][3]

            column_box = self.marks_edit_view.bbox(selected_iid, column)
            
            entry = Entry(self.marks_edit_view, width=column_box[2])

            entry.edditting_column_index = column_index
            entry.edditting_item_iid = selected_iid
            entry.insert(0, selected_mark)
            entry.select_range(0, tkEND)
            entry.focus()
            def on_enter(event):
                entry_column = event.widget.edditting_column_index
                entry_selected_iid = event.widget.edditting_item_iid
                new_mark = event.widget.get()
                current_value = self.marks_edit_view.item(entry_selected_iid)["values"]
                current_value[entry_column] = new_mark
                self.marks_edit_view.item(entry_selected_iid, values=current_value)
                self.studentMarkController.insert_mark({"course_id": self.current_edit_course_id, "student_id": current_value[0], "mark": float(current_value[3])})
                event.widget.destroy()
            entry.bind("<FocusOut>", on_enter)
            entry.bind("<Return>", on_enter)
            entry.place(x=column_box[0],
                        y=column_box[1],
                        w=column_box[2],
                        h=column_box[3]
                        ) 

        def save_marks():
            pass

        self.insert_mark_window = Toplevel()
        self.insert_mark_window.title("Insert mark")
        self.insert_mark_window.state("zoomed")
        self.insert_mark_window.resizable(True, True)
        self.insert_mark_window.grab_set()
        
        actions_frame = Frame(self.insert_mark_window,background="black")
        actions_frame.pack(fill="x", ipadx=10, ipady=10)    
        input_frame = Frame(self.insert_mark_window)
        input_frame.pack(fill="both", expand=True)

        
        id_label = Label(actions_frame, "Course ID:", background=COLORS.BLACK, foreground=COLORS.WHITE)
        id_label.pack(side="left")

        self.id_entry = Entry(actions_frame)
        self.id_entry.pack(side="left", fill="x")

        find_button = Button(actions_frame,
            create_mark_sheet,
            "FIND", 
            width=12,
            height=2,
            background="white",
            foreground="black",
            activebackground="white",
            activeforeground="black"
        )

        save_button = Button(actions_frame,
            save_marks,
            "SAVE", 
            width=12,
            height=2,
            background="white",
            foreground="black",
            activebackground="white",
            activeforeground="black"
        )
        save_button.pack(side="right")
        find_button.pack(side="right")
        scrollbar = Scrollbar(input_frame, orient="vertical")
        self.marks_edit_view = ttk.Treeview(input_frame, yscrollcommand=scrollbar.set)
        self.marks_edit_view.bind("<Double-1>", double_click)
        scrollbar.config(command=self.marks_edit_view.yview)

        self.marks_edit_view["columns"] = ("id", "name", "dob", "mark")
        self.marks_edit_view.column("#0", width=0, stretch=False)
        self.marks_edit_view.column("id", width=80)
        self.marks_edit_view.column("name", width=200)
        self.marks_edit_view.column("dob", width=80)
        self.marks_edit_view.column("mark", width=40)

        # Create headings
        self.marks_edit_view.heading("#0", text="")
        self.marks_edit_view.heading("id", text="ID", anchor="w")
        self.marks_edit_view.heading("name", text="Name", anchor="w")
        self.marks_edit_view.heading("dob", text="DOB", anchor="w")
        self.marks_edit_view.heading("mark", text="Mark", anchor="w")
        self.marks_edit_view.pack(side="left", fill="both", expand=True)

        scrollbar.pack(side="left", fill="y")

        # def save_student():
        #     student_data = {
        #         "id": id_entry.get(),
        #         "name": name_entry.get(),
        #         "dob": dob_entry.get()
        #     }
        #     try:
        #         self.studentMarkController.add_student(student_data)
        #         self.insert_mark_window.destroy()
        #         self.get_list()
        #     except Exception as e:
        #         messagebox.showerror("Failed to add student", str(e))
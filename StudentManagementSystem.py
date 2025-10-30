import tkinter as tk
from tkinter import messagebox, ttk

class StudentDatabase:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Student Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#dbeafe")  # Light blue background

        self.details = {}

        # Title Label
        title = tk.Label(self.root, text="🎓 Student Management System", 
                         font=("Helvetica", 22, "bold"), bg="#1e3a8a", fg="white", pady=10)
        title.pack(fill=tk.X)

        # Frame for Entry Fields
        frame = tk.Frame(self.root, bg="#dbeafe", pady=10)
        frame.pack()

        tk.Label(frame, text="ID:", bg="#dbeafe", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(frame, text="Name:", bg="#dbeafe", font=("Helvetica", 12, "bold")).grid(row=1, column=0, padx=10, pady=5)
        tk.Label(frame, text="Subject:", bg="#dbeafe", font=("Helvetica", 12, "bold")).grid(row=2, column=0, padx=10, pady=5)
        tk.Label(frame, text="Marks:", bg="#dbeafe", font=("Helvetica", 12, "bold")).grid(row=3, column=0, padx=10, pady=5)

        self.id_entry = tk.Entry(frame, font=("Helvetica", 12))
        self.name_entry = tk.Entry(frame, font=("Helvetica", 12))
        self.sub_entry = tk.Entry(frame, font=("Helvetica", 12))
        self.marks_entry = tk.Entry(frame, font=("Helvetica", 12))

        self.id_entry.grid(row=0, column=1, padx=10, pady=5)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)
        self.sub_entry.grid(row=2, column=1, padx=10, pady=5)
        self.marks_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#dbeafe")
        btn_frame.pack(pady=10)

        style = {"font": ("Helvetica", 11, "bold"), "bg": "#1e40af", "fg": "white", "width": 15, "relief": "raised", "bd": 2}

        tk.Button(btn_frame, text="Add Student", command=self.addDetails, **style).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="Show Details", command=self.showDetails, **style).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(btn_frame, text="Search Student", command=self.searchDetails, **style).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(btn_frame, text="Update Details", command=self.updateDetails, **style).grid(row=0, column=3, padx=10, pady=5)
        tk.Button(btn_frame, text="Delete Student", command=self.deleteDetails, **style).grid(row=0, column=4, padx=10, pady=5)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Subject", "Marks"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Subject", text="Subject")
        self.tree.heading("Marks", text="Marks")

        self.tree.column("ID", width=80, anchor=tk.CENTER)
        self.tree.column("Name", width=200, anchor=tk.CENTER)
        self.tree.column("Subject", width=200, anchor=tk.CENTER)
        self.tree.column("Marks", width=100, anchor=tk.CENTER)

        self.tree.pack(pady=20)

        # Save Button at Bottom
        tk.Button(self.root, text="💾 Save to File", command=self.saveDetails, 
                  font=("Helvetica", 12, "bold"), bg="#059669", fg="white", width=20).pack(pady=10)

    # Add details
    def addDetails(self):
        try:
            id = int(self.id_entry.get())
            name = self.name_entry.get()
            sub = self.sub_entry.get()
            marks = self.marks_entry.get()

            if id in self.details:
                messagebox.showerror("Error", "Student ID already exists!")
                return
            if not (name and sub and marks):
                messagebox.showwarning("Warning", "Please fill all fields!")
                return

            self.details[id] = {"name": name, "sub": sub, "marks": marks}
            messagebox.showinfo("Success", "Student added successfully!")
            self.clearEntries()
            self.showDetails()

        except ValueError:
            messagebox.showerror("Error", "Invalid ID! Please enter a number.")

    # Show all details
    def showDetails(self):
        # Clear old rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        for id, details in self.details.items():
            self.tree.insert("", tk.END, values=(id, details['name'], details['sub'], details['marks']))

    # Search student
    def searchDetails(self):
        try:
            id = int(self.id_entry.get())
            if id in self.details:
                student = self.details[id]
                messagebox.showinfo("Student Found", f"ID: {id}\nName: {student['name']}\nSubject: {student['sub']}\nMarks: {student['marks']}")
            else:
                messagebox.showwarning("Not Found", "No student found with this ID.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric ID.")

    # Update student
    def updateDetails(self):
        try:
            id = int(self.id_entry.get())
            if id in self.details:
                name = self.name_entry.get() or self.details[id]["name"]
                sub = self.sub_entry.get() or self.details[id]["sub"]
                marks = self.marks_entry.get() or self.details[id]["marks"]

                self.details[id] = {"name": name, "sub": sub, "marks": marks}
                messagebox.showinfo("Success", "Student details updated!")
                self.clearEntries()
                self.showDetails()
            else:
                messagebox.showwarning("Not Found", "Student ID not found.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric ID.")

    # Delete student
    def deleteDetails(self):
        try:
            id = int(self.id_entry.get())
            if id in self.details:
                confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this student?")
                if confirm:
                    del self.details[id]
                    messagebox.showinfo("Deleted", "Student record deleted.")
                    self.clearEntries()
                    self.showDetails()
            else:
                messagebox.showwarning("Not Found", "Student not found.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric ID.")

    # Save to file
    def saveDetails(self):
        with open("details.txt", "w") as f:
            for id, details in self.details.items():
                f.write(f"ID: {id} | Name: {details['name']} | Subject: {details['sub']} | Marks: {details['marks']}\n")
        messagebox.showinfo("Saved", "All details saved to details.txt successfully!")

    # Clear entry fields
    def clearEntries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.sub_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)


# Run the Tkinter window
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentDatabase(root)
    root.mainloop()

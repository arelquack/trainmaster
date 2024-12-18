"""
Annotate Dataset Page View
"""
from tkinter import Label, Button, Frame, ttk, messagebox, colorchooser, Entry
from model.annotation_model import AnnotationModel

class AnnotateView:
    def __init__(self, parent):
        self.parent = parent
        self.annotation_model = AnnotationModel()
        self.selected_dataset = {"name": None}
        self.label_entries = []

        self.step1()

    def clear_body(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def step1(self):
        self.clear_body()
        Label(self.parent, text="STEP 1: PICK A DATASET", font=("Arial", 16, "bold")).pack(pady=10)

        dataset_list = self.annotation_model.get_dataset_list()

        search_frame = Frame(self.parent)
        search_frame.pack(pady=10)
        self.dataset_dropdown = ttk.Combobox(search_frame, values=dataset_list, width=50)
        self.dataset_dropdown.pack(side="left", padx=5)

        submit_button = Button(self.parent, text="SUBMIT", command=self.pick_dataset)
        submit_button.pack(pady=10)

    def pick_dataset(self):
        dataset_name = self.dataset_dropdown.get().strip()
        if self.annotation_model.validate_dataset(dataset_name):
            self.selected_dataset["name"] = dataset_name
            self.step2()
        else:
            messagebox.showerror("Error", "Invalid dataset selected!")

    def step2(self):
        self.clear_body()
        self.label_entries.clear()
        Label(self.parent, text="STEP 2: CREATE LABELS.JSON", font=("Arial", 16, "bold")).pack(pady=10)
        label_frame = Frame(self.parent)
        label_frame.pack(pady=10, fill="x")

        def add_label_form():
            form_frame = Frame(label_frame)
            form_frame.pack(pady=5, fill="x")

            name_entry = Entry(form_frame, width=30)
            name_entry.pack(side="left", padx=5)
            name_entry.insert(0, "LABEL")

            color_entry = Entry(form_frame, width=15)
            color_entry.pack(side="left", padx=5)

            def pick_color():
                color_code = colorchooser.askcolor(title="Pick a Color")[1]
                if color_code:
                    color_entry.delete(0, "end")
                    color_entry.insert(0, color_code)

            color_button = Button(form_frame, text="PICK COLOR", command=pick_color)
            color_button.pack(side="left", padx=5)

            self.label_entries.append((name_entry, color_entry))

        add_label_form()

        Button(self.parent, text="TAMBAH LABEL", command=add_label_form).pack(pady=5)
        Button(self.parent, text="SAVE", command=self.save_labels).pack(pady=10)

    def save_labels(self):
        labels = [{"name": entry[0].get(), "color": entry[1].get()} for entry in self.label_entries if entry[0].get() and entry[1].get()]
        if not labels:
            messagebox.showerror("Error", "Please add at least one valid label!")
            return
        success = self.annotation_model.save_labels(self.selected_dataset["name"], labels)
        if success:
            messagebox.showinfo("Success", "Labels saved successfully!")
        else:
            messagebox.showerror("Error", "Failed to save labels!")

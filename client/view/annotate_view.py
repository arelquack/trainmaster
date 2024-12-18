"""
Annotate Dataset Page View
"""
from tkinter import Label, Button, Frame, ttk, messagebox, colorchooser, Entry
from model.annotation_model import AnnotationModel


class AnnotateView:
    """
    AnnotateView handles the GUI for annotating datasets and creating labels.
    """

    def __init__(self, parent):
        """
        Initialize the AnnotateView object.

        Args:
            parent (tk.Frame): Parent frame to place the annotate view in.

        Attributes:
            parent (tk.Frame): Parent frame.
            annotation_model (AnnotationModel): Model for annotation functionality.
            selected_dataset (dict): Dictionary containing the name of the selected dataset.
            label_entries (list): List of label entries created by the user.
        """
        self.parent = parent
        self.annotation_model = AnnotationModel()
        self.selected_dataset = {"name": None}
        self.label_entries = []
        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the user interface starting from step 1."""
        self.show_step1()

    def clear_body(self):
        """Clear all widgets from the parent frame."""
        for widget in self.parent.winfo_children():
            widget.destroy()

    def show_step1(self):
        """Display the first step: selecting a dataset."""
        self.clear_body()
        Label(
            self.parent, text="STEP 1: PICK A DATASET", font=("Arial", 16, "bold")
        ).pack(pady=10)

        dataset_list = self.annotation_model.get_dataset_list()

        search_frame = Frame(self.parent)
        search_frame.pack(pady=10)
        self.dataset_dropdown = ttk.Combobox(search_frame, values=dataset_list, width=50)
        self.dataset_dropdown.pack(side="left", padx=5)

        Button(self.parent, text="SUBMIT", command=self.pick_dataset).pack(pady=10)

    def pick_dataset(self):
        """Handle the selection of a dataset."""
        dataset_name = self.dataset_dropdown.get().strip()
        if self.annotation_model.validate_dataset(dataset_name):
            self.selected_dataset["name"] = dataset_name
            self.show_step2()
        else:
            messagebox.showerror("Error", "Invalid dataset selected!")

    def show_step2(self):
        """Display the second step: creating labels."""
        self.clear_body()
        self.label_entries.clear()
        Label(
            self.parent, text="STEP 2: CREATE LABELS.JSON", font=("Arial", 16, "bold")
        ).pack(pady=10)
        label_frame = Frame(self.parent)
        label_frame.pack(pady=10, fill="x")

        self.add_label_form(label_frame)

        Button(self.parent, text="ADD LABEL", command=lambda: self.add_label_form(label_frame)).pack(pady=5)
        Button(self.parent, text="SAVE", command=self.save_labels).pack(pady=10)

    def add_label_form(self, parent_frame):
        """Add a new label form dynamically."""
        form_frame = Frame(parent_frame)
        form_frame.pack(pady=5, fill="x")

        name_entry = Entry(form_frame, width=30)
        name_entry.pack(side="left", padx=5)
        name_entry.insert(0, "LABEL")

        color_entry = Entry(form_frame, width=15)
        color_entry.pack(side="left", padx=5)

        def pick_color():
            """Open color chooser and insert selected color."""
            color_code = colorchooser.askcolor(title="Pick a Color")[1]
            if color_code:
                color_entry.delete(0, "end")
                color_entry.insert(0, color_code)

        Button(form_frame, text="PICK COLOR", command=pick_color).pack(side="left", padx=5)

        self.label_entries.append((name_entry, color_entry))

    def save_labels(self):
        """Save labels to the dataset."""
        labels = [
            {"name": entry[0].get(), "color": entry[1].get()}
            for entry in self.label_entries
            if entry[0].get() and entry[1].get()
        ]
        if not labels:
            messagebox.showerror("Error", "Please add at least one valid label!")
            return
        try:
            success = self.annotation_model.save_labels(self.selected_dataset["name"], labels)
            if success:
                messagebox.showinfo("Success", "Labels saved successfully!")
            else:
                raise ValueError("Saving labels failed!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
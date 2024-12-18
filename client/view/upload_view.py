"""
Upload Dataset Page View with ttkbootstrap
"""
from ttkbootstrap import Label, Button, Entry, Frame
from ttkbootstrap.constants import SUCCESS, INFO, PRIMARY, SECONDARY, WARNING
from model.dataset_model import DatasetModel
from tkinter import filedialog, messagebox

class UploadView:
    def __init__(self, parent):
        self.parent = parent
        self.dataset_model = DatasetModel()
        self.setup_ui()

    def setup_ui(self):
        Label(self.parent, text="🚀 UPLOAD DATASET 🚀", font=("Arial", 20, "bold"), bootstyle=INFO).pack(pady=10)

        # Dataset Name Input
        Label(self.parent, text="NAME OF DATASET:", bootstyle=PRIMARY).pack(pady=5)
        self.name_entry = Entry(self.parent, bootstyle=SECONDARY, width=40)
        self.name_entry.pack(pady=5)

        # Directory Path Input
        Label(self.parent, text="PATH TO DIRECTORY:", bootstyle=PRIMARY).pack(pady=5)
        path_frame = Frame(self.parent, bootstyle=SECONDARY)
        path_frame.pack(pady=5)

        self.path_entry = Entry(path_frame, width=30)
        self.path_entry.pack(side="left", padx=(0, 5))
        Button(path_frame, text="Browse", command=self.browse_directory, bootstyle=SUCCESS).pack(side="left")

        # Submit Button
        Button(self.parent, text="SUBMIT", command=self.save_dataset, bootstyle=WARNING, padding=10).pack(pady=20)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, directory)

    def save_dataset(self):
        dataset_name = self.name_entry.get().strip()
        directory_path = self.path_entry.get().strip()

        if not dataset_name or not directory_path:
            messagebox.showerror("Error", "Please fill out all fields!")
            return
        
        success = self.dataset_model.save_dataset(dataset_name, directory_path)
        if success:
            messagebox.showinfo("Success", f"Dataset '{dataset_name}' has been saved successfully!")
        else:
            messagebox.showerror("Error", "Failed to save dataset!")

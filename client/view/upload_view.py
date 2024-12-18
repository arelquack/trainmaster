from ttkbootstrap import Label, Button, Entry, Frame
from ttkbootstrap.constants import SUCCESS, INFO, PRIMARY, SECONDARY, WARNING
from model.dataset_model import DatasetModel
from tkinter import filedialog, messagebox
import os

class UploadView:
    """
    A GUI view for uploading datasets using ttkbootstrap.
    """

    def __init__(self, parent):
        """
        Initialize the UploadView class.

        :param parent: Parent tkinter widget.
        """
        self.parent = parent
        self.dataset_model = DatasetModel()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface elements.
        """
        Label(self.parent, text="🚀 UPLOAD DATASET 🚀", font=("Arial", 20, "bold"), bootstyle=INFO).pack(pady=10)

        # Dataset Name Input
        Label(self.parent, text="NAME OF DATASET:", bootstyle=PRIMARY).pack(pady=5)
        self.dataset_name_entry = Entry(self.parent, bootstyle=SECONDARY, width=40)
        self.dataset_name_entry.pack(pady=5)

        # Directory Path Input
        Label(self.parent, text="PATH TO DIRECTORY:", bootstyle=PRIMARY).pack(pady=5)
        path_frame = Frame(self.parent, bootstyle=SECONDARY)
        path_frame.pack(pady=5)

        self.directory_path_entry = Entry(path_frame, width=30)
        self.directory_path_entry.pack(side="left", padx=(0, 5))
        Button(path_frame, text="Browse", command=self._browse_directory, bootstyle=SUCCESS).pack(side="left")

        # Submit Button
        Button(self.parent, text="SUBMIT", command=self._handle_submit, bootstyle=WARNING, padding=10).pack(pady=20)

    def _browse_directory(self):
        """
        Open a directory dialog for the user to select a directory.
        """
        directory = filedialog.askdirectory()
        if directory:
            self.directory_path_entry.delete(0, "end")
            self.directory_path_entry.insert(0, directory)

    def _handle_submit(self):
        """
        Handle the submit button click event.
        """
        dataset_name = self.dataset_name_entry.get().strip()
        directory_path = self.directory_path_entry.get().strip()

        if not self._validate_inputs(dataset_name, directory_path):
            return

        try:
            success = self.dataset_model.save_dataset(dataset_name, directory_path)
            if success:
                messagebox.showinfo("Success", f"Dataset '{dataset_name}' has been saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save dataset! Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def _validate_inputs(self, dataset_name, directory_path):
        """
        Validate the inputs provided by the user.

        :param dataset_name: Name of the dataset.
        :param directory_path: Path to the directory.
        :return: True if inputs are valid, False otherwise.
        """
        if not dataset_name:
            messagebox.showerror("Error", "Dataset name cannot be empty!")
            return False

        if not directory_path:
            messagebox.showerror("Error", "Directory path cannot be empty!")
            return False

        if not os.path.isdir(directory_path):
            messagebox.showerror("Error", "The specified directory does not exist!")
            return False

        if not os.access(directory_path, os.W_OK):
            messagebox.showerror("Error", "The specified directory is not writable!")
            return False

        return True

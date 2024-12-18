import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class UploadDatasetPage:
    def __init__(self, parent_frame):
        """Initialize the Upload Dataset Page."""
        self.parent_frame = parent_frame
        self.name_entry = None
        self.path_entry = None
        self.body_frame = tk.Frame(self.parent_frame)
        self.body_frame.pack(fill="both", expand=True)
        self._create_ui()

    def _create_ui(self):
        """Create UI elements for the upload page."""
        tk.Label(self.body_frame, text="UPLOAD DATASET", font=("Arial", 16, "bold")).pack(pady=10)

        # Dataset Name
        tk.Label(self.body_frame, text="NAME OF DATASET:", font=("Arial", 12)).pack()
        self.name_entry = tk.Entry(self.body_frame, width=40)
        self.name_entry.pack(pady=5)

        # Path to Directory
        tk.Label(self.body_frame, text="PATH TO DIRECTORY:", font=("Arial", 12)).pack()
        path_frame = tk.Frame(self.body_frame)
        path_frame.pack(pady=5)

        self.path_entry = tk.Entry(path_frame, width=30)
        self.path_entry.pack(side="left", padx=(0, 5))

        browse_button = tk.Button(path_frame, text="Browse", command=self._browse_directory, bg="lightgray")
        browse_button.pack(side="left")

        # Submit Button
        submit_button = tk.Button(
            self.body_frame, text="SUBMIT", command=self._save_dataset, bg="lightgray", padx=20, pady=10
        )
        submit_button.pack(pady=20)

    def _browse_directory(self):
        """Browse and select a directory."""
        directory = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, directory)

    def _save_dataset(self):
        """Save dataset to the specified directory."""
        dataset_name = self.name_entry.get().strip()
        directory_path = self.path_entry.get().strip()

        if not dataset_name or not directory_path:
            messagebox.showerror("Error", "Please fill out all fields!")
            return

        main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset", dataset_name)
        os.makedirs(main_dataset_dir, exist_ok=True)

        image_extensions = (".png", ".jpg", ".jpeg")
        
        try:
            self._process_files(directory_path, main_dataset_dir, image_extensions)
            messagebox.showinfo("Success", f"Dataset '{dataset_name}' has been saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def _process_files(self, source_dir, dest_dir, valid_extensions):
        """Process and save image files from the source directory to the destination directory."""
        counter = 1
        for file in os.listdir(source_dir):
            if file.lower().endswith(valid_extensions):
                file_path = os.path.join(source_dir, file)
                try:
                    img = Image.open(file_path).convert("RGB")
                    output_file_path = os.path.join(dest_dir, f"{counter}.png")
                    img.save(output_file_path, "PNG")
                    counter += 1
                except Exception as e:
                    print(f"Error processing {file}: {e}")

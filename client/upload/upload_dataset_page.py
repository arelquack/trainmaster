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
        self.body_frame.pack()
        self.create_ui()

    def create_ui(self):
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

        browse_button = tk.Button(path_frame, text="Browse", command=self.browse_directory, bg="lightgray")
        browse_button.pack(side="left")

        # Submit Button
        submit_button = tk.Button(self.body_frame, text="SUBMIT", command=self.save_dataset, bg="lightgray", padx=20, pady=10)
        submit_button.pack(pady=20)

    def browse_directory(self):
        """Browse and select a directory."""
        directory = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, directory)

    def save_dataset(self):
        """Save dataset to the specified directory."""
        dataset_name = self.name_entry.get().strip()
        directory_path = self.path_entry.get().strip()

        if not dataset_name or not directory_path:
            messagebox.showerror("Error", "Please fill out all fields!")
            return

        # Create the main dataset directory
        main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset", dataset_name)
        os.makedirs(main_dataset_dir, exist_ok=True)

        # Process files in the directory
        image_extensions = (".png", ".jpg", ".jpeg")
        counter = 1

        for file in os.listdir(directory_path):
            if file.lower().endswith(image_extensions):
                file_path = os.path.join(directory_path, file)

                try:
                    # Open image and convert to PNG
                    img = Image.open(file_path)
                    img = img.convert("RGB")  # Ensure RGB format

                    # Save with sequential numbering in the named subfolder
                    output_file_path = os.path.join(main_dataset_dir, f"{counter}.png")
                    img.save(output_file_path, "PNG")
                    counter += 1

                except Exception as e:
                    print(f"Error processing {file}: {e}")

        messagebox.showinfo("Success", f"Dataset '{dataset_name}' has been saved successfully!")

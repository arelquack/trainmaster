import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO  # Pastikan YOLO sudah terinstall
from utils import get_server_port  # Mengimpor get_server_port

class PredictPage:
    def __init__(self, parent_frame):
        """Initialize Predict Page."""
        self.parent_frame = parent_frame
        self.main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset")
        self.selected_dataset = {"name": None}
        
        self.body_frame = tk.Frame(self.parent_frame)
        self.body_frame.pack(fill="both", expand=True)

        # Start Step 1
        self.step1()

    def clear_body(self):
        """Clear all widgets inside the body frame."""
        for widget in self.body_frame.winfo_children():
            widget.destroy()

    def step1(self):
        """Step 1: Pick a dataset."""
        self.clear_body()
        
        def pick_dataset(event=None):
            dataset_name = dataset_dropdown.get().strip()
            if dataset_name in dataset_list:
                self.selected_dataset["name"] = dataset_name
                self.step2()  # Move to Step 2
        
        # Load dataset names
        dataset_list = [d for d in os.listdir(self.main_dataset_dir) if os.path.isdir(os.path.join(self.main_dataset_dir, d))]
        
        tk.Label(self.body_frame, text="STEP 1: PICK A DATASET", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.body_frame, text="SELECT DATASET:", font=("Arial", 12)).pack(pady=5)
        
        # Searchable dropdown
        search_frame = tk.Frame(self.body_frame)
        search_frame.pack(pady=10)
        
        dataset_dropdown = ttk.Combobox(search_frame, values=dataset_list, width=50)
        dataset_dropdown.pack(side="left", padx=5)
        dataset_dropdown.bind("<<ComboboxSelected>>", pick_dataset)
        
        submit_button = tk.Button(self.body_frame, text="SUBMIT", command=lambda: pick_dataset())
        submit_button.pack(pady=10)

    def step2(self):
        """Step 2: List files with .pt extension."""
        self.clear_body()

        dataset_name = self.selected_dataset["name"]
        dataset_path = os.path.join(self.main_dataset_dir, dataset_name)

        # Get all .pt files in the dataset folder
        pt_files = [f for f in os.listdir(dataset_path) if f.endswith(".pt")]
        
        if not pt_files:
            messagebox.showinfo("No Files Found", f"No .pt files found in {dataset_name}.")
            return
        
        # Display .pt files
        tk.Label(self.body_frame, text="FILES WITH .PT EXTENSION", font=("Arial", 16, "bold")).pack(pady=10)
        
        for pt_file in pt_files:
            tk.Label(self.body_frame, text=pt_file, font=("Arial", 12)).pack(pady=5)

            # Move to Step 3 after displaying .pt files
            self.step3(dataset_name, pt_file)
            break

    def step3(self, dataset_name, pt_file):
        """Step 3: Predict using YOLO model."""
        model = YOLO(f"list_of_dataset/{dataset_name}/{pt_file}")
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Cannot open webcam")
            return

        # Function to update the camera feed
        def update_frame():
            ret, frame = cap.read()  # Read a frame from the camera
            if ret:
                # Convert the frame from BGR to RGB
                results = model(frame, stream=True)
                for result in results:
                    annotated_frame = result.plot()
                frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                
                # Convert the frame into an Image object
                img = Image.fromarray(frame_rgb)
                img_tk = ImageTk.PhotoImage(img)
                
                # Update the image displayed in the label
                label.img_tk = img_tk  # Store a reference to avoid garbage collection
                label.configure(image=img_tk)
            
            # Call this function again after 10ms to update the feed
            label.after(10, update_frame)
        
        # Start the update loop
        label = tk.Label(self.parent_frame)
        label.pack()
        update_frame()

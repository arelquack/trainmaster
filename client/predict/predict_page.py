import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO

class PredictPage:
    """GUI Page for predicting using YOLO model."""

    def __init__(self, parent_frame):
        """Initialize PredictPage with parent frame."""
        self.parent_frame = parent_frame
        self.main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset")
        self.selected_dataset = {"name": None}

        self.body_frame = tk.Frame(self.parent_frame)
        self.body_frame.pack(fill="both", expand=True)

        self.step1()  # Initialize Step 1

    def clear_body(self):
        """Clear all widgets inside the body frame."""
        for widget in self.body_frame.winfo_children():
            widget.destroy()

    def step1(self):
        """Step 1: Pick a dataset from available options."""
        self.clear_body()

        def pick_dataset(event=None):
            dataset_name = dataset_dropdown.get().strip()
            if dataset_name in dataset_list:
                self.selected_dataset["name"] = dataset_name
                self.step2()  # Proceed to Step 2

        dataset_list = [
            d for d in os.listdir(self.main_dataset_dir) 
            if os.path.isdir(os.path.join(self.main_dataset_dir, d))
        ]

        tk.Label(self.body_frame, text="STEP 1: PICK A DATASET", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.body_frame, text="SELECT DATASET:", font=("Arial", 12)).pack(pady=5)

        # Create searchable dropdown
        search_frame = tk.Frame(self.body_frame)
        search_frame.pack(pady=10)

        dataset_dropdown = ttk.Combobox(search_frame, values=dataset_list, width=50)
        dataset_dropdown.pack(side="left", padx=5)
        dataset_dropdown.bind("<<ComboboxSelected>>", pick_dataset)

        submit_button = tk.Button(
            self.body_frame, text="SUBMIT", command=lambda: pick_dataset()
        )
        submit_button.pack(pady=10)

    def step2(self):
        """Step 2: List all .pt files in the selected dataset."""
        self.clear_body()

        dataset_name = self.selected_dataset["name"]
        dataset_path = os.path.join(self.main_dataset_dir, dataset_name)

        pt_files = [
            f for f in os.listdir(dataset_path) 
            if f.endswith(".pt")
        ]

        if not pt_files:
            messagebox.showinfo("No Files Found", f"No .pt files found in {dataset_name}.")
            self.step1()
            return

        tk.Label(self.body_frame, text="FILES WITH .PT EXTENSION", font=("Arial", 16, "bold")).pack(pady=10)

        for pt_file in pt_files:
            tk.Label(self.body_frame, text=pt_file, font=("Arial", 12)).pack(pady=5)

        # Use the first .pt file for prediction
        if pt_files:
            self.step3(dataset_name, pt_files[0])

    def step3(self, dataset_name, pt_file):
        """Step 3: Perform prediction using YOLO model."""
        model_path = os.path.join(self.main_dataset_dir, dataset_name, pt_file)
        model = YOLO(model_path)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot open webcam.")
            return

        def update_frame():
            ret, frame = cap.read()
            if ret:
                results = model(frame, stream=True)
                for result in results:
                    annotated_frame = result.plot()
                frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)

                img = Image.fromarray(frame_rgb)
                img_tk = ImageTk.PhotoImage(img)

                label.img_tk = img_tk  # Prevent garbage collection
                label.configure(image=img_tk)

            label.after(10, update_frame)

        label = tk.Label(self.parent_frame)
        label.pack()
        update_frame()

        self.body_frame.protocol("WM_DELETE_WINDOW", lambda: self._cleanup(cap))

    def _cleanup(self, cap):
        """Release resources and close the application."""
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()

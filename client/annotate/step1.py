import tkinter as tk
from tkinter import ttk
import os

def show_step1(body_frame, main_dataset_dir, selected_dataset, step2_callback):
    """Step 1: Pick a dataset."""
    # Clear existing content
    for widget in body_frame.winfo_children():
        widget.destroy()

    def pick_dataset(event=None):
        dataset_name = dataset_dropdown.get().strip()
        if dataset_name:
            selected_dataset["name"] = dataset_name
            step2_callback()  # Move to Step 2

    # Load dataset names from the directory
    dataset_list = [d for d in os.listdir(main_dataset_dir) if os.path.isdir(os.path.join(main_dataset_dir, d))]

    # UI for Step 1
    tk.Label(body_frame, text="STEP 1: PICK A DATASET", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(body_frame, text="SELECT DATASET:", font=("Arial", 12)).pack(pady=5)

    # Searchable dropdown for datasets
    search_frame = tk.Frame(body_frame)
    search_frame.pack(pady=10)

    dataset_dropdown = ttk.Combobox(search_frame, values=dataset_list, width=50)
    dataset_dropdown.pack(side="left", padx=5)
    dataset_dropdown.bind("<<ComboboxSelected>>", pick_dataset)

    submit_button = tk.Button(body_frame, text="SUBMIT", command=lambda: pick_dataset())
    submit_button.pack(pady=10)

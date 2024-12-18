import tkinter as tk
from tkinter import ttk
import os

def show_step1(body_frame, main_dataset_dir, selected_dataset, step2_callback):
    """Step 1: Pick a dataset.
    
    Parameters:
    body_frame (tk.Frame): The frame where UI elements will be displayed.
    main_dataset_dir (str): The directory where datasets are located.
    selected_dataset (dict): Dictionary to store the selected dataset name.
    step2_callback (function): Callback function to move to the next step.
    """
    # Clear existing content
    for widget in body_frame.winfo_children():
        widget.destroy()

    def pick_dataset(event=None):
        """Handles the selection of a dataset."""
        dataset_name = dataset_dropdown.get().strip()
        if dataset_name:
            selected_dataset["name"] = dataset_name
            step2_callback()  # Move to Step 2

    def load_datasets(dataset_dir):
        """Load dataset names from the specified directory.
        
        Args:
        dataset_dir (str): The directory containing dataset folders.
        
        Returns:
        list: A list of dataset names found in the directory.
        """
        if not os.path.exists(dataset_dir):
            raise FileNotFoundError(f"Directory {dataset_dir} does not exist.")
        
        dataset_list = [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]
        if not dataset_list:
            raise ValueError("No datasets found in the specified directory.")
        
        return dataset_list

    try:
        # Load dataset names from the directory
        dataset_list = load_datasets(main_dataset_dir)
    except (FileNotFoundError, ValueError) as e:
        # Handle errors gracefully
        tk.Label(body_frame, text=str(e), fg="red", font=("Arial", 12)).pack(pady=10)
        return

    # UI for Step 1
    tk.Label(body_frame, text="STEP 1: PICK A DATASET", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(body_frame, text="SELECT DATASET:", font=("Arial", 12)).pack(pady=5)

    # Searchable dropdown for datasets
    search_frame = tk.Frame(body_frame)
    search_frame.pack(pady=10)

    dataset_dropdown = ttk.Combobox(search_frame, values=dataset_list, width=50, state="readonly")
    dataset_dropdown.pack(side="left", padx=5)
    dataset_dropdown.bind("<<ComboboxSelected>>", pick_dataset)

    submit_button = tk.Button(body_frame, text="SUBMIT", command=pick_dataset)
    submit_button.pack(pady=10)

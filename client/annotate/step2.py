import tkinter as tk
from tkinter import colorchooser, messagebox
import os
import json

def show_step2(body_frame, main_dataset_dir, selected_dataset, step3_callback):
    """Step 2: Fill labels.json.
    
    Parameters:
    body_frame (tk.Frame): The frame where UI elements will be displayed.
    main_dataset_dir (str): The directory where datasets are located.
    selected_dataset (dict): Dictionary to store the selected dataset name.
    step3_callback (function): Callback function to move to the next step.
    """
    # Clear existing content
    for widget in body_frame.winfo_children():
        widget.destroy()

    label_entries = []  # To store label entry references

    def pick_color(entry):
        """Open color chooser and set color."""
        color_code = colorchooser.askcolor(title="Pick a Color")[1]
        if color_code:
            entry.delete(0, tk.END)
            entry.insert(0, color_code)

    def add_label_form():
        """Add a new label form for entering label and color."""
        form_frame = tk.Frame(label_frame)
        form_frame.pack(pady=5, fill="x")

        name_entry = tk.Entry(form_frame, width=30)
        name_entry.pack(side="left", padx=5)
        name_entry.insert(0, "LABEL")

        color_entry = tk.Entry(form_frame, width=15)
        color_entry.pack(side="left", padx=5)

        color_button = tk.Button(form_frame, text="PICK COLOR", command=lambda: pick_color(color_entry), bg="lightgray")
        color_button.pack(side="left", padx=5)

        label_entries.append((name_entry, color_entry))

    def save_labels_and_continue():
        """Save the entered labels and colors to a JSON file."""
        labels_data = []
        for name_entry, color_entry in label_entries:
            name = name_entry.get().strip()
            color = color_entry.get().strip()
            if name and color:
                labels_data.append({"name": name, "color": color})

        if not labels_data:
            messagebox.showerror("Error", "Please add at least one label.")
            return

        # Save labels.json
        dataset_path = os.path.join(main_dataset_dir, selected_dataset["name"])
        json_path = os.path.join(dataset_path, "labels.json")

        # Check if the dataset directory exists and is writable
        if not os.path.exists(dataset_path):
            messagebox.showerror("Error", f"Dataset directory '{dataset_path}' does not exist.")
            return
        
        try:
            with open(json_path, "w") as json_file:
                json.dump(labels_data, json_file, indent=4)
            step3_callback(selected_dataset["name"])  # Move to Step 3
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    # UI for Step 2
    tk.Label(body_frame, text="STEP 2: CREATE LABELS.JSON", font=("Arial", 16, "bold")).pack(pady=10)

    label_frame = tk.Frame(body_frame)
    label_frame.pack(pady=10, fill="x")

    add_label_form()  # Add initial form

    # Buttons
    add_label_button = tk.Button(body_frame, text="ADD LABEL", command=add_label_form, bg="lightgray", padx=10, pady=5)
    add_label_button.pack(pady=5)

    save_button = tk.Button(body_frame, text="SAVE AND CONTINUE", command=save_labels_and_continue, bg="lightgray", padx=20, pady=10)
    save_button.pack(pady=10)

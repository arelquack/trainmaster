import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os

def show_step3(body_frame, dataset_name):
    """Step 3: Display images, annotate with rectangles, and save labels in YOLOv8 format.
    
    Parameters:
    body_frame (tk.Frame): The frame where UI elements will be displayed.
    dataset_name (str): The name of the selected dataset.
    """
    # Clear existing content
    for widget in body_frame.winfo_children():
        widget.destroy()

    current_image_index = 0
    image_files = []
    rectangles = []  # Store annotated rectangles
    is_first_click = True
    start_x, start_y = None, None
    rect_id = None
    selected_color = None

    # Path to the dataset folder
    dataset_path = os.path.join("list_of_dataset", dataset_name)
    
    # Get all PNG files in the folder
    image_files = [f for f in os.listdir(dataset_path) if f.endswith(".png")]
    if not image_files:
        messagebox.showerror("Error", "No images found in the selected dataset.")
        return

    # Initialize label colors and names
    labels_json_path = os.path.join(dataset_path, "labels.json")
    if not os.path.exists(labels_json_path):
        messagebox.showerror("Error", "labels.json not found in the dataset folder.")
        return

    with open(labels_json_path, "r") as file:
        labels = json.load(file)

    label_index_map = {label["name"]: idx for idx, label in enumerate(labels)}

    # Frame for navigation and image display
    nav_frame = tk.Frame(body_frame)
    nav_frame.pack(pady=10)

    # Label for dataset name
    dataset_label = tk.Label(body_frame, text=dataset_name, font=("Arial", 16, "bold"))
    dataset_label.pack()

    # Prev Button
    prev_button = tk.Button(nav_frame, text="PREV", command=lambda: navigate_image(-1), bg="lightgray", padx=10, pady=5)
    prev_button.pack(side="left", padx=10)

    # Current Image Name
    image_name_label = tk.Label(nav_frame, text="", font=("Arial", 14))
    image_name_label.pack(side="left", padx=10)

    # Next Button
    next_button = tk.Button(nav_frame, text="NEXT", command=lambda: navigate_image(1), bg="lightgray", padx=10, pady=5)
    next_button.pack(side="left", padx=10)

    # Dropdown for labels
    dropdown_frame = tk.Frame(body_frame)
    dropdown_frame.pack(pady=10)

    tk.Label(dropdown_frame, text="Select Label:", font=("Arial", 12)).pack(side="left", padx=5)
    label_dropdown = ttk.Combobox(dropdown_frame, values=[label["name"] for label in labels], width=30)
    label_dropdown.pack(side="left", padx=5)

    color_label = tk.Label(dropdown_frame, text="", font=("Arial", 12))
    color_label.pack(side="left", padx=10)

    def on_label_select(event):
        """Update the selected color based on the dropdown selection."""
        nonlocal selected_color
        selected_label = label_dropdown.get()
        for label in labels:
            if label["name"] == selected_label:
                selected_color = label["color"]
                color_label.config(text=f"Color: {selected_color}", bg=selected_color)
                break

    label_dropdown.bind("<<ComboboxSelected>>", on_label_select)

    # Frame for displaying the image
    image_frame = tk.Frame(body_frame, bg="white")
    image_frame.pack(pady=10)

    # Canvas for the image
    canvas = tk.Canvas(image_frame, width=500, height=500, bg="lightgray")
    canvas.pack()

    def display_image():
        """Load and display the current image."""
        try:
            image_path = os.path.join(dataset_path, image_files[current_image_index])
            img = Image.open(image_path)
            img = img.resize((500, 500))  # Resize for display purposes
            img_tk = ImageTk.PhotoImage(img)

            # Clear the canvas
            canvas.delete("all")
            canvas.create_image(0, 0, anchor="nw", image=img_tk)
            canvas.image = img_tk  # Keep a reference to avoid garbage collection

            # Update the current image name
            image_name_label.config(text=image_files[current_image_index])

            # Clear previous rectangles
            rectangles.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def navigate_image(step):
        """Navigate between images and save rectangles to file before moving."""
        nonlocal current_image_index
        save_rectangles_to_file()

        current_image_index += step

        # Ensure index is within bounds
        if current_image_index < 0:
            current_image_index = len(image_files) - 1
        elif current_image_index >= len(image_files):
            current_image_index = 0

        # Display the updated image
        display_image()

    def save_rectangles_to_file():
        """Save all rectangles in YOLOv8 format to a .txt file."""
        if not rectangles:
            return

        image_name = os.path.splitext(image_files[current_image_index])[0]
        txt_path = os.path.join(dataset_path, f"{image_name}.txt")

        try:
            with open(txt_path, "w") as file:
                for label_name, x1, y1, x2, y2 in rectangles:
                    # Convert rectangle coordinates to YOLOv8 format (normalized center x, center y, width, height)
                    label_index = label_index_map[label_name]
                    center_x = (x1 + x2) / 2 / 500
                    center_y = (y1 + y2) / 2 / 500
                    width = abs(x2 - x1) / 500
                    height = abs(y2 - y1) / 500
                    file.write(f"{label_index} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save annotations: {str(e)}")

    def click_event(event):
        """Handle mouse clicks for initiating and finalizing the rectangle."""
        nonlocal start_x, start_y, is_first_click, rect_id

        if not selected_color or not label_dropdown.get():
            messagebox.showwarning("Warning", "Please select a label first.")
            return

        if is_first_click:
            # First click: record the starting point and create the rectangle
            start_x, start_y = event.x, event.y
            rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline=selected_color, width=2)
            is_first_click = False
        else:
            # Second click: finalize the rectangle
            end_x, end_y = event.x, event.y
            rectangles.append((label_dropdown.get(), start_x, start_y, end_x, end_y))
            is_first_click = True

    def motion_event(event):
        """Update the rectangle dimensions dynamically as the cursor moves."""
        nonlocal rect_id, start_x, start_y, is_first_click

        if not is_first_click and rect_id:
            # Update the rectangle's coordinates based on the cursor position
            canvas.coords(rect_id, start_x, start_y, event.x, event.y)

    canvas.bind("<Button-1>", click_event)  # Handle clicks
    canvas.bind("<Motion>", motion_event)  # Handle cursor movement

    # Display the first image initially
    display_image()

import os
import tkinter as tk
from annotate.step1 import show_step1
from annotate.step2 import show_step2
from annotate.step3 import show_step3

class AnnotatePage:
    def __init__(self, parent_frame):
        """Initialize Annotate Page."""
        self.parent_frame = parent_frame
        self.main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset")
        self.selected_dataset = {"name": None}
        
        self.body_frame = tk.Frame(self.parent_frame)
        self.body_frame.pack(fill="both", expand=True)

        # Start Step 1
        show_step1(self.body_frame, self.main_dataset_dir, self.selected_dataset, self.show_step2)

    def show_step2(self):
        """Move to Step 2 (Call from step1.py)."""
        show_step2(self.body_frame, self.main_dataset_dir, self.selected_dataset, self.show_step3)

    def show_step3(self, dataset_name):
        """Move to Step 3 (Call from step2.py)."""
        # show_step3(self.body_frame, self.selected_dataset["name"])
        show_step3(self.body_frame, dataset_name)

"""
Predict Dataset Page View
"""
from tkinter import Label, Button, Frame, ttk, messagebox
from model.predict_model import PredictModel

class PredictView:
    def __init__(self, parent):
        self.parent = parent
        self.predict_model = PredictModel()
        self.selected_dataset = None

        self.setup_ui()

    def setup_ui(self):
        Label(self.parent, text="PREDICT PAGE", font=("Arial", 16, "bold")).pack(pady=10)

        dataset_list = self.predict_model.get_dataset_list()
        if not dataset_list:
            Label(self.parent, text="No datasets found!", fg="red").pack(pady=10)
            return

        # Dataset Selection
        Label(self.parent, text="CHOOSE DATASET:").pack(pady=5)
        self.selected_dataset_var = ttk.Combobox(self.parent, values=dataset_list, state="readonly", width=40)
        self.selected_dataset_var.pack(pady=5)

        Button(self.parent, text="START PREDICTION", command=self.start_prediction).pack(pady=10)

    def start_prediction(self):
        dataset_name = self.selected_dataset_var.get()
        if not dataset_name:
            messagebox.showerror("Error", "Please select a dataset!")
            return

        success = self.predict_model.start_prediction(dataset_name)
        if not success:
            messagebox.showerror("Error", "Failed to start prediction!")

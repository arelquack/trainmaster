"""
Train Dataset Page View
"""
from tkinter import Label, Button, Frame, ttk, messagebox
from model.train_model import TrainModel

class TrainView:
    def __init__(self, parent):
        self.parent = parent
        self.train_model = TrainModel()
        self.selected_dataset = None

        self.setup_ui()

    def setup_ui(self):
        Label(self.parent, text="TRAIN PAGE", font=("Arial", 16, "bold")).pack(pady=10)

        dataset_list = self.train_model.get_dataset_list()
        if not dataset_list:
            Label(self.parent, text="No datasets found!", fg="red").pack(pady=10)
            return

        # Dropdown for dataset selection
        Label(self.parent, text="CHOOSE DATASET:").pack(pady=5)
        self.selected_dataset_var = ttk.Combobox(self.parent, values=dataset_list, state="readonly", width=40)
        self.selected_dataset_var.pack(pady=5)

        Button(self.parent, text="SEND FILES TO SERVER", command=self.send_files).pack(pady=5)
        Button(self.parent, text="RECEIVE BEST MODEL", command=self.receive_best_model).pack(pady=5)

        self.status_label = Label(self.parent, text="", fg="green")
        self.status_label.pack(pady=5)

    def send_files(self):
        dataset_name = self.selected_dataset_var.get()
        if not dataset_name:
            messagebox.showerror("Error", "Please select a dataset!")
            return

        success, message = self.train_model.send_files_to_server(dataset_name)
        if success:
            self.status_label.config(text=message, fg="green")
        else:
            self.status_label.config(text=message, fg="red")

    def receive_best_model(self):
        dataset_name = self.selected_dataset_var.get()
        if not dataset_name:
            messagebox.showerror("Error", "Please select a dataset!")
            return

        success, message = self.train_model.receive_best_model_from_server(dataset_name)
        if success:
            self.status_label.config(text=message, fg="green")
        else:
            self.status_label.config(text=message, fg="red")

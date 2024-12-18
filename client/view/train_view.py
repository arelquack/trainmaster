"""
Train Dataset Page View
"""
from tkinter import Label, Button, Frame, ttk, messagebox
from model.train_model import TrainModel

class TrainView:
    def __init__(self, parent):
        """
        Initializes the TrainView class.

        Args:
            parent (tkinter widget): The parent widget of this view.

        Attributes:
            parent (tkinter widget): The parent widget of this view.
            train_model (TrainModel): The model that handles the training process.
            selected_dataset (str): The name of the dataset selected by the user.
        """

        self.parent = parent
        self.train_model = TrainModel()
        self.selected_dataset = None

        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface components for the Train page."""
        Label(self.parent, text="TRAIN PAGE", font=("Arial", 16, "bold")).pack(pady=10)

        dataset_list = self.train_model.get_dataset_list()
        if not dataset_list:
            self.display_message("No datasets found!", "red")
            return

        # Dropdown for dataset selection
        Label(self.parent, text="CHOOSE DATASET:").pack(pady=5)
        self.dataset_selector = ttk.Combobox(self.parent, values=dataset_list, state="readonly", width=40)
        self.dataset_selector.pack(pady=5)

        # Buttons
        Button(self.parent, text="SEND FILES TO SERVER", command=self.handle_send_files).pack(pady=5)
        Button(self.parent, text="RECEIVE BEST MODEL", command=self.handle_receive_best_model).pack(pady=5)

        # Status Label
        self.status_label = Label(self.parent, text="", fg="green")
        self.status_label.pack(pady=5)

    def handle_send_files(self):
        """Handles sending files to the server."""
        self.execute_action(self.train_model.send_files_to_server, "Files sent successfully!", "Failed to send files.")

    def handle_receive_best_model(self):
        """Handles receiving the best model from the server."""
        self.execute_action(self.train_model.receive_best_model_from_server, "Model received successfully!", "Failed to receive model.")

    def execute_action(self, action, success_message, failure_message):
        """Executes a given action with standardized error handling."""
        dataset_name = self.dataset_selector.get()
        if not dataset_name:
            self.show_error("Please select a dataset!")
            return

        try:
            success, message = action(dataset_name)
            if success:
                self.display_message(success_message, "green")
            else:
                self.display_message(message or failure_message, "red")
        except Exception as e:
            self.log_error(e)
            self.display_message("An unexpected error occurred.", "red")

    def display_message(self, message, color):
        """Displays a status message with a given color."""
        self.status_label.config(text=message, fg=color)

    def show_error(self, message):
        """Displays an error message to the user."""
        messagebox.showerror("Error", message)

    def log_error(self, error):
        """Logs an error for debugging purposes."""
        # For production, replace print with proper logging
        print(f"Error: {error}")

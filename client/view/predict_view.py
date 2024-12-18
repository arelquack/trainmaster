import logging
from tkinter import Tk, Label, Button, messagebox
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PredictView:
    def __init__(self, root: Tk, datasets: List[str]):
        """Initialize the PredictView GUI.

        Args:
            root (Tk): The root Tkinter window.
            datasets (List[str]): A list of available datasets.
        """
        self.root = root
        self.datasets = datasets
        self.selected_dataset = None

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface for the PredictView."""
        self.create_title_label()
        self.create_dataset_selector()
        self.create_start_button()

    def create_title_label(self):
        """Create and display the title label."""
        title_label = Label(self.root, text="Prediction Interface", font=("Arial", 16))
        title_label.pack(pady=10)

    def create_dataset_selector(self):
        """Create dataset selector buttons."""
        for dataset in self.datasets:
            Button(self.root, text=dataset, command=lambda d=dataset: self.select_dataset(d)).pack(pady=5)

    def create_start_button(self):
        """Create the start prediction button."""
        start_button = Button(self.root, text="Start Prediction", command=self.start_prediction, state="normal")
        start_button.pack(pady=20)

    def select_dataset(self, dataset: str):
        """Set the selected dataset.

        Args:
            dataset (str): The dataset selected by the user.
        """
        logging.info(f"Dataset selected: {dataset}")
        self.selected_dataset = dataset
        messagebox.showinfo("Dataset Selection", f"You have selected {dataset}.")

    def start_prediction(self):
        """Start the prediction process."""
        if not self.selected_dataset:
            self.display_error("No dataset selected. Please select a dataset to proceed.")
            return

        try:
            result = self.predict(self.selected_dataset)
            logging.info("Prediction successful.")
            messagebox.showinfo("Prediction Result", f"Prediction completed for dataset {self.selected_dataset}: {result}")
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            self.display_error(f"An error occurred during prediction: {e}")

    def predict(self, dataset: str):
        """Perform the prediction for the selected dataset.

        Args:
            dataset (str): The dataset to predict.

        Returns:
            str: The prediction result.
        """
        # Placeholder for prediction logic
        return "Success"

    def display_error(self, message: str):
        """Display an error message to the user.

        Args:
            message (str): The error message to display.
        """
        logging.warning(message)
        messagebox.showerror("Error", message)

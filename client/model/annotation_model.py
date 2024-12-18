import os
import json
import logging

class AnnotationModel:
    def __init__(self):
        """
        Initialize the AnnotationModel object.

        Attributes:
            main_dataset_dir (str): Path to the main dataset directory.
        """
        self.main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset")
        # Setup logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def get_dataset_list(self):
        """Retrieve the list of available datasets."""
        try:
            return [d for d in os.listdir(self.main_dataset_dir) if os.path.isdir(os.path.join(self.main_dataset_dir, d))]
        except FileNotFoundError:
            logging.error("Dataset directory not found.")
            return []

    def validate_dataset(self, dataset_name):
        """Check if the dataset exists."""
        return os.path.exists(os.path.join(self.main_dataset_dir, dataset_name))

    def save_labels(self, dataset_name, labels):
        """Save label data to the dataset."""
        try:
            dataset_path = os.path.join(self.main_dataset_dir, dataset_name)
            if not self.validate_dataset(dataset_name):
                logging.warning(f"Dataset {dataset_name} not found.")
                return False
            with open(os.path.join(dataset_path, "labels.json"), "w") as f:
                json.dump(labels, f, indent=4)
            logging.info(f"Labels saved successfully for dataset: {dataset_name}")
            return True
        except Exception as e:
            logging.error(f"Error saving labels: {e}")
            return False

    def load_labels(self, dataset_name):
        """Load label data from the dataset."""
        try:
            dataset_path = os.path.join(self.main_dataset_dir, dataset_name)
            if not self.validate_dataset(dataset_name):
                logging.warning(f"Dataset {dataset_name} not found.")
                return None
            labels_file = os.path.join(dataset_path, "labels.json")
            if not os.path.exists(labels_file):
                logging.info(f"No labels.json file found in dataset: {dataset_name}")
                return {}
            with open(labels_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading labels: {e}")
            return None

    def add_dataset(self, dataset_name):
        """Add a new dataset."""
        try:
            dataset_path = os.path.join(self.main_dataset_dir, dataset_name)
            if os.path.exists(dataset_path):
                logging.warning(f"Dataset {dataset_name} already exists.")
                return False
            os.makedirs(dataset_path)
            logging.info(f"Dataset {dataset_name} created successfully.")
            return True
        except Exception as e:
            logging.error(f"Error creating dataset: {e}")
            return False

    def delete_dataset(self, dataset_name):
        """Delete a dataset."""
        try:
            dataset_path = os.path.join(self.main_dataset_dir, dataset_name)
            if not self.validate_dataset(dataset_name):
                logging.warning(f"Dataset {dataset_name} not found.")
                return False
            for root, dirs, files in os.walk(dataset_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(dataset_path)
            logging.info(f"Dataset {dataset_name} deleted successfully.")
            return True
        except Exception as e:
            logging.error(f"Error deleting dataset: {e}")
            return False

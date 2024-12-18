"""
Model for Annotation Operations.
Handles label creation and dataset management.
"""
import os
import json

class AnnotationModel:
    def __init__(self):
        self.main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset")

    def get_dataset_list(self):
        return [d for d in os.listdir(self.main_dataset_dir) if os.path.isdir(os.path.join(self.main_dataset_dir, d))]

    def validate_dataset(self, dataset_name):
        return os.path.exists(os.path.join(self.main_dataset_dir, dataset_name))

    def save_labels(self, dataset_name, labels):
        try:
            dataset_path = os.path.join(self.main_dataset_dir, dataset_name)
            with open(os.path.join(dataset_path, "labels.json"), "w") as f:
                json.dump(labels, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving labels: {e}")
            return False

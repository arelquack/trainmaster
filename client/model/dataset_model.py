"""
Model for Dataset Operations.
Handles file saving and directory management.
"""
import os
from PIL import Image

class DatasetModel:
    def save_dataset(self, dataset_name, directory_path):
        try:
            main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset", dataset_name)
            os.makedirs(main_dataset_dir, exist_ok=True)

            image_extensions = (".png", ".jpg", ".jpeg")
            counter = 1
            for file in os.listdir(directory_path):
                if file.lower().endswith(image_extensions):
                    file_path = os.path.join(directory_path, file)
                    img = Image.open(file_path)
                    img = img.convert("RGB")
                    output_file_path = os.path.join(main_dataset_dir, f"{counter}.png")
                    img.save(output_file_path, "PNG")
                    counter += 1
            return True
        except Exception as e:
            print(f"Error processing files: {e}")
            return False

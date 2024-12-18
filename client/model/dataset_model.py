import os
from PIL import Image
import logging

class DatasetModel:
    def __init__(self):
        self.supported_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".tiff")
        # Setup logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def save_dataset(self, dataset_name, directory_path, overwrite=False):
        """
        Save dataset images to a structured directory.

        Parameters:
            dataset_name (str): The name of the dataset to create.
            directory_path (str): The path to the directory containing source images.
            overwrite (bool): Whether to overwrite existing dataset.

        Returns:
            bool: True if the process succeeds, False otherwise.
        """
        try:
            # Main directory for datasets
            main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset", dataset_name)

            # Check if dataset already exists
            if os.path.exists(main_dataset_dir) and not overwrite:
                logging.warning(f"Dataset '{dataset_name}' already exists. Use overwrite=True to overwrite.")
                return False

            # Create dataset directory
            os.makedirs(main_dataset_dir, exist_ok=True)
            logging.info(f"Directory '{main_dataset_dir}' created successfully.")

            # Process files in the source directory
            counter = 1
            for file in os.listdir(directory_path):
                if file.lower().endswith(self.supported_extensions):
                    file_path = os.path.join(directory_path, file)
                    try:
                        img = Image.open(file_path)
                        img = img.convert("RGB")
                        output_file_path = os.path.join(main_dataset_dir, f"{counter}.png")
                        img.save(output_file_path, "PNG")
                        logging.info(f"Saved: {output_file_path}")
                        counter += 1
                    except Exception as img_error:
                        logging.error(f"Error processing file '{file}': {img_error}")

            if counter == 1:
                logging.warning("No valid images found in the source directory.")
                return False

            logging.info(f"Dataset '{dataset_name}' saved successfully with {counter-1} images.")
            return True
        except Exception as e:
            logging.error(f"Error processing files: {e}")
            return False

"""
Model for Prediction Operations.
Handles interaction with YOLO and displays predictions.
"""
import os
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
from typing import List, Optional

class PredictModel:
    def __init__(self) -> None:
        """Initialize the PredictModel class."""
        self.main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset")

    def get_dataset_list(self) -> List[str]:
        """Get the list of datasets available in the main dataset directory.

        Returns:
            List[str]: A list of dataset names.
        """
        try:
            return [
                d for d in os.listdir(self.main_dataset_dir)
                if os.path.isdir(os.path.join(self.main_dataset_dir, d))
            ]
        except FileNotFoundError:
            print("[ERROR] Dataset directory not found.")
            return []

    def _validate_dataset(self, dataset_name: str) -> Optional[str]:
        """Validate the selected dataset and return the path to the model file.

        Args:
            dataset_name (str): The name of the dataset.

        Returns:
            Optional[str]: Path to the model file if valid, else None.
        """
        dataset_path = os.path.join(self.main_dataset_dir, dataset_name)
        if not os.path.exists(dataset_path):
            print(f"[ERROR] Dataset {dataset_name} does not exist.")
            return None

        model_files = [
            f for f in os.listdir(dataset_path)
            if f.endswith(".pt")
        ]
        if not model_files:
            print(f"[ERROR] No model files found in dataset {dataset_name}.")
            return None

        return os.path.join(dataset_path, model_files[0])

    def _initialize_webcam(self) -> Optional[cv2.VideoCapture]:
        """Initialize and validate the webcam.

        Returns:
            Optional[cv2.VideoCapture]: A VideoCapture object if the webcam is accessible, else None.
        """
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[ERROR] Cannot open webcam.")
            return None
        return cap

    def _process_frame(self, model: YOLO, frame: cv2.Mat) -> cv2.Mat:
        """Process a single frame using the YOLO model.

        Args:
            model (YOLO): The YOLO model for predictions.
            frame (cv2.Mat): The frame to process.

        Returns:
            cv2.Mat: The annotated frame after processing.
        """
        results = model(frame)
        return results[0].plot()

    def start_prediction(self, dataset_name: str) -> bool:
        """Start the prediction process using the YOLO model and webcam.

        Args:
            dataset_name (str): The name of the dataset to use.

        Returns:
            bool: True if the process runs successfully, else False.
        """
        model_path = self._validate_dataset(dataset_name)
        if not model_path:
            return False

        try:
            model = YOLO(model_path)
            cap = self._initialize_webcam()
            if not cap:
                return False

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("[ERROR] Failed to read frame from webcam.")
                    break

                annotated_frame = self._process_frame(model, frame)
                cv2.imshow("Prediction", annotated_frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("Exiting prediction loop.")
                    break

            cap.release()
            cv2.destroyAllWindows()
            return True
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred during prediction: {e}")
            return False

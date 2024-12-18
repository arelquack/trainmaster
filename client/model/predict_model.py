"""
Model for Prediction Operations.
Handles interaction with YOLO and displays predictions.
"""
import os
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO

class PredictModel:
    def __init__(self):
        self.main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset")

    def get_dataset_list(self):
        return [d for d in os.listdir(self.main_dataset_dir) if os.path.isdir(os.path.join(self.main_dataset_dir, d))]

    def start_prediction(self, dataset_name):
        try:
            model_files = [f for f in os.listdir(os.path.join(self.main_dataset_dir, dataset_name)) if f.endswith(".pt")]
            if not model_files:
                print("No model files found!")
                return False

            model = YOLO(os.path.join(self.main_dataset_dir, dataset_name, model_files[0]))
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                print("Error: Cannot open webcam.")
                return False

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                results = model(frame)
                annotated_frame = results[0].plot()

                cv2.imshow("Prediction", annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cap.release()
            cv2.destroyAllWindows()
            return True
        except Exception as e:
            print(f"Error starting prediction: {e}")
            return False

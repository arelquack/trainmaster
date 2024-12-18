from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap import Frame, Button, Label

from controller.main_controller import MainController
from view.upload_view import UploadView
from view.annotate_view import AnnotateView
from view.train_view import TrainView
from view.predict_view import PredictView

class MainView:
    def __init__(self, root):
        # Setup TTKBootstrap theme
        self.style = Style(theme="darkly")  # Pilih theme: darkly, flatly, solar, dll
        self.root = root
        self.root.title("Menu Interface")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        self.main_controller = MainController(self)
        self.setup_top_menu()

        self.body_frame = Frame(self.root, bootstyle=SECONDARY, width=800, height=400)
        self.body_frame.pack(expand=True, fill="both")

        self.show_home_page()

    def setup_top_menu(self):
        button_frame = Frame(self.root, bootstyle=PRIMARY)
        button_frame.pack(side="top", fill="x")

        buttons = [
            ("HOME", self.main_controller.load_home),
            ("UPLOAD DATASET", self.main_controller.load_upload_page),
            ("ANNOTATE", self.main_controller.load_annotate_page),
            ("TRAIN", self.main_controller.load_train_page),
            ("PREDICT", self.main_controller.load_predict_page),
            ("EXIT", self.root.destroy),
        ]

        for text, command in buttons:
            Button(button_frame, text=text, command=command, bootstyle=SUCCESS, padding=10).pack(
                side="left", fill="x", expand=True, padx=5, pady=5
            )

    def clear_body(self):
        for widget in self.body_frame.winfo_children():
            widget.destroy()

    def show_home_page(self):
        self.clear_body()
        Label(self.body_frame, text="🔥 SELAMAT DATANG 🔥", font=("Arial", 24, "bold"), bootstyle=INFO).pack(pady=50)
        Label(self.body_frame, text="Aplikasi Berbasis Tkinter & ttkbootstrap", bootstyle=SUCCESS).pack(pady=10)

    def show_upload_page(self):
        self.clear_body()
        UploadView(self.body_frame)

    def show_annotate_page(self):
        self.clear_body()
        AnnotateView(self.body_frame)

    def show_train_page(self):
        self.clear_body()
        TrainView(self.body_frame)

    def show_predict_page(self):
        self.clear_body()
        PredictView(self.body_frame)
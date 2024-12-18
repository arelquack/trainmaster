from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap import Frame, Button, Label
from tkinter import messagebox

from controller.main_controller import MainController
from view.upload_view import UploadView
from view.annotate_view import AnnotateView
from view.train_view import TrainView
from view.predict_view import PredictView

class MainView:
    """
    MainView is the primary user interface for the application.
    It sets up the main menu, controls navigation between pages, and ensures a consistent layout.
    """

    def __init__(self, root):
        """
        Initialize the MainView class.

        :param root: The root Tkinter window.
        """
        self._setup_style()
        self.root = root
        self.root.title("Menu Interface")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        self.main_controller = MainController(self)

        self._setup_top_menu()
        self._setup_body_frame()
        self._show_home_page()

    def _setup_style(self):
        """
        Set up the TTKBootstrap style for the application.
        """
        self.style = Style(theme="darkly")  # Choose themes: darkly, flatly, solar, etc.

    def _setup_top_menu(self):
        """
        Set up the top menu with navigation buttons.
        """
        button_frame = Frame(self.root, bootstyle=PRIMARY)
        button_frame.pack(side="top", fill="x")

        buttons = [
            ("HOME", self.main_controller.load_home),
            ("UPLOAD DATASET", self.main_controller.load_upload_page),
            ("ANNOTATE", self.main_controller.load_annotate_page),
            ("TRAIN", self.main_controller.load_train_page),
            ("PREDICT", self.main_controller.load_predict_page),
            ("EXIT", self._confirm_exit),
        ]

        for text, command in buttons:
            Button(
                button_frame,
                text=text,
                command=command,
                bootstyle=SUCCESS,
                padding=10
            ).pack(side="left", fill="x", expand=True, padx=5, pady=5)

    def _setup_body_frame(self):
        """
        Set up the main content frame.
        """
        self.body_frame = Frame(self.root, bootstyle=SECONDARY, width=800, height=400)
        self.body_frame.pack(expand=True, fill="both")

    def _clear_body(self):
        """
        Clear all widgets from the body frame.
        """
        for widget in self.body_frame.winfo_children():
            widget.destroy()

    def _confirm_exit(self):
        """
        Show a confirmation dialog before exiting the application.
        """
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

    def _show_home_page(self):
        """
        Display the home page.
        """
        self._clear_body()
        Label(
            self.body_frame,
            text="🔥 SELAMAT DATANG 🔥",
            font=("Arial", 24, "bold"),
            bootstyle=INFO
        ).pack(pady=50)
        Label(
            self.body_frame,
            text="Aplikasi Berbasis Tkinter & ttkbootstrap",
            bootstyle=SUCCESS
        ).pack(pady=10)

    def show_upload_page(self):
        """
        Display the upload page.
        """
        self._clear_body()
        UploadView(self.body_frame)

    def show_annotate_page(self):
        """
        Display the annotate page.
        """
        self._clear_body()
        AnnotateView(self.body_frame)

    def show_train_page(self):
        """
        Display the train page.
        """
        self._clear_body()
        TrainView(self.body_frame)

    def show_predict_page(self):
        """
        Display the predict page.
        """
        self._clear_body()
        PredictView(self.body_frame)
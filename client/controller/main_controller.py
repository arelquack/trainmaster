"""
Controller for Main Application Logic.
Handles navigation and central control.
"""
class MainController:
    def __init__(self, view):
        self.view = view

    def load_home(self):
        self.view.show_home_page()

    def load_upload_page(self):
        self.view.show_upload_page()

    def load_annotate_page(self):
        self.view.show_annotate_page()

    def load_train_page(self):
        self.view.show_train_page()

    def load_predict_page(self):
        self.view.show_predict_page()

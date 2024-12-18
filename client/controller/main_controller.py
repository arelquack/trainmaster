"""
Controller for Main Application Logic.
Handles navigation and central control.
"""

class MainController:
    """MainController class to handle navigation logic in the application."""

    def __init__(self, view):
        """
        Initialize MainController with a given view.

        Args:
            view: The view instance responsible for rendering pages.
        """
        self.view = view
        self.page_routes = {
            "home": self.view.show_home_page,
            "upload": self.view.show_upload_page,
            "annotate": self.view.show_annotate_page,
            "train": self.view.show_train_page,
            "predict": self.view.show_predict_page,
        }

    def load_page(self, page_name: str) -> None:
        """
        Load a specific page based on the given page name.

        Args:
            page_name (str): Name of the page to be loaded.
        
        Raises:
            ValueError: If the page_name is invalid.
        """
        try:
            page_method = self.page_routes.get(page_name)
            if not page_method:
                raise ValueError(f"Invalid page name: {page_name}")
            page_method()
        except Exception as e:
            print(f"[ERROR] Failed to load page '{page_name}': {e}")

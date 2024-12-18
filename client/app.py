from menu.menu_bar import MenuBar
from controller import home, upload_dataset, annotate, train, predict, exit_app
import ttkbootstrap as ttk

class App:
    """
    Main application class for a menu interface.

    Attributes:
        root (ttk.Window): The main application window.
        body_frame (ttk.Frame): The frame for displaying content.
    """
    def __init__(self):
        """Initialize the main application."""
        self.root = self._initialize_window()
        self.body_frame = self._initialize_body_frame()
        self._initialize_menu_bar()
        home(self.body_frame)  # Load the Home Page by default

    def _initialize_window(self):
        """Set up the main application window."""
        root = ttk.Window(themename="darkly")
        root.title("Menu Interface")
        root.geometry("800x500")
        root.configure(bg="white")

        # Configure grid layout for scalability
        root.grid_rowconfigure(0, weight=0)  # Row 0 for menu bar (fixed height)
        root.grid_rowconfigure(1, weight=1)  # Row 1 for body_frame (flexible height)
        root.grid_columnconfigure(0, weight=1)  # Column 0 spans the entire width

        return root

    def _initialize_body_frame(self):
        """Create and configure the body frame."""
        body_frame = ttk.Frame(self.root, bootstyle="dark")
        body_frame.grid(row=1, column=0, sticky="nsew")
        return body_frame

    def _initialize_menu_bar(self):
        """Set up the menu bar with buttons."""
        button_frame = ttk.Frame(self.root, bootstyle="secondary")
        button_frame.grid(row=0, column=0, sticky="ew")

        buttons = [
            ("HOME", home),
            ("UPLOAD DATASET", upload_dataset),
            ("ANNOTATE", annotate),
            ("TRAIN", train),
            ("PREDICT", predict),
            ("EXIT", exit_app),
        ]

        MenuBar(self.root, button_frame, buttons, self.body_frame)

    def run(self):
        """Start the application."""
        self.root.mainloop()

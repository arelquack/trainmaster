from home.home_page import HomePage
from annotate.annotate_page import AnnotatePage
from train.train_page import TrainPage
from predict.predict_page import PredictPage
from upload.upload_dataset_page import UploadDatasetPage
from utils import clear_body

def switch_page_dummy(page_name):
    """
    Dummy function for switching pages.
    Args:
        page_name (str): Name of the page to switch to.
    """
    print(f"Switching to page: {page_name}")

def navigate_to_page(page_class, body_frame, *args, **kwargs):
    """
    Clears the body frame and initializes the given page class.
    Args:
        page_class (type): The class of the page to instantiate.
        body_frame (ttk.Frame): The frame to display the page content.
        *args: Positional arguments for the page class.
        **kwargs: Keyword arguments for the page class.
    """
    clear_body(body_frame)
    page_class(body_frame, *args, **kwargs)

def home(body_frame):
    """Load the Home Page."""
    navigate_to_page(HomePage, body_frame, switch_page_dummy)

def upload_dataset(body_frame):
    """Load the Upload Dataset Page."""
    navigate_to_page(UploadDatasetPage, body_frame)

def annotate(body_frame):
    """Load the Annotate Page."""
    navigate_to_page(AnnotatePage, body_frame)

def train(body_frame):
    """Load the Train Page."""
    navigate_to_page(TrainPage, body_frame)

def predict(body_frame):
    """Load the Predict Page."""
    navigate_to_page(PredictPage, body_frame)

def exit_app(root):
    """
    Exit the application.
    Args:
        root (ttk.Window): The main application window.
    """
    root.quit()
    root.destroy()

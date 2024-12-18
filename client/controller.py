from home.home_page import HomePage
from annotate.annotate_page import AnnotatePage
from train.train_page import TrainPage
from predict.predict_page import PredictPage
from upload.upload_dataset_page import UploadDatasetPage
from utils import clear_body

def switch_page_dummy(page_name):
    print(f"Berpindah ke halaman: {page_name}")

def home(body_frame):
    """Home Page Content."""
    clear_body(body_frame)
    HomePage(body_frame, switch_page_dummy)

def upload_dataset(body_frame):
    """Upload Dataset Page."""
    clear_body(body_frame)
    UploadDatasetPage(body_frame)

def annotate(body_frame):
    """Annotate Page."""
    clear_body(body_frame)
    AnnotatePage(body_frame)

def train(body_frame):
    """Train Page."""
    clear_body(body_frame)
    TrainPage(body_frame)

def predict(body_frame):
    """Predict Page."""
    clear_body(body_frame)
    PredictPage(body_frame)

def exit_app(root):
    root.quit()
    root.destroy()
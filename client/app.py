from menu.menu_bar import MenuBar
from controller import home, upload_dataset, annotate, train, predict, exit_app
import ttkbootstrap as ttk

class App:
    """
    Aplikasi utama yang menggunakan paradigma OOP untuk memisahkan tampilan dan logika.
    Fungsionalitas utama aplikasi adalah pengaturan tampilan dengan framework Tkinter.
    """
    def __init__(self):
        """Initialize the main application."""
        self.root = ttk.Window(themename="darkly")
        self.root.title("Menu Interface")
        self.root.geometry("800x500")
        self.root.configure(bg="white")

        # Body frame
        self.body_frame = ttk.Frame(self.root, bootstyle="dark")
        self.body_frame.grid(row=1, column=0, sticky="nsew")  # Pastikan body_frame menempati seluruh ruang

        # Konfigurasi grid untuk body_frame agar mengisi ruang
        self.root.grid_rowconfigure(0, weight=0)  # Row 0 untuk menu bar (tidak fleksibel)
        self.root.grid_rowconfigure(1, weight=1)  # Row 1 untuk body_frame (fleksibel)
        self.root.grid_columnconfigure(0, weight=1)  # Kolom 0 untuk body_frame dan menu bar (fleksibel)

        # Menu bar
        button_frame = ttk.Frame(self.root, bootstyle="secondary")
        button_frame.grid(row=0, column=0, sticky="ew")  # Letakkan menu bar di row 0

        buttons = [
            ("HOME", home),
            ("UPLOAD DATASET", upload_dataset),
            ("ANNOTATE", annotate),
            ("TRAIN", train),
            ("PREDICT", predict),
            ("EXIT", exit_app),
        ]
        
        # Inisialisasi MenuBar
        MenuBar(self.root, button_frame, buttons, self.body_frame)
        
        # Muat halaman awal (Home Page)
        home(self.body_frame)

    def run(self):
        """Start the application."""
        self.root.mainloop()
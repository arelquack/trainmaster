import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# Konstanta untuk teks statis
HEADER_TEXT = "TrainMaster"
SUB_HEADER_TEXT = "Manajemen Training Model YOLO Jadi Lebih Mudah"
WELCOME_TEXT = "🔰 Selamat Datang di TrainMaster 🔰"
DESCRIPTION_TEXT = (
    "TrainMaster dirancang untuk membantu Anda:\n"
    "- Mengelola dataset untuk training\n"
    "- Membuat anotasi gambar dengan mudah\n"
    "- Melakukan training model dengan server terdistribusi\n"
    "- Memantau hasil training melalui GUI interaktif"
)
GUIDE_TEXT = (
    "PANDUAN TRAINMASTER CIK\n\n"
    "1️⃣ Upload Dataset:\n   - Pergi ke halaman Upload Dataset.\n"
    "   - Kasih nama dataset, terus klik 'Browse' buat pilih folder.\n"
    "   - Submit dan tunggu sampe muncul notifikasi keberhasilan.\n\n"
    "2️⃣ Annotate Gambar:\n   - Pilih dataset yang udah di-upload dari dropdown.\n"
    "   - Buat label dan kotakin objek di gambar satu per satu.\n"
    "   - Ngotakinnya pas-in lho ya\n\n"
    "3️⃣ Training Time:\n   - Pilih dataset yang udah di-annotate.\n"
    "   - Klik 'Send Files to Server', tunggu status upload sampe selesai.\n"
    "   - Terima model YOLO yang udah jadi, mantappp! 💪\n\n"
    "4️⃣ Predict Dataset:\n   - Pilih dataset yang udah ditrain.\n"
    "   - Tunggu webcam nyala, terus lihat magic-nya!\n\n"
    "🔥 Easy kan? Gaskeun sekarang, eksplor TrainMaster!"
)

class HomePage:
    def __init__(self, parent_frame, switch_page_callback):
        """Initialize Home Page."""
        self.parent_frame = parent_frame
        self.switch_page_callback = switch_page_callback  # Callback untuk pindah halaman
        self.body_frame = ttk.Frame(self.parent_frame, bootstyle="dark")
        self.body_frame.pack(fill=BOTH, expand=True)

        # Build the home page content
        self.build_content()

    def clear_body(self):
        """Clear all widgets inside the body frame."""
        for widget in self.body_frame.winfo_children():
            widget.destroy()

    def build_content(self):
        """Build the content for the Home Page."""
        self.clear_body()

        # Header Section
        self._create_header_section()

        # Main Content Section
        self._create_main_content_section()

        # Action Buttons
        self._create_action_buttons()

    def _create_header_section(self):
        """Create the header section of the page."""
        header_frame = ttk.Frame(self.body_frame, padding=30, bootstyle="primary")
        header_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(
            header_frame,
            text=HEADER_TEXT,
            font=("Arial", 28, "bold"),
            bootstyle="default",
            anchor=CENTER
        ).pack(fill=X)

        ttk.Label(
            header_frame,
            text=SUB_HEADER_TEXT,
            font=("Arial", 14),
            bootstyle="light",
            anchor=CENTER
        ).pack(fill=X)

    def _create_main_content_section(self):
        """Create the main content section."""
        content_frame = ttk.Frame(self.body_frame, padding=20, bootstyle="secondary")
        content_frame.pack(expand=True, fill=BOTH, padx=30, pady=20)

        ttk.Label(
            content_frame,
            text=WELCOME_TEXT,
            font=("Arial", 16, "bold"),
            bootstyle="success",
            anchor=CENTER
        ).pack(pady=10)

        ttk.Label(
            content_frame,
            text=DESCRIPTION_TEXT,
            font=("Arial", 12),
            bootstyle="light",
            justify="center",
            anchor=CENTER
        ).pack(pady=20)

    def _create_action_buttons(self):
        """Create action buttons for the page."""
        button_frame = ttk.Frame(self.body_frame)
        button_frame.pack(pady=10)

        # Start Button
        self._create_button(
            button_frame, "MULAI SEKARANG", SUCCESS, self.on_start_button_click
        ).pack(side=LEFT, padx=10)

        # Guide Button
        self._create_button(
            button_frame, "LIHAT PANDUAN", INFO, self.on_guide_button_click
        ).pack(side=LEFT, padx=10)

    def _create_button(self, parent, text, style, command):
        """Utility method to create a button."""
        return ttk.Button(
            parent,
            text=text,
            bootstyle=style,
            padding=10,
            width=20,
            command=command
        )

    def on_start_button_click(self):
        """Handle the start button click event."""
        messagebox.showinfo(
            "Yuk Mulai!", 
            "🚀 Gas langsung ke halaman Upload Dataset aja brow, siapin folder dan dataset lo!"
        )
        self.switch_page_callback("upload_dataset")

    def on_guide_button_click(self):
        """Handle the guide button click event."""
        messagebox.showinfo("Panduan Penggunaan TrainMaster 📘", GUIDE_TEXT)
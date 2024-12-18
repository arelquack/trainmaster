import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

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
        header_frame = ttk.Frame(self.body_frame, padding=30, bootstyle="primary")
        header_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(
            header_frame,
            text="TrainMaster",
            font=("Arial", 28, "bold"),
            bootstyle="default",
            anchor=CENTER
        ).pack(fill=X)

        ttk.Label(
            header_frame,
            text="Manajemen Training Model YOLO Jadi Lebih Mudah",
            font=("Arial", 14),
            bootstyle="light",
            anchor=CENTER
        ).pack(fill=X)

        # Main Content Section
        content_frame = ttk.Frame(self.body_frame, padding=20, bootstyle="secondary")
        content_frame.pack(expand=True, fill=BOTH, padx=30, pady=20)

        # Welcome Message
        ttk.Label(
            content_frame,
            text="🔰 Selamat Datang di TrainMaster 🔰",
            font=("Arial", 16, "bold"),
            bootstyle="success",
            anchor=CENTER
        ).pack(pady=10)

        # Description Section
        ttk.Label(
            content_frame,
            text=(
                "TrainMaster dirancang untuk membantu Anda:\n"
                "- Mengelola dataset untuk training\n"
                "- Membuat anotasi gambar dengan mudah\n"
                "- Melakukan training model dengan server terdistribusi\n"
                "- Memantau hasil training melalui GUI interaktif"
            ),
            font=("Arial", 12),
            bootstyle="light",
            justify="center",
            anchor=CENTER
        ).pack(pady=20)

        # Action Button Section
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=10)

        # Tombol Start
        ttk.Button(
            button_frame,
            text="MULAI SEKARANG",
            bootstyle=SUCCESS,
            padding=10,
            width=20,
            command=self.on_start_button_click,  # Event start
        ).pack(side=LEFT, padx=10)

        # Tombol Guide
        ttk.Button(
            button_frame,
            text="LIHAT PANDUAN",
            bootstyle=INFO,
            padding=10,
            width=20,
            command=self.on_guide_button_click,  # Event guide
        ).pack(side=LEFT, padx=10)

    def on_start_button_click(self):
        """Handle the start button click event: Redirect to UPLOAD DATASET."""
        messagebox.showinfo("Yuk Mulai!", "🚀 Gas langsung ke halaman Upload Dataset aja brow, siapin folder dan dataset lo!")
        self.switch_page_callback("upload_dataset")  # Pindah ke halaman UPLOAD DATASET

    def on_guide_button_click(self):
        """Handle the guide button click event: Show a guide pop-up."""
        guide_text = (
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

        messagebox.showinfo("Panduan Penggunaan TrainMaster 📘", guide_text)
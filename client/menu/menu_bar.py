import tkinter as tk
from controller import exit_app

class MenuBar:
    def __init__(self, root, button_frame, commands, body_frame):
        """Initialize MenuBar with buttons."""
        self.root = root
        self.button_frame = button_frame
        self.commands = commands
        self.body_frame = body_frame  # Menyimpan body_frame dari App
        self._create_menu_buttons()

    def _create_menu_buttons(self):
        """Create and pack buttons for the menu."""
        for text, command in self.commands:
            if text == "EXIT":
                # Khusus untuk exit, panggil fungsi exit_app dengan root
                button = tk.Button(self.button_frame, text=text, command=lambda: exit_app(self.root), bg="lightgray", padx=10, pady=10)
            else:
                # Untuk tombol lainnya, panggil fungsi biasa dengan body_frame
                button = tk.Button(self.button_frame, text=text, command=lambda cmd=command: cmd(self.body_frame), bg="lightgray", padx=10, pady=10)
            
            button.pack(side="left", fill="x", expand=True)

import tkinter as tk
from controller import exit_app
from typing import Callable, List, Tuple

class MenuBar:
    def __init__(
        self, 
        root: tk.Tk, 
        button_frame: tk.Frame, 
        commands: List[Tuple[str, Callable[[tk.Frame], None]]], 
        body_frame: tk.Frame
    ) -> None:
        """Initialize the menu bar with buttons.

        Args:
            root (tk.Tk): The main application root.
            button_frame (tk.Frame): Frame where buttons will be placed.
            commands (List[Tuple[str, Callable]]): List of button text and associated commands.
            body_frame (tk.Frame): The frame used for body content.
        """
        self.root = root
        self.button_frame = button_frame
        self.commands = commands
        self.body_frame = body_frame
        self._create_menu_buttons()

    def _create_menu_buttons(self) -> None:
        """Create and add menu buttons to the button frame."""
        for text, command in self.commands:
            button = self._create_button(text, command)
            button.pack(side="left", fill="x", expand=True)

    def _create_button(self, text: str, command: Callable[[tk.Frame], None]) -> tk.Button:
        """Create a button for the menu.

        Args:
            text (str): The label for the button.
            command (Callable): The command to execute when clicked.

        Returns:
            tk.Button: A configured tkinter button.
        """
        if text == "EXIT":
            return tk.Button(
                self.button_frame,
                text=text,
                command=lambda: self._handle_exit(),
                bg="lightgray",
                padx=10,
                pady=10
            )
        return tk.Button(
            self.button_frame,
            text=text,
            command=lambda: self._handle_command(command),
            bg="lightgray",
            padx=10,
            pady=10
        )

    def _handle_command(self, command: Callable[[tk.Frame], None]) -> None:
        """Safely execute the command associated with a button.

        Args:
            command (Callable): The command to execute.
        """
        try:
            command(self.body_frame)
        except Exception as e:
            print(f"[ERROR] Failed to execute command: {e}")

    def _handle_exit(self) -> None:
        """Handle application exit."""
        try:
            exit_app(self.root)
        except Exception as e:
            print(f"[ERROR] Failed to exit application: {e}")

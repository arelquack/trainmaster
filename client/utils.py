import socket
import tkinter as tk
from typing import Optional

BUFFER_SIZE = 1024
BRIDGE_HOST = '127.0.0.1'  # Bridge server address
BRIDGE_PORT = 12345        # Port where the bridge is running

def clear_body(body_frame: tk.Frame) -> None:
    """Clear all widgets inside the body frame.

    Args:
        body_frame (tk.Frame): The frame to clear.
    """
    for widget in body_frame.winfo_children():
        widget.destroy()

def get_server_port() -> Optional[int]:
    """Connect to the bridge to get the least loaded server's port.

    Returns:
        Optional[int]: The port number of the least loaded server, or None if an error occurs.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bridge_socket:
            bridge_socket.connect((BRIDGE_HOST, BRIDGE_PORT))
            server_port_data = bridge_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            if not server_port_data.isdigit():
                raise ValueError(f"Received invalid port data: {server_port_data}")
            server_port = int(server_port_data)
            print(f"Redirected to server on port {server_port}")
            return server_port
    except (socket.error, ValueError) as e:
        print(f"[ERROR] Could not get server port from the bridge: {e}")
        return None

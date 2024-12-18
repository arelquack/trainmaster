import socket
import tkinter as tk

BUFFER_SIZE = 1024
BRIDGE_HOST = '127.0.0.1'  # Bridge server address
BRIDGE_PORT = 12345        # Port where the bridge is running

def clear_body(body_frame):
    """Clear all widgets inside the body frame."""
    for widget in body_frame.winfo_children():
        widget.destroy()

def get_server_port():
    """Connect to the bridge to get the least loaded server's port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bridge_socket:
            bridge_socket.connect((BRIDGE_HOST, BRIDGE_PORT))
            server_port = int(bridge_socket.recv(BUFFER_SIZE).decode('utf-8'))
            print(f"Redirected to server on port {server_port}")
            return server_port
    except Exception as e:
        print(f"[ERROR] Could not get server port from the bridge: {e}")
        return None
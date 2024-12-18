import os
import socket
from typing import Optional, Tuple, List

BUFFER_SIZE = 1024
BRIDGE_HOST = "127.0.0.1"
BRIDGE_PORT = 12345

class TrainModel:
    """Handles file transfers and communication with the server."""

    def __init__(self):
        self.main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset")

    def get_dataset_list(self) -> List[str]:
        """Retrieve a list of datasets available in the main directory.

        Returns:
            List[str]: List of dataset names.
        """
        try:
            return [
                d for d in os.listdir(self.main_dataset_dir) 
                if os.path.isdir(os.path.join(self.main_dataset_dir, d))
            ]
        except FileNotFoundError as e:
            print(f"[ERROR] Dataset directory not found: {e}")
            return []

    def send_files_to_server(self, dataset_name: str) -> Tuple[bool, str]:
        """Send files from a dataset to the server.

        Args:
            dataset_name (str): Name of the dataset.

        Returns:
            Tuple[bool, str]: Status and message of the operation.
        """
        try:
            dataset_path = os.path.join(self.main_dataset_dir, dataset_name)
            files = self._get_valid_files(dataset_path)

            if not files:
                return False, "No valid files found in the dataset!"

            server_port = self._get_server_port()
            if not server_port:
                return False, "Failed to retrieve server port!"

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((BRIDGE_HOST, server_port))
                client_socket.send(dataset_name.encode())

                for file_name in files:
                    file_path = os.path.join(dataset_path, file_name)
                    self._send_file(client_socket, file_name, file_path)

            return True, "Files sent to server successfully!"
        except Exception as e:
            print(f"[ERROR] Sending files failed: {e}")
            return False, "Error sending files to server!"

    def receive_best_model_from_server(self, dataset_name: str) -> Tuple[bool, str]:
        """Receive the best model file from the server.

        Args:
            dataset_name (str): Name of the dataset.

        Returns:
            Tuple[bool, str]: Status and message of the operation.
        """
        try:
            server_port = self._get_server_port()
            if not server_port:
                return False, "Failed to retrieve server port!"

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((BRIDGE_HOST, server_port))
                client_socket.send(dataset_name.encode())

                model_name = client_socket.recv(BUFFER_SIZE).decode()
                client_socket.send(b"ACK")

                model_path = os.path.join(self.main_dataset_dir, dataset_name, model_name)
                self._receive_file(client_socket, model_path)

            return True, "Best model received successfully!"
        except Exception as e:
            print(f"[ERROR] Receiving model failed: {e}")
            return False, "Error receiving best model!"

    def _get_valid_files(self, dataset_path: str) -> List[str]:
        """Retrieve valid files from the dataset directory.

        Args:
            dataset_path (str): Path to the dataset.

        Returns:
            List[str]: List of valid file names.
        """
        try:
            return [
                f for f in os.listdir(dataset_path) 
                if f.endswith((".png", ".jpg", ".txt", ".json"))
            ]
        except FileNotFoundError as e:
            print(f"[ERROR] Dataset path not found: {e}")
            return []

    def _send_file(self, client_socket: socket.socket, file_name: str, file_path: str) -> None:
        """Send a single file to the server.

        Args:
            client_socket (socket.socket): The socket connection to the server.
            file_name (str): Name of the file.
            file_path (str): Path to the file.
        """
        client_socket.send(file_name.encode())
        client_socket.recv(BUFFER_SIZE)  # Acknowledge
        with open(file_path, "rb") as f:
            while (chunk := f.read(BUFFER_SIZE)):
                client_socket.send(chunk)
            client_socket.send(b"<END>")
            client_socket.recv(BUFFER_SIZE)  # Final Acknowledge

    def _receive_file(self, client_socket: socket.socket, file_path: str) -> None:
        """Receive a file from the server.

        Args:
            client_socket (socket.socket): The socket connection to the server.
            file_path (str): Path where the file will be saved.
        """
        with open(file_path, "wb") as f:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if data.endswith(b"<END>"):
                    f.write(data[:-5])
                    break
                f.write(data)

    def _get_server_port(self) -> Optional[int]:
        """Retrieve the server port from the bridge.

        Returns:
            Optional[int]: The port number or None if an error occurs.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bridge_socket:
                bridge_socket.connect((BRIDGE_HOST, BRIDGE_PORT))
                port_data = bridge_socket.recv(BUFFER_SIZE).decode().strip()
                if port_data.isdigit():
                    return int(port_data)
                else:
                    print(f"[ERROR] Invalid port data received: {port_data}")
                    return None
        except (socket.error, ValueError) as e:
            print(f"[ERROR] Failed to connect to bridge: {e}")
            return None

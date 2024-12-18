"""
Model for Training Operations.
Handles file transfers and communication with the server.
"""
import os
import socket

class TrainModel:
    def __init__(self):
        self.buffer_size = 1024
        self.bridge_host = "127.0.0.1"
        self.bridge_port = 12345
        self.main_dataset_dir = os.path.join(os.getcwd(), "list_of_dataset")

    def get_dataset_list(self):
        return [d for d in os.listdir(self.main_dataset_dir) if os.path.isdir(os.path.join(self.main_dataset_dir, d))]

    def send_files_to_server(self, dataset_name):
        try:
            dataset_path = os.path.join(self.main_dataset_dir, dataset_name)
            files = [f for f in os.listdir(dataset_path) if f.endswith(('.png', '.jpg', '.txt', '.json'))]

            if not files:
                return False, "No valid files found in the dataset!"

            server_port = self._get_server_port()
            if not server_port:
                return False, "Failed to retrieve server port!"

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.bridge_host, server_port))
                client_socket.send(dataset_name.encode())

                for file_name in files:
                    file_path = os.path.join(dataset_path, file_name)
                    with open(file_path, "rb") as f:
                        client_socket.send(file_name.encode())
                        client_socket.recv(self.buffer_size)  # Acknowledge
                        while (chunk := f.read(self.buffer_size)):
                            client_socket.send(chunk)
                        client_socket.send(b"<END>")
                        client_socket.recv(self.buffer_size)

            return True, "Files sent to server successfully!"
        except Exception as e:
            print(f"Error sending files: {e}")
            return False, "Error sending files to server!"

    def receive_best_model_from_server(self, dataset_name):
        try:
            server_port = self._get_server_port()
            if not server_port:
                return False, "Failed to retrieve server port!"

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.bridge_host, server_port))
                client_socket.send(dataset_name.encode())

                model_name = client_socket.recv(self.buffer_size).decode()
                client_socket.send(b"ACK")

                model_path = os.path.join(self.main_dataset_dir, dataset_name, model_name)
                with open(model_path, "wb") as f:
                    while True:
                        data = client_socket.recv(self.buffer_size)
                        if data.endswith(b"<END>"):
                            f.write(data[:-5])
                            break
                        f.write(data)

            return True, "Best model received successfully!"
        except Exception as e:
            print(f"Error receiving model: {e}")
            return False, "Error receiving best model!"

    def _get_server_port(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bridge_socket:
                bridge_socket.connect((self.bridge_host, self.bridge_port))
                return int(bridge_socket.recv(self.buffer_size).decode())
        except Exception as e:
            print(f"Error connecting to bridge: {e}")
            return None

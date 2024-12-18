import os
import socket
import tkinter as tk
from tkinter import ttk, messagebox
from utils import clear_body, get_server_port

BUFFER_SIZE = 1024  # Sesuaikan dengan ukuran buffer yang digunakan dalam komunikasi

class TrainPage:
    def __init__(self, parent_frame):
        """Initialize Train Page."""
        self.parent_frame = parent_frame
        self.dataset_dir = "list_of_dataset"
        self.selected_dataset = tk.StringVar()
        self.selected_dataset.set("Select a dataset")
        
        self.body_frame = tk.Frame(self.parent_frame)
        self.body_frame.pack(fill="both", expand=True)

        # Initialize UI
        self._init_ui()

    def _init_ui(self):
        """Initialize the UI elements for the Train Page."""
        clear_body(self.body_frame)
        
        label = tk.Label(self.body_frame, text="Train Page", font=("Arial", 14))
        label.pack(pady=10)

        # Fetch list of dataset directory names
        try:
            dataset_names = [name for name in os.listdir(self.dataset_dir) if os.path.isdir(os.path.join(self.dataset_dir, name))]
        except FileNotFoundError:
            dataset_names = []  # If directory doesn't exist, set an empty list

        # Check if datasets are available
        if not dataset_names:
            error_label = tk.Label(self.body_frame, text="No datasets found in 'list_of_dataset' directory.", fg="red")
            error_label.pack(pady=10)
            return

        # Dropdown for selecting dataset
        dropdown_label = tk.Label(self.body_frame, text="Choose a Dataset:")
        dropdown_label.pack(pady=5)

        dataset_dropdown = ttk.Combobox(self.body_frame, textvariable=self.selected_dataset, values=dataset_names, state="readonly")
        dataset_dropdown.pack(pady=5)

        # Buttons for sending and receiving files
        send_button = tk.Button(self.body_frame, text="Send Files to Server", command=self.send_files_to_server)
        send_button.pack(pady=5)

        receive_button = tk.Button(self.body_frame, text="Receive Best Model", command=self.receive_best_model_from_server)
        receive_button.pack(pady=5)

        # Error and Success labels
        self.error_label = tk.Label(self.body_frame, text="", font=("Arial", 10))
        self.error_label.pack(pady=5)

        self.success_label = tk.Label(self.body_frame, text="", font=("Arial", 10))
        self.success_label.pack(pady=5)

    def send_files_to_server(self):
        """Send dataset files to the selected server."""
        dataset_name = self.selected_dataset.get()
        if dataset_name == "Select a dataset":
            self.error_label.config(text="Please select a valid dataset.", fg="red")
            return

        # Step 1: Retrieve the least loaded server's port
        server_port = get_server_port()
        if not server_port:
            self.error_label.config(text="Failed to get server information. Please try again.", fg="red")
            return

        # Step 2: Get the path of the dataset and prepare the list of files to send
        dataset_path = os.path.join(self.dataset_dir, dataset_name)
        print(f"Sending files from dataset: {dataset_name}")

        # Include .png, .jpg, .txt, and .json files
        files_to_send = [f for f in os.listdir(dataset_path) if f.endswith(('.png', '.jpg', '.txt', '.json'))]

        if not files_to_send:
            self.error_label.config(text="No .png, .jpg, .txt, or .json files found in the selected dataset.", fg="red")
            return

        try:
            # Step 3: Connect to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("127.0.0.1", server_port))
            print(f"Connected to server on port {server_port}.")

            # Step 4: Send the dataset name to the server
            client_socket.send(dataset_name.encode())
            client_socket.recv(BUFFER_SIZE)  # Acknowledge dataset name

            # Step 5: Send all files (.png, .jpg, .txt, .json) to the server
            for file_name in files_to_send:
                file_path = os.path.join(dataset_path, file_name)
                print(f"Sending file: {file_name}")
                
                # Send file name to the server
                client_socket.send(file_name.encode())
                client_socket.recv(BUFFER_SIZE)  # Acknowledge file name

                # Send file content to the server
                with open(file_path, "rb") as f:
                    while (chunk := f.read(BUFFER_SIZE)):
                        client_socket.send(chunk)

                # Indicate end of file transfer for this file
                client_socket.send(b"<END>")
                client_socket.recv(BUFFER_SIZE)  # Acknowledge end of transfer
                print(f"File {file_name} sent successfully.")

            # Step 6: Indicate all files have been sent
            client_socket.send(b"<DONE>")
            print("All files sent successfully.")

            # Step 7: Receive model.txt from the server
            model_name = client_socket.recv(BUFFER_SIZE).decode()
            client_socket.send(b"ACK")  # Acknowledge model.txt name

            model_path = os.path.join(dataset_path, model_name)
            print(f"Receiving {model_name}")

            with open(model_path, "wb") as model_file:
                while True:
                    data = client_socket.recv(BUFFER_SIZE)
                    if data.endswith(b"<END>"):
                        model_file.write(data[:-5])  # Remove <END> marker
                        break
                    model_file.write(data)

            client_socket.send(b"ACK")  # Acknowledge model file transfer
            print(f"Model file saved to {model_path}")
            self.success_label.config(text="Files and model received successfully.", fg="green")

        except Exception as e:
            print(f"Error sending files: {e}")
            self.error_label.config(text=f"Error sending files: {e}", fg="red")
        finally:
            client_socket.close()

    def receive_best_model_from_server(self):
        """Receive the best model file from the server."""
        dataset_name = self.selected_dataset.get()
        if dataset_name == "Select a dataset":
            self.error_label.config(text="Please select a valid dataset.", fg="red")
            return

        # Step 1: Retrieve the least loaded server's port
        server_port = get_server_port()
        if not server_port:
            self.error_label.config(text="Failed to get server information. Please try again.", fg="red")
            return

        # Connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", server_port))

        try:
            # Send dataset name to the server
            client_socket.send(dataset_name.encode())
            client_socket.recv(BUFFER_SIZE)  # Acknowledge dataset name

            # Step 2: Receive the best.pt file
            file_name = client_socket.recv(BUFFER_SIZE).decode()  # Receive file name
            client_socket.send(b"ACK")  # Acknowledge file name

            file_path = os.path.join(self.dataset_dir, dataset_name, file_name)

            with open(file_path, "wb") as best_model_file:
                while True:
                    data = client_socket.recv(BUFFER_SIZE)
                    if data.endswith(b"<END>"):
                        best_model_file.write(data[:-5])  # Remove <END> marker
                        break
                    best_model_file.write(data)

            client_socket.send(b"ACK")  # Acknowledge file transfer
            print(f"Best model {file_name} received and saved at {file_path}")

            self.success_label.config(text="Best model received successfully.", fg="green")
        except Exception as e:
            print(f"Error receiving best model: {e}")
            self.error_label.config(text=f"Error receiving best model: {e}", fg="red")
        finally:
            client_socket.close()

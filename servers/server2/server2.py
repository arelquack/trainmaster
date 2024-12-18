import socket
import os
import json
import threading
import shutil
import time

# Server configuration
HOST = '127.0.0.1'
PORT = 5002  # Change this for multiple servers
BUFFER_SIZE = 1024
DATA_DIR = "received_datasets"
MAPPING_FILE = "directory_mapping.json"

# Global variables
client_count = 0  # Track connected clients
lock = threading.Lock()  # Thread safety for client count

def load_mapping():
    """Load the dataset directory mapping."""
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r") as f:
            return json.load(f)
    return {}

def save_mapping(mapping):
    """Save the dataset directory mapping."""
    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=4)

def get_next_directory(mapping):
    """Determine the next directory number for storing datasets."""
    existing_dirs = [int(k) for k in mapping.keys()]
    return str(max(existing_dirs) + 1 if existing_dirs else 0)

def handle_load_request(conn):
    """Handle bridge request for server load."""
    global client_count
    try:
        conn.send(str(client_count).encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Sending load failed: {e}")
    finally:
        conn.close()

def handle_client(conn, addr):
    global client_count
    with lock:
        client_count += 1  # Increment client count

    directory_mapping = load_mapping()

    try:
        print(f"[NEW CONNECTION] {addr} connected.")
        # Receive the dataset name
        dataset_name = conn.recv(BUFFER_SIZE).decode()
        print(f"[DATASET RECEIVED] Dataset name: {dataset_name}")
        conn.send(b"ACK")  # Acknowledge dataset name

        # Create a new directory for the dataset
        dir_number = get_next_directory(directory_mapping)
        new_dir = os.path.join(DATA_DIR, dir_number)
        os.makedirs(new_dir)
        directory_mapping[dir_number] = dataset_name
        save_mapping(directory_mapping)
        print(f"[DIRECTORY CREATED] Directory {new_dir} for dataset '{dataset_name}'.")

        # Receive files
        while True:
            # Receive file name
            file_name = conn.recv(BUFFER_SIZE).decode()
            if file_name == "<DONE>":
                print("[TRANSFER COMPLETE] All files received.")
                break
            print(f"[RECEIVING FILE] {file_name}")
            conn.send(b"ACK")  # Acknowledge file name

            # Receive file content
            file_path = os.path.join(new_dir, file_name)
            with open(file_path, "wb") as f:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if data.endswith(b"<END>"):
                        f.write(data[:-5])  # Remove <END> marker
                        break
                    f.write(data)

            conn.send(b"ACK")  # Acknowledge file transfer
            print(f"[FILE SAVED] {file_name} saved to {file_path}.")

        # Add dummy model file
        model_path = os.path.join(new_dir, "model.txt")
        with open(model_path, "w") as f:
            f.write(f"""path: {os.getcwd()}/{new_dir}
train: images/train
val: images/train

names:
""")
        
        # Move .png and .txt files to appropriate directories
        source_path = new_dir
        destination_path1 = os.path.join(new_dir, 'images', 'train')  # For image files (.png)
        destination_path2 = os.path.join(new_dir, 'labels', 'train')  # For label files (.txt)

        os.makedirs(destination_path1, exist_ok=True)
        os.makedirs(destination_path2, exist_ok=True)

        # Move files based on extension
        for filename in os.listdir(source_path):
            source_file = os.path.join(source_path, filename)

            if os.path.isfile(source_file):
                if filename.lower().endswith('.png'):  # Check for image files
                    destination_file = os.path.join(destination_path1, filename)
                elif filename.lower().endswith('.txt'):  # Check for label files
                    destination_file = os.path.join(destination_path2, filename)
                else:
                    continue  # Skip files that are not .png or .txt

                shutil.move(source_file, destination_file)

        print("Files moved successfully!")

        # Write labels.json and config.yaml
        labels_json_path = os.path.join(new_dir, 'labels.json')
        with open(labels_json_path, 'r') as f:
            labels = json.load(f)

        to_write = f"""path: {os.getcwd()}/{new_dir}
train: images/train
val: images/train

names:
"""
        to_write = to_write.replace("\\", "/")  
        for i in range(len(labels)):
            to_write += f"  {i}: {labels[i]['name']}\n"

        with open(os.path.join(new_dir, "config.yaml"), "w") as f:
            f.write(to_write)
            print("config.yaml written.")

        # Create latih.py (training script)
        code_train = f"""from ultralytics import YOLO

model = YOLO("yolov8n.yaml")
results = model.train(data="{new_dir}/config.yaml", epochs=1)
""".replace("\\", "/")
        # with open(os.path.join(new_dir, "latih.py"), "w") as f:
        #     f.write(code_train)
        #     print("latih.py written.")
        with open(f"latih{dir_number}.py", "w") as f:
            f.write(code_train)
            print("latih.py written.")

        # Run training
        os.system(f'python latih{dir_number}.py')
        print("Training complete.")

        # Move the best.pt model to the correct destination
        best_model_path = os.path.join("runs", "detect", "train", "weights", "best.pt")
        destination_best_model = os.path.join(new_dir, "best.pt")
        shutil.move(best_model_path, destination_best_model)
        print(f"Best model moved to {destination_best_model}.")

        # Remove the 'runs' directory
        runs_dir = "runs"
        if os.path.exists(runs_dir):
            shutil.rmtree(runs_dir)
            print(f"Removed the 'runs' directory at {runs_dir}.")

        # Step 8: Send best.pt to the client
        with open(destination_best_model, 'rb') as best_model_file:
            file_data = best_model_file.read()
            file_name = "best.pt"

            conn.send(file_name.encode())  # Send the file name
            conn.recv(BUFFER_SIZE)  # Wait for ACK

            # Send the file data
            conn.send(file_data)

            # Send end of transfer
            conn.send(b"<END>")
            conn.recv(BUFFER_SIZE)  # Wait for ACK
            print(f"Best model {file_name} sent to client.")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        with lock:
            client_count -= 1  # Decrement client count
        print(f"[DISCONNECT] {addr} disconnected. Current client count: {client_count}")

def start_server():
    """Start the server to accept connections."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[STARTING] Server is listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()

            # Peek into the data to determine if it's a load query or a client transfer
            client_type = conn.recv(BUFFER_SIZE, socket.MSG_PEEK).decode('utf-8')

            if client_type == "GET_LOAD":
                # Handle load request from bridge
                threading.Thread(target=handle_load_request, args=(conn,)).start()
            else:
                # Handle dataset transfer from client
                threading.Thread(target=handle_client, args=(conn, addr)).start()

    except KeyboardInterrupt:
        print("\n[SHUTTING DOWN] Server stopped.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()

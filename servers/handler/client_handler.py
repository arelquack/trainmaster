import threading

class ClientHandler:
    def __init__(self, client_socket, client_address, server_manager):
        """Initialize ClientHandler."""
        self.client_socket = client_socket
        self.client_address = client_address
        self.server_manager = server_manager

    def handle(self):
        """Handle the client's request and redirect them to the least loaded server."""
        print(f"[NEW CLIENT] {self.client_address} connected to Bridge.")
        try:
            # Update server loads
            self.server_manager.update_server_loads()

            # Choose the server with the least load
            chosen_server = self.server_manager.get_least_loaded_server()

            print(f"[REDIRECT] Sending {self.client_address} to server on port {chosen_server['port']}")
            self.client_socket.send(str(chosen_server["port"]).encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            self.client_socket.close()
            print(f"[DISCONNECT] {self.client_address} disconnected from Bridge.")

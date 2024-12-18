import socket
import threading
from handler.client_handler import ClientHandler
from manager.server_manager import ServerManager

class BridgeServer:
    def __init__(self, host='127.0.0.1', port=12345, servers=None):
        """Initialize the BridgeServer."""
        if servers is None:
            servers = [
                {"port": 5001, "client_count": 0},
                {"port": 5002, "client_count": 0},
            ]
        self.host = host
        self.port = port
        self.server_manager = ServerManager(servers)

    def start(self):
        """Start the bridge server."""
        bridge_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bridge_socket.bind((self.host, self.port))
        bridge_socket.listen(5)
        print(f"[STARTING] Bridge listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = bridge_socket.accept()
                handler = ClientHandler(client_socket, client_address, self.server_manager)
                threading.Thread(target=handler.handle).start()
        except KeyboardInterrupt:
            print("\n[SHUTTING DOWN] Bridge stopped.")
        finally:
            bridge_socket.close()

if __name__ == "__main__":
    bridge = BridgeServer()
    bridge.start()

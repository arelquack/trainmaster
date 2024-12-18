import socket
import threading
from handler.client_handler import ClientHandler
from manager.server_manager import ServerManager

class BridgeServer:
    """
    A server that acts as a bridge between clients and available servers.

    Attributes:
        host (str): The IP address the server listens on.
        port (int): The port the server listens on.
        server_manager (ServerManager): Manages server assignments for clients.
    """

    def __init__(self, host: str = '127.0.0.1', port: int = 12345, servers: list = None):
        """
        Initialize the BridgeServer.

        Args:
            host (str): The IP address to bind the server to.
            port (int): The port number to bind the server to.
            servers (list): List of available servers with their configurations.
        """
        if servers is None:
            servers = [
                {"port": 5001, "client_count": 0},
                {"port": 5002, "client_count": 0},
            ]
        self.host = host
        self.port = port
        self.server_manager = ServerManager(servers)

    def start(self) -> None:
        """
        Start the bridge server to listen for client connections.
        """
        bridge_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            bridge_socket.bind((self.host, self.port))
            bridge_socket.listen(5)
            print(f"[STARTING] Bridge listening on {self.host}:{self.port}")

            while True:
                try:
                    client_socket, client_address = bridge_socket.accept()
                    print(f"[CONNECTED] Client connected from {client_address}")
                    handler = ClientHandler(client_socket, client_address, self.server_manager)
                    thread = threading.Thread(target=handler.handle, daemon=True)
                    thread.start()
                except Exception as e:
                    print(f"[ERROR] Failed to handle client connection: {e}")

        except KeyboardInterrupt:
            print("\n[SHUTTING DOWN] Bridge stopped by user.")

        except Exception as e:
            print(f"[ERROR] An unexpected error occurred: {e}")

        finally:
            bridge_socket.close()
            print("[CLOSED] Bridge socket closed.")

if __name__ == "__main__":
    try:
        bridge = BridgeServer()
        bridge.start()
    except Exception as main_error:
        print(f"[FATAL ERROR] BridgeServer failed to start: {main_error}")
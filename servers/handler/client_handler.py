import logging
from typing import Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ClientHandler:
    """
    Handles client connections, processes their requests, and redirects them to the least loaded server.
    """

    def __init__(self, client_socket: Any, client_address: tuple, server_manager: Any) -> None:
        """
        Initialize ClientHandler.

        Args:
            client_socket (Any): The client's socket object.
            client_address (tuple): The client's address (IP, port).
            server_manager (Any): The server manager instance to determine server load.
        """
        self.client_socket = client_socket
        self.client_address = client_address
        self.server_manager = server_manager

    def handle(self) -> None:
        """
        Handle the client's request and redirect them to the least loaded server.
        """
        logging.info(f"[NEW CLIENT] {self.client_address} connected to Bridge.")
        try:
            # Update server loads
            self.server_manager.update_server_loads()

            # Choose the least loaded server
            chosen_server = self.server_manager.get_least_loaded_server()

            if chosen_server["port"] is None:
                raise ValueError("No available servers to handle the request.")

            # Inform the client about the chosen server
            logging.info(f"[REDIRECT] Sending {self.client_address} to server on port {chosen_server['port']}")
            self._send_response(str(chosen_server["port"]))

        except ValueError as ve:
            logging.error(f"[ERROR] {ve}")
            self._send_response("No available servers, please try again later.")
        except Exception as e:
            logging.exception(f"[ERROR] Unexpected error while handling {self.client_address}: {e}")
        finally:
            self.client_socket.close()
            logging.info(f"[DISCONNECT] {self.client_address} disconnected from Bridge.")

    def _send_response(self, message: str) -> None:
        """
        Send a response to the client.

        Args:
            message (str): The message to send to the client.
        """
        try:
            self.client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            logging.error(f"[ERROR] Failed to send message to {self.client_address}: {e}")

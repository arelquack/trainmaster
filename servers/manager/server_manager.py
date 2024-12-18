import socket
from typing import List, Dict, Union


class ServerManager:
    """
    Manage server loads and provide server assignments based on current loads.

    Attributes:
        servers (List[Dict[str, Union[int, float]]]): List of servers with their load details.
    """

    def __init__(self, servers: List[Dict[str, Union[int, float]]]) -> None:
        """
        Initialize ServerManager with a list of servers.

        Args:
            servers (List[Dict[str, Union[int, float]]]): List of servers with initial configurations.
        """
        self.servers = servers

    def query_server_load(self, server_port: int) -> float:
        """
        Query a server for its current client count.

        Args:
            server_port (int): Port of the server to query.

        Returns:
            float: Current client count or a high load value on failure.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)  # Add timeout to prevent hanging connections
                s.connect(("127.0.0.1", server_port))
                s.sendall(b"GET_LOAD")  # Use consistent byte encoding
                load = float(s.recv(1024).decode('utf-8'))
                return load
        except (socket.timeout, socket.error) as e:
            print(f"[ERROR] Could not query server {server_port}: {e}")
            return float('inf')  # High load on failure

    def update_server_loads(self) -> None:
        """
        Update the load for all servers by querying their current client count.
        """
        for server in self.servers:
            server["client_count"] = self.query_server_load(server["port"])

    def get_least_loaded_server(self) -> Dict[str, Union[int, float]]:
        """
        Return the server with the least load.

        Returns:
            Dict[str, Union[int, float]]: Server with the least client count.
        """
        return min(self.servers, key=lambda s: s["client_count"], default={"port": None, "client_count": float('inf')})

import socket

class ServerManager:
    def __init__(self, servers):
        """Initialize ServerManager with a list of servers."""
        self.servers = servers

    def query_server_load(self, server_port):
        """Query a server for its current client count."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("127.0.0.1", server_port))
                s.send("GET_LOAD".encode('utf-8'))  # Request the load
                load = int(s.recv(1024).decode('utf-8'))  # Receive the load
                return load
        except Exception as e:
            print(f"[ERROR] Could not query server {server_port}: {e}")
            return float('inf')  # Return a high load on failure

    def update_server_loads(self):
        """Update the load for all servers."""
        for server in self.servers:
            server["client_count"] = self.query_server_load(server["port"])

    def get_least_loaded_server(self):
        """Return the server with the least load."""
        return min(self.servers, key=lambda s: s["client_count"])

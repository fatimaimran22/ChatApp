import socket
from threading import Thread, Lock
from config import HOST, PORT, BUFFER_SIZE
import time

class Server:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.clients = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print("-----Welcome to Chat Room-----")

    def accept_clients(self):
        try:
            while True:
                client_socket, client_address = self.server.accept()
                client_socket.settimeout(10000)
                thread = Thread(target=self.handle_client)
        except KeyboardInterrupt as e:
            print("\nServer is Shutting Down.")
        finally:
            self.server_shutdown()

    def handle_client_username(self, client_socket):
        while True:
            try:
                user = client_socket.recv(BUFFER_SIZE).decode().strip()
            except (socket.timeout, ConnectionAbortedError, ConnectionAbortedError, OSError):
                return None

            if not user:
                return 0

            with self.lock:
                if user in self.clients:
                    client_socket.send("Username already taken.".encode())
                    continue
            
                self.clients[user] = client_socket

            client_socket.send("OK".encode())
            return user

    def handle_client(self,client_socket):
        user = self.handle_client_username(client_socket)
        if not user:
            return
        print(f"*{user} has joined the chat*")

        try:
            while True:
                message = (client_socket.recv(BUFFER_SIZE)).decode()
                if not message:
                    break
                self.broadcast(user,message)
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(f"{user} connection lost!: {e}")
        except socket.timeout:
            print(f"{user} was inactive for 1000 seconds.")
        finally:
            self.remove_client(client_socket, message)

    def broadcast(self, user, msg):
        with self.lock:
            clients = list(self.clients.items())
        for username, client in clients:
            try:
                if username != user:
                    client.sendall((f"{user}:{msg}"))
            except (ConnectionError, OSError) as e:
                self.remove_client(client, username)

    def remove_client(self, client_socket, user):
        with self.lock:
            existed = self.clients.pop(user, None)

        if existed is not None:
            print(f"*{user} has left the chat*")
            self.broadcast(user,f" left the chat")

        client_socket.close()

    
    def server_shutdown(self):
        with self.lock:
            clients = list(self.clients.items())
        for user, client in clients:
            self.remove_client(client)
        self.server.close()

    def run(self):
        try:
            self.start()
            self.accept_clients()
        except OSError as e:
            print(f"Failed to start server: {e}")
        finally:
            self.server.close()

if __name__ == "__main__":
    server = Server()
    server.run()
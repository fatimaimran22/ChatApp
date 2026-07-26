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
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lock = Lock()

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print("-----Welcome to Chat Room-----")

    def accept_clients(self):
        try:
            while True:
                client_socket, client_address = self.server.accept()
                thread = Thread(target=self.handle_client, args=(client_socket,), daemon=True)
                thread.start()
        except KeyboardInterrupt as e:
            print("\nServer is Shutting Down.")
        finally:
            self.server_shutdown()

    def handle_client(self,client_socket):
        user = (client_socket.recv(BUFFER_SIZE)).decode()
        if not user:
            client_socket.close()
            return
        with self.lock:
            if user in self.clients:
                client_socket.sendall("Username already taken.".encode())
                client_socket.close()
                return

            self.clients[user] = client_socket
        print(f"*{user} has joined the chat*")

        try:
            while True:
                message = (client_socket.recv(BUFFER_SIZE)).decode()
                if not message:
                    break
                print(f"{user}:{message}")
                self.broadcast(user,message)
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(f"{user} connection lost!: {e}")
        finally:
            self.remove_client(client_socket, user)

    def broadcast(self, user, msg):
        with self.lock:
            clients = list(self.clients.items())
        for username, client in clients:
            try:
                if username != user:
                    client.sendall((f"{user}:{msg}").encode())
            except (ConnectionError, OSError) as e:
                self.remove_client(client, username)

    def remove_client(self, client_socket, user):
        with self.lock:
            existed = self.clients.pop(user, None)

        if existed is not None:
            print(f"*{user} has left the chat*")

        client_socket.close()

    
    def server_shutdown(self):
        with self.lock:
            clients = list(self.clients.items())
        for user, client in clients:
            self.remove_client(client, user)
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
    
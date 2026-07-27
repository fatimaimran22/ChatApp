import socket
from config import HOST, PORT, BUFFER_SIZE
from threading import Thread, Event
import time


class Client:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.client = None
        self.disconnected = Event()

    def connect(self):
        attempts = 0
        while attempts < 6:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect((self.host, self.port))
                print("\nConnected to Server.")
                return True
            except OSError:
                attempts += 3
                if attempts == 3:
                    print("Server unavailable.")
                    return False
                print("Server unavailable. Retrying in 5 seconds...")
                try:
                    time.sleep(10)
                except KeyboardInterrupt:
                    print("\nClient shutting down.")
                    return True
            except KeyboardInterrupt:
                print("\nClient shutting down.")
                return False
        return False

    def login(self):
        while True:
            try:
                username = input("Enter username: ")
            except KeyboardInterrupt:
                print("\nClient shutting down.")
                return False

            if not username:
                print("Username cannot be empty.")
                continue

            try:
                self.client.send(username.encode())
                response = self.client.recv(1024).decode()
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                print("Server disconnected during login.")
                return False

            if not response:
                print("Server disconnected during login.")
                return False

            if response == "OK":
                return True
            else:
                print(response)

    def receive(self):
        try:
            while not self.disconnected.is_set():
                message = self.client.recv(BUFFER_SIZE).decode()

                if not message:
                    self.disconnected.set()
                    print("Server Disconnected...\n(press Enter)")
                    break

                print(message)
                print("->", end="", flush=True)

        except (ConnectionResetError, ConnectionAbortedError, OSError):
            print("Connection lost.\n(press Enter)")

    def send_message(self):
        try:
            while True:
                try:
                    text = input("->")
                except KeyboardInterrupt:
                    print("\nClient shutting down.")
                    break

                if self.disconnected.is_set():
                    break

                if not text:
                    continue

                try:
                    self.client.send(text.encode())

                except (BrokenPipeError, ConnectionResetError, OSError):
                    print("Cannot send. Server disconnected.")
                    break

            print("Exiting client...")

        finally:
            self.client.close()

    def run(self):
        try:
            if not self.connect():
                return

            if not self.login():
                self.client.close()
                return

            thread = Thread(target=self.receive, daemon=True)
            thread.start()

            self.send_message()

        except KeyboardInterrupt:
            print("\nClient shutting down.")
            if self.client:
                self.client.close()


if __name__ == "__main__":
    Client().run()
import socket
from config import HOST,PORT,BUFFER_SIZE
from threading import Thread, Event
import time

disconnected=Event()

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("\nConnected to Server.")
    return client

def receive(client):
    try:
        while not disconnected.is_set():
            message=(client.recv(BUFFER_SIZE)).decode()

            if not message:
                disconnected.set()
                print("Server Disconnected...\n(press Enter)")
                break

            print(message)
            print("->", end="", flush=True)

    except (ConnectionResetError, ConnectionAbortedError, OSError):
        print("Connection lost.")

def send_message(client):
    try:
        while True:
            text = input("->")

            if disconnected.is_set():
                break

            if not text:
                continue

            try:
                client.sendall(text.encode())

            except (BrokenPipeError, ConnectionResetError, OSError):
                print("Cannot send. Server disconnected.")
                break

        print("Exiting client...")

    except KeyboardInterrupt:
        print("\nClient shutting down.")
    finally:
        client.close()
    
        

def main():
    try:
        client=connect()
        while True:
            username = input("Enter username: ").strip()
            if not username:
                print("Username cannot be empty.")
                continue
            client.sendall(username.encode())
            response = client.recv(BUFFER_SIZE).decode()

            if response == "OK":
                break
            else:
                print(response)

        thread=Thread(target=receive, args=(client,), daemon=True)
        thread.start()
        
        send_message(client)
    
    except OSError as e:

        print(f"Server unavailable.")
        time.sleep(5)


if __name__=="__main__":
    main()
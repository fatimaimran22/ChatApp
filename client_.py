import socket
from config import HOST,PORT,BUFFER_SIZE
from threading import Thread

def receive(client):
    try:
        while True:
            message=(client.recv(BUFFER_SIZE)).decode()

            if not message:
                print("Server Disconnected.")
                break

            print(message)

    except (ConnectionResetError, ConnectionAbortedError, OSError):
        print("Connection lost.")
    
        

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST,PORT))
        print("Connected to Server.")
        username = (input('Enter Username: ')).encode()
        client.sendall(username)
        print("Username sent.")

        thread=Thread(target=receive, args=(client,), daemon=True) #This prevents the receive thread from keeping the program alive if the main thread exits.
        thread.start()
        
        try:
            while True:
                text=input('->')
                if not text:
                    continue
                try:
                    client.sendall(text.encode())

                except (BrokenPipeError, ConnectionResetError, OSError):
                    print("Cannot send. Server disconnected.")
                    break

        except KeyboardInterrupt:
            print("\nClient shutting down.")
        finally:
            client.close()
        
    except OSError as e:
        print(f"CONNECTION FAILED: {e}")


if __name__=="__main__":
    main()
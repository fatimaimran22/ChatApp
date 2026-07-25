import socket
from threading import Thread
from config import HOST, PORT, BUFFER_SIZE
import sys

clients=[]

def handle_client(client_socket):
    username=(client_socket.recv(BUFFER_SIZE)).decode()
    print(f"*{username} has joined the chat*")
    try:
        while True:
            message=(client_socket.recv(BUFFER_SIZE)).decode()
            if not message:
                break
            else:
                print(f"{username}: {message}")
    except ConnectionResetError as e:
        print(f"{username} connection lost!")
    finally:
        client_socket.close()
        print(f"*{username} has left the chat*")
        #print(clients)
        clients.remove(client_socket)
        #print(clients)
        

def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST,PORT))
    server.listen()
    print("----Welcome to Chat App----")
    #print(f"Server is listening on {HOST}:{PORT}")
    threads=[]
    try:
        while True:
            client_socket, client_address = server.accept()
            clients.append(client_socket)
            #print(f"Connection from {client_address}")
            thread=Thread(target=handle_client, args=(client_socket,), daemon=True)
            thread.start()
            threads.append(thread)
            
    except KeyboardInterrupt as e:
        print("\nServer is Shutting down.")

    finally:
        #print("Finally block")

        for client in clients:
            client.close()

        server.close()
        # sys.exit(1)


if __name__=="__main__":
    main()

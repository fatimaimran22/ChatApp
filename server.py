import socket
from threading import Thread
from config import HOST, PORT, BUFFER_SIZE

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
            #print(f"Connection from {client_address}")
            thread=Thread(target=handle_client, args=(client_socket,))
            thread.start()
            threads.append(thread)
            
    except KeyboardInterrupt as e:
        print("\nServer is Shutting down.")

    finally:
        server.close()


if __name__=="__main__":
    main()

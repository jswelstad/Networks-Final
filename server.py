import socket
import select
from _thread import *
import sys

SERVER = "127.0.0.1" #Standard loopback interface address (localhost)
PORT = 5239
BUFF_SIZE = 10
HEADER_LENGTH = 10

def main() -> None:

    keepRunning = True

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER, PORT))
        s.listen()

        print("Binding complete")
        print("Listening for connection")

        socket_list = [s]
        clients = {}

        while keepRunning:
            #Used to determine which sockets are open for reading, writing, and/or exceptions. We are only interested in the read sockets
            read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list, 1)
            for notifiedSocket in read_sockets:
                if notifiedSocket == s:     #If the notified socket is the server socket, we have an incoming connection
                    client_socket, client_address = s.accept()      #Accept the connection
                    print(f"Accepted new connection from: {client_address}")
                    socket_list.append(client_socket)       #Append new client socket to list of sockets
                    username = client_socket.recv(1024).decode()
                    print(f"New connection's username is: {username}")
                    clients[client_socket] = username
                else:       #That means the notified socket is not the server socket so it is an existing client
                    data = notifiedSocket.recv(1024).decode()
                    print(f"Received: {data}")
                    username = clients[notifiedSocket]

                    for key in clients:
                        if key != notifiedSocket:
                            key.sendall(f"{username}: {data}".encode())

                    if data == "quit":
                        print(f"Client {username} has disconnected")
                        notifiedSocket.close()
                        socket_list.remove(notifiedSocket)
                        del clients[notifiedSocket]

                    if data == "close server":
                        s.close()
                        break

    print("Server shutting down")    
if(__name__ == "__main__"):
    main()
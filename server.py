import socket
import select
from _thread import *
import sys
from kyle import Game
from kyle import Player

SERVER = "127.0.0.1" #Standard loopback interface address (localhost)
PORT = 5235
BUFF_SIZE = 10
HEADER_LENGTH = 10

def main():
    game = Game(30, 10, 10, "words.txt")

    keepRunning = True
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #IPV4 and TCP

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)         #Allows us to reuse the socket when it doesn't close properly

        s.bind((SERVER, PORT))

        print("Binding complete")

        print("Listening for connection")
        s.listen()
            
        socket_list = [s]
        clients = {}

        while(keepRunning):
            #Used to determine which sockets are open for reading, writing, and/or exceptions. We are only interested in the read sockets
            read_sockets, blank, exeption_sockets = select.select(socket_list, [], socket_list)
            
            for notifiedSocket in read_sockets:
                if(notifiedSocket == s):        #If the notified socket is the server socket, we have an incoming connection
                    client_socket, client_address = s.accept()    #Accept the connection
                    print(f"Accepted new connection from: {client_address}")
                    socket_list.append(client_socket)   #Append new client socket to list of sockets
                    username = client_socket.recv(1024).decode()
                    player = Player(username)
                    game.addPlayer(client_socket, player)
                    print(f"New connecions username is: {username}")
                else:                     #That means the notified socket is not the server socket so it is an existing client
                    data = notifiedSocket.recv(1024).decode()
                    print("Received: ", data)
                    notifiedSocket.sendall(data.encode())
                    if(data == "quit"):
                        print(f'{(game.playerDictionary[notifiedSocket]).username} has quit.')
                        game.deletePlayer(notifiedSocket)
                        socket_list.remove(notifiedSocket)
                        notifiedSocket.close()
                        if (game.getPlayerCount() == 0):
                            keepRunning = False
                            break
        s.close()
    
if(__name__ == "__main__"):
    main()
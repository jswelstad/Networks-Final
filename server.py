import socket
import select
from _thread import *
import sys
from kyle import Game
from kyle import Player
import time

SERVER = "127.0.0.1" #Standard loopback interface address (localhost)
BUFF_SIZE = 10
HEADER_LENGTH = 10

def waitForPlayers(hostSocket, gameDatabase):
    timer = time.time()
    while time.time() - timer < 30: #timer for 30 seconds, gives players time to join.
        read_socket, _, exception_socket = select.select(gameDatabase.playerDictionary.keys(), [], gameDatabase.playerDictionary.keys())
        for notified_socket in read_socket:
            if notified_socket ==hostSocket:
                # accept new connection from new client
                conn, addr = hostSocket.accept()
                print(f"Accepted new connection from: {addr}")
                username = conn.recv(4096)
                print(f"{username} just joined")
                player = Player(username)
                gameDatabase.addPlayer(conn, player)
            # else:                    
            #     serial_data = notified_socket.recv(4096)
                # if serial_data.decode == "quit": #maybe handle quiting in a separate function.
                #     playerName = (gameDatabase.playerDictionary[notified_socket].username)
                #     gameDatabase.deletePlayer(playerName)
                #     socket_list.remove(notified_socket)
                #     notified_socket.close()
                #     if (game.getPlayerCount == 0):
                #         break
                # print(f"Sending pickled data to {clients[conn]}")
                # for key in game.playerDictionary:
                #     if key != notified_socket:
                #         key.sendall(serial_data)
                #         # key.sendall("Sending you pickles".encode())
                #         print(f"Sending data to {clients[key]}")

def sendToPlayers(sockets, message):
    for sock in sockets.playerDictionary:
        if (sockets.playerDictionar[sock].username != 'host'):
            sock.sendall(message.encode())

def main():
    game = Game(30, 10, 3, 'words.txt')
    host = "127.0.0.1"
    port = 1239

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        game.addPlayer(s, "host")
        waitForPlayers(s, game)
        sendToPlayers(game, "STARTGAME")
        while (game.getPlayerCount() > 1): #will run for multiple rounds depending on is the players stay connected
            game.startGame()
            while (game.gameFinished != True): #while loop contains the each game game.
                game.assignDrawer()
                for player in game.playerDictionary: #assign the players their role in the round
                    if (game.playerDictionary[player].username == 'host'):
                        break
                    if game.playerDictionary[player].drawer == True: 
                        player.sendall("DRAWER".encode())
                    else:
                        player.sendall("GUESSER".encode())
                game.startRound()
                while (game.getTimeRemaining() > 0): #while loop contains each round
                    read_socket, _, exception_socket = select.select(game.playerDictionary.keys(), [], game.playerDictionary.keys()) #might need socket_list = [hostSocket]
                    for sock in read_socket:
                        if sock == s:
                            print("No new connections are allowed here")
                        elif game.playerDictionary[sock].drawer == True:
                            serial_data = sock.recv()
                            if serial_data.decode() == "quit":
                                playerName = (game.playerDictionary[sock].username)
                                game.deletePlayer(playerName)
                                sock.close()
                                if (game.getPlayerCount == 0):
                                    break
                            # print(f"Sending pickled data to {clients[conn]}")
                            for key in game.playerDictionary:
                                if key != notified_socket:
                                    key.sendall(serial_data)
                                    # key.sendall("Sending you pickles".encode())
                                    print(f"Sending data to {clients[key]}")
                sendToPlayers(game, "ROUNDFINISHED")       
            sendToPlayers(game, "GAMEFINISH")
            game.resetGame()
            time.sleep(30) #intermission time: 30 seconds
                
                

        while True:
            read_socket, _, exception_socket = select.select(game.playerDictionary.keys(), [], game.playerDictionary.keys()) #might need socket_list = [hostSocket]
            for notified_socket in read_socket:
                if notified_socket == s:
                    # accept new connection from new client
                    conn, addr = s.accept()
                    print(f"Accepted new connection from: {addr}")
                    username = conn.recv(4096)
                    print(f"{username} just joined")
                    player = Player(username)
                    game.addPlayer(conn, player)
                    if game.getPlayerCount() == 1:
                        conn.sendall("1".encode())
                    else:
                        conn.sendall("-1".encode())
                else:                    
                    serial_data = notified_socket.recv(4096)
                    if serial_data.decode == "quit":
                        playerName = (game.playerDictionary[notified_socket].username)
                        game.deletePlayer(playerName)
                        notified_socket.close()
                        if (game.getPlayerCount == 0):
                            break
                    # print(f"Sending pickled data to {clients[conn]}")
                    for key in game.playerDictionary:
                        if key != notified_socket:
                            key.sendall(serial_data)
                            print("hello")
                            # key.sendall("Sending you pickles".encode())
                            print(f"Sending data to {clients[key]}")
                    
if __name__ == "__main__":
    main()
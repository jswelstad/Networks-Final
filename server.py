import socket
import select
from _thread import *
import sys

SERVER = "127.0.0.1" #Standard loopback interface address (localhost)
BUFF_SIZE = 10
HEADER_LENGTH = 10

def main():
    NUMCLIENTS = 0
    host = "127.0.0.1"
    port = 1239

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        socket_list = [s]
        clients = {}

        while True:
            read_socket, _, exception_socket = select.select(socket_list, [], socket_list)
            for notified_socket in read_socket:
                if notified_socket == s:
                    # accept new connection from new client
                    conn, addr = s.accept()
                    print(f"Accepted new connection from: {addr}")
                    socket_list.append(conn)
                    username = conn.recv(4096)
                    print(f"{username} just joined")
                    clients[conn] = username.decode()
                    NUMCLIENTS += 1
                    if NUMCLIENTS == 1:
                        conn.sendall("1".encode())
                    else:
                        conn.sendall("-1".encode())
                else:                    
                    serial_data = notified_socket.recv(4096)
                    # print(f"Sending pickled data to {clients[conn]}")
                    for key, value in clients.items():
                        if key != notified_socket:
                            key.sendall(serial_data)
                            print("hello")
                            # key.sendall("Sending you pickles".encode())
                            print(f"Sending data to {clients[key]}")
                    
if __name__ == "__main__":
    main()
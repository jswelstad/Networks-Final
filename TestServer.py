import socket
import select

BUFF_SIZE = 1024
HEADER_LENGTH = 10

def main():
    host = "127.0.0.1"
    port = 1234

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
                    message_header = conn.recv(HEADER_LENGTH)
                    username = conn.recv(int(message_header.decode().strip()))
                    clients[conn] = username.decode()
                    print(f"{clients}")
                else:
                    # receive new message from existing connection
                    message_header = notified_socket.recv(HEADER_LENGTH)
                    message = notified_socket.recv(int(message_header.decode().strip()))
                    print(f"{message}")
                    if(message == 'close'):
                        username = clients[notified_socket]
                        username_length = len(username)
                        message_header = f"{username_length:<{HEADER_LENGTH}}".encode()
                        message = f"{username} has left"
                        del clients[notified_socket]
                    else:
                        username = clients[notified_socket]
                        username_length = len(username)
                        message_header = f"{username_length:<{HEADER_LENGTH}}".encode()

                    for k,v in clients.items():
                        if k != notified_socket:
                            k.send(message_header+username.encode())
                            message_header2 = f"{len(message.decode()):<{HEADER_LENGTH}}".encode()
                            k.send(message_header2+message)

main()
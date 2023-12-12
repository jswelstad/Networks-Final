import socket
import select
import errno
import sys
import threading

BUFF_SIZE = 1024
MESSAGE_LEN = 10

def receive_messages(s, stop_event):
    while not stop_event.is_set():
        try:
            message_header = s.recv(MESSAGE_LEN)
            recv_username = s.recv(int(message_header.decode().strip()))
            message_header = s.recv(MESSAGE_LEN)
            message = s.recv(int(message_header.decode().strip()))
            print(f"Received from {recv_username.decode()}: {message.decode()}")

            if message == 'close':
                print("Received 'close' message. Closing connection.")
                break
        except ConnectionResetError:
            print("Connection to server closed.")
            break

def main():
    host = "127.0.0.1"
    port = 1234
    username = input("Please enter your username: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        username_length = len(username)
        message_header = f"{username_length:<{MESSAGE_LEN}}".encode()
        print(f"'{message_header}'")
        s.send(message_header+username.encode())

        stop_event = threading.Event()
        receive_thread = threading.Thread(target=receive_messages, args=(s, stop_event))
        receive_thread.start()
        
        while True:
            try:
                message = input(f"{username} > ")
                message_length = len(message)
                message_header = f"{message_length:<{MESSAGE_LEN}}".encode()
                print(f"'{message_header}'")
                s.send(message_header+message.encode())                

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    sys.exit()
                print(f"{e.errno}")
                continue
        
 
        s.send('close'.encode())
        stop_event.set()
        receive_thread.join()
        s.close()

main()
import pygame
import socket
import select
import errno
import threading
from pygame.locals import *

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (127, 127, 127)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

LINECOLOR = BLACK
BACKGROUNDCOLOR = CYAN

BUFF_SIZE = 1024
MESSAGE_LEN = 10
HOST = "127.0.0.1" #Standard loopback interface address (localhost)
PORT = 5235

def receive_messages(sock, stop_event):
    while not stop_event.is_set():
        try:
            data = sock.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"Received: {message}\n")

            if message.lower() == 'close':
                print("Received 'close' message. Closing connection.")
                break
        except ConnectionResetError:
            print("Connection to server closed.")
            break

def main():
    
    # game()
    
    keepRunning = True
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")
    #s.setblocking(False)

    username = input("Please enter your username\n")
    s.sendall(username.encode('utf-8'))
    
    stop_event = threading.Event()
    receive_thread = threading.Thread(target=receive_messages, args=(s, stop_event))
    receive_thread.start()

    while(keepRunning):
        print("Enter your message: ")
        message = input()
        s.sendall(message.encode('utf-8'))
        if(message == "close"):
            keepRunning = False
        #message = s.recv(1024).decode('utf-8')
        #print("Client received:", message)

    # Send a 'close' message to the server before stopping the thread
    s.send('close'.encode('utf-8'))

    # Set the event to signal the receive thread to stop
    stop_event.set()

    # Wait for the receive thread to finish
    receive_thread.join()

    # Close the socket
    s.close()

def game():
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    keepRunning = True

    drawing = False
    points = []
    drawingSegments = []
    running = True

    # Create the game screen        
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Drawing Example")

    while keepRunning:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):   
                keepRunning = False
            elif (event.type == KEYDOWN and event.key == K_ESCAPE):
                keepRunning = False
            elif (event.type == MOUSEBUTTONDOWN):             #Initiate drawing and have it follow the mouse
                points.append(event.pos)
                drawing = True
            elif (event.type == MOUSEBUTTONUP and drawing):     #Terminate drawing
                drawing = False
                drawingSegments.append(points)                  #Save the drawn segments
                points = []                                     #Clear the points array so it doesn't pick up unwanted points
            elif (event.type == MOUSEMOTION and drawing):         #While drawing is active, record the points
                points.append(event.pos)

        screen.fill(BACKGROUNDCOLOR)

        if len(points) > 1:                                    #Display points as they are recorded so you can see where you are drawing
            pygame.draw.lines(screen, LINECOLOR, False, points, 5)

        for segment in drawingSegments:                         #Display all points permanently 
            if len(segment) > 1:
                pygame.draw.lines(screen, LINECOLOR, False, segment, 5)
        pygame.display.update()

    pygame.quit()
    
    
if __name__ == "__main__":
    main()

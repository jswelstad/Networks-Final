import pygame
import socket
import select
import errno
import pickle
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

BUFF_SIZE = 1024
MESSAGE_LEN = 10


def main():
    game()
        

def game():
    host = "127.0.0.1"
    port = 1239
    drawer = False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 800
        keepRunning = True

        drawing = False
        points = []
        drawingSegments = []

        username = input("Please enter your username: ")

        s.sendall(username.encode())
        
        variable = s.recv(4096).decode()
        
        # Create the game screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill(BACKGROUNDCOLOR)
        pygame.display.set_caption("Drawing Example")
        print("SETUP PYGAME WINDOW")

        if variable == "1":
            drawer = True
        else:
            drawer = False
            
        if drawer:

            while keepRunning:
                for event in pygame.event.get():
                    # print(f"PYGAME EVENT IS: {event}")
                    if event.type == pygame.QUIT:
                        keepRunning = False
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        keepRunning = False
                    elif event.type == MOUSEBUTTONDOWN:
                        points.append(event.pos)
                        drawing = True
                        print("THE USER STARTED DRAWING")
                    elif event.type == MOUSEBUTTONUP and drawing:
                        print("THE USER STOPPED DRAWING")
                        drawing = False
                        drawingSegments.append(points)
                        serialized_points = pickle.dumps(drawingSegments)
                        s.sendall(serialized_points)
                        points = []
                    elif event.type == MOUSEMOTION and drawing:
                        print("THE USER IS DRAWING")
                        points.append(event.pos)

                if len(points) > 1:
                    pygame.draw.lines(screen, LINECOLOR, False, points, 5)

                for segment in drawingSegments:
                    if len(segment) > 1:
                        pygame.draw.lines(screen, LINECOLOR, False, segment, 5)
                pygame.display.update()

        else:
            
            while keepRunning:
                for event in pygame.event.get():
                    # print(f"PYGAME EVENT IS: {event}")
                    if event.type == pygame.QUIT:
                        keepRunning = False
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        keepRunning = False

                if len(points) > 1:
                    pygame.draw.lines(screen, LINECOLOR, False, points, 5)

                print("RECIEVING DRAWING DATA FROM SERVER")
                received_data = s.recv(4096)
                drawingSegments = pickle.loads(received_data)

                for segment in drawingSegments:
                    if len(segment) > 1:
                        pygame.draw.lines(screen, LINECOLOR, False, segment, 5)
                pygame.display.update()
            
        
        pygame.quit()

        s.close()

if __name__ == "__main__":
    main()

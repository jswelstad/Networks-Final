import time
import socket
def enterGuess(s, guessIsCorrect): #takes in a socket connection s and a boolean guess is correct
    guess = input("Please enter your guess: ")
    s.sendall(guess.encode())
    message = (s.recv(1024)).decode()
    if (message == "Correct"): #server will be programmed to send back 'Correct' or 'Incorrect'
        guessIsCorrect = True
    else:
        guessIsCorrect = False #my vision for there is a while loop on the game that will break when guessIsCorrect is true

def startTimer():
    startTime = time.time() #store the current time into a variable
    while time.time() - startTime < 30: #compare the variable with the new current time until the distance is 30 seconds
        time.sleep(1) #Debuging purposes, that way the while loop doesn't print a thousand times
        print("The Timer Is Working")
        continue 

def updateScore():


    
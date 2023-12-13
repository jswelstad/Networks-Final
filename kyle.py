import time
import socket
import random
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

class Player:
    def __init__(self, name, socket):
        self.username = name
        self.socket = socket
        self.points = 0

class Game: #my vision is that the Game class will be used on the server side to handle game logic.
    def __init__(self, roundTime, maxPlayers, maxRounds, fileName):
        self.maxRoundTime = roundTime
        self.maxPlayerCount = maxPlayers
        self.maxRounds = maxRounds
        self.roundCount = 0
        self.timer 
        self.gameFinished = False
        self.gameStarted = False
        self.playerList = []
        self.wordList = []
        loadWordList(fileName)

    def addPlayer(self, player):
        self.playerList.insert(player)

    def deletePlayer(self, playerName):
        if (len(self.playerList) < 1):
            print("No players to delete")
        elif playerName in self.playerList:
            self.playerList.remove(playerName)
            if (len(self.playerList) <= 1 and self.gameStarted == True):
                print("Not enough players to continue the game.")
                self.gameFinished == True
        else:
            print(f"{playerName} not found in database.")
    
    def startGame(self):
        if (len(self.playerList) <= 1 or self.gameStarted == True):
            print("Unable to start game because either there aren't at least 2 players or there is already a game going.")
            return
        else:
            self.gameStarted = True
    
    def startRound(self):
        if (self.roundCount >= self.maxRounds):
            self.gameFinished = True
            return
        self.roundCount += 1
        self.timer = time.time()

    def getTimeRemaining(self):
        if (self.gameStarted):
            return time.time() - self.timer
        else:
            print("Round has not started")
            return -1
    
    def resetGame(self):
        self.roundCount = 0
        self.gameFinished = False
        self.gameStarted = False

    def randomWordGenerator(self):
        randomNumber = random.randrange(0, len(self.wordList))
        return self.wordList[randomNumber]
    
    def loadwordList(self, fileName):
        with open(fileName, 'r') as file:
            self.wordList = file.readlines()
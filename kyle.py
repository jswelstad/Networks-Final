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
    def __init__(self, name): #Player class will just consist of username and points
        self.username = name
        self.points = 0

class Game: #my vision is that the Game class will be used on the server side to handle game logic.
    def __init__(self, roundTime, maxPlayers, maxRounds, fileName):
        self.maxRoundTime = roundTime
        self.maxPlayerCount = maxPlayers
        self.maxRounds = maxRounds
        self.roundCount = 0 #counter to keep track of the rounds
        self.timer = time.time()  #this will be used to keep track of how much time as passed
        self.gameFinished = False
        self.gameStarted = False
        self.playerDictionary = {} #player dictionary will consist of these data types - socket : Player (the class I have created up top)
        self.wordList = [] #will store the drawing prompts
        self.loadWordList(fileName)

    def addPlayer(self, socket, player):
        self.playerDictionary[socket] = player #will automatically add a key value pair to the dictionary

    def deletePlayer(self, player):
        if (len(self.playerDictionary) < 1):
            print("No players to delete")
        for key in self.playerDictionary: #
            if ((self.playerDictionary[key]).username == player):
                self.playerDictionary.pop(key)
                if (len(self.playerDictionary) <= 1 and self.gameStarted == True): #if there aren't enough players, gameFinished is set to true
                    print("Not enough players to continue the game.")
                    self.gameFinished == True
                return
        print(f"{player} not found in database.") 
    
    def startGame(self):
        if (len(self.playerDictionary) <= 1 or self.gameStarted == True): 
            print("Unable to start game because either there aren't at least 2 players or there is already a game going.")
            return
        else:
            self.gameStarted = True
    
    def startRound(self):
        if (self.roundCount >= self.maxRounds): #checks to see if the game has already finished its last round.
            self.gameFinished = True
            return
        self.roundCount += 1 
        self.timer = time.time() #each round will have a new timer

    def getTimeRemaining(self):
        if (self.gameStarted):
            return time.time() - self.timer 
        else:
            print("Round has not started")
            return -1
    
    def getPlayerCount(self):
        return len(self.playerDictionary)
    
    def resetGame(self):
        self.roundCount = 0
        self.gameFinished = False
        self.gameStarted = False
        for key in self.playerDictionary:
            (self.playerDictionary[key]).points = 0 #resets all teh players points to zero

    def randomWordGenerator(self):
        randomNumber = random.randrange(0, len(self.wordList))
        return self.wordList[randomNumber]
    
    def loadWordList(self, fileName):
        with open(fileName, 'r') as file:
            self.wordList = file.readlines()

    def addPoints(self, player):
        earnedPoints = (self.maxRoundTime - self.getTimeRemaining())^2
        for key in self.playerDictionary:
            if (self.playerDictionary[key]).username == player:
                (self.playerDictionary[key]).points += earnedPoints
        
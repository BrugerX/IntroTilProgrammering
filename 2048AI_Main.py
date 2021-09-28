from Game2048 import Game2048
import numpy as np
import pygame
import random
import time
import copy
import threading
import InferentialStatistics as inf


class AI2048:
    """
    //Terminology:
    A run: Stepping random moves until the cheap game (game2) is done
    A search: Running x-amount of runs for a single possible move
    A full search: Running x-amount of runs for all possible moves, such that the next proper step can be determined
    A proper step: Stepping the determined move from the full search in the proper game (game1)
    A full game: Stepping enough proper steps, such that the proper game (game1) is done.
    A simulation: N-amount of full games//
    """

    def __init__(self, initX,initSample):

        # Game environments
        self.game1 = Game2048()  # The proper game
        self.game2 = Game2048((self.game1.board, self.game1.score))  # The cheap game

        # Run data
        self.endGameScore = 0  # Score at the end of a single run
        self.endGameReward = 0  # Reward at the end of a single run

        # Search Data
        self.runsScoresList = []  # Used to accumulate scores from runs
        self.rewardsList = []  # Used to accumulate rewards from runs
        self.searchTimeStart = 0 #taken at the start of each search
        self.searchTimeEnd = 0 #taken at the end of each search

        # Full Search Data
        self.sumsList = []  # For summing up non-proportional variables
        self.proportionsList = []  # For summing up proportions
        self.properMove = None
        self.listSearchTimes = [] #A list for time elapsed per search


        # Full game data
        self.game1Done = False  # Used to determine if the proper game is done
        self.game2Done = False  # Used to determine if the cheap game is done
        self.fullGameTimeStart = 0 #taken at the start of each fullgame
        self.fullGameTimeEnd = 0 #taken at the end of each fullgame

        # Simulation Data - this is the data used for our conclusion
        self.fullGamesScores = []
        self.listGameTimes = []
        self.resultList = [None,None,None,None,None,None]

        # Simulation settings
        self.x = initX  # How many runs in a search
        self.N = initSample  # How many full games for a simulation

        # Constants
        self.possibleMoves = ['left', 'right', 'up', 'down']  # Alle possible moves

    # The main loop
    def simulate(self):
        for sims in range(self.N): #Amount of full games is equal to the requested sample size
            self.fullGameTimeStart = time.monotonic()
            self.doFullGame()

            self.extractGameScoreTime() #Calculates the time elapsed and stores it

            self.resetFullGame()

        self.calculateResultList() #Calculates the resultList, which is the data we need for our calculation

    #Adds the correct data to the end list
    def extractGameScoreTime(self):
        self.fullGameTimeEnd = (time.monotonic() - self.fullGameTimeStart)
        self.listGameTimes = self.listGameTimes + [self.fullGameTimeEnd] #Time elapsed from fullgames
        self.fullGamesScores = self.fullGamesScores + [self.game1.score] #Score data from fullgames

    def calculateResultList(self):
        self.resultList[0] = self.listGameTimes
        self.resultList[1] = self.fullGamesScores
        inferentialGameTime = inf.sampleDataSet(self.resultList[0])
        inferentialGameScores = inf.sampleDataSet(self.resultList[1])

        self.resultList[2] = [inferentialGameTime.sampEstMean,inferentialGameTime.cInterval[0],inferentialGameTime.cInterval[1]]
        self.resultList[3] = [inferentialGameScores.sampEstMean,inferentialGameScores.cInterval[0],inferentialGameScores.cInterval[1]]
        self.resultList[4] = [self.x]
        self.resultList[5] = [self.N]

        """
        resultList = endList i format:
        endList[0] = time game data
        endList[1] = scores game data
        endList[2] = [meanGameTime, meanGameTime + C.I, meangGameTime - C.I]
        endList[3] = [meanGameScores, meanGameScores + C.I, meanGameScores - C.I]
        endList[4] = x
        endList[5] = N
        """



    """"
    Do methods:

    Do methods are the methods that actually drive the simulation forward, and play the games.

    """

    # Will run an unknown amounts of full searches, until the proper game is done
    def doFullGame(self):
        while not self.game1Done:
            self.doFullSearch()
            self.calculateProperStep()
            (self.game1.board, self.game1.score), reward, self.game1Done = self.game1.step(self.properMove)
            self.resetFullSearch()

    # TODDO: Some sort of data accumulation for the simulation (conclusion-data)

    # Will run through all the possible moves and determine the next move based on a defined reward system
    def doFullSearch(self):
        for move in self.possibleMoves:
            self.doSearch(move)
            self.listSearchTimes = self.listSearchTimes + [self.searchTimeEnd]
            self.sumsList = self.sumsList + [sum(self.runsScoresList)]
            self.resetSearch()  # Resets run and sets the scoreslist = 0


    def calculateProperStep(self):
        self.properMove = self.possibleMoves[self.sumsList.index(max(self.sumsList))]

    # Will do N amount of runs and add the score from the N amount of runs to the sums list
    def doSearch(self, nextMove):
        self.game2 = Game2048((self.game1.board, self.game1.score))
        self.searchTimeStart = time.monotonic()
        for i in range(self.x):  # Do N amount of runs
            self.doRun(nextMove)
            self.resetRun()

    # Will do a single run of the cheap game with the starting move first and set the scoreslist
    def doRun(self, startingMove):

        (self.board2, self.score2), reward, self.game2Done = self.game2.step(startingMove)
        self.randTillDone()  # Will run random moves until the run is done
        self.runsScoresList = self.runsScoresList + [self.score2]  # Will add to the runs' scoreslist

    def randTillDone(self):  # Will run random moves, until the run is done
        while not self.game2Done:
            (self.board2, self.score2), reward, self.game2Done = self.game2.step(self.possibleMoves[np.random.randint(4)])

    """
    Reset commands:

    Used to turn the "setting" variables back to default.

    We're using a clean-up-after-yourself philosophy. Each reset method is called a level above its own method.

    I.e resetSearch is called at fullSearch, resetRun is called at search etc.

    A reset method is used to revert "setting" variables, such that each new method call will be done in the same manner as the previous.
    """

    # Resets the sim
    def resetSim(self):
        # TODO: Self.resetFullSearch()
        # TODO: self.resetEnvironments()
        print("Move along citizen")

    # Resets the run variables, such that a new run can be conducted exactly as the previous one
    def resetRun(self):
        self.game2Done = False
        self.game2 = Game2048((self.game1.board, self.game1.score))

    def resetSearch(self):
        self.runsScoresList = []

    def resetFullSearch(self):
        self.sumsList = []

    def resetFullGame(self):
        self.game1.reset()
        self.game1Done = False

"""
DEN DEL AF KODEN I SKAL RØRE VED STARTER HER
"""

x = 30
N = 10

gameSim = AI2048(x,N)
gameSim.simulate()
resultList = gameSim.resultList

filLokationOgNavn = r"C:\Users\benja\OneDrive\Documents\2048Data\2048AI-30-1" \
                    r"0-2.txt" #Din fil lokation og navn

string = ""

for x in resultList:
    string = string + f"{x}" + "@"
string = string + "&"
print(string)

fil = open(filLokationOgNavn,"a")
fil.write(string)
fil.close()

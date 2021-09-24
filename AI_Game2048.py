# Game 2048: Artificial intelligence

# Instructions:
#   Move up, down, left, or right to merge the tiles. The objective is to 
#   get a tile with the number 2048 (or higher)
#
# Control:
#    arrows  : Merge up, down, left, or right
#    r       : Restart game
#    q / ESC : Quit

from Game2048 import Game2048
import numpy as np
import pygame
import random
import time

# env = Game2048()
# env.reset()
# actions = ['left', 'right', 'up', 'down']
# exit_program = False
# action_taken = False
# while not exit_program:
#     env.render()
#
#     # Process game events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             exit_program = True
#         if event.type == pygame.KEYDOWN:
#             if event.key in [pygame.K_ESCAPE, pygame.K_q]:
#                 exit_program = True
#             if event.key == pygame.K_UP:
#                 action, action_taken = 'up', True
#             if event.key == pygame.K_DOWN:
#                 action, action_taken  = 'down', True
#             if event.key == pygame.K_RIGHT:
#                 action, action_taken  = 'right', True
#             if event.key == pygame.K_LEFT:
#                 action, action_taken  = 'left', True
#             if event.key == pygame.K_r:
#                 env.reset()

    # INSERT YOUR CODE HERE
    #
    # Implement an AI to play 2048 using simple Monte Carlo search
    #
    # The information you have available is the game state (board, score)
    # 
    # You control the game by setting the action to either
    #    'up', 'down', 'left', or 'right'
    #
    # HINTS
    # You can set up a new game simulation at the current game state like this
    # sim = Game2048((env.board, env.score))
    #
    # You can then play a random game like this
    # done = False
    # while not done:                
    #     action = actions[np.random.randint(4)]
    #     (board, score), reward, done = sim.step(action)
    #
    # When you take an action, set the variable action_taken to True. As you 
    # can see below, the code only steps the envirionment when action_taken 
    # is True, since the whole game runs in an infinite loop.
    
    #Vælge et initMove
class MonteCarlo:
        def __init__(self,initN):

            #For simulations
            self.possibleMoves = ['left', 'right', 'up', 'down'] #Alle possible moves
            self.maxMoves = 1000  # The amount of moves in the sequence, before it is done - based on the minimum amount of moves to win the game.
            self.moveSequence = [] #Moves in which sequence
            self.N = initN #How many simulations to run per move - based on a pilot study

            #Temporary calculations
            self.scoresList = []
            self.meansList = []

            #Data processing
            self.sampleSize = 4198 *2  #How many simulations we'll run before calculating the estimated proportion - based on Basma's calculations
            self.endResults = [] #Consists of lists in the form of [sequenceNumber,initMove,[scores],mean,contains2048]
            self.sumScores = []

            #Will be used for proportion calculation
            self.sequenceFinished = False #movesequence

            #Game
            self.env = Game2048()
            self.sim = Game2048((self.env.board, self.env.score))
            self.done = False


        def runDataCollection(self):
            self.runSimulation()
            for x in range(self.sampleSize):
                self.runGame(nextMove=None)
                print(f"These are the scores{self.scoresList}")
                self.scoresList = []

        def runSimulation(self): #Will run N games and add a new move to the movessequence


            while (len(self.moveSequence)<self.maxMoves +1 ): #Will continue to run simulations, until the movesequence has reached our desired size
                for move in self.possibleMoves: #Will iterate over every possible new move at the start of our new branch

                    for x in range(self.N + 1):
                        #print(f"This is the move: {move}")
                        #print(f"This is x: {x}")
                        self.runGame(move)


                    self.sumScores = self.sumScores + [sum(self.scoresList)]
                    self.scoresList = [] #Resets the scoreslist

                    print(f"These are the sumscores: {self.sumScores}")
                self.calculateBestMove()
            dataFile = open(r"C:\Users\Benja\Documents\2048Data.txt","a")
            dataFile.write(f"Move sequences :{self.moveSequence}: \nN :{self.N}: \nMoveSequenceLimit :{self.maxMoves}:")
            dataFile.close()



        def runGame(self,nextMove): #Will run a full game until the game is over and return score
            #env = Game2048()
            exit_program = False
            action_taken = False
            while not exit_program:


                # Process game events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_program = True
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                            exit_program = True
                        if event.key == pygame.K_UP:
                            action, action_taken = 'up', True
                        if event.key == pygame.K_DOWN:
                            action, action_taken = 'down', True
                        if event.key == pygame.K_RIGHT:
                            action, action_taken = 'right', True
                        if event.key == pygame.K_LEFT:
                            action, action_taken = 'left', True
                        if event.key == pygame.K_r:
                            self.env.reset()

                self.sequenceFinished = False #For checking if the movesequence finishes
                for moves in self.moveSequence:
                    (board, score), reward, self.done = self.sim.step(moves) #Runs first all moves in our move sequence
                self.sequenceFinished = True
                if nextMove != None: #In order to just run the game
                    self.sim.step(nextMove) #Runs the next move
                self.randTillDone() #Runs random moves, until the game is done
                exit_program = True



            self.sim = Game2048((self.env.board, self.env.score))





                #TODO: Find en måde at se om 2048 indgår

        def calculateBestMove(self): #Sets self.nextBestMove to the move calcualted
            for x in self.sumScores:
                self.meansList = self.meansList + [x/self.N]
            self.moveSequence = self.moveSequence + [self.possibleMoves[self.meansList.index(max(self.meansList))]]
            print(f"These are the means: {self.meansList}")
            print(f"These are the best moves: {self.moveSequence}")
            self.resetData()

        def resetData(self):
            self.meansList = []
            self.scoresList = []
            self.sumScores = []

        def randTillDone(self): #Will run random moves, until the game is done
            score = 0

            while not self.done:
                (board, score), reward, self.done = self.sim.step(self.possibleMoves[np.random.randint(4)])

            self.scoresList = self.scoresList + [score]
            self.done = False






simulation1 = MonteCarlo(1000)
simulation1.runSimulation()

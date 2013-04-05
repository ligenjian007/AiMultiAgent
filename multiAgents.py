# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    foodAttraction=0
    for i in range(newFood.width):
        for j in range(newFood.height):
            if newFood[i][j]:
                foodAttraction+=1.0/math.pow(util.manhattanDistance((i,j), newPos),2)
    ghostThreat=0
    for ghost in newGhostStates:
        if newScaredTimes[newGhostStates.index(ghost)]<1:
            if util.manhattanDistance(ghost.configuration.pos,newPos)<=1:
                if util.manhattanDistance(ghost.configuration.pos,newPos)==0:
                    ghostThreat+=-10000
                else:
                    ghostThreat+=-300
            else:
                ghostThreat+=10.0/util.manhattanDistance(ghost.configuration.pos,newPos)
        else:
            ghostThreat+=0
    return 25*foodAttraction+ghostThreat+10*successorGameState.getScore()
#    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    def ghostChoise(state,depth,index):
#        print "index",index,"depth",depth
        if state.data._lose or state.data._win:
            return self.evaluationFunction(state)
        if index==(state.getNumAgents()-1):
            if depth==1:
                states=[state.generateSuccessor(index,action) for action in state.getLegalActions(index)]
                states.append(state)
                minScore=100000
                for nextState in states:
                    if self.evaluationFunction(nextState)<minScore:
                        minScore=self.evaluationFunction(nextState)
                return minScore
            else:
           #     print "the last node in depth",depth
                states=[state.generateSuccessor(index,action) for action in state.getLegalActions(index)]
                states.append(state)
                minScore=100000
                for nextState in states:
                    pacmanScore=pacmanChoise(nextState,depth-1)
                    if pacmanScore<minScore:
                        minScore=pacmanScore
                return minScore
        else:
            states=[state.generateSuccessor(index,action) for action in state.getLegalActions(index)]
            states.append(state)
            minScore=100000
            for nextState in states:
                ghostScore=ghostChoise(nextState,depth,index+1)
                if ghostScore<minScore:
                    minScore=ghostScore
            return minScore
    
    def pacmanChoise(state,depth):
   #     print "index 0","depth",depth
        actions=state.getLegalActions(0)
        actions.append(Directions.STOP)
        maxScore=-1000000
        if state.data._lose or state.data._win:
            return self.evaluationFunction(state)
        for action in actions:
            nextState=state.generateSuccessor(0,action)
            ghostScore=ghostChoise(nextState,depth,1)
            if ghostScore>maxScore:
                newAction=action
                maxScore=ghostScore
        if depth==self.depth:
            return newAction,maxScore
        else:
            return maxScore
    
    action,score=pacmanChoise(gameState,self.depth)
    print score
    return action

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    def ghostChoise(state,depth,index,a,b):
#        print "index",index,"depth",depth
        if state.data._lose or state.data._win:
            return self.evaluationFunction(state)
        if index==(state.getNumAgents()-1):
            if depth==1:
                states=[state.generateSuccessor(index,action) for action in state.getLegalActions(index)]
                states.append(state)
                minScore=100000
                for nextState in states:
                    if self.evaluationFunction(nextState)<minScore:
                        minScore=self.evaluationFunction(nextState)
                    if minScore<=a:
                        return minScore
                    if minScore<b:
                        b=minScore
                return minScore
            else:
           #     print "the last node in depth",depth
                states=[state.generateSuccessor(index,action) for action in state.getLegalActions(index)]
                states.append(state)
                minScore=100000
                for nextState in states:
                    pacmanScore=pacmanChoise(nextState,depth-1,a,b)
                    if pacmanScore<minScore:
                        minScore=pacmanScore
                    if minScore<=a:
                        return minScore
                    if minScore<b:
                        b=minScore
                return minScore
        else:
            states=[state.generateSuccessor(index,action) for action in state.getLegalActions(index)]
            states.append(state)
            minScore=100000
            for nextState in states:
                ghostScore=ghostChoise(nextState,depth,index+1,a,b)
                if ghostScore<minScore:
                    minScore=ghostScore
                if minScore<=a:
                    return minScore
                if minScore<b:
                    b=minScore
            return minScore
    
    def pacmanChoise(state,depth,a,b):
   #     print "index 0","depth",depth
        actions=state.getLegalActions(0)
        actions.append(Directions.STOP)
        maxScore=-1000000
        if state.data._lose or state.data._win:
            return self.evaluationFunction(state)
        for action in actions:
            nextState=state.generateSuccessor(0,action)
            ghostScore=ghostChoise(nextState,depth,1,a,b)
            if ghostScore>maxScore:
                newAction=action
                maxScore=ghostScore
            if maxScore>=b:
                return maxScore
            if maxScore>a:
                a=maxScore
        if depth==self.depth:
            return newAction,maxScore
        else:
            return maxScore
    
    action,score=pacmanChoise(gameState,self.depth,-1000000,1000000)
    print score
    return action
    util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    startState={}
    startState["position"]=problem.getStartState()
    startState["path"]=[]
    startState["visited"]=[startState["position"]]
    startState["cost"]=0
    
    toProcess=util.Stack()
    toProcess.push(startState);
  
    best={}
    best["cost"]=1000000
    
    while not toProcess.isEmpty():
        nextState=toProcess.pop()
        if problem.isGoalState(nextState["position"]):
            if nextState["cost"]<best["cost"]:
                best=nextState
        else:
            toAddPath=copy.copy(problem.getSuccessors(nextState["position"]))
            while not len(toAddPath)==0:
                newToAdd=toAddPath.pop()
                if not (newToAdd[0] in tuple(nextState["visited"])):
                    newState=copy.copy(nextState)
                    newState["position"]=copy.copy(newToAdd[0])
                    newState["path"]=copy.copy(nextState["path"])
                    newState["path"].append(newToAdd[1])
                    newState["visited"]=copy.copy(nextState["visited"])
                    newState["visited"].append(newToAdd[0])
                    newState["cost"]=nextState["cost"]+newToAdd[2]
                    toProcess.push(newState)
    return best["path"]

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    startState={}
    startState["position"]=problem.getStartState()
    startState["path"]=[]
    visited=[]
    visited.append(startState["position"])
    startState["cost"]=0
    
    toProcess=util.Queue()
    toProcess.push(startState);
    
    while not toProcess.isEmpty():
        nextState=toProcess.pop()
        if problem.isGoalState(nextState["position"]):
            return nextState["path"]
        else:
            toAddPath=copy.copy(problem.getSuccessors(nextState["position"]))
            while not len(toAddPath)==0:
                newToAdd=toAddPath.pop()
                if not (newToAdd[0] in tuple(visited)):
                    newState=copy.copy(nextState)
                    newState["position"]=copy.copy(newToAdd[0])
                    newState["path"]=copy.copy(nextState["path"])
                    newState["path"].append(newToAdd[1])
                    visited.append(newToAdd[0])
                    newState["cost"]=nextState["cost"]+newToAdd[2]
                    toProcess.push(newState)

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    
    startState={}
    startState["position"]=problem.getStartState()
    startState["path"]=[]
    visited=[]
    visited.append(startState["position"])
    startState["cost"]=0
    
    toProcess=util.PriorityQueue()
    toProcess.push(startState, 1)
    
    while not toProcess.isEmpty():
        nextState=toProcess.pop()
        if problem.isGoalState(nextState["position"]):
            return nextState["path"]
        else:
            toAddPath=copy.copy(problem.getSuccessors(nextState["position"]))
            while not len(toAddPath)==0:
                newToAdd=toAddPath.pop()
                if not (newToAdd[0] in tuple(visited)):
                    newState=copy.copy(nextState)
                    newState["position"]=copy.copy(newToAdd[0])
                    newState["path"]=copy.copy(nextState["path"])
                    newState["path"].append(newToAdd[1])
                    visited.append(newToAdd[0])
                    newState["cost"]=nextState["cost"]+newToAdd[2]
                    toProcess.push(newState,newToAdd[2])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    startState={}
    startState["position"]=problem.getStartState()
    startState["path"]=[]
    visited=[]
    visited.append(startState["position"])
    startState["cost"]=0
    
    toProcess=util.PriorityQueue()
    toProcess.push(startState, 1)
    
    number=0
    
    while not toProcess.isEmpty():
        nextState=toProcess.pop()
        price=heuristic(nextState["position"],problem)
 #       if not price==number:
 #           number=price
 #       print "position",nextState["position"][0],"heuristic number:",price,"passed: ",nextState["cost"] 
        if problem.isGoalState(nextState["position"]):
            return nextState["path"]
        else:
            toAddPath=copy.copy(problem.getSuccessors(nextState["position"]))
            while not len(toAddPath)==0:
                newToAdd=toAddPath.pop()
 #               print heuristic(newToAdd[0],problem)+newToAdd[2]
                if not (newToAdd[0] in tuple(visited)):
                    newState=copy.copy(nextState)
                    newState["position"]=copy.copy(newToAdd[0])
                    newState["path"]=copy.copy(nextState["path"])
                    newState["path"].append(newToAdd[1])
                    visited.append(newToAdd[0])
                    newState["cost"]=nextState["cost"]+newToAdd[2]
                    toProcess.push(newState,newState["cost"]+heuristic(newState["position"],problem))
#                    print(price)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

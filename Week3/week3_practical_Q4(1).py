from AIMA.search import *
from inspect import signature


"""
Defined in search.py 
Modified by Yue Xu, May 2019
"""

# Code for comparing searching algorithms, calculate some statistics for searching process
class InstrumentedProblem(Problem):
    """
    Delegates to a problem, and keeps statistics.
    self.problem: object of Problem, define the search problem including initial
             state, goal state, goal_test(), path_cost(), actions(), …
    self.succs: number of nodes which have been expanded, excluding leafs
    self.states: number of nodes which have been created, including leafs
    self.goal_tests: number of times that the goal was tested
    self.found: the goal state which has been found
    self.nodes_explanded: a list of nodes expanded excluding leafs
    self.nodes_created: a list of nodes created including leafs
    self.nodes_tested: a list of nodes tested

    """

    def __init__(self, problem):
        self.problem = problem
        self.succs = self.goal_tests = self.states = 0
        self.nodes_expanded = []
        self.nodes_created = []
        self.tested = []
        self.found = None

    def actions(self, state):
        self.succs += 1
        self.nodes_expanded.append(state)
        return self.problem.actions(state)

    def result(self, state, action):
        self.states += 1
        self.nodes_created.append(action)
        return self.problem.result(state, action)

    def goal_test(self, state):
        self.goal_tests += 1
        self.tested.append(state)
        result = self.problem.goal_test(state)
        if result:
            self.found = state
        return result

    def path_cost(self, c, state1, action, state2):
        return self.problem.path_cost(c, state1, action, state2)

    def value(self, state):
        return self.problem.value(state)

    def __getattr__(self, attr):
        return getattr(self.problem, attr)

    def __repr__(self):
        return '#nodes_expanded:{:2d}, #nodes_created: {:2d}, #goal_test: {:2d}, goal_state: {}\n Nodes_explored: {} '.format(self.succs,
                                               self.states, self.goal_tests, str(self.found), self.nodes_expanded )
    def nodes_explored(self):
        return 'Nodes_explored:' + str(self.nodes_expanded)

 
def compare_searchers(problem, searchers):
    def do(problem, searcher, f=None):
        p = InstrumentedProblem(problem)
        if len(signature(searcher).parameters)== 2: # if the function requires two parameters
            goal_node = searcher(p,f) # search function returns goal node
        elif len(signature(searcher).parameters)== 1: # if the function requires one parameter
            goal_node = searcher(p)  # search function returns goal node
        else: return None

        return p, 'Path-cost: ' + str(goal_node.path_cost)
    
    table = [[name(s)] + [do(problem, s, f)] +['\n']  for (s,f) in searchers]
    print('#----------------------------------------------------------------------------------------#')
    print_table(table) # print_table() is a utils method
    print('#----------------------------------------------------------------------------------------#')  
 

#---------------------------------------------------------------------------------------------------# 


class EightPuzzle_Manhattan(EightPuzzle):
    """Define a specific eight puzzle problem using Manhattan distance as the cost estimate"""

    def __init__(self, initial, goal):
        EightPuzzle.__init__(self, initial, goal)

    def h(self, node):
        """
        This method is to calculate cost-estimate of node based on node.state.
        A state is a 3X3 two-dimensional array. It consists of 9 tiles.
        In this implementation, a state is represented as a tuple of 9 numbers
        from 0 to 8. Each number represents a tile, 0 represents blank.
        
        The cost-estimate is the sum of each tile's manhattan distance between the
        tile's position in node.state and the tile's position in goal.
        goal is a state, the state of the goal.

        e.g., for a tile with number 5, node.state.index(5) returns the position of 5
        in node state, while self.goal.index(5) returns the position of 5 in goal state.
        
        You can calculate the manhattan distance between two positions using the given
        method manhattan(n, m) below where n, m are two positions in a tuple of size 9.
        
        """

        #-------------- Your code goes here to complete this method --------------------







  
        #------------------------------------------------------------------------------   

    def manhattan(self,n, m):
        """
        n, m are two positions in a tuple of size 9.
        Return manhattan distance betwen the two positions.
        """
        # Define the coordinates in 3X3 board of each position in a tuple of size 9.      
        coordinates = {0:(0,0), 1:(0,1), 2:(0,2),
                       3:(1,0), 4:(1,1), 5:(1,2),
                       6:(2,0), 7:(2,1), 8:(2,2)}
       
        x1,y1 = coordinates[n]
        x2,y2 = coordinates[m]
        return abs(x1-x2) + abs(y1-y2)
 

# Write code to compare A* algorithm using two different cost-estimate methods:
# the number of misplaced tiles defined in Class EightPuzzle and the manhattan distance defined in Class EightPuzzle_Manhattan
# The initial and goal states are given below

initial = (1,2,3,4,5,6,7,0,8)
goal = (4,1,3,2,0,6,7,5,8)

#-------------- Your code goes here --------------------

# Create the search problems
 

# Heuristic function, cost-estimate

 
# Compare A*


# Using number of misplaced tiles
 

# Using Manhattan distance
 




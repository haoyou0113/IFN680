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

# Question Q3_e
# A subclass of GraphProblem defining Q3 problem
class Q3Problem(GraphProblem):
    """Define a specific graph search problem for Q3 problem"""

    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph

    def h(self, node):
        """h function returns the heuristic values defined in Table 1"""
        table1=dict(S=10, A=5, C=4, D=3, F=4, G=0, H=2)
        
        return table1[node.state]
 


# Write code to compare greetdy and A* algorithms to verify your answer to Q3_c and Q3_d 
# The initial and goal states are given below

initial = 'S'
goal = 'G'

# Define a dict to store the graph in Figure 1
figure1 = dict(
    S=dict(F=7, A=2), A=dict(F=8, C=4), F=dict(A=8, G=5, H=2),
    C=dict(D=3, G=5), D=dict(G=3))

#-------------- Your code goes here ------------------------------------------------------------

# Create a direct Graph to define the state-transition model
 

# Define a Q3Problem search problem, initial state is 'S', goal state is 'G'
 

# Define heuristic function to estimate the cost, cost-estimate, for greedy search
 

# Compare greedy search and A* with cost-estimate
print('Compare greedy search and A* with cost-estimate')
 

# Define heuristic function for A* search
 

# Compare best-first search with this heuristic function and A* search with cost-estimate
# The results should be the same for the two algorithms
print('Compare best-first search with this heuristic function and A* search with cost-estimate')
 

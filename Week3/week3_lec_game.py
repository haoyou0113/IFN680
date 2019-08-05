from AIMA.games import *
"""
Defined by Yue Xu, June 2019

"""
class GraphGame(Game):
    
    def __init__(self, initial, terminal, succs, utils, maxORmin = None, MiniMax_score=None):
        self.succs = succs
        self.utils = utils
        self.initial = initial
        self.terminal = terminal

        if MiniMax_score == None:
            self.MiniMax_score = {}
        else:
            self.MiniMax_score = MiniMax_score

        if maxORmin == None:
            self.maxORmin = dict({initial:'MAX'})
        else:
            self.maxORmin = maxORmin

    def actions(self, state):
        return list(self.succs.get(state, {}).keys()) # return state's children, state is expanded

    def result(self, state, move): # 'move' is a link between 'state' and the returned state,
        new_state = self.succs[state][move]
        self.maxORmin.update({new_state : 'MIN' if self.maxORmin[state]=='MAX' else 'MAX'})
        return new_state #return a state reached from 'state' via 'move'

    def utility(self, state, player): # state should be a leaf node, return its utility value
        if player == 'MAX':
            return self.utils[state]
        else:
            return -self.utils[state]

    def terminal_test(self, state): # if state is a terminal or leaf node
        return state in self.terminal

    def to_move(self, state):
        return self.maxORmin[state]
    
    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        count = 0
        while True:
            for player in players:
                count=count+1
                move = player(self, state)  
                state = self.result(state, move)
                if self.terminal_test(state):
                    return self.utility(state, self.to_move(self.initial))
                
                
# Code for playing games
class InstrumentedGame(GraphGame):
    """
    Delegates to a GraphGame, and keeps statistics.
    self.game: object of GraphGame, define the search problem including initial
             state,  terminal_test(), actions(), …
    self.succs_max, self.succs_min: number of nodes which have been expanded by MAX or MIN player,
                                    excluding leafs
    self.states_max, self.states_min: number of nodes which have been created by MAX or MIN player,
                                    including leafs
    self.terminal_tests_max, self.terminal_tests_min: number of times that terminal nodes were tested
    self.nodes_explanded_max, self.nodes_explanded_min: a list of nodes expanded by MAX or MIN
                                                    player excluding leafs
    self.nodes_created_max, self.nodes_created_min: a list of nodes created by MAX or MIN player including leafs
    self.nodes_tested_max, self.nodes_tested_min: a list of nodes tested by MAX or MIN player
    self.found: the terminal state which has been found
    self.game.maxORmin:  a dict storing MAX nodes or MIN nodes in the graph
    self.MiniMax_score: a dict storing mini-max scores    
    
    """
    
    def __init__(self, game):
        self.game = game
        self.succs_max = self.succs_min = self.terminal_tests_max = 0
        self.terminal_tests_min = self.states_max = self.states_min = 0
        self.nodes_expanded_max = []
        self.nodes_expanded_min = []
        self.nodes_created_max = []
        self.nodes_created_min = []
        self.tested_max = []
        self.tested_min = []
        self.found = None
        self.game.maxORmin
        self.MiniMax_score ={}

        GraphGame.__init__(self, game.initial, game.terminal, game.succs, game.utils, game.maxORmin, game.MiniMax_score )
        
    def actions(self, state):
        if self.game.to_move(state) == 'MAX':
            self.succs_max += 1
            self.nodes_expanded_max.append(state)
        else:
            self.succs_min += 1
            self.nodes_expanded_min.append(state)            
        return self.game.actions(state)

    def result(self, state, action):
        new_state = self.game.result(state, action)
        if self.game.to_move(state) == 'MAX':
            self.states_max += 1
            self.nodes_created_max.append(new_state)
        else:
            self.states_min += 1
            self.nodes_created_min.append(new_state)            
        return new_state

    def terminal_test(self, state):
        if self.game.to_move(state) == 'MAX':
            self.terminal_tests_max += 1
            self.tested_max.append(state)
        else:
            self.terminal_tests_min += 1
            self.tested_min.append(state)            
        result = self.game.terminal_test(state)
        if result:
            if self.game.to_move(state) == 'MAX':
                self.found = 'MAX: ' + state
            else:
                self.found = 'MIN: ' + state 
        return result

    def utility(self, state, player):
        return self.game.utility(state, player)


    def __repr__(self):
        exp_max = 'MAX: \n#nodes_expanded:{:2d}, #nodes_created: {:2d}, #terminal_test: {:2d}, terminal_state: {}\n Nodes_explored: {}\n Nodes_created: {}\n Nodes_tested: {}\n'.format(self.succs_max,
                                               self.states_max, self.terminal_tests_max, str(self.found), self.nodes_expanded_max, self.nodes_created_max, self.tested_max)
        exp_min = 'MIN: \n#nodes_expanded:{:2d}, #nodes_created: {:2d}, #terminal_test: {:2d}, terminal_state: {}\n Nodes_explored: {}\n Nodes_created: {}\n Nodes_tested: {}\n'.format(self.succs_min,
                                               self.states_min, self.terminal_tests_min, str(self.found), self.nodes_expanded_min, self.nodes_created_min, self.tested_min )

        MiniMax_score = 'MiniMax scores \n' + ','.join(str(e) for e in [(x,abs(y)) for (x,y) in self.game.MiniMax_score.items()])
             
        return exp_max + '\n' + exp_min  + '\n' + MiniMax_score
    
    def nodes_explored(self):
        return 'Nodes_explored:' + '(MAX: ' + str(self.nodes_expanded_max) + '), ' + '(MIN: ' + str(self.nodes_expanded_min) + ')\n'
 
def play(game, player1, player2):
    instrumentedGame = InstrumentedGame(game)
    instrumentedGame.play_game(player1, player2)
    print('#----------------------------------------------------------------------------------------#')
    print("Algorithm: ", player1.__name__, '\n')
    print(instrumentedGame)
    print('#----------------------------------------------------------------------------------------#')

# Modified minimax_decision() and alphabeta_search()
def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        game.MiniMax_score.update({state: v}) # save mini-max score
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        game.MiniMax_score.update({state: v}) # save mini-max score
        return v

    # Body of minimax_decision:
    return argmax(game.actions(state),
                  key=lambda a: min_value(game.result(state, a)))


def alphabeta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                game.MiniMax_score.update({state: v}) # save mini-max score
                return v
            alpha = max(alpha, v)
        game.MiniMax_score.update({state: v}) # save mini-max score
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                game.MiniMax_score.update({state: v}) # save mini-max score
                return v
            beta = min(beta, v)
        game.MiniMax_score.update({state: v}) # save mini-max score
        return v

    # Body of alphabeta_search:
    best_score = -infinity
    beta = infinity
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


# Define player
def minimax_player(game, state):
    return  minimax_decision(state, game)

# Define player
def alphabeta_player(game, state):
    return alphabeta_search(state, game)
#---------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------#

# Define successors
succs = dict(A=dict(a1='B', a2='C', a3='D'), B=dict(b1='B1', b2='B2', b3='B3'),
                 C=dict(c1='C1', c2='C2', c3='C3'), D=dict(d1='D1', d2='D2', d3='D3'))
# Define utility values
utils = dict(B1=3, B2=12, B3=8, C1=2, C2=4, C3=6, D1=14, D2=5, D3=2)

# Specify initial state
initial = 'A'

# Specify terminal states
terminal = ['B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'D1', 'D2', 'D3']

# Create the game object
f52_game = GraphGame(initial, terminal, succs, utils)
 
# Play the game using minimax algorithm
play(f52_game, minimax_player, minimax_player)

# Create the game object again for using alphabeta_search
f52_game = GraphGame(initial, terminal, succs, utils)

# Play the game using alpha-beta pruning
play(f52_game, alphabeta_player, alphabeta_player)






 

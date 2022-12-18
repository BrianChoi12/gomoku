import collections
import time
import random

# Parameters to change based off heuristic
win_reward = 100000
ttabminimax = None

# Source for LRU Cache: https://pastebin.com/LDwMwtp8
class LRU:
 
    def __init__(self, func, maxsize=128):
        self.cache = collections.OrderedDict()
        self.func = func
        self.maxsize = maxsize
        self.hits = 0
 
    def __call__(self, *args):
        cache = self.cache

        storedargs = args[0] # state
        depth = args[4] # depth
        alpha = args[1]
        beta = args[2]

        if storedargs in cache and cache[storedargs][0] >= depth:
            pruning_done = cache[storedargs][1][3]
            value = cache[storedargs][1][0]
            if pruning_done == True:
                if storedargs.actor() == 0:
                    # White, max node
                    if value >= beta:
                        cache.move_to_end(storedargs)
                        self.hits += 1
                        return cache[storedargs][1]
                else:
                    # Black, min node
                    if value <= alpha:
                        cache.move_to_end(storedargs)
                        self.hits += 1
                        return cache[storedargs][1]
            else:
                cache.move_to_end(storedargs)
                self.hits += 1
                return cache[storedargs][1]
        
        result = self.func(*args)
        cache[storedargs] = [depth, result]

        if len(cache) > self.maxsize:
            cache.popitem(last=False)

        return result

def heur(state):
    # Do a O(n) search
    return state.heuristic()

def abminimax(state, alpha, beta, h, depth, start_time, time_limit):
    '''
    Returns: The value of the node and the move to take at the node (value, move, finished, pruning_done)
    '''
    global ttabminimax
    pruning_done = False

    # Check if we have remaining time
    if time.time() - start_time >= time_limit:
        return (None, None, False, pruning_done)

    # Check first if you are done with game
    if state.is_terminal():
        return (win_reward * state.payoff(), None, True, pruning_done)
    # If leaf, find heuristic
    if depth == 0:
        return (h(state), None, True, pruning_done)
    
    # Max position (white = 0)
    if state.actor() == 0:
        a = float('-inf') # Value of best child so far, a lower bound on the state
        best_move = None
        for move in state.get_actions():
            if alpha >= beta:
                pruning_done = True
                break
            value, _, finish, _ = ttabminimax(state.successor(move), alpha, beta, h, depth-1, start_time, time_limit)
            if not finish:
                return (None, None, False, pruning_done)
            a = max(a, value)
            if a > alpha:
                alpha = a
                best_move = move
        return (a, best_move, True, pruning_done)
    
    else:
    # Min position (black = 1)
        b = float('inf')
        best_move = None
        for move in state.get_actions():
            if alpha >= beta:
                pruning_done = True
                break
            value, _, finish, _ = ttabminimax(state.successor(move), alpha, beta, h, depth-1, start_time, time_limit)
            if not finish:
                return (None, None, False, pruning_done)
            b = min(b, value)
            if b < beta:
                beta = b
                best_move = move
        return (b, best_move, True, pruning_done)


def baseline_policy(time_limit):
    '''
    Input: 
        time: (secs)
    Output: 
        lambda function that can take a position and return the move suggested by alpha-beta pruned minimax

    Lambda wrapper for alpha-beta minimax policy
    '''

    # You only need transposition table within a single fxn call; initialize it in fxn

    def fxn(root):
        global ttabminimax

        # Time 
        start_time = time.time()
        best_move = None
        
        # Init transpotision table
        ttabminimax = LRU(abminimax, maxsize=1024)
        
        # Searching at depth 1
        it_depth = 2
        searched_depth = None

        while (time.time() - start_time < time_limit):
            val, move, finished, _ = ttabminimax(root, float('-inf'), float('inf'), heur, it_depth, start_time, time_limit)
            if finished:
                best_move = move
                
                # Increase iterative deepening
                searched_depth = it_depth
                break
                it_depth += 1
            else:
                break
        
        # print(f"Deepest depth searched: {searched_depth}")
        # print(ttabminimax.cache)
        # print(f"Hits: {ttabminimax.hits}")

        return best_move
    return fxn

def abminimax_policy(time_limit):
    '''
    Input: 
        time: (secs)
    Output: 
        lambda function that can take a position and return the move suggested by alpha-beta pruned minimax

    Lambda wrapper for alpha-beta minimax policy
    '''

    # You only need transposition table within a single fxn call; initialize it in fxn

    def fxn(root):
        global ttabminimax

        # Time 
        start_time = time.time()
        best_move = None
        
        # Init transpotision table
        ttabminimax = LRU(abminimax, maxsize=10000)
        
        # Iterative deepening, begin searching at depth 2
        it_depth = 2
        searched_depth = None

        while (time.time() - start_time < time_limit):
            val, move, finished, _ = ttabminimax(root, float('-inf'), float('inf'), heur, it_depth, start_time, time_limit)
            if finished:
                best_move = move
                
                # Increase iterative deepening
                searched_depth = it_depth
                if searched_depth == 4:
                    break
                it_depth += 2
            else:
                break
        
        # print(f"Deepest depth searched: {searched_depth}")
        # print(ttabminimax.cache)
        # print(f"Hits: {ttabminimax.hits}")

        return best_move
    return fxn

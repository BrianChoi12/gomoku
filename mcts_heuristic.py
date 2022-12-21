from abminimax import LRU, heur, abminimax

ttabminimax = None
win_reward = 10000

def abminimax(state, alpha, beta, h, depth, start_time, time_limit):
    """
        copy of function in abminimax function with slight modifications for application in mcts
        completes alpha beta search starting with state and using bounds alpha and beta

        state - state of the board
        alpha, beta - alpha beta bounds
        h - heuristic function
        depth - depth to search to
    """
    global ttabminimax
    pruning_done = False

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

def mcts_h(state):
    """
        wrapper function for heuristic used in mcts
        takes in state and returns heuristic value based on alpha beta search to a depth of 2

        state - state of the board that the heuristic value corresponds to
    """
    global ttabminimax
    ttabminimax = LRU(abminimax, maxsize=1024)
    value = abminimax(state, float('-inf'), float('inf'), heur, 2, 0, 1000)[0]; 
    return value



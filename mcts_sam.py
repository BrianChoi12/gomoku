import time
import random
import math
'''
Create a Python 3 module called mcts (so this must be in a file called mcts.py) that implements a function called mcts_policy 
that takes the allowed CPU time in seconds and returns a function that takes a position and returns the move suggested by running 
MCTS for that amount of time starting with that position.
'''
def mcts_policy(allowed_time):
    def MCTS(root):
        c = 2 # scaling factor
        start_time = time.time()
        edges_dict = dict()
        exploit = lambda f: f[2][0] / f[2][1]
        visits = lambda f: f[2][1]
        child = lambda f: f[1]
        action = lambda f: f[0]
        player = 1 if root.actor() == 0 else -1
        while time.time() - start_time < allowed_time: # Make sure to add checks throughout code for this
            # Traverse Tree: Root to leaf
            node_history = []
            index_history = []
            leaf = root
            while leaf in edges_dict.keys():
                # Compute UCB1 Values
                player = 1 if leaf.actor() == 0 else -1
                best_UCB_val = -1 * player * math.inf
                T = sum([visits(x) for x in edges_dict[leaf]])
                best_child = None
                best_index = None
                edges = edges_dict[leaf]
                for i in range(len(edges)):
                    edge = edges[i]
                    child_node = child(edge)
                    if visits(edge) == 0:
                        best_child = child_node
                        best_index = i
                        break
                    else:
                        UCB_val = exploit(edge) + player * math.sqrt(c * math.log(T) / visits(edge))
                        if UCB_val * player > best_UCB_val * player:
                            best_UCB_val = UCB_val
                            best_child = child(edge)
                            best_index = i
                leaf = best_child
                node_history.append(leaf)
                index_history.append(best_index)
            # Up to leaf is added into history
            # If leaf is expandable (non terminal, haven't added children yet) add its children 
            result = 0
            if leaf.is_terminal():
                result = leaf.payoff()
            else:
                edges_dict[leaf] = [] # list full of [action, child, [sum values, n]]
                for move in leaf.get_actions():
                    edges_dict[leaf].append([move, leaf.successor(move), [0, 0]])
                
                # Simulate: Play to terminal position
                random_index = random.choice(range(len(edges_dict[leaf])))
                random_walk = child(edges_dict[leaf][random_index])#leaf.successor(random.choice(leaf.get_actions()))
                index_history.append(random_index)
                node_history.append(random_walk)
                
                while not random_walk.is_terminal():
                    random_walk = random_walk.successor(random.choice(random_walk.get_actions()))
                result = random_walk.payoff()
            
            # Update: Backpropogate Strats Along Path Through Tree From Point Simulation Started to Root
            prev = root
            for i in range(len(node_history)):
                edges_dict[prev][index_history[i]][2][0] += result
                edges_dict[prev][index_history[i]][2][1] += 1
                prev = node_history[i]
        # Select move based on current statistics (highest average or highest visit count) 
        highest_visit = 0
        ret = None
        for edge in edges_dict[root]:
            if visits(edge) > highest_visit:
                highest_visit = visits(edge)
                ret = action(edge)
        return ret
    return MCTS

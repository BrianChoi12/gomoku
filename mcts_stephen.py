import time
import math
import random

# Allowed up to 6 global variables for adjusting UCB tunable constant \overline{r}_j + sqrt(c ln(T)/n_j)
ucb_const = 2 # Arbitrary starting value
reward_min = float('inf')
reward_max = float('-inf')

def ucb2(node, table, who):
    '''
    Returns True and child of node with the highest UCB, or the first child found with no playthroughs from curr node
    Or False and curr node we have reached a leaf
    '''
    global ucb_const
    highest = float('-inf')
    highest_node = None
    total = 0

    # our root node is new
    if table[node][0][1] == 0:
        return False, node
        
    for k,v in table[node][1].items():
        # Add to total T for exploration in UCB
        total += v[1]

        # Check if there is a zero visit child from current node
        if v[1] == 0:
            return False, k

    exploration_factor = ucb_const * math.log(total)

    for k,v in table[node][1].items():
        # Mean reward sum(reward edges going in) / sum(number of visits from edges going in)
        mean_reward = (table[k][0][0] / table[k][0][1])

        # Exploration factor for all edges from original node
        ucb_cur = who * mean_reward + math.sqrt(exploration_factor / v[1])

        if ucb_cur > highest:
            highest = ucb_cur
            highest_node = k

    return True, highest_node

    

def mcts_policy(time_limit):
    '''
    Input: 
        time: (secs)
    Output: 
        lambda function that can take a position and return the move suggested by mcts

    Lambda wrapper for mcts policy
    '''
    global ucb_const
    global reward_max
    global reward_min
    global count
    node_edges_table = dict() # Dict of nodes -> [[reward, visits], {child -> [action, visits]}] for calculating UCB2
    if reward_max != float('-inf') and reward_min != float('inf'):
        ucb_const = (abs(reward_max) + abs(reward_min))/2

    def fxn(root):
        global reward_max
        global reward_min
        # My variables, note that we can directly use pos as a key for a dict with the implicit __hash__ and __eq__
        start_time = time.time()
        who = -1 if int(root.actor()) == 1 else 1 # 1 or 0
        # print(pos.actor(), who)

        # Set tree = root
        if root not in node_edges_table:
            node_edges_table[root] = [[0,0], dict()]
        # count = 0

        # Until no time
        while (time.time() - start_time < time_limit):
            # count += 1
            # Traverse tree to leaf using UCB2
            look, leaf = True, root
            payoff = None
            history = [root]

            while (look):
                # Add to history for future back-prop
                var_who = -1 if int(leaf.actor()) == 1 else 1
                look, leaf = ucb2(leaf, node_edges_table, var_who)
                
                history.append(leaf)
                if (leaf.is_terminal()):
                    break
            
            if history[0] == history[1]:
                assert(len(history) == 2)
                history = [root]

            if (leaf.is_terminal()):
                payoff = leaf.payoff()
            else:
                # Expand if leaf non-terminal and we haven't added the children yet, then add children
                for act in leaf.get_actions():
                    child = leaf.successor(act)
                    if child not in node_edges_table[leaf][1]:
                        node_edges_table[leaf][1][child] = [act, 0]
                    if child not in node_edges_table:
                        node_edges_table[child] = [[0,0], dict()]

                # Simulate game down to terminal using good policy
                while (not leaf.is_terminal()):
                    actions = leaf.get_actions()
                    leaf = leaf.successor(actions[random.randint(0,len(actions)-1)])
                payoff = leaf.payoff()
            
            # Update ucb range vars
            reward_min = min(reward_min, payoff)
            reward_max = max(reward_max, payoff)

            # Back prop result up the tree from start of tree to root
            for i in range(len(history)-1):
                node = history[i]
                node_edges_table[node][0][0] += payoff
                node_edges_table[node][0][1] += 1
                node_edges_table[node][1][history[i+1]][1] += 1
            node_edges_table[history[len(history)-1]][0][0] += payoff
            node_edges_table[history[len(history)-1]][0][1] += 1

        # Return the move to child with optimal stats (highest mean reward or highest visit count)
        best_move = None
        best_stats = float('-inf')
        # who = -1 if int(root.actor()) else 1 # 1 or 0
        # print("iterations:", count)
        for k,v in node_edges_table[root][1].items():
            child = k
            # if node_edges_table[child][0][1] == 0:
            #     continue

            # child_stats = who * node_edges_table[child][0][0] / node_edges_table[child][0][1]
            child_stats = v[1]
            if best_stats < child_stats:
                best_stats = child_stats
                best_move = v[0]

        return best_move
    return fxn
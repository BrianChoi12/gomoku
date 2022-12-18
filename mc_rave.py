import random
import math
import time
import copy
from mcts_heuristic import mcts_h

NUM_SIMULATE = 50 #number of times to simulate when leaf node has been found, for rapid average value estimation
WEIGHT_HEURISTIC = 100 #hyper parameter of how much to weight the heuristic used in MCTS

class myNode():
    """
        node class that represents node in MCTS tree, saving various features.
        the variables stored in this class persist throughout a single game but 
        not throughout the entire lifetime of the program

        position - state that the game is in 
    """
    def __init__(self, position):
        self.position = position
        self.child = [] #keep track of children
        self.actions = position.get_actions()
        self.payoff = 0 #total payoff from simulations
        self.times = 0 #total number of times simulated
        self.isLeaf = False
        self.visited = [] #keep track of child visit counts
        self.terminal = self.position.is_terminal()
        self.aToc = dict() #key is action, c is resulting child, stored for faster computation
        self.check = False #if the visit count is nonzero but the node hasn't been visited yet
                            #case when the newly expanded node has initialized values

def traverse(node, nodeDict):
    """
        find leaf node by traversing from starting node and applying UCB2 formula

        node - node representing starting position (represents root of MCTS tree)
        nodeDict - dictionary that stores all the nodes
    """

    #sequence represents the path taken down the mcts tree for backpropagation
    sequence = []
    while(True):
        sequence.append(node)

        #if terminal node
        if(node.terminal): 
            return sequence
        
        #if node has never been visited before
        if node.times == 0 or node.check: 
            node.isLeaf = True
            return sequence

        if node.position.actor() == 0:
            player = 1
        else:
            player = -1

        #if leaf node, expand children
        if node.isLeaf:
            for act in node.actions:
                next_state = node.position.successor(act)
                nodeDict[node.position].aToc[act] = next_state
                inTree = True
                if next_state not in nodeDict:
                    nextNode = myNode(next_state)
                    nodeDict[next_state] = nextNode
                    inTree = False
                else:
                    nextNode = nodeDict[next_state] 

                    #if heuristic hasn't been used yet on node and node
                    #hasn't been visited many times
                    if nextNode.times < WEIGHT_HEURISTIC:
                        inTree = False
                
                node.child.append(nextNode)
                
                if not inTree:
                    #initialize node visit and payoff counts based on heuristic
                    result = mcts_h(next_state)
                    if(result == 100000): #check if heuristic indicates terminal state
                        nextNode.payoff += 1 * WEIGHT_HEURISTIC
                    else: #otherwise normalize heuristic value
                        nextNode.payoff += result/10000 * WEIGHT_HEURISTIC
                        
                    nextNode.times += 1 * WEIGHT_HEURISTIC
                    nextNode.check = True
                node.visited.append(nextNode.times)
            
            node.isLeaf = False
            possible = node.child[0]
            possible.isLeaf = True
            node.visited[0] += 1
            sequence.append(possible)
            return sequence
        
        maxVal = float('-inf')  
        maxState = None
        maxIndex = 0

        visitIndex = 0

        #apply UCB2 formula for each child node
        for childNode in node.child:
            visits = node.visited[visitIndex]
            
            if(visits == 0):
                node.visited[visitIndex] += 1
                sequence.append(childNode)
                if childNode.child == []:
                    childNode.isLeaf = True
                return sequence

            prob = player * childNode.payoff/(childNode.times) + math.sqrt(2 * math.log(node.times)/visits) 
            if prob > maxVal:
                maxVal = prob; 
                maxState = childNode
                maxIndex = visitIndex
            visitIndex += 1
        
        node.visited[maxIndex] += 1
        node = maxState

def simulate(leaf, nodeDict):
    """
        rollout from leaf node and return payoff

        leaf - node representing leaf found through traverse    
    """
    search = leaf
    moves = set()

    while search.is_terminal() == False:
        actions = search.get_actions()

        #choose random action
        choice = actions[random.randint(0,len(actions)-1)]
        moves.add(choice)
        nextSearch = search.successor(choice)
        search = nextSearch

    pay = search.payoff()
    
    check = nodeDict[leaf].aToc
    
    #update weights in rapid average value estimation, based on actions taken
    for move in moves:
        if move in check:
            if check[move] in nodeDict: 
                nodeDict[check[move]].times += 1/NUM_SIMULATE
                nodeDict[check[move]].payoff += pay/NUM_SIMULATE
            else:
                position = leaf.successor(move)
                nodeDict[check[move]] = myNode(position)
                nodeDict[check[move]].times += 1/NUM_SIMULATE
                nodeDict[check[move]].payoff += pay/NUM_SIMULATE
                nodeDict[check[move]].check = True

    return pay


def mcts_policy(seconds):
    """
        run mcts for given number of seconds

        seconds - number of seconds to run for
    """
    nodeDict = dict()

    def policy(state): 
        
        if state not in nodeDict:
            nodeDict[state] = myNode(state)
        node = nodeDict[state]

        end = time.time() + seconds
        while(time.time() < end):
            sequence = traverse(node, nodeDict)
            leaf = sequence[-1]
            value = 0

            for action in leaf.actions:
                nodeDict[leaf.position].aToc[action] = leaf.position.successor(action)
            
            for i in range(NUM_SIMULATE): 
                value += simulate(leaf.position, nodeDict)

            for i in range(len(sequence)):
                sequence[i].payoff += value
                sequence[i].times += NUM_SIMULATE
        player = -1
        if(state.actor() == 0):
            player = 1
        
        #iterate through possible actions and choose the best one
        possible = state.get_actions()
        if player == 1: 
            maxIndex = 0
            maxVal = None
            for i in range(len(possible)):
                next_state = state.successor(possible[i])
                if(next_state in nodeDict and nodeDict[next_state].times != 0): 
                    nodeVal = nodeDict[next_state].payoff/nodeDict[next_state].times
                    if(maxVal == None or nodeVal > maxVal):
                        maxVal = nodeVal
                        maxIndex = i
            return possible[maxIndex]
        else:
            maxIndex = 0
            maxVal = None
            for i in range(len(possible)):
                next_state = state.successor(possible[i])
                if(next_state in nodeDict and nodeDict[next_state].times != 0): 
                    nodeVal = nodeDict[next_state].payoff/nodeDict[next_state].times
                    if(maxVal == None or nodeVal < maxVal):
                        maxVal = nodeVal
                        maxIndex = i
            return possible[maxIndex]
    
    return policy

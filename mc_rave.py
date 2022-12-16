

import random
import math
import time
import copy

class myNode():
    """
        node class that represents node in MCTS tree, saving various features.
        the variables stored in this class persist throughout a single game but 
        not throughout the entire lifetime of the program

        position - state that the game is in 
    """
    def __init__(self, position):
        self.position = position
        self.child = []
        self.actions = position.get_actions()
        self.payoff = 0
        self.times = 0
        self.isLeaf = False
        self.visited = []
        self.terminal = self.position.is_terminal()
        self.aToc = dict() #key is action, c is child


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
        if(node.terminal): 
            return sequence
        
        if node.times == 0: 
            node.isLeaf = True
            return sequence

        if node.isLeaf:
            for act in node.actions:
                next_state = node.position.successor(act)
                nodeDict[node.position].aToc[act] = next_state
                if next_state not in nodeDict:
                    nextNode = myNode(next_state)
                    nodeDict[next_state] = nextNode
                else:
                    nextNode = nodeDict[next_state] 
                
                node.child.append(nextNode)
                node.visited.append(0)

            node.isLeaf = False
            possible = node.child[0]
            possible.isLeaf = True
            node.visited[0] += 1
            sequence.append(possible)
            return sequence
        
        if node.position.actor() == 0:
            player = 1
        else:
            player = -1

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
        choice = actions[random.randint(0,len(actions)-1)]
        moves.add(choice)
        nextSearch = search.successor(choice)
        search = nextSearch

    pay = search.payoff()

    check = nodeDict[leaf].aToc
    for move in moves:
        if move in check:
            nodeDict[check[move]].times += 1
            nodeDict[check[move]].payoff += pay

    return pay


def mcts_policy(seconds):
    """
        run mcts for given number of seconds

        seconds - number of seconds to run for
    """
    nodeDict = dict()
    NUM_SIMULATE = 1
    def policy(state): 
        if state not in nodeDict:
            nodeDict[state] = myNode(state)
        node = nodeDict[state]

        end = time.time() + seconds
        while(time.time() < end):
            sequence = traverse(node, nodeDict)
            leaf = sequence[-1]
            value = 0
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

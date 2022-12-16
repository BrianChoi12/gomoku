import copy
import itertools
import time
import random

# Precompute tuple to heuristic evaluation
sz = 10
row_to_heur = dict()
block = {2:10, 3:200, 4:500, 5:100000}
unblocked = {2:50, 3:500, 4:4800, 5:100000}
# starter = time.time()
for i in range(5,sz+1):
    for rw in list(itertools.product(*[(-1, 0, 1)] * i)):
        heuristic = 0
        players = [-1,1]
        for player in players: 
            blocked = True
            count = 0
            for i in range(len(rw)):
                if count == 0 and rw[i] == -1 * player:
                    blocked = True
                elif count == 0 and rw[i] == 0:
                    blocked = False
                elif rw[i] == player:
                    count += 1
                else:
                    # We have hit either empty (0) or enemy stone and we have some streak of ours
                    if count == 1:
                        count = 0
                        if rw[i] == 0: 
                            blocked = False
                        else:
                            blocked = True
                        continue
                    elif count > 5:
                        count = 5
                    if blocked and rw[i] == 0:
                        if player == 1:
                            heuristic -= block[count]
                        else:
                            heuristic += block[count]
                        blocked = False
                    elif not blocked and rw[i] == -1 * player:
                        if player == 1:
                            heuristic -= block[count]
                        else:
                            heuristic += block[count]
                        blocked = True
                    elif not blocked and rw[i] == 0:
                        if player == 1:
                            heuristic -= unblocked[count]
                        else:
                            heuristic += unblocked[count]
                        blocked = False
                    count = 0
            if count > 1:
                if count > 5:
                    count = 5
                if not blocked:
                    if player == 1:
                        heuristic -= block[count]
                    else:
                        heuristic += block[count]
        row_to_heur[rw] = heuristic
# print(f"This took {time.time() - starter} seconds")   
# for k in random.choices(list(row_to_heur), k=5):
#     print(k, row_to_heur[k])


class State:
    def __init__(self, size, player0, player1, empty, board, board90, board45, board135, move, potential=set(), start=False):
        self.size = size
        self.pieces = dict()
        self.pieces[0] = copy.deepcopy(player0) #player 0 pieces (white)
        self.pieces[1] = copy.deepcopy(player1) #player 1 pieces (black)
        self.pieces[2] = copy.deepcopy(empty) #empty squares //TODO: get rid of self.pieces[2] 
        self.pay = 0
        self.board = copy.deepcopy(board) #[[0] * self.size for i in range(self.size)]
        self.board45 = copy.deepcopy(board45)
        self.board90 = copy.deepcopy(board90)
        self.board135 = copy.deepcopy(board135)
        self.next_moves = copy.deepcopy(potential)
        self.move = move
        self.start = start

        if(move != None): 
            actor = self.actor()
            if(actor == 1): 
                self.board[self.move[0]][self.move[1]] = 1 # Black stones are 1
                self.board90[self.move[1]][self.move[0]] = 1
                self.board45[self.move[1] + self.move[0]][min(self.move[1], self.size - self.move[0] - 1)] = 1
                self.board135[self.move[0] + self.size - 1 - self.move[1]][min(self.size - self.move[1] - 1, self.size - self.move[0] - 1)] = 1
            else:
                self.board[self.move[0]][self.move[1]] = -1 # White stones are -1
                self.board90[self.move[1]][self.move[0]] = -1
                self.board45[self.move[1] + self.move[0]][min(self.move[1], self.size - self.move[0] - 1)] = -1
                self.board135[self.move[0] + self.size - 1 - self.move[1]][min(self.size - self.move[1] - 1, self.size - self.move[0] - 1)] = -1
            
            if(move in self.next_moves):
                self.next_moves.remove(move)

            directions = [[0,1],[0,-1],[1,0],[-1,0],[1,1],[-1,-1],[1,-1],[-1,1]]
            x, y = move[0], move[1]
            for d in directions: 
                surrounding = (x+d[0], y+d[1])
                if self.valid(surrounding) and surrounding not in self.pieces[0] \
                and surrounding not in self.pieces[1]:
                    self.next_moves.add(surrounding)

            self.pieces[actor].add(self.move)
            self.pieces[2].remove(self.move)
        
        self._compute_hash()

    def valid(self, coordinates):
        for element in coordinates:
            if element < 0 or element >= self.size:
                return False
        return True
        
    def actor(self):
        '''
        Returns the next actor (white=0, black=1) for the current state
        '''
        # White (0) should move first
        if ((len(self.pieces[0]) - 1) == len(self.pieces[1])):
            return 1
        elif (len(self.pieces[0]) == len(self.pieces[1])):
            return 0
        else:
            raise Exception("Difference between # white and # black is not 1 or 0")

    def successor(self, action):
        return State(self.size, self.pieces[0], self.pieces[1],\
         self.pieces[2], self.board, self.board90, self.board45, self.board135, action, self.next_moves)

    def is_terminal(self):
        if(self.checkWinner() or len(self.pieces[2]) == 0):
            return True
        return False

    def checkHorizontal(self, coordinates):
        i = coordinates[1] - 1
        target = self.board[coordinates[0]][coordinates[1]]
        count = 1
        while(i >= 0):
            if self.board[coordinates[0]][i] == target:
                count += 1
            else: 
                break
            i -= 1
        i = coordinates[1] + 1
        while(i < self.size):
            if self.board[coordinates[0]][i] == target:
                count += 1
            else: 
                break
            i += 1
        
        return count >= 5

    def checkVertical(self, coordinates):
        j = coordinates[0] - 1
        target = self.board[coordinates[0]][coordinates[1]]
        count = 1
        while(j >= 0):
            if self.board[j][coordinates[1]] == target:
                count += 1
            else: 
                break
            j -= 1
        j = coordinates[0] + 1
        while(j < self.size):
            if self.board[j][coordinates[1]] == target:
                count += 1
            else: 
                break
            j += 1
        
        return count >= 5

    def checkDiagonal(self, coordinates):
        target = self.board[coordinates[0]][coordinates[1]]
        count = 1
        i = coordinates[0] - 1
        j = coordinates[1] - 1
        while(i >= 0 and j >= 0):
            if self.board[i][j] == target:
                count += 1
            else: 
                break
            i -= 1
            j -= 1
        
        i = coordinates[0] + 1
        j = coordinates[1] + 1
        while(i < self.size and j < self.size):
            if self.board[i][j] == target:
                count += 1
            else: 
                break
            i += 1
            j += 1
        
        if count >= 5:
            return True
        
        count = 1
        i = coordinates[0] - 1
        j = coordinates[1] + 1
        while(i >= 0 and j < self.size):
            if self.board[i][j] == target:
                count += 1
            else: 
                break
            i -= 1
            j += 1
        
        i = coordinates[0] + 1
        j = coordinates[1] - 1
        while(i < self.size and j >= 0):
            if self.board[i][j] == target:
                count += 1
            else: 
                break
            i += 1
            j -= 1

        return count >= 5
    
    def checkWinner(self):
        if self.move == None:
            return False
        check = self.checkHorizontal(self.move) or self.checkVertical(self.move) \
        or self.checkDiagonal(self.move)

        if(check):
            # The game is over and the next move is white (0, player 1), so black (1, player 2)
            # won the game which means the payoff (from player 1's POV) is -1
            if(self.actor() == 0):
                self.pay = -1
            else:
                self.pay = 1
        return check

    def payoff(self):
        return self.pay

    def get_actions(self):
        if self.start:
            return [(self.size//2, self.size//2)]  # force player to move in the center to start
        else: 
            return list(self.next_moves)

    def display(self):
        to_display = ""

        for row in self.board:
            for square in row:
                if square == 0:
                    to_display += ". "
                elif square == 1:
                    # Black stones are 1
                    to_display += "O "
                elif square == -1:
                    # White stones are -1
                    to_display += "\033[07mO\033[0m "
                else:
                    raise Exception(f"Invalid character in board: {square}")
            to_display += "\n"

        print(to_display)

    def heuristic(self):
        # Black stones = 1, White Stones = -1
        h = 0
        for board in [self.board, self.board90, self.board45, self.board135]:
            for row in board:
                if len(row) >= 5:
                    h += row_to_heur[tuple(row)]
        return h

    """
    def get_pred(self, action):
        return pHelper(self, action)
    """

    def _compute_hash(self):
        # this may have hash conflicts given that the board size is so large 3^(n^2)
        self.hash = hash(tuple([tuple(x) for x in self.board])) + self.actor()
        
    def __hash__(self):
        return self.hash

    def __eq__(self, other):
            return isinstance(other, self.__class__) and self.actor() == other.actor() and self.board == other.board

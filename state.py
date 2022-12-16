import copy

class State:
    def __init__(self, size, player0, player1, empty, board, move, potential=set(), start=False):
        self.size = size
        self.pieces = dict()
        self.pieces[0] = copy.deepcopy(player0) #player 0 pieces (white)
        self.pieces[1] = copy.deepcopy(player1) #player 1 pieces (black)
        self.pieces[2] = copy.deepcopy(empty) #empty squares //TODO: get rid of self.pieces[2] 
        self.pay = 0
        self.board = copy.deepcopy(board) #[[0] * self.size for i in range(self.size)]
        self.next_moves = copy.deepcopy(potential)
        self.move = move
        self.start = start

        if(move != None): 
            actor = self.actor()
            if(actor == 1): 
                self.board[self.move[0]][self.move[1]] = 1 # Black stones are 1
            else:
                self.board[self.move[0]][self.move[1]] = -1 # White stones are -1
            
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
         self.pieces[2], self.board, action, self.next_moves)

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

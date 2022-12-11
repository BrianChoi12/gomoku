class State:
    def __init__(self, size, player0, player1, empty, board, move):
        self.size = size
        self.pieces = dict()
        self.pieces[0] = player0 #player 0 pieces (white)
        self.pieces[1] = player1 #player 1 pieces (black)
        self.pieces[2] = empty #empty squares
        self.pay = 0
        self.board = board #[[0] * self.size for i in range(self.size)]
        
        if(move != None): 
            self.board[self.move[0]][self.move[1]] = self.actor()
            self.pieces[self.actor()].add(self.move)
            self.pieces[2].remove(self.move)
        
        self.move = move

    def actor(self):
        if(len(self.pieces[0]) > len(self.pieces[1])):
            return 1
        else:
            return 0

    def successor(self, action):
        return State(self.size, self.pieces[0], self.pieces[1], self.pieces[2], self.board, self.move)

    def is_terminal(self):
        if(self.checkWinner()):
            return True
        return False

    def checkVertical(self, coordinates):
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
        
        return count >= self.goal

    def checkHorizontal(self, coordinates):
        j = coordinates[0] - 1
        target = self.board[coordinates[0]][coordinates[1]]
        count = 1
        while(j >= 0):
            if self.board[j][coordinates[1]] == target:
                count += 1
            else: 
                break
            j -= 1
        j = coordinates[1] + 1
        while(j < self.size):
            if self.board[j][coordinates[1]] == target:
                count += 1
            else: 
                break
            j += 1
        
        return count >= self.goal

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
        
        if count >= self.goal:
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

        return count >= self.goal
    
    def checkWinner(self):
        if self.move == None:
            return False
        return self.checkHorizontal(self.move) or self.checkVertical(self.move) \
        or self.checkDiagonal(self.move)

        

    
    """def checkWinner(self):
        #copied from stack overflow: 
        # https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python

        max_col = len([0])
        max_row = len(self.board)
        cols = [[] for _ in range(max_col)]
        rows = [[] for _ in range(max_row)]
        fdiag = [[] for _ in range(max_row + max_col - 1)]
        bdiag = [[] for _ in range(len(fdiag))]
        min_bdiag = -max_row + 1

        for x in range(max_col):
            for y in range(max_row):
                cols[x].append(self.board[y][x])
                rows[y].append(self.board[y][x])
                fdiag[x+y].append(self.board[y][x])
                bdiag[x-y-min_bdiag].append(self.board[y][x])

        return self.inARow(cols) or self.inARow(rows) or self.inARow(fdiag) or self.inARow(bdiag)"""

    def payoff(self):
        return self.pay

    def get_actions(self):
        return list(self.pieces[2])
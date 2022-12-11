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

    def actor(self):
        if(len(self.pieces[0]) > len(self.pieces[1])):
            return 1
        else:
            return 0

    def successor(self, action):
        return State(self.size, self.pieces[0], self.pieces[1], self.board, self.move)

    def is_terminal(self):
        if(self.checkWinner()):
            return True
        return False

    """
    def checkFiveH(self, coord):
        if(coord[1] > self.size - 5):
            return False
        if coord in self.pieces[0]:
            target = 0
        else:
            target = 1
        for i in range(coord[1]+1,coord[1]+5):
            if (coord[0], i) not in self.pieces[target]:
                return False
        return True

    def checkFiveV(self, coord):
        if(coord[0] > self.size - 5):
            return False
        if coord in self.pieces[0]:
            target = 0
        else:
            target = 1
        for i in range(coord[0]+1,coord[0]+5):
            if (i, coord[1]) not in self.pieces[target]:
                return False
        return True   

    def checkHorVer(self):
        for i in range(self.size):
            for j in range(self.size):
                if((i,j) not in self.pieces[2]): 
                    if self.checkFiveH((i,j)) or self.checkFiveV((i,j)):
                        return True
        return False

    """

    def inARow(self, sequence):
        
        for lst in sequence: 
            if len(lst) < self.size:
                continue
            
            for i in range(len(lst)):
                target = lst[i]
                count = 1
                i += 1
                while(i < len(lst)):
                    if lst[i] == target:
                        count += 1
                    else:
                        break
                if(count > self.size): 
                    if(target == 0):
                        self.pay = 1
                    else:
                        self.pay = -1

                    return True
        return False


    def checkWinner(self):
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

        return self.inARow(cols) or self.inARow(rows) or self.inARow(fdiag) or self.inARow(bdiag)

    def payoff(self):
        return self.pay

    def get_actions(self):
        return self.pieces[2]
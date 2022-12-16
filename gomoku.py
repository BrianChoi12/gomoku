from state import State

class gomoku:
    def __init__(self, size):
        self.size = size
    
    def initial_state(self):
        board = [[0] * self.size for i in range(self.size)]

        board_diag = []
        for i in range(self.size):
            board_diag.append([0] * (i+1))
        for i in range(self.size-1):
            board_diag.append([0] * (self.size-i-1))
            
        empty = set()
        for i in range(self.size):
            for j in range(self.size):
                empty.add((i,j))
        return State(self.size, set(), set(), empty, board, board, board_diag, board_diag, None, set(), start=True)
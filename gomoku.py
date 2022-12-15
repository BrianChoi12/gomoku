from state import State

class gomoku:
    def __init__(self, size):
        self.size = size
    
    def initial_state(self):
        board = [[0] * self.size for i in range(self.size)]
        empty = set()
        for i in range(self.size):
            for j in range(self.size):
                empty.add((i,j))
        return State(self.size, set(), set(), empty, board, None, set(), start=True)
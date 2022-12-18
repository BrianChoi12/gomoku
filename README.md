# Gomoku

## Description 
We developed three agents to play Gomoku. The first agent is a baseline agent, made by Samuel Kim, that uses a simple heuristic based on possible shapes of pieces and minimax to search to a depth of 1 (after each player plays a move). The second agent, made by Stephen Yin, uses alpha-beta pruning with iterative deepening and transposition tables within an allocated time to make a move, applying the same heuristic as the previous step. The third agent, by Brian Choi, uses Monte Carlo Tree Search with rapid average value estimation to initialize node reward and visit counts.

## Basic Usage
To build the Gomoku game, run 
```
make
```
and to clean, run
```
make clean
```

The Gomoku script can be run with arguments 
```
--count #           The number of games to play (default=2) 
--time #            The time for each agent per move in seconds (default=2)
--size #            The size of the Gomoku board, where size is the side length of the square board (default=7) 
--game              Which agent you wish to play against the baseline ["mcts", "abminimax"] (default="mcts")
```
Note that there is a limit of game board size 10 because in `state.py` precomputation is only done for game boards up to size 10. Changing the `sz` variable can fix this.

## Results
The winning percentage of the alpha-beta minimax agent over the baseline agent over 100 games on an 9x9 Gomoku board with either 15 seconds per move OR when depth 2 finished searching is 61%. 

The winning percentage of the third agent over the first agent over NUM_GAMES games with N seconds to make a move is PERCENT_WIN.

## References
For the heuristic function, we based our initial weights off of [this poster](https://stanford-cs221.github.io/autumn2019-extra/posters/14.pdf). The MC-RAVE algorithm was based off of [this paper](https://www.sciencedirect.com/science/article/pii/S000437021100052X).

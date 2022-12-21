# Gomoku

## Submission
Samuel Kim (smk227), Stephen Yin (syy2), Brian Choi (bc749)

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
The winning percentage of the alpha-beta minimax agent over the baseline agent over 1000 games on an 9x9 Gomoku board with either 15 seconds per move OR when depth 2 (each player moves twice, we define it as depth 4) finished searching is 59.35%. Each player had a 10% chance of playing a random move. Note this took around 16 hours to complete, so testing on 100 games may be more reasonable. See `results.txt`. The exact command run for this test was: `./Gomoku --count=1000 --time=15 --size=9 --game=abminimax`. 

The winning percentage of the MC-rave agent over the baseline agent over 1000 games on a 9x9 with 15 seconds to make a move is 42.7%. The baseline agent had a 10% chance of playing a random move, while the MC-rave agent always chose the best move based on the UCB2 formula. See `results2.txt` and `results3.txt`. The exact command run for this test was: `./Gomoku --count=1000 --time=15 --size=9 --game=mcts`. 

## Comments on MC-rave results
Although on the surface the all moves as first heuristic seems reasonable for the game of Gomoku, in practice we found that the rapid average value estimation using the AMAF heuristic was not very effective. This is likely true for a number of reasons. Firstly, moves in Gomoku are fairly deterministic. For example, if the opponent has three of their pieces in a row and both ends are unblocked, you must place a piece blocking their streak, otherwise your opponent is guaranteed to win the game (assuming you cannot win the game in the next two moves). Therefore, the use of the minimax agent has an advantage in that it will always choose the "obvious" move in this case, whereas the random nature of the MC-rave algorithm can lead to "mistakes," which the baseline agent generally is able to capitalize on. Secondly, random playout seemed not to be a very good indicator of success, likely because of the aforementioned rules that often in Gomoku there are "obvious" moves that should be chosen. Non-random playouts were explored but were too computationally expensive for efficient tree search. To combat this, we ended up applying a similar heuristic as the baseline agent to initialize the reward and visit counts of newly expanded nodes in the game tree in an attempt to balance finding "obvious" moves with more complex strategies based on MCTS to achieve reasonable performance. 

## References
For the heuristic function, we based our initial weights off of [this poster](https://stanford-cs221.github.io/autumn2019-extra/posters/14.pdf). The MC-RAVE algorithm was based off of [this paper](https://www.sciencedirect.com/science/article/pii/S000437021100052X).

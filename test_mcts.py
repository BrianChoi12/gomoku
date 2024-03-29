import random
import sys
import mcts
import mcts_stephen
import mcts_sam
import abminimax
import argparse
import mc_rave

from gomoku import gomoku

class MCTSTestError(Exception):
    pass
        

def random_choice(position):
    moves = position.get_actions()
    return random.choice(moves)


def compare_policies(game, p1, p2, games, p1_prob, p2_prob):
    p1_wins = 0
    p2_wins = 0
    p1_score = 0

    for i in range(games):
        # start with fresh copies of the policy functions
        p1_policy = p1()
        p2_policy = p2()
        position = game.initial_state()

        while not position.is_terminal():
            if position.actor() == i % 2:
                prob = p1_prob
            else:
                prob = p2_prob
            # position.display()
            if random.random() < prob:
                if position.actor() == i % 2:
                    move = p1_policy(position)
                else:
                    move = p2_policy(position)
            else:
                move = random_choice(position)
            
            position = position.successor(move)
        
        p1_score += position.payoff() * (1 if i % 2 == 0 else -1)
        if position.payoff() == 0:
            p1_wins += 0.5
            p2_wins += 0.5
        elif (position.payoff() > 0 and i % 2 == 0) or (position.payoff() < 0 and i % 2 == 1):
            p1_wins += 1
        else:
            p2_wins += 1
        print(f"Payoff (policy 1 playing as {'White' if i % 2 == 0 else 'Black'}): {position.payoff() * (1 if i % 2 == 0 else -1)}")
        position.display()

    return p1_score / games, p1_wins / games


def test_game(game, count, p1_random, p2_random, p1_policy_fxn, p2_policy_fxn):
    ''' Tests a search policy through a series of complete games of Kalah.
        The test passes if the search wins at least the given percentage of
        games and calls its heuristic function at most the given proportion of times
        relative to Minimax.  Writes the winning percentage of the second
        policy to standard output.

        game -- a game
        count -- a positive integer
        p_random -- the probability of making a random move instead of the suggested move
        p1_policy_fxn -- a function that takes no arguments and returns
                         a function that takes a position and returns the
                       suggested move
        p2_policy_fxn -- a function that takes no arguments and returns
                         a function that takes a position and returns the
                       suggested move
                      
    '''
    margin, wins = compare_policies(game, p1_policy_fxn, p2_policy_fxn, count, 1.0 - p1_random, 1.0 - p2_random)

    print("NET: ", margin, "; WINS: ", wins, sep="")

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test MCTS agent")
    parser.add_argument('--count', dest='count', type=int, action="store", default=2, help='number of games to play (default=2)')
    parser.add_argument('--time', dest='time', type=float, action="store", default=2, help='time for MCTS per move in seconds')
    parser.add_argument('--game', dest="game", choices=["mcts", "abminimax"], default="mcts", help="game to play")
    parser.add_argument('--size', dest='size', type=int, action="store", default=7, help='size of board (default 5)')

    args = parser.parse_args()

    try:
        if args.count < 1:
            raise MCTSTestError("count must be positive")
        if args.time <= 0:
            raise MCTSTestError("time must be positive")

        game = gomoku(args.size)
        if args.game == "mcts":
            test_game(game,
                    args.count,
                    0,
                    0.1,
                    lambda: mc_rave.mcts_policy(args.time),
                    lambda: abminimax.baseline_policy(args.time))
        elif args.game == "abminimax":
            test_game(game,
                    args.count,
                    0.1, 
                    0.1,
                    lambda: abminimax.baseline_policy(args.time),
                    lambda: abminimax.abminimax_policy(args.time))
                    
        else:
            raise MCTSTestError("agent not in list")
        sys.exit(0)
    except MCTSTestError as err:
        print(sys.argv[0] + ":", str(err))
        sys.exit(1)
    

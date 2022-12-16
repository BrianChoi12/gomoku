Gomoku:
	echo "#!/bin/bash" > Gomoku
	echo "pypy3 test_mcts.py \"\$$@\"" >> Gomoku
	chmod u+x Gomoku

clean:
	rm Gomoku

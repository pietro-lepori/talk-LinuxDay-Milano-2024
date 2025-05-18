import random
from sudoku import Sudoku
from sys import argv

def new_puzzle(seed):
	board = Sudoku(3, 3, seed=seed).solve().board
	l = [(i,j) for i in range(9) for j in range(9)]
	random.shuffle(l)
	last = None
	while l:
		while True:
			if not l:
				last = None
				break
			puzzle = Sudoku(3, 3, board=board)
			if puzzle.has_multiple_solutions():
				break
			i, j = l.pop()
			last = i, j, board[i][j]
			board[i][j] = 0
		if last is not None:
			i, j, x = last
			board[i][j] = x
	return board

if __name__ == "__main__":
	n = int(argv[1])
	for k in range(n):
		board = new_puzzle(k)
		for row in board:
			s = "".join(map(str, row))
			print(s)
		print(flush=True)


from sys import argv
solver, filename = argv[1:3]

from sudoku_bool import sudoku_solve as solver_bool
from sudoku_int import sudoku_solve as solver_int
from sudoku import Sudoku
def solver_default(board):
	s = Sudoku(3, 3, board=board)
	return s.solve().board

solver = {
	"bool": solver_bool,
	"int": solver_int,
	"default": solver_default,
}[solver]

def solve(solver, table):
	table = [[x if x else None for x in row] for row in table]
	ans = solver(table)
	if ans is None: return str(ans)
	res = ("".join(str(x) for x in row) for row in ans)
	res = "\n".join(res)
	return res

with open(filename) as f:
	table = []
	for i, line in enumerate(f, 1):
		if not i%10:
			print(solve(solver, table))
			print()
			table = []
			continue
		table.append(list(map(int, line.strip())))

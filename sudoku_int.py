from z3 import *

vars = [
  [Int(f"v_{i}_{j}")
    for j in range(1,10)]
  for i in range(1,10)]

valid_range = [
  And(v > 0, v < 10)
  for row in vars
  for v in row]

valid_rows = [
  Distinct(*row)
  for row in vars]

valid_columns = [
  Distinct(*(
    row[j]
    for row in vars))
  for j in range(9)]

valid_blocks = [
  Distinct(*(
    vars[3*ii+i][3*jj+j]
    for i in range(3)
    for j in range(3)))
  for ii in range(3)
  for jj in range(3)]

s = Solver()
s.add(valid_range)
s.add(valid_rows)
s.add(valid_columns)
s.add(valid_blocks)
#s.check()

def sudoku_solve(grid):
	s.push()
	for i, row in enumerate(grid):
		for j, x in enumerate(row):
			if x is not None:
				s.add(vars[i][j] == x)
	if s.check() != sat:
		return None
	m = s.model()
	ans = []
	for row in vars:
		l = []
		ans.append(l)
		for v in row:
			x = m.evaluate(v)
			l.append(x)
	s.pop()
	return tuple(tuple(r) for r in ans)

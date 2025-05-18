from z3 import *

vars = [[[Bool(f"v_{i}_{j}_{k}")
      for k in range(1,10)]
    for j in range(1,10)]
  for i in range(1,10)]

def exactly_one(*fs):
	some = Or(*fs)
	at_most = []
	for i, f in enumerate(fs):
		x = Or(*fs[:i], *fs[i+1:])
		x = Implies(f, Not(x))
		at_most.append(x)
	return And(some, *at_most)

determine_cell = [
  exactly_one(*(
    vars[i][j][k]
    for k in range(9)))
  for i in range(9)
  for j in range(9)]

row_rule = [
  exactly_one(*(
    vars[i][j][k]
    for i in range(9)))
  for j in range(9)
  for k in range(9)]

column_rule = [
  exactly_one(*(
    vars[i][j][k]
    for j in range(9)))
  for i in range(9)
  for k in range(9)]

block_rule = [
  exactly_one(*(
    vars[3*ii+i][3*jj+j][k]
    for j in range(3)
    for i in range(3)))
  for jj in range(3)
  for ii in range(3)
  for k in range(9)]

s = Solver()
s.add(determine_cell)
s.add(row_rule)
s.add(column_rule)
s.add(block_rule)
s.check()

def sudoku_solve(grid):
	s.push()
	for i, row in enumerate(grid):
		for j, x in enumerate(row):
			if x is not None:
				s.add(vars[i][j][x-1])
	if s.check() != sat:
		return None
	m = s.model()
	ans = []
	for row in vars:
		l = []
		ans.append(l)
		for v in row:
			for k in range(9):
				if m.evaluate(v[k]):
					l.append(k+1)
					break
			else: assert False, f"{v[0]}"
	s.pop()
	return tuple(tuple(r) for r in ans)

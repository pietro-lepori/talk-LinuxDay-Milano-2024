from z3 import *

# A: ???
# B: "A said he is a knave"
# C: "B is lying"

a, b, c = Bools("A B C")
f1 = Implies(b, False)
f2 = Implies(c, Not(b))	# this is not the correct formalization... why? (hint: ex falso quodlibet)

print(solve(f1, f2))

import random

class NimState:
	def __init__(self, *args):
		self.stacks = [n for n in (int(x) for x in args) if n > 0]
	def move(self, index, n):
		stacks = self.stacks
		if not 0 < index <= len(stacks):
			return False
		index -= 1
		v = stacks[index]
		if not 0 < n <= v:
			return False
		stacks[index] = v - n
		return True
	def __bool__(self):
		return any(self.stacks)
	def __str__(self):
		return "\n".join(f"\t{i}:\t{v}" for i, v in enumerate(self.stacks, 1))
	def to_dict(self):
		return {i:v for i, v in enumerate(self.stacks, 1) if v > 0}

def random_board(max_stack=5, max_n=8):
	n = random.randint(max_stack - 2, max_stack)
	return [random.randint(1, max_n) for _ in range(n)]

def player_random(moves):
	index = random.choice(list(moves))
	v = moves[index]
	n = random.randint(1,v)
	return index, n

def player_perfect(moves):
	x = 0
	for v in moves.values():
		x ^= v
	if not x:
		index = max(moves, key=moves.get)
		n = moves[index]
#		n = 1
		return index, n
	d = x.bit_length() - 1
	index, v = next((i, v) for i, v in moves.items() if v & (1<<d))
	x ^= v
	n = v - x
	assert 0 < n <= v
	return index, n

def player_human(moves):
	index, n = map(int, input("stack and value:\t").split())
	return index, n

positions_memory = {}
# key: sorted tuple of non empty stack sizes
# value: None if key corresponds to a losing position
# value: the key corresponding to a reachable losing position
def player_tree(moves, memory=positions_memory):
	def normalize_dict(d):
		l = list(d.values())
		l.sort()
		return tuple(l)
	def children(t):
		for k in range(len(t)):
			if k and t[k] == t[k-1]:
				continue
			yield t[:k] + t[k+1:]
			for j in range(1,t[k]):
				t1 = *t[:k], j
				yield tuple(sorted(t1)) + t[k+1:]
	t = normalize_dict(moves)
	work = [(None, t, children(t))] if t not in memory else []
	while work:
		previous, t, it = work[-1]
		for t1 in it:
			if t1 not in memory:
				frame = t, t1, children(t1)
				work.append(frame)
				break
			if memory[t1] is None:
				memory[t] = t1
				work.pop()
				break
		else:
			memory[t] = None
			work.pop()
			if previous is not None:
				memory[previous] = t
				work.pop()
	t1 = memory[t]
	if t1 is None:
		index = max(moves, key=moves.get)
		n = moves[index]
#		n = 1
		return index, n
	l, l1 = len(t), len(t1)
	if l == l1 + 1:
		v1 = 0
		for x, y in zip(t, t1):
			if x != y:
				v = x
				break
		else:
			v = t[-1]
	elif l == l1:
		v, v1 = None, None
		for x, y in zip(t, t1):
			if v1 is None:
				if x != y:
					v1 = y
					v = x
			elif y == v:
				v = x
			else:
				break
	else: assert False, f"{t} - {t1}"
	assert v1 < v
	n = v - v1
	for index, x in moves.items():
		if v == x:
			return index, n
	assert False, f"{t} - {t1}, {moves = }"

def game(board, *players, verbose=True, reask=True):
	board = random_board() if board is None else board
	n_players = len(players)
	assert n_players > 0
	s = NimState(*board)
	pri = print if verbose else lambda *a, **k: None
	index_player = 0
	while True:
		index_player %= n_players
		pri(s)
		pri("Player", index_player + 1)
		if not s:
			pri("has lost!")
			pri("Game ended.")
			return index_player
		while True:
			index, n = players[index_player](s.to_dict())
			pri(f"reduced {index} by {n}")
			correct = s.move(index, n)
			if correct:
				break
			if reask:
				print("(invalid move)")
			else:
				assert False, f"{index_player=}; {(index, n) = }; {s.stacks}"
				return None
		index_player += 1

def test(max_stack=4, max_n=10, repetitions=10000):
	from itertools import product
	players = [
		("random", player_random),
		("perfect", player_perfect),
#		("search", player_tree),
	]
	for (n1, p1), (n2, p2) in product(players, repeat=2):
		print(n1, "VS", n2, end=":\t", flush=True)
		res = [0,0]
		for _ in range(repetitions):
			board = random_board(max_stack, max_n)
			loser = game(board, p1, p1, verbose=False, reask=False)
			res[1 - loser] += 1
		print(*res, sep=" - ")
	print("memorized positions:", len(positions_memory))

if __name__ == "__main__":
	from sys import argv
	args = map(int, argv[1:])
	test(*args)

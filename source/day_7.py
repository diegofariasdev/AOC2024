def read_input(test_mode):
	if test_mode:
		return [
			[190, [10, 19]],
			[3267, [81, 40, 27]],
			[83, [17, 5]],
			[156, [15, 6]],
			[7290, [6, 8, 6, 15]],
			[161011, [16, 10, 13]],
			[192, [17, 8, 14]],
			[21037, [9, 7, 18, 13]],
			[292, [11, 6, 16, 20]],
		]

	ops = []
	with open("data/data_day_7.txt") as f:
		while line := f.readline():
			t = line.split(":")
			li = [int(t[0]), [int(x) for x in t[1].split()]]
			ops.append(li)
	return ops

def operate(l, e):
	if len(l) == 2:
		if l[0] * l[1] == e: return True
		if l[0] + l[1] == e: return True
		return False
	return operate([l[0] * l[1]] + l[2:], e) or operate([l[0] + l[1]] + l[2:], e)

def cc(in1, in2):
	return int(str(in1) + str(in2))

def operate2(l, e):
	if len(l) == 2:
		if l[0] * l[1] == e: return True
		if l[0] + l[1] == e: return True
		if cc(l[0], l[1]) == e: return True
		return False
	return operate2([l[0] * l[1]] + l[2:], e) \
		or operate2([l[0] + l[1]] + l[2:], e) \
		or operate2([cc(l[0], l[1])] + l[2:], e)

def day7_1(test_mode):
	ops = read_input(test_mode)
	a = 0
	for op in ops:
		if operate(op[1], op[0]):
			a += op[0]
	print('the sum of the valid operations is {}'.format(a))

def day7_2(test_mode):
	ops = read_input(test_mode)
	a = 0
	for op in ops:
		if operate2(op[1], op[0]):
			a += op[0]
	print('the sum of the valid operations is {}'.format(a))


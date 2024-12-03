import re

mult_token_regex = r'mul\((?P<mul1>[0-9]+),(?P<mul2>[0-9]+)\)'
mult_token_regex_2 = r'(?P<do>do\(\))|(?P<dont>don\'t\(\))|(?P<mul>mul\((?P<mul1>[0-9]+),(?P<mul2>[0-9]+)\))'

def find_valid_segments(regex, memory_dump):
	segments = []
	for i in range(len(memory_dump)):
		segments += re.findall(regex, memory_dump[i])
	return segments

def read_input(test_mode):
	if test_mode:
		return ['xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))']
	else:
		content = []
		with open('data/data_day_3_1.txt') as f:
			while line := f.readline():
				content.append(line)
		return content

def read_input_2(test_mode):
	if test_mode:
		return ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]
	else:
		return read_input(False)


def day3_1(test_mode):
	memory_dump = read_input(test_mode)

	segments = find_valid_segments(mult_token_regex, memory_dump)
	sum_result = sum([int(result[0]) * int(result[1]) for result in segments])
	print('the operation result is {}'.format(sum_result))

def day3_2(test_mode):
	memory_dump = read_input_2(test_mode)
	segments = find_valid_segments(mult_token_regex_2, memory_dump)
	mul_enabled = True
	result = 0
	for segment in segments:
		if segment[0] == "do()":
			mul_enabled = True
		elif segment[1] == "don't()":
			mul_enabled = False
		elif segment[2].startswith("mul") and mul_enabled:
			result += int(segment[3]) * int(segment[4])

	print('the result is {}'.format(result))


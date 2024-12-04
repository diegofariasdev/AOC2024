def read_input(test_mode):
	if test_mode:
		return [
			'MMMSXXMASM',
			'MSAMXMSMSA',
			'AMXSXMAAMM',
			'MSAMASMSMX',
			'XMASAMXAMM',
			'XXAMMXXAMA',
			'SMSMSASXSS',
			'SAXAMASAAA',
			'MAMMMXMMMM',
			'MXMXAXMASX',
		]
	content = []
	with open('data/data_day_4_1.txt') as f:
		while line := f.readline():
			content.append(line)
	return content

def count_xmas(letter_matrix, start_row, start_col):
	counter = 0
	for row_switch in range(-1,2):
		for col_switch in range(-1,2):
			if row_switch == 0 and col_switch == 0:
				continue
			for letter, i in zip('XMAS', range(4)):
				if len(letter_matrix) <= start_row + (row_switch * i):
					break
				if start_row + (row_switch * i) < 0:
					break
				if len(letter_matrix[start_row + (row_switch * i)]) <= start_col + (col_switch * i):
					break
				if start_col + (col_switch * i) < 0:
					break
				if letter_matrix[start_row + (row_switch * i)][start_col + (col_switch * i)] != letter:
					break
			else:
				counter += 1
	return counter


def day4_1(test_mode):
	letter_matrix = read_input(test_mode)
	total_xmas = 0
	for i in range(len(letter_matrix)):
		for j in range(len(letter_matrix[i])):
			if letter_matrix[i][j] == "X":
				total_xmas += count_xmas(letter_matrix, i, j)
	print('total xmas ocurrences is {}'.format(total_xmas))

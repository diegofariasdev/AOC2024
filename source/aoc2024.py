import sys

from day_1 import day1_1, day1_2

challenges = {'11': day1_1}
challenges = {'12': day1_2}

def print_usage_and_exit():
	print('The usage of this tool is {} -c n1n2'.format(clargs[0]))
	print(' n1 between 1 and 25, that corresponds to the day of the challenge')
	print(' n2 between 1 and 2, that corresponds to the number of the challenge')
	print('example: {} -c d12 will execute challenge 2 of day 1')
	exit(1)

if __name__ == '__main__':
	clargs = sys.argv
	if (len(clargs) < 3):
		print_usage_and_exit()

	if (clargs[1] != '-c'):
		print_usage_and_exit()

	try:
		challenges[clargs[2]]()
	except KeyError:
		print('The challenge number {} of the day {} is not supported'
			.format(clargs[2][1], clargs[2][0]))
		print_usage_and_exit()
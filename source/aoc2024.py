import sys

from day_1 import day1_1, day1_2
from day_2 import day2_1, day2_2

challenges = {
	'11': day1_1,
	'12': day1_2,
	'21': day2_1,
	'22': day2_2,
}


class CliArgError(Exception):
	pass


def print_usage_and_exit(script_name):
	print('The usage of this tool is {} -c n1n2 [-t]'.format(clargs[0]))
	print(' n1 between 1 and 25, that corresponds to the day of the challenge')
	print(' n2 between 1 and 2, that corresponds to the number of the challenge')
	print(' -t indicates to use test data')
	print('example: {} -c d12 will execute challenge 2 of day 1'.format(script_name))
	exit(1)

def find_option(args, option):
	for i in range(1, len(args)):
		if args[i] == option:
			return i
	else:
		return -1

def parse_args(args):
	options_dict = {}
	expected_options = [
		{'flag':'-c','has_args':True, 'optional':False},
		{'flag':'-t','has_args':False, 'optional':True},
	]
	for expected_option in expected_options:
		option = expected_option['flag']
		index = find_option(args, option)
		if not expected_option['optional'] and index == -1:
			raise CliArgError('required option {} is missing'.format(option))
		if expected_option['has_args']:
			if len(args) - 1 == index or args[index + 1][0] == '-':
				raise CliArgError('option {} requires an argument'.format(option))
			options_dict[option] = {'option_spec':expected_option, 'value':args[index + 1]}
		elif expected_option['optional'] and index > 0:
			options_dict[option] = {'option_spec':expected_option, 'value':True}
		else:
			options_dict[option] = {'option_spec':expected_option, 'value':False}
	return options_dict

if __name__ == '__main__':
	clargs = sys.argv
	if (len(clargs) < 3):
		print_usage_and_exit(clargs[0])

	args_dict = None
	try:
		args_dict = parse_args(clargs)
	except CliArgError:
		print_usage_and_exit(clargs[0])

	try:
		print('running challenge {} {}'.format(args_dict['-c']['value'], '(test mode)' if args_dict['-t']['value'] else ''))
		challenges[args_dict['-c']['value']](args_dict['-t']['value'])
	except KeyError:
		print('The challenge number {} of the day {} is not supported'
			.format(clargs[2][1], clargs[2][0]))
		print_usage_and_exit(clargs[0])

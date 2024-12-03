def iterate_reports(func, test_mode):
	filename = "data_day_2_1.txt"
	if test_mode:
		filename = "test_" + filename
	total_safe_reports = 0
	with open("data/" + filename) as f:
		while line := f.readline():
			if func(line):
				total_safe_reports += 1
	return total_safe_reports


def evaluate_report_safety(report):
	levels = [int(level) for level in report.split(' ')]
	asc_dsc = None
	for i in range(1, len(levels)):
		if asc_dsc is None:
			if levels[i - 1] < levels[i]:
				asc_dsc = 'asc'
			else:
				asc_dsc = 'dsc'
		if asc_dsc == 'asc' and levels[i - 1] >= levels[i]:
			return False
		if asc_dsc == 'dsc' and levels[i - 1] <= levels[i]:
			return False
		if not (1 <= abs(levels[i - 1] - levels[i]) <= 3):
			return False
	return True

def day2_1(test_mode = False):
	print('total safe reports is {}'.format(iterate_reports(evaluate_report_safety, test_mode)))
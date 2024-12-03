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

def _evaluate_report_safety(levels):
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

def evaluate_report_safety_1(report):
	levels = [int(level) for level in report.split(' ')]
	return _evaluate_report_safety(levels)

def evaluate_report_safety_2(report):
	levels = [int(level) for level in report.split(' ')]
	if _evaluate_report_safety(levels):
		return True
	for i in range(0 , len(levels)):
		levels_dropped = levels.copy()
		del levels_dropped[i]
		if _evaluate_report_safety(levels_dropped):
			return True
	return False

def day2_1(test_mode = False):
	print('total safe reports is {}'.format(iterate_reports(evaluate_report_safety_1, test_mode)))

def day2_2(test_mode = False):
	print('total safe reports is {}'.format(iterate_reports(evaluate_report_safety_2, test_mode)))
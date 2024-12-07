from functools import cmp_to_key

"""
Rules to be stored in a map like structure, the key is the number at the left (greater than),
and the value is a list of the numbers at the right (lower than).

Sort input passing a comparing function that uses the map above.
"""

def read_input(test_mode):
	if test_mode:
		return [
			"47|53",
			"97|13",
			"97|61",
			"97|47",
			"75|29",
			"61|13",
			"75|53",
			"29|13",
			"97|29",
			"53|29",
			"61|53",
			"97|53",
			"61|29",
			"47|13",
			"75|47",
			"97|75",
			"47|61",
			"75|61",
			"47|29",
			"75|13",
			"53|13",
		], [
			["75","47","61","53","29"],
			["97","61","53","29","13"],
			["75","29","13"],
			["75","97","47","61","53"],
			["61","13","29"],
			["97","13","75","29","47"],
		]
	rules = list()
	updates = list()
	read_updates = False
	with open("data/data_day_5_1.txt") as f:
		while line := f.readline():
			if "" == line.strip():
				read_updates = True
				continue
			if not read_updates:
				rules.append(line.strip())
			else:
				updates.append(line.strip().split(','))
	return rules, updates


def process_rules(rules_list):
	rules_dict = {}
	for rule in rules_list:
		rule_parts = rule.split('|')
		if rule_parts[0] not in rules_dict:
			rules_dict[rule_parts[0]] = set()
		rules_dict[rule_parts[0]].add(rule_parts[1])
	return rules_dict

def is_greater_than(a,b, rules):
	if a in rules and b in rules[a]:
		return -1
	if b in rules and a in rules[b]: 
		return 1
	return 0

def day5_1(test_mode):
	rules_list, update_list = read_input(test_mode)
	rules = process_rules(rules_list)
	middle_pages_sum = 0
	for update in update_list:
		sorted_update = sorted(update, key=cmp_to_key(lambda a,b : is_greater_than(a,b,rules)))
		if sorted_update == update:
			middle_pages_sum += int(update[int(len(update)/2)])
	print("The total of the sum of the valid middle pages is {}".format(middle_pages_sum))

def day5_2(test_mode):
	rules_list, update_list = read_input(test_mode)
	rules = process_rules(rules_list)
	middle_pages_sum = 0
	for update in update_list:
		sorted_update = sorted(update, key=cmp_to_key(lambda a,b : is_greater_than(a,b,rules)))
		if sorted_update != update:
			middle_pages_sum += int(sorted_update[int(len(update)/2)])
	print("The total of the sum of the invalid middle pages is {}".format(middle_pages_sum))

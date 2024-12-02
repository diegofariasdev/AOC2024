import sys

def read_input():
	list1 = []
	list2 = []
	with open("data/data_day_1_1.txt", "r") as f:
		while line := f.readline():
			tokens = line.split("   ")
			list1.append(int(tokens[0]))
			list2.append(int(tokens[1]))

	return list1, list2

def sort_list(list):
	list.sort()
	return list

def day1_1():
	list1, list2 = read_input()
	list1 = sort_list(list1)
	list2 = sort_list(list2)
	total_dist = 0
	for i in range(len(list1)):
		dist = list1[i] - list2[i]
		dist = abs(dist)
		total_dist += dist
	print('total dist between the two lists is {}'.format(total_dist))

def day1_2():
	list1, list2 = read_input()
	similarity_score_map = {}
	similarity_score_sum = 0
	for item in list1:
		if item not in similarity_score_map:
			found_items = [item2 for item2 in list2 if item2 == item]
			similarity_score = item * len(found_items)
			similarity_score_map[item] = similarity_score
		similarity_score_sum += similarity_score_map[item]
	print ('total similarity score is {}'.format(similarity_score_sum))
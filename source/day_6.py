def read_input(test_mode):
	if test_mode:
		return [
		"....#.....",
		".........#",
		"..........",
		"..#.......",
		".......#..",
		"..........",
		".#..^.....",
		"........#.",
		"#.........",
		"......#...",
		]
	content = []
	with open("data/data_day_6_1.txt") as f:
		while line := f.readline():
			content.append(line.strip())
	return content

def parse_map(guard_map):
	blockers = []
	start_position = None
	for i in range(len(guard_map)):
		for j in range(len(guard_map[i])):
			if guard_map[i][j] == '^':
				start_position = (i, j)
			if guard_map[i][j] == "#":
				blockers.append((i, j))
	return start_position, blockers

class InvalidDirectionException(Exception):
	pass

class InvalidPointsException(Exception):
	pass

def is_blocking_guard(guard_position, blocker_position, direction):
	if direction == "up": return guard_position[0] > blocker_position[0] \
		and guard_position[1] == blocker_position[1]
	if direction == "right": return guard_position[0] == blocker_position[0] \
		and guard_position[1] < blocker_position[1]
	if direction == "down": return guard_position[0] < blocker_position[0] \
		and guard_position[1] == blocker_position[1]
	if direction == "left": return guard_position[0] == blocker_position[0] \
		and guard_position[1] > blocker_position[1]

def new_guard_position(blocker_position, direction):
	if direction == "up": return (blocker_position[0] + 1, blocker_position[1])
	if direction == "right": return (blocker_position[0], blocker_position[1] - 1)
	if direction == "down": return (blocker_position[0] - 1, blocker_position[1])
	if direction == "left": return (blocker_position[0], blocker_position[1] + 1)
	raise InvalidDirectionException()

def rotate(direction):
	if direction == "up": return "right"
	if direction == "right": return "down"
	if direction == "down": return "left"
	if direction == "left": return "up"
	raise InvalidDirectionException()

def get_step(start, end):
	return -1 if start > end else 1

def get_positions(start_position, end_position):
	if start_position[0] == end_position[0]:
		return [(start_position[0], column) for column \
			in range(start_position[1], end_position[1], get_step(start_position[1], end_position[1]))]
	if start_position[1] == start_position[1]:
		return [(row, start_position[1]) for row \
			in range(start_position[0], end_position[0], get_step(start_position[0], end_position[0]))]
	raise InvalidPointsException()

def get_closest_blocker(guard_position, blockers_positions):
	closest = blockers_positions[0]
	for blocker in blockers_positions:
		distance_to_closest = abs(guard_position[0] - closest[0]) + abs(guard_position[1] - closest[1])
		distance_to_blocker = abs(guard_position[0] - blocker[0]) + abs(guard_position[1] - blocker[1])
		if distance_to_blocker < distance_to_closest:
			closest = blocker
	return closest

def get_edge_position(start_position, max_row, max_col, direction):
	if direction == "up": return (-1, start_position[1])
	if direction == "right":  return (start_position[0], max_col)
	if direction == "down": return (max_row, start_position[1])
	if direction == "left": return (start_position[0], -1)
	raise InvalidDirectionException()

"""
Step 1. Read-through the matrix to find blockers positions, and guard position
Step 2. Store blockers positions in a set
Step 3. Set direction as "up"
Step 4. Taking (row,col) of the guard, search for a blocker in the indicated direction,
for "up" search in all rows < guard row, and all cols = guard col
(-1, 0)
for "right" search in row = guard row, and cols > guard col
(0, 1)
for "down" search in all rows > guard row, and cols = guard col
(1, 0)
for "left" search in row = guard row, and cols < guard col
(0, -1)
Step 5. If a blocker is found, add up the difference between guard position and blocker position
to the total distance.
Step 6. Reposition the guard and change the direction 90°
Step 7. If no blocker is found, add up the difference between guard position and the edge of the map
"""
def day6_1(test_mode):
	guard_map = read_input(test_mode)
	guard_position, blockers_positions = parse_map(guard_map)
	direction = "up"
	unique_positions = set()
	for i in range(len(guard_map) * len(guard_map[0])): # setting a max of iterations
		found_blockers = [blocker for blocker in blockers_positions \
			if is_blocking_guard(guard_position, blocker, direction)]
		if found_blockers:
			found_blocker = get_closest_blocker(guard_position, found_blockers)
			unique_positions.update(get_positions(guard_position, found_blocker))
			guard_position = new_guard_position(found_blocker, direction)
			direction = rotate(direction)
		else:
			unique_positions.update(get_positions(guard_position, \
				get_edge_position(guard_position, len(guard_map), len(guard_map[0]), direction)))
			break
	print("The sum of unique positions is {}".format(len(unique_positions)))

def calculate_seg_lenght(end1, end2):
	return abs(end2[0] - end1[0]) + abs(end2[1] - end1[1])

def is_point_on_line(end1, end2, point):
	return (end2[0] - end1[0]) * (point[1] - end1[1]) ==\
		(end2[1] - end1[1]) * (point[0] - end1[0])

"""
idea: a new blocker can create a loop if the third path segment is longer than the first one,
and the guard was not in the third segment.
A window can be created to store three segments at a time, and stepping one by one, 
in each step it should validate that the third segment is longer than the first one, and that
the guard was not in the third segment initially, and if those two conditions are true, we can
add 1 to the sum of places where a new blocker can be put to create a loop
guard pos: (gr, gc)
window: [((r1,c1),(r2,c2),(r3,c3),(r4,c4))]
first segment long = abs(r1 - r2) + abs(c1 - c2)
third segment long = abs(r3 - r4) + abs(c3 - c4)
guard is in a segment? (r4 - r3) * (gc - c3) == (c4 - c3) * (gr - r3)
"""
def day6_2(test_mode):
	guard_map = read_input(test_mode)
	guard_position, blockers_positions = parse_map(guard_map)
	initial_guard_position = guard_position
	direction = "up"
	evaluating_window = [initial_guard_position]
	total_valid_blockers = 0
	for i in range(len(guard_map) * len(guard_map[0])): # setting a max of iterations
		found_blockers = [blocker for blocker in blockers_positions \
			if is_blocking_guard(guard_position, blocker, direction)]
		if found_blockers:
			found_blocker = get_closest_blocker(guard_position, found_blockers)
			guard_position = new_guard_position(found_blocker, direction)

			if len(evaluating_window) < 4:
				evaluating_window.append(guard_position)
			if len(evaluating_window) == 4:
				first_seg_len = calculate_seg_lenght(evaluating_window[0], evaluating_window[1])
				third_seg_len = calculate_seg_lenght(evaluating_window[2], evaluating_window[3])
				if first_seg_len >= third_seg_len and \
					not is_point_on_line(evaluating_window[2], evaluating_window[3], initial_guard_position):
					print("blocker on {} {}".format(evaluating_window[2], evaluating_window[3]))
					total_valid_blockers += 1
				evaluating_window.pop(0)

			direction = rotate(direction)
		else:
			#unique_positions.update(get_positions(guard_position, \
				#get_edge_position(guard_position, len(guard_map), len(guard_map[0]), direction)))
			break
	print("The total of possible blockers is {}".format(total_valid_blockers))

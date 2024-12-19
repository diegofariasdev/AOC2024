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

"""
Segment by segment evaluation
Steps: take current positon, and the closest blocker, for each position in between them
if no previous blocker has been added, add a blocker, and evaluate if a loop is made.
if a loop occurs, add 1.

to evaluate a loop, while blocker ahead, or edge ahead, if the blocker ahead has been
hitted in the same direction in the past, it must be a loop. if not move forward until
after the most closest blocker, and turn 90 degres to the right.
if out of the while, return false as no loop has been found
"""
def is_blocker_hit_already(hit_blockers, blocker, direction):
	return blocker in hit_blockers and direction in hit_blockers[blocker]

def does_guard_loops(map_widht, map_height, blockers_positions, guard_position):
	direction = "up"
	hit_blockers = {}
	for i in range(map_widht * map_height): # setting a max of iterations
		found_blockers = [blocker for blocker in blockers_positions \
			if is_blocking_guard(guard_position, blocker, direction)]
		if found_blockers:
			found_blocker = get_closest_blocker(guard_position, found_blockers)

			if is_blocker_hit_already(hit_blockers, found_blocker, direction):
				print('loop found!!!')
				return True
			if found_blocker not in hit_blockers:
				hit_blockers[found_blocker] = set()
			if direction not in hit_blockers[found_blocker]:
				hit_blockers[found_blocker].add(direction)

			guard_position = new_guard_position(found_blocker, direction)
			direction = rotate(direction)
		else:
			return False

def day6_2(test_mode):
	guard_map = read_input(test_mode)
	guard_position, blockers_positions = parse_map(guard_map)
	initial_guard_position = guard_position
	direction = "up"
	map_widht = len(guard_map)
	map_height = len(guard_map[0])
	looping_blockers = set()
	for i in range(map_widht * map_height): # setting a max of iterations
		found_blockers = [blocker for blocker in blockers_positions \
			if is_blocking_guard(guard_position, blocker, direction)]
		if found_blockers:
			found_blocker = get_closest_blocker(guard_position, found_blockers)
			for position in get_positions(guard_position, found_blocker):
				new_blockers_position = blockers_positions + [position]
				if does_guard_loops(map_widht, map_height, new_blockers_position, initial_guard_position):
					looping_blockers.add(position)
					print('A new blocker in {} loops the guard'.format(position))
			guard_position = new_guard_position(found_blocker, direction)
			direction = rotate(direction)
		else:
			edge_position = get_edge_position(guard_position, map_widht + 1, map_height + 1, direction)
			for position in get_positions(guard_position, edge_position):
				new_blockers_position = blockers_positions + [position]
				if does_guard_loops(map_widht, map_height, new_blockers_position, initial_guard_position):
					looping_blockers.add(position)
					print('A new blocker in {} loops the guard'.format(position))
			break
			looping_blockers.delete(initial_guard_position)
	print('The total number of looping blockers is {}'.format(len(looping_blockers)))

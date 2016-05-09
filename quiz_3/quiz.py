# Question 1
# --------
def get_popular_edge(graph, paths):
	# Dictionary maps tuples start/end points to counter
	edge_count = {}
	# Count paths
	for path in paths:
		if path_valid(path, graph):
			for city_i in range(len(path)):
				# not end of path, so keep going
				if city_i < len(path) - 1:
					if (path[city_i], path[city_i + 1]) in edge_count:
						edge_count[(path[city_i], path[city_i + 1])] += 1
					else:
						edge_count[(path[city_i], path[city_i + 1])] = 1
	# Sort to get most congested a return tuple
	max_edge = ()
	max_count = 0
	for edge, count in edge_count.iteritems():
		if count >= max_count:
			max_count = count
			max_edge = edge

	# print edge_count
	return max_edge


def city_valid(city, graph):
	if city in graph:
		return True
	else:
		return False

def path_valid(path, graph):
	# go through each city in path
	for city_i in range(len(path)):

		# get the city destinations
		destinations = graph[path[city_i]]
		# check if next city in path is in destinations, if there is a next city
		if city_i < len(path):
			if path[city_i + 1] in destinations:
				return True
			else:
				return False
		elif path[city_i] not in destinations:
			return False


# Question 2
# ---------
possible_boards = []
def can_ben_lose( board, benTurn ):
	global final_boards

	generate_boards(board, benTurn)
	for b in final_boards:
		if ben_lose(b):
			return True

	return False



# Complete boards
final_boards = []
# Generate all possible remaining boards
def generate_boards(board, benTurn):
	global final_boards

	if benTurn:
		fill = 0
	else:
		fill = 1

	# news boards for next round
	new_boards = []
	# counter to see if any spots unfilled
	count = 0
	# possible next boards
	for r in range(len(board)):
		for c in range(len(board)):
			# unfilled spot in board
			if board[r][c] == -1:
				next_board = board[:]
				next_board[r][c] = fill
				new_boards.append(next_board)
			# spot filled
			else:
				count += 1

	if count == 9:
		final_boards.append(board)
		return True
	else:
		# recurse on all new boards
		for b in new_boards:
			generate_boards(b, not benTurn)


# Check if board is a ben winner
def ben_lose(board):
	# check rows
	for row_i in range(len(board)):
		row = board[row_i]
		if row == [1, 1, 1]:
			return True
	# check columns
	for column_i in range(len(board)):
		count = 0
		if board[0][column_i] == 1 and board[1][column_i] == 1 and board[2][column_i] == 1: 
			return True
	# Check diagonals
	if board[1][1] == 0:
		if board[0][0] == 1 and board[2][2] == 1:
			return True
		elif board[2][0] == 1 and board[0][2] == 1:
			return True

	# Otherwise it is not a winning board for ben
	return False



# Question 3
# ---------
def earliest_meeting(building, day_of_week, default_db, update_db):
	default_db = add_to_db(default_db, update_db)

	min_meeting = []
	min_time = 20
	for meeting in default_db:
		time = int(meeting[1])
		day = meeting[2]
		check_building = meeting[3]
		if time < min_time:
			if day_of_week == day:
				if building == check_building:
					min_time = time
					min_meeting = meeting

	if len(min_meeting) == 0:
		return None
	else:
		return min_meeting


def add_to_db(default_db, update_db):
	for command in update_db:
		if command[0] == "ADD":
			default_db.append(command[1:])

	return default_db













def find_shortest_path(graph, start, end, twisty):
	# Remember to return a list of edges as defined in README
	# i.e.: [{"start":[x1,y1], "end":[x2,y2]}, {"start":[x2,y2], "end":[x3,y3]}]
	def find_shortest_path(graph, start, end, path=[]):
		path = path + [start]
		if start == end:
			return path
		if not graph.has_key(start):
			return None
		shortest = None
		for node in graph[start]:
			if node not in path:
				newpath = find_shortest_path(graph, node, end, path)
				if newpath:
					if not shortest or len(newpath) < len(shortest):
						shortest = newpath
		return shortest

	a = find_shortest_path(graph, start, end, [])
	print a
	return a
	#return []

def vector(start, end):
	return (end[0] - start[0], end[1] - start[1])

def cross_product(d1, d2):
	return d1[0]*d2[1] - d1[1]*d2[0]

def dot_product(d1, d2):
	return d1[0]*d2[0] + d1[1]*d2[1]

# Never allowed to do
def uturn(d1, d2):
	if cross_product(d1, d2) == 0 and dot_product(d1, d2) < 0:
		return True
	else:
		return False

def straight(d1, d2):
	if cross_product(d1, d2) == 0 and dot_product(d1, d2) > 0:
		return True
	else:
		return False

def left(d1, d2):
	if cross_product(d1, d2) < 0:
		return True
	else:
		return False

def right(d1, d2):
	if cross_product(d1, d2) > 0:
		return True
	else:
		return False




## BONUS
def find_shortest_path_bonus(graph, start, end, num_left_turns):
	# Remember to return a list of edges as defined in README
	# i.e.: [{"start":[x1,y1], "end":[x2,y2]}, {"start":[x2,y2], "end":[x3,y3]}]
	return []

from datetime import datetime

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
	for film_tuple in data:
		if film_tuple[0] == actor_id_1 and film_tuple[1] == actor_id_2:
			return True
		elif film_tuple[1] == actor_id_1 and film_tuple[0] == actor_id_2:
			return True
	return False


# def get_actors_with_bacon_number(data, n):

# 	def get_relations(actors):
# 		relations = []
# 		for actor in actors:
# 			for film_tuple in data:
# 				if film_tuple[0] == actor:
# 					relations.append(film_tuple[1])
# 				elif film_tuple[1] == actor:
# 					relations.append(film_tuple[0])
# 		return relations

# 	# Only Kevin Bacon at First
# 	relations = [[4724]]
# 	# Go N levels deep
# 	for depth in range(n):
# 		relations.append(get_relations(relations[depth]))

# 	for n_state in range(len(relations)):
# 		duplicates_removed = list(set(relations[n_state]))
# 		relations[n_state] = duplicates_removed


# 	# Remove everyone in lower levels that is duplicated
# 	for depth in range(n):
# 		for earlier_connection in relations[depth]:
# 			if earlier_connection in relations[n]:
# 				relations[n].remove(earlier_connection)

# 	# Sort ascending order
# 	nth_degree_relations = list(set(relations[n]))
# 	nth_degree_relations.sort()

# 	return nth_degree_relations

def people_by_bacon_number(relationships, bacon_dic, actor_dic, n, m, previous_set):
	if m == n:
		return [bacon_dic, actor_dic]
	else:
		for bacon_child in bacon_dic[m]:
			for child in relationships[bacon_child]:
				if not child in previous_set:
					bacon_dic.setdefault(m+1, set([])).update([child])
					actor_dic[child] = m+1
					previous_set.update([child])
		m += 1
		return people_by_bacon_number(relationships, bacon_dic, actor_dic, n, m, previous_set)

def get_actors_with_bacon_number_up_to(data, n):
	relationships = build_relationship_dictionary(data)
	return people_by_bacon_number(relationships, {0:set([4724])}, {4724:1}, n, 0, set([4724]))
	

def get_actors_with_bacon_number(data, n):
	people_of_n_bacon_number = list(get_actors_with_bacon_number_up_to(data, n)[0][n])
	people_of_n_bacon_number.sort()
	return people_of_n_bacon_number

def build_relationship_dictionary(data):
	relationships = {}
	
	# Build all relationships
	for film_tuple in data:
		relationships.setdefault(film_tuple[0], []).append(film_tuple[1])
		# relationships.setdefault(film_tuple[1], []).append(film_tuple[0])

	# Remove Duplicates and Parents
	for actor_id in relationships:
		# remove duplicates
		relationships[actor_id] = list(set(relationships[actor_id]))
		# remove parent if present
		if actor_id in relationships[actor_id]:
			relationships[actor_id].remove(actor_id)

	# remember multi-step loops may still exist, ex. a -> b -> c -> a
	return relationships


def bfs(data, actor_id):
	relationships = build_relationship_dictionary(data)
	bacon_magic = people_by_bacon_number(relationships, {0:set([4724])}, {4724:1}, 4, 0, set([4724]))
	bacon_to_actors = bacon_magic[0]
	actor_to_bacon = bacon_magic[1]

	# No solution case
	if not actor_id in actor_to_bacon:
		return None

	actor_depth = actor_to_bacon[actor_id]

	queue = []
	# Start search from back (turns out to be faster, less initial connections)
	queue.append([actor_id]) 

	# Search until queue is empty
	# n = 1
	# m = 1
	while queue:
		# a = datetime.now()
		path = queue.pop(0)
		# # if path runs over itself, remove/pop a new one
		# while len(set(path)) < len(path):
		# 	print 'ding'
		# 	path = queue.pop(0)

		node = path[-1]
		# print node
		# print relationships.get(node, [])

		# Finally found kevin bacon!
		if node == 4724:
			path.reverse()
			print path
			return path

		# print 'big loop'
		# m += 1
		# print m
		# b = datetime.now()
		#new_path = path[:]
		for child in relationships.get(node, []):
			# if bacon_to_actors
			new_path = path[:]
			# n+=1
			# print 'lil loop'
			# print n
			# print new_path
			# Stop circular paths
			# if not child in new_path:
			new_path.append(child)
			if len(set(new_path)) == len(new_path):
				queue.append(new_path)
			#new_path.pop(-1)

		# print datetime.now() - b
		# print datetime.now() - a


def get_bacon_path(data, actor_id):
	return bfs(data, actor_id)















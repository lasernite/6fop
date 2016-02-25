def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
	for film_tuple in data:
		if film_tuple[0] == actor_id_1 and film_tuple[1] == actor_id_2:
			return True
		elif film_tuple[1] == actor_id_1 and film_tuple[0] == actor_id_2:
			return True
	return False


def get_actors_with_bacon_number(data, n):

	def get_relations(actors):
		relations = []
		for actor in actors:
			for film_tuple in data:
				if film_tuple[0] == actor:
					relations.append(film_tuple[1])
				elif film_tuple[1] == actor:
					relations.append(film_tuple[0])
		return relations

	# Only Kevin Bacon at First
	relations = [[4724]]
	# Go N levels deep
	for depth in range(n):
		relations.append(get_relations(relations[depth]))

	for n_state in range(len(relations)):
		duplicates_removed = list(set(relations[n_state]))
		relations[n_state] = duplicates_removed


	# Remove everyone in lower levels that is duplicated
	for depth in range(n):
		for earlier_connection in relations[depth]:
			if earlier_connection in relations[n]:
				relations[n].remove(earlier_connection)

	# Sort ascending order
	nth_degree_relations = list(set(relations[n]))
	nth_degree_relations.sort()

	return nth_degree_relations


def build_relationship_dictionary(data):
	relationships = {}

	# Build all relationships
	for film_tuple in data:
		if film_tuple[0] in relationships.keys():
			relationships[film_tuple[0]] += [film_tuple[1]]
		else:
			relationships[film_tuple[0]] = [film_tuple[1]]

		if film_tuple[1] in relationships.keys():
			relationships[film_tuple[1]] += [film_tuple[0]]
		else:
			relationships[film_tuple[1]] = [film_tuple[0]]

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

	queue = []
	# Append Kevin Bacon Start
	queue.append([4724]) 

	# Search until queue is empty
	while queue:
		path = queue.pop(0)
		node = path[-1]

		if node == actor_id:
			return path

		for children in relationships.get(node, []):
			new_path = path[:]
			new_path.append(children)
			queue.append(new_path)


def get_bacon_path(data, actor_id):
	print bfs(data, actor_id)
	


	
	return bfs(data, actor_id)















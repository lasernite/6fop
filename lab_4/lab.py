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


def get_bacon_path(data, actor_id):
    raise ValueError("Implement me!")
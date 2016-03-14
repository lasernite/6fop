# Problem 1
# ---------
def second_largest( A ):
	A.sort()
	return A[-2]

# Problem 2
# ---------
def run_length_encode( S ):
	encoded = ""

	S_list = [letter for letter in S]

	counter = 1
	for letter_i in range(1,len(S)):
		if S_list[letter_i] == S_list[letter_i - 1]:
			counter += 1
		else:
			addendum = S_list[letter_i - 1] + str(counter)
			encoded += addendum
			counter = 1

	# Last letter condition
	if not len(S) == 0:
		addendum = S_list[-1] + str(counter)
		encoded += addendum

	return encoded

# Problem 3
# ---------
def histogram( A, low, high, n ):
	h_range = high - low
	h_interval = h_range / n

	buckets = [0 for i in range(n)]

	for num in A:
		# ignore numbers higher and lower
		if not (num < low or num > high):
			# generate num index and add 1 to appropriate bucket
			num_index = (num - low)/h_interval
			buckets[num_index] += 1

	return buckets

# Problem 4
# ---------
def knight_in_two_moves( A, B ):
	# generate all 2 state transitions from A and check presence of B

	def next_possible_states(current_states):
		new_states = []
		for state in current_states:
			for change1 in [2, -2]:
				for change2 in [1, -1]:
					# append both combinations, 8 possible states for each state
					x1 = state[0] + change1
					y1 = state[1] + change2
					if not (x1 > 7 or x1 < 0) and not (y1 > 7 or y1 < 0):
						new_states.append([x1, y1])

					x2 = state[0] + change2
					y2 = state[1] + change1
					if not (x2 > 7 or x2 < 0) and not (y2 > 7 or y2 < 0):
						new_states.append([x2, y2])

		return new_states

	first_states = next_possible_states([A])
	second_states = next_possible_states(first_states)

	return (B in second_states)




































# Problem 1
# ---------
def median( A ):
	asort = A[:]
	asort.sort()

	length = len(asort)

	# if odd, take middle number
	if length % 2 == 1:
		return asort[length/2]
	# average middle two if even
	else:
		return (float(asort[length/2]) + float(asort[(length/2)-1]))/2


# Problem 2
# ---------
def is_quasidrome( s ):

	def reverse_s(thestring):
		return [thestring[i] for i in range(len(thestring)-1,-1,-1)]

	def make_list(thestring):
		return [thestring[i] for i in range(len(thestring))]

	# check if palindrome
	if reverse_s(s) == make_list(s):
		return True

	# check if palindrome after removing one element
	for i in range(len(s)):
		string_list = make_list(s)
		del string_list[i]
		preserved = string_list[:]
		string_list.reverse()
		if preserved == string_list:
			return True

	# nothing checked out
	return False



# Problem 3
# ---------
def is_permutation( A, B ):

	adic = {}
	for letter in A:
		if letter in adic:
			adic[letter] += 1
		else:
			adic[letter] = 1

	bdic = {}
	for letter in B:
		if letter in bdic:
			bdic[letter] += 1
		else:
			bdic[letter] = 1

	return adic == bdic



# Problem 4
# ---------
def count_triangles( edges ):

	triangle_counter = 0
	for edge1 in edges:
		edge1_left_matches = []
		edge1_right_matches = []
		for edge2 in edges:
			# Get left and right matches
			if edge1[0] == edge2[0]:
				# ignore self
				if not edge1[1] == edge2[1]:
					edge1_left_matches.append(edge2)
			if edge1[1] == edge2[1]:
				# ignore self
				if not edge1[0] == edge2[0]:
					edge1_right_matches.append(edge2)

		# check if edge1's matches match
		for edge0 in edge1_left_matches:
			for edge1 in edge1_right_matches:
				if edge0[1] == edge1[0]:
					triangle_counter += 1

	return triangle_counter


			











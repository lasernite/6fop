# Problem 1
# ---------
def remove_first_repeated( A ):
	if A == list(set(A)):
		return A
	else:
		for x in range(len(A)):
			if A[x] in A[0:x]:
				del A[x]
				return A

# Problem 2
# ---------
def cherrypick( A, n, required_sum ):

	# edge cases
	if len(A) == n:
		if sum(A) == required_sum:
			return True
		else:
			return False

	if len(A) - 1 == n:
		for num in A:
			B = A[:]
			B.remove(num)
			if sum(B) == required_sum:
				return True
		return False

	# recursive solution
	C = A[:]
	for first_current in C:
		solution = recurse(C,n,required_sum,[],first_current,set())
		if solution[0] == True:
			return True
	
	return False


# cherrypick recursion helper
def recurse(A,n,required_sum,elements,current,searched):
	# recursion depth should stop once n elements have been selected
	if len(elements) == n:
		# if it's the right value, return True
		if sum(elements) == required_sum:
			return True, elements
		# otherwise 
		else:
			#print 'dog'
			#print elements
			return False, elements
	elif len(A) == 0:
		# exhausted 
		#print 'cat'
		return False
	# otherwise remove current keep recursing on all remaining
	else:
		B = A[:]
		# add current to elements searched
		new_elements = elements[:]
		new_elements.append(current)
		# remove term now being searched from possibilities
		B.remove(current)

		# if set(new_elements) in searched:
		# 	print 'catdog'
		# 	return False, elements
		# else:
			#recurse all remaining
		for new_current in B:
			# update search history to prune
			# print new_elements
			# print searched
			# searched.update((new_elements))
			# print searched
			#print searched

			a = recurse(B,n,required_sum,new_elements,new_current,searched)
			# some depth returned true
			if a[0] == True:
				return True, elements
			# no recursion returned true
			#print 'horse'
			#print elements
		return False, elements








# Problem 3
# ---------
def eval_ast( ast ):
	# edge case
	if type(ast['node']) == int:
		return ast['node']

	a = eval_ast(ast['left'])
	b = eval_ast(ast['right'])

	# both are integers, compute operation
	if type(ast['left']) == int and type(ast['right']) == int:
		if ast['node'] == '+':
			return ast['left'] + ast['right']
		elif ast['node'] == '*':
			return ast['left'] * ast['right']
	# one if integer
	elif type(ast['left']) == int:
		if ast['node'] == '+':
			return ast['left'] + eval_ast(ast['right'])
		elif ast['node'] == '*':
			return ast['left'] * eval_ast(ast['right'])
	# other is integer
	elif type(ast['right']) == int:
		if ast['node'] == '+':
			return eval_ast(ast['left']) + ast['right']
		elif ast['node'] == '*':
			return eval_ast(ast['left']) * ast['right']
	# neither is integer
	else: 
		if ast['node'] == '+':
			return eval_ast(ast['left']) + eval_ast(ast['right'])
		elif ast['node'] == '*':
			return eval_ast(ast['left']) * eval_ast(ast['right'])

	































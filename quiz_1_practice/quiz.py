# Problem 1
# ---------
def is_unique( A ):
    if len(set(A)) < len(A):
    	return False
    else:
    	return True

# Problem 2
# ---------
def matrix_product( A, B, m, n, k ):
	# First turn A and B into lists of rows and columns
	A_rows = []
	for row_number in range(m):
		start_row = n*row_number
		end_row = n*(row_number+1)
		row = A[start_row:end_row]
		A_rows.append(row)

	B_columns = []
	for column_number in range(k):
		column = []
		for row_number in range(n):
			element = B[row_number*k+column_number]
			column.append(element)
		B_columns.append(column)

	# Do matrix multiplication
	mproduct = []
	for row in A_rows:
		for column in B_columns:
			element = 0
			for i in range(n):
				element += row[i] * column[i]
			mproduct.append(element)

	return mproduct




# Problem 3
# ---------
def mode( A ):

	# Make dictionary of number of occurences of each number
	occurences = {}
	for value in A:
		if value in occurences:
			occurences[value] += 1
		else:
			occurences[value] = 1

	# Get max number of occurences
	mode_count = max(occurences.values())

	modes = []
	for okey in occurences:
		if occurences[okey] == mode_count:
			modes.append(okey)

	modes_keys = []

	for mode in modes:
		modes_keys.append(A.index(mode))

	return A[min(modes_keys)]



# Problem 4
# ---------
def transpose( A, m, n ):
	new_matrix = []
	# Width
	for column in range(n):
		# Height
		for row in range(m):
			new_matrix.append(A[column+(row*n)])

	return new_matrix












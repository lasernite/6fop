# Problem 1
# ---------
def check_valid_paren(s):
	counter = 0
	for l in s:
		if l == ")":
			counter -= 1
		elif l == "(":
			counter += 1

		if counter < 0:
			return False

	if counter == 0:
		return True
	else:
		return False

# Problem 2
# ---------
def get_all_elements(root):
	ls = []
	# Recursive function
	def elements(root):
		ls.append(root['value'])
		if root['right'] == None and root['left'] == None:
			return True
		elif root['right'] and root['left']:
			elements(root['right'])
			elements(root['left'])
		elif root['right']:
			elements(root['right'])
		elif root['left']:
			elements(root['left'])
		else:
			return False

	elements(root)

	return ls
			


# Problem 3
# ---------
def solve_magicsquare_recursive(grid, magic_sum, choices):





def is_valid(grid):





























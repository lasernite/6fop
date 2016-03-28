# "Find an empty square using some fixed order. Say going on the top row, 
# then the next to top row, etc.  Check if you can place the sleeping bag 
# horizontally with its anchor on the empty square. (The anchor is the left of the bag, 
# 	or the top of the bag.) If you can, recurse.  If not, try to place it vertically.  
# If you can, recurse.  If either recursion returns true, return true, i.e., the solution.  
# If neither works, return False.

def pack(tentSize, missingSquares):
    # Take care to return a list of dictionaries with keys:
    #  "anchor": [x,y]
    #  "orientation": 0/1
    sleepers = []
    stored = recurse_pack(tentSize, missingSquares, sleepers, [0,0])
    print stored
    return stored


def recurse_pack(tentSize, missingSquares, sleepers, currentSquare):
	# if all squares have rocks or sleepers, horray it worked, return sleepers!
	# print 'MissingSquares and tentSize and sleepers'
	# print len(missingSquares)
	# print tentSize[0]*tentSize[1]
	# print sleepers
	if len(missingSquares) == tentSize[0]*tentSize[1]:
		return sleepers

	
	valid_h = is_valid(tentSize, missingSquares, 0, currentSquare)
	valid_v = is_valid(tentSize, missingSquares, 1, currentSquare)
	# False if neither can be placed
	if not valid_h and not valid_v:
		return False

	# horizontal test
	if valid_h: 
		# add sleeper to sleepers
		new_sleepers = sleepers[:]
		new_sleepers.append({"anchor":currentSquare, "orientation": 0})
		# Append new horizontal sleeper squares to missing
		newMissingSquares = missingSquares[:]
		newMissingSquares.append([currentSquare[0],currentSquare[1]])
		newMissingSquares.append([currentSquare[0]+1,currentSquare[1]])
		newMissingSquares.append([currentSquare[0]+2,currentSquare[1]])
		# Move three spaces forward while adding spaces to MissingSquares
		new_square = next_square(tentSize, currentSquare)
		new_square2 = next_square(tentSize, new_square)
		new_square3 = next_square(tentSize, new_square2) 
		# recurse again to fill the next spot
		recurse_pack(tentSize, newMissingSquares, new_sleepers, new_square3)

	# vertical test
	if valid_v:
		# add sleeper to sleepers
		new_sleepers = sleepers[:]
		new_sleepers.append({"anchor":currentSquare, "orientation": 1})
		# Append new vertical sleeper squares to missing
		newMissingSquares = missingSquares[:]
		newMissingSquares.append([currentSquare[0],currentSquare[1]])
		newMissingSquares.append([currentSquare[0],currentSquare[1]+1])
		newMissingSquares.append([currentSquare[0],currentSquare[1]+2])
		# Move three spaces forward
		new_square = next_square(tentSize, currentSquare)
		new_square2 = next_square(tentSize, new_square)
		new_square3 = next_square(tentSize, new_square2) 
		# recurse again to fill the next spot
		recurse_pack(tentSize, newMissingSquares, new_sleepers, new_square3)

	return False


def is_valid(tentSize, missingSquares, orientation, currentSquare):
	# calculate sleeping bag spaces
	# horizontal
	if orientation == 0:
		bed = [[currentSquare[0], currentSquare[1]],
					[currentSquare[0]+1, currentSquare[1]],
					[currentSquare[0]+2, currentSquare[1]]]
	# vertical
	elif orientation == 1:
		bed = [[currentSquare[0], currentSquare[1]],
					[currentSquare[0], currentSquare[1]+1],
					[currentSquare[0], currentSquare[1]+2]]

	# Check all bed spaces to ensure validity
	for space in bed:
		# If a rock or person return false
		if space in missingSquares:
			return False
		# Elif out of bounds return false
		elif (space[0] < 0) or (space[0] >= tentSize[0]) or (space[1] < 0) or (space[1] >= tentSize[1]):
			return False 

	# All checks passed
	return True


def next_square(tentSize, currentSquare):

	if currentSquare[0] + 1 < tentSize[0]:
		next_square = [currentSquare[0] + 1, currentSquare[1]]
	else:
		next_square = [currentSquare[0], currentSquare[1] + 1]

	return next_square















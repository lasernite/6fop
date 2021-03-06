# "Find an empty square using some fixed order. Say going on the top row, 
# then the next to top row, etc.  Check if you can place the sleeping bag 
# horizontally with its anchor on the empty square. (The anchor is the left of the bag, 
# 	or the top of the bag.) If you can, recurse.  If not, try to place it vertically.  
# If you can, recurse.  If either recursion returns true, return true, i.e., the solution.  
# If neither works, return False.

from datetime import datetime

def pack(tentSize, missingSquares):
    # Take care to return a list of dictionaries with keys:
    #  "anchor": [x,y]
    #  "orientation": 0/1
    sleepers = []
    result = recurse_pack(tentSize, missingSquares, sleepers, [0,0])
    if result[0]:
    	return result[1]
    else:
    	return False


def recurse_pack(tentSize, missingSquares, sleepers, currentSquare):
	# if all squares have rocks or sleepers, horray it worked, return sleepers!
	if len(missingSquares) == tentSize[0]*tentSize[1]:
		return True, sleepers

	
	valid_h = is_valid(tentSize, missingSquares, 0, currentSquare)
	valid_v = is_valid(tentSize, missingSquares, 1, currentSquare)
	# False if neither can be placed
	if not valid_h and not valid_v:
		return False, sleepers

	# a = datetime.now()
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
		new_square = next_square(tentSize, currentSquare, newMissingSquares) 
		# recurse again to fill the next spot
		h = recurse_pack(tentSize, newMissingSquares, new_sleepers, new_square)

		if h[0]:
			return True, h[1]
	# if (datetime.now() - a).microseconds > 100000:
	# 	print datetime.now() - a
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
		# Move one spaces forward
		new_square = next_square(tentSize, currentSquare, newMissingSquares)
		# recurse again to fill the next spot
		v = recurse_pack(tentSize, newMissingSquares, new_sleepers, new_square)

		if v[0]:
			return True, v[1]

	return False, sleepers


def is_valid(tentSize, missingSquares, orientation, currentSquare):
	# calculate sleeping bag spaces
	# horizontal
	if orientation == 0:
		bed = [[currentSquare[0], currentSquare[1]], [currentSquare[0]+1, currentSquare[1]], [currentSquare[0]+2, currentSquare[1]]]
	# vertical
	elif orientation == 1:
		bed = [[currentSquare[0], currentSquare[1]], [currentSquare[0], currentSquare[1]+1], [currentSquare[0], currentSquare[1]+2]]

	# remaining squares count must be divisble by 3
	if len(missingSquares) > 0:
		a = float(tentSize[0]*tentSize[1])
		if a > 0:
			if (a - len(missingSquares)) % 3 != 0:
				return False
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


def next_square(tentSize, currentSquare, missingSquares):
	# if can continue on line, do so
	# exit case
	if currentSquare == [tentSize[0]-1, tentSize[1]-1]:
		return currentSquare
	# continue on linecase
	elif currentSquare[0] + 1 < tentSize[0]:
		nsquare = [currentSquare[0] + 1, currentSquare[1]]
		if nsquare in missingSquares:
			return next_square(tentSize, nsquare, missingSquares)
		else:
			return nsquare
	# otherwise jump to the next line
	else:
		# if next line first square is in missing square, call function again
		nsquare = [0, currentSquare[1] + 1]
		if nsquare in missingSquares:
			return next_square(tentSize, nsquare, missingSquares)
		# otherwise just return first square of next line
		else:
			return nsquare















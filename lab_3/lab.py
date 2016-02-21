def step(gas):
    # Put your solution here.  Good luck!  
    return 0


def collision_state_change(gas):
	new_gas = gas[:]

	for state in new_gas:
		# Change state of gases colliding with walls
		if 'w' in state:
			# Change gases in all wall states to reverse direction
			for particle in state:
				if particle == "l":
					particle = "r"
				elif particle == "r":
					particle = "l"
				elif particle == "u":
					particle = "d"
				elif particle == "d":
					particle = "u"

		# Change state of gases colliding
		else:
			for particle in state:
				if particle == "l":
					particle = "d"
				elif particle == "r":
					particle = "u"
				elif particle == "u":
					particle = "l"
				elif particle == "d":
					particle = "r"

	return new_gas


def propogate_state(gas):
	







	
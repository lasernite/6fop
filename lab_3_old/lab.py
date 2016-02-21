def step(gas):
    # Put your solution here.  Good luck! 
    # print "original gas"
    # print gas
    # print "state changed gas"
    # print collision_state_change(gas)
    return propogate_state(collision_state_change(gas))


def collision_state_change(gas):

	for state in gas['state']:
		# Change state of gases colliding with walls
		if 'w' in state:
			# Change gases in all wall states to reverse direction
			for particle_index in range(len(state)):
				if state[particle_index] == "l":
					state[particle_index] = "r"
				elif state[particle_index] == "r":
					state[particle_index] = "l"
				elif state[particle_index] == "u":
					state[particle_index] = "d"
				elif state[particle_index] == "d":
					state[particle_index] = "u"

		# Change state of gases colliding
		else:
			# Only change particles if 2 present
			if len(state) == 2:
				for particle_index in range(len(state)):
					if state[particle_index] == "l":
						state[particle_index] = "d"
					elif state[particle_index] == "r":
						state[particle_index] = "u"
					elif state[particle_index] == "u":
						state[particle_index] = "l"
					elif state[particle_index] == "d":
						state[particle_index] = "r"

	return gas


def propogate_state(gas):
	new_gas = [[] for x in range(gas['width'] * gas['height'])]

	# propogate new state of gas
	for state_index in range(gas['width'] * gas['height']):
		states = gas['state']

		for particle in states[state_index]:
			if particle == "w":
				new_gas[state_index].append('w')
			elif particle == "l":
				new_gas[state_index - 1].append('l')
			elif particle == "r":
				new_gas[state_index + 1].append('r')
			elif particle == "u":
				new_gas[state_index - gas['width']].append('u')
			elif particle == "d":
				new_gas[state_index + gas['width']].append('d')

	gas['state'] = new_gas

	return gas











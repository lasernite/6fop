def step(gas):
    return propogate_state(collision_state_change(gas))


def collision_state_change(gas):

	for state_index in range(len(gas['state'])):
		state = gas['state'][state_index]
		# Change state of gases colliding with walls
		if 'w' in state:
			# Change gases in all wall states to reverse direction
			for particle_index in range(len(gas['state'][state_index])):
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
			if len(gas['state'][state_index]) == 2:
				if gas['state'][state_index] == ['l', 'r'] or gas['state'][state_index] == ['r', 'l']:
					gas['state'][state_index] = ['u', 'd']
				elif gas['state'][state_index] == ['u','d'] or gas['state'][state_index] == ['d', 'u']:
					gas['state'][state_index] = ['l', 'r']

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











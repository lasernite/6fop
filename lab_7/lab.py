import operator
import string

def generate_trie(words):
	trie = {'frequency':0, 'children':{}}
	for word in words:
		trie = add_word_to_trie(trie, word)
	return trie


def add_word_to_trie(trie, word):
	# create working copy, saving original trie root pointer
	working_trie = trie

	for letter_i in range(len(word)):
		# make working trie a level deeper
		working_trie = working_trie['children']

		# last letter of word, then increment frequency
		if letter_i == len(word) - 1:
			if word[letter_i] in working_trie:
				working_trie[word[letter_i]]['frequency'] += 1
			else:
				working_trie[word[letter_i]] = {'frequency':1, 'children':{}}
		# otherwise add node if neccesary and expand deeper
		else:
			if not word[letter_i] in working_trie:
				working_trie[word[letter_i]] = {'frequency':0, 'children':{}}

		working_trie = working_trie[word[letter_i]]

	return trie


def autocomplete(trie, prefix, N):
	working_trie = trie

	# get the relevant portion of tree for the prefix
	for letter in prefix:
		if letter in working_trie['children']:
			working_trie = working_trie['children'][letter]
		else:
			return []

	counting = {}

	# count most popular extensions after prefix
	def count_extensions(trie, letters):
		# if no children, end of word, return
		if not trie['children']:
			counting[letters] = trie['frequency']
			return True
		# otherwise expand all possibilities
		else:
			if trie['frequency'] > 0:
				if letters not in trie['children']:
					counting[letters] = trie['frequency']
			for letter in trie['children']:
				new = letters + letter
				count_extensions(trie['children'][letter], new)

	count_extensions(working_trie, "")

	# # edge case where prefix is trie
	# pre = get_trie(trie, prefix)
	# if pre:
	# 	if pre['frequency'] > 0:
	# 		counting[""] = pre['frequency']

	sort = sorted(counting.items(), key=operator.itemgetter(1))
	sort.reverse()
	nitems = sort[0:N]

	final = []
	for t in nitems:
		final.append(prefix + t[0])

	# print 'prefix'
	# print prefix
	# print 'trie'
	# print trie
	# print 'working trie'
	# print working_trie
	# print 'counting'
	# print counting
	# print 'final'
	# print final
	return final

def get_trie(trie, word):
	working_trie = trie.copy()
	for letter in word:
		if letter in working_trie['children']:
			working_trie = working_trie['children'][letter]
		else:
			return False
	return working_trie


def autocorrect(trie, prefix, N):
	autocompleted = autocomplete(trie, prefix, N)

	num_needed = N - len(autocompleted)
	
	if num_needed > 0:
		valid_edits = {}
		# Add valid edits
		for letter_i in range(len(prefix)):
			# for a through z
			for l in string.lowercase:
				# single character insertion
				new_word = prefix[0:letter_i] + l + prefix[letter_i:len(prefix)]
				existent_word = get_trie(trie, new_word)
				if existent_word:
					if existent_word['frequency'] > 0:
						valid_edits[new_word] = existent_word['frequency']
				# single character replacement
				new_word = prefix[0:letter_i] + l + prefix[letter_i+1:len(prefix)]
				existent_word = get_trie(trie, new_word)
				if existent_word:
					if existent_word['frequency'] > 0:
						valid_edits[new_word] = existent_word['frequency']
			# single character deletion
			new_word = prefix[0:letter_i] + prefix[letter_i+1:len(prefix)]
			existent_word = get_trie(trie, new_word)
			if existent_word:
				if existent_word['frequency'] > 0:
					valid_edits[new_word] = existent_word['frequency'] 
			# two character transpose
			for letter_x in range(len(prefix)):
				new_word = prefix[0:letter_i] + prefix[letter_x] + prefix[letter_i+1:letter_x] + prefix[letter_i] + prefix[letter_x+1:len(prefix)]
				if not new_word == prefix:
					existent_word = get_trie(trie, new_word)
					if existent_word:
						if existent_word['frequency'] > 0:
							valid_edits[new_word] = existent_word['frequency']

		# get autocompleted words inside valid for frequency sorting
		for word in autocompleted:
			valid_edits[word] = get_trie(trie, word)['frequency']

		sort = sorted(valid_edits.items(), key=operator.itemgetter(1))
		sort.reverse()
		nitems = sort[0:N]
		final = []
		for x in nitems:
			final.append(x[0])
		print N
		print nitems
		print final
		return final

	else:
		return autocompleted








































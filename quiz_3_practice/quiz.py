# Problem 1
# ---------
# Returns the number of viable sets of animals
def count_viable(weights, capacity):
	if capacity < 0:
		return 0
	elif len(weights) == 0:
		if capacity < 0:
			return 0
		else:
			return 1

	def count
	count_viable(weights[1:len(weights)], capacity - weight[0])

# Problem 2
# ---------
# Returns a valid ordering of classes
def find_valid_ordering(class_graph):
    return "Implement Me!"

# Problem 3
# ---------
# Returns a representation of the information in default_db and update_db
#  This representation will be used to implement the other methods
def build_rep(default_db, update_db):
    # Default Representation
    rep = [default_db, update_db] # CHANGE ME!
    return rep

# Returns a list of lists class_dates where class_dates[i] is a list of all
#  dates on which class_list[i] meets
def get_class_days(class_list, rep):
    return "Implement Me!"

# Returns a list of all classes that never meet before the specified time
def get_late_classes(time, rep):
    return "Implement Me!"

import traceback

def get_prereq_dict(class_graph):
    prereq_dict = {}
    for node in class_graph:
        prereq_dict[node] = []

    for node in class_graph:
        for successor in class_graph[node]:
            prereq_dict[successor] += [node]
    return prereq_dict

def check_DAG(ordering, class_graph):
    try:
        if sorted(ordering) != sorted(class_graph.keys()):
            return False
        prereq_dict = get_prereq_dict(class_graph)
        valid_next = set([c for c in prereq_dict if len(prereq_dict[c]) == 0])
        for c in ordering:
            if c not in valid_next:
                return False
            valid_next.remove(c)
            for succ in class_graph[c]:
                valid_next.add(succ)
        return True
    except:
        return False

def load_database():
    with open("resources/database/default_db.txt") as f:
        default_db = [line.split() for line in f.read().split("\n")]
    with open("resources/database/update_db.txt") as f:
        update_db = [line.split() for line in f.read().split("\n")]
    return default_db, update_db

def verify( result, input_data, gold ):
  try:
    message = "isn't right :(, your code produces %s" % str(result)
    ok = False
    if (input_data["function"] == "find_valid_ordering"):
        result = map(str, result)
        ok = check_DAG(result, input_data["inputs"]["class_graph"])
        message = "isn't right :(, not a valid ordering of all classes."
    elif (input_data["function"] == "get_late_classes"):
        ok = (sorted(result) == sorted(gold))
    elif (input_data["function"] == "get_class_days"):
        # Result should be a list of lists
        is_list_of_lists = True
        if type(result) is not list:
            is_list_of_lists = False
        else:
            for x in result:
                if (type(x) is not list):
                    is_list_of_lists = False
                    break
        if not is_list_of_lists:
            ok = False
            message = "result should be a list of lists of pairs! :("
        elif (len(result) != len(gold)):
            ok = False
            message = "result is not of correcect length :("
        else:
            result2 = []
            for item in result:
                result2.append(sorted(item))
            gold2 = []
            for item in gold:
                gold2.append(sorted(item))
            ok = (sorted(result2) == sorted(gold2))
    else:
        ok =  (result == gold)
    if ok:
      message = "looks good, yay!"
  except:
    print traceback.format_exc()
    ok = False
    message = "CRASHED! :(. See above for details."
  return ok, message

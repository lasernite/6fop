import quiz, json, traceback

def run_test( input_data ):
  result = ""
  try:
    f = getattr(quiz, input_data["function"])
    if (input_data["function"] in ["get_class_days", "get_late_classes", "get_class_times_on_day"]):
        default_db, update_db = load_database()
        rep = quiz.build_rep(default_db, update_db)
        input_data["inputs"]["rep"]  = rep
    result = f(**input_data["inputs"])
  except:
    result = traceback.format_exc()
  return result

def load_database():
    with open("resources/database/default_db.txt") as f:
        default_db = [line.split() for line in f.read().split("\n")]
    with open("resources/database/update_db.txt") as f:
        update_db = [line.split() for line in f.read().split("\n")]
    return default_db, update_db

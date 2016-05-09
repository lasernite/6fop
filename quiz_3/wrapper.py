import json, traceback, sys, itertools

# Blacklist itertools
itertools_module = sys.modules["itertools"]
sys.modules["itertools"] = None
import quiz
sys.modules["itertools"] = itertools_module

def run_test( input_data ):
  result = ""
  try:
    f = getattr(quiz, input_data["function"])
    if (input_data["function"] in ["earliest_meeting"]):
        default_db, update_db = load_database()
        input_data["inputs"]["default_db"] = default_db
        input_data["inputs"]["update_db"] = update_db
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

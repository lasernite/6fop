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
    result = f(**input_data["inputs"])
  except:
    result = traceback.format_exc()
  return result

import traceback

def verify( result, input_data, gold ):
  try:
    ok =  (result == gold)
    message = "incorrect next song! Your code suggests song # %s" % str(result)
    if ok:
      message = "correctly suggested song # %d" % result
  except:
    print traceback.format_exc()
    ok = false
    message = "your code crashed :(. Stack trace is printed above so you can debug."
  return ok, message

import traceback

def verify( result, input_data, gold ):
  try:
    ok = False
    message = "isn't right :(, your code produces %s" % str(result)
    ok =  (result == gold)
    if ok:
      message = "looks good, yay!"
  except:
    print traceback.format_exc()
    ok = False
    message = "CRASHED! :(. See above for details."
  return ok, message

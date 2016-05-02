import traceback
import math, time
import copy

def verify(result, input_data, gold):
    ok = True
    message = "looks good"
    try:
        if isinstance(result, str) or isinstance(result, unicode):
            # There was an exception in wrapper, pass it along
            ok = False
            message = result
        elif not compareObjL(result, gold["end"]):
          ok = False
          message = "isn't close enough to the correct result.  Your ball or paddles are probably in the wrong location.  Try using the GUI to see where you went wrong.  "
    except:
        traceback.print_exc();
        ok = False
        message = "crashed :(. Stack trace is printed above so you can debug."

    return ok, message

# Helper things!
def close(a,b):
  if type(a)!=type(b):
    if type(a)==type(3.14) and type(b)==type(3):
      b = float(b)
    elif type(b)==type(3.14) and type(a)==type(3):
      a = float(a)
    elif type(a)==type("") and type(b)==type(u""):
      b = str(b)
    elif type(a)==type(u"") and type(b)==type(""):
      a = str(a)
    elif type(a)==type(()) and type(b)==type([]):
      pass
    elif type(b)==type([]) and type(a)==type(()):
      pass
    else:
      print(type(a))
      print(type(b))
      raise Exception("Incorrect types")
  if type(a)==type('') or type(a)==type(u""):
    return a==b
  if type(a)==type((2.,3.)):
    if len(a) != len(b): return False
    return all(map(close,a,b))
  if type(a)==type(3):
    return a==b
  if type(a)==type(3.14):
    return abs(a-b)<1e-6
  if type(a)==type([]):
    if len(a) != len(b): return False
    return all(map(close,a,b))
  if type(a)==type({"a":"b"}):
    if len(a) != len(b): return False
    for it in a:
      if it not in b:
        return False
      t = close(a[it],b[it])
      if not t:
        return False
    return True
  print(type(a))
  print(type(b))
  raise Exception("Incorrect types")

def compareObjL(a,b):
  a = copy.deepcopy(a)
  b = copy.deepcopy(b)
  if len(a) != len(b): return False
  for ai in a:
    found = False
    for i,bi in enumerate(b):
      if close(ai,bi):
        found = True
        del b[i]
        break
    if not found: return False
  return True

class CanvasToList:
  def __init__(self):
    self.shapes = []

  def objects(self):
    return self.shapes

  def draw_circle(self, center_x, center_y, radius, color_string):
    self.shapes.append({"shape":"circle","center":(center_x,center_y), "radius":radius})

  def draw_rectangle(self, upper_left_x, upper_left_y, lower_right_x, lower_right_y, color_string):
    self.shapes.append({"shape":"rect","min":(upper_left_x,upper_left_y),"max":(lower_right_x, lower_right_y)})

import lab, json, traceback

reload(lab) # this forces the student code to be reloaded when page is refreshed

def run_test(input_data):
  result = ""
  try:
    # f = getattr(lab, input_data["function"])
    # result = f(**input_data["inputs"])

    # Run student code
    lab.init(   input_data['width'],
                input_data['height'],
                input_data['ballPosition'],
                input_data['ballVelocity'],
                input_data['blocks'] )

    for m,s in enumerate(input_data['steps']):
      st = lab.step(    s['time'],
                        input_data['paddle1X'],
                        input_data['paddle2X'],
                        input_data['paddle_offset'],
                        input_data['paddle_radius'] )

      if not close(st, s['winner']):  # TODO: Ideally, this should happen in the reducer. This is sketchy because a clever student has access to the expected values! In this case, good enough because we expose all test cases anyway...

        test_okay = False
        raise Exception("Incorrect winner state at timestep {} got {} expected {}".format(str(m),str(st),str(s['winner'])) )

    tocheck = CanvasToList()
    lab.draw(   tocheck,
                input_data['paddle1X'],
                input_data['paddle2X'],
                input_data['paddle_offset'],
                input_data['paddle_radius'] )
    result = tocheck.objects()

  except:
    result = traceback.format_exc()
  return result

def close(a,b):
  if type(a)!=type(b):
    if type(a)==type(3.14) and type(b)==type(3):
      b = float(b)
    elif type(b)==type(3.14) and type(a)==type(3):
      a = float(a)
    elif type(a)==type("") and type(b)==type(u""):
      b = str(b)
    elif type(b)==type(u"") and type(a)==type(""):
      a = str(a)
    elif type(a)==type(()) and type(b)==type([]):
      pass
    elif type(b)==type([]) and type(a)==type(()):
      pass
    else:
      print(type(a))
      print(type(b))
      raise Exception("Incorrect types")
  if type(a)==type(''):
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

class CanvasToList:
  def __init__(self):
    self.shapes = []

  def objects(self):
    return self.shapes

  def draw_circle(self, center_x, center_y, radius, color_string):
    self.shapes.append({"shape":"circle","center":(center_x,center_y), "radius":radius})

  def draw_rectangle(self, upper_left_x, upper_left_y, lower_right_x, lower_right_y, color_string):
    self.shapes.append({"shape":"rect","min":(upper_left_x,upper_left_y),"max":(lower_right_x, lower_right_y)})

# Presistent state
canvas = None

# UI interface
def init(input_data):
    global canvas
    canvas = Canvas()
    return lab.init(   input_data['width'],
                input_data['height'],
                input_data['ball_position'],
                input_data['ball_velosity'],
                input_data['blocks'] )

def draw(input_data):
  lab.draw(    canvas.clear(),
                input_data['paddle_1_xpos'],
                input_data['paddle_2_xpos'],
                input_data['paddle_offset'],
                input_data['paddle_radius'] )
  return canvas.get_state()

def step(input_data):
    return lab.step(   input_data['time'],
                input_data['paddle_1_xpos'],
                input_data['paddle_2_xpos'],
                input_data['paddle_offset'],
                input_data['paddle_radius'] )

# A canvas object
class Canvas:
  def __init__(self):
    self.state = {"circles": [], "rectangles": []}

  def draw_circle(self, pos_x, pos_y, radius, color):
    self.state["circles"].append((pos_x, pos_y, radius, color))

  def draw_rectangle(self, pos_x, pos_y, width, height, color):
    self.state["rectangles"].append((pos_x, pos_y, width, height, color))

  def get_state(self):
    return self.state

  def clear(self):
    self.state["circles"] = []
    self.state["rectangles"] = []
    return self

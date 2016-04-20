import lab, json, traceback, copy, random
import sys
sys.path.append('resources')
import GameClient as GC
reload(lab) # this forces the student code to be reloaded when page is refreshed

def run_test(input_data):
  state = input_data["state"]
  state_double = copy.deepcopy(state)
  world = lab.World(state_double)
  GC.init()
  if input_data["test"] == "i":
    return run_init(world)

  return run_moves(input_data, world)


def run_moves(input_data, world):
  result = {}
  player_result = []
  turn_result = []
  location_result = []
  for move in input_data["moves"]:
      player = world.get_current_player_name()
      player_result.append(player)
      temp = GC.handle_input(move, world)
      turn_result.append(temp[0])

      location_result.append(world.get_location(player))

  revealed_result = world.get_revealed_cards()
  seen_result = []
  for player in world.get_players():
      seen_result.append(world.get_seen_cards(player))

  result["playerResult"] = player_result
  result["locationResult"] = location_result
  result["seenResult"] = seen_result
  result["turnResult"] = turn_result
  result["revealedResult"] = revealed_result
  result["returnResult"] = turn_result
  return result

def run_init(world):
  result = []
  result.append(world.get_current_player_name())
  result.append(world.get_players())
  for player in world.get_players():
    result.append(world.get_location(player))
    result.append(world.get_cards(player))
    result.append(world.get_seen_cards(player))
    result.append(world.get_revealed_cards())

  return result

# UI interface
ui_world = None

def ui_init(input_data):
    global ui_world
    parameters = None
    with open("resources/world.json", 'r') as f:
        parameters = json.loads(f.read())
    state = {}

    suspects = parameters["suspects"]
    weapons = parameters["weapons"]
    rooms = parameters["rooms"]
    random.shuffle(suspects)
    random.shuffle(weapons)
    random.shuffle(rooms)

    state["players"] = parameters["players"]
    state["envelope"] = [ suspects.pop(), weapons.pop(), rooms.pop() ]

    num_players = len(parameters["players"])
    num_rooms = (len(rooms)-1)/num_players
    num_weapons = (len(weapons)-1)/num_players
    num_suspects = (len(suspects)-1)/num_players

    card_assignments = {}
    for player in parameters["players"]:
        card_assignments[player] = {}
        c = card_assignments[player]
        #assign rooms
        c["rooms"] = [ rooms.pop() for x in range(num_rooms) ]
        c["weapons"] = [ weapons.pop() for x in range(num_weapons) ]
        c["suspects"] = [ suspects.pop() for x in range(num_suspects) ]

    state["playersCards"] = card_assignments
    ui_world = lab.World(state)
    return GC.init()

def ui_handle_input(input_data):
    global ui_world
    return GC.handle_input(input_data["input"], ui_world)

#import lab as code
import GameParser as parser

global deck
deck = {}
game_over = False
number_rooms = 0
number_suspects = 0
number_weapons = 0

state = {}

state["envelope"] = ["rope", "kitchen", "scarlett"]
player = {}
player["Srini"] = ["rope", "kitchen"]
state["players"]= player

##world = None

def init():
  # Use code.??? to init game state to a known configuration
  # Query game state and produce output
  global number_rooms
  global number_suspects
  global number_weapons

  global deck
  initialize_cards()

  number_rooms = len(deck.rooms)
  number_suspects = len(deck.suspects)
  number_weapons = len(deck.weapons)

  message = "Welcome to Boddy Estate! Remember, the rules are simple. Correctly solve the murder, before its too late! Don't be afraid to {look} around... although, who knows what you may find?"
  #player = code.get_current_player()
  return ("", message, "Mario")
def handle_input(input_string, world):
  # Parse input, reject illegal things
  # Use code.??? to manipulate game state
  # Query game state and produce output
  player = world.get_current_player_name()
  global deck
  input_string = input_string.lower()


  if input_string == "look":
    place = world.get_location(player)
    if place in deck.rooms:#.keys():
      des = "Looking around the " + place + " you see..."
      des += deck.rooms[place].description
      return ("",des, world.get_current_player_name())
    else:
      return "Your code is saying your player is in a non-existent room"


  if input_string == "sheet":
    return ("", get_sheet(world), world.get_current_player_name())

  if input_string == "cards":
    res = (world.get_current_player_name() + ", you have the following cards:\n")
    cards = world.get_cards(player)
    sus = cards["suspects"]
    weap = cards["weapons"]
    rooms = cards["rooms"]

    res += "{suspects:} "
    for card in sus:
      res += (" "+card)

    res += "\n {rooms:} "
    for card in rooms:
      res += (" "+card)

    res += "\n {weapons:} "
    for card in weap:
      res += (" "+card)

    return ("", res, world.get_current_player_name())

  result = parser.parse_input(input_string, deck)

  if result == "game over":
    init()
    return ("", "game over", "no one")

  if type(result) == str:
    return ("", result, world.get_current_player_name())

  if result is None:
    return ("", "That was an invalid input!", world.get_current_player_name())

  res_type = result["type"]
  res_args = result["args"]

  if res_type == "guess" or res_type == "accuse" or res_type == "travel":
    player = world.get_current_player_name()
    code_res = world.take_turn(res_type, res_args)
    #players = code.get_players()
    #current_index = players.index(player)
    #number_players = len(players)
    #next_index = (current_index + 1)%number_players

    if res_type == "guess":

      s = res_args["suspect"]
      w = res_args["weapon"]
      r = res_args["room"]
      to_print = (player + " guessed " + s + " with the " + w + " in the "+ r)
      to_print += (" and the card revealed was: " + code_res)

    elif res_type == "accuse":

      s = res_args["suspect"]
      w = res_args["weapon"]
      r = res_args["room"]
      to_print = (player + " accused " + s + " with the " + w + " in the "+ r)
      if (player == code_res):
        to_print += (" and won! Congrats, you saved us all! :)")
      else:
        to_print += (" and lost! Apologies, you have failed us all! :'( To start a new game, press refresh!")
    elif res_type == "travel":

      to_print = (player + " travelled to the " + res_args)
    elif code_res == "invalid room":
      to_print = "The guess involved an invalid room! Turn forfeited"
    #print (code_res, to_print , code.get_current_player())
    #return code_res
    return (code_res, to_print , world.get_current_player_name())


  return "Oh snap! There was some input: \"%s\". That was interesting." % input

def get_cards():
  global deck
  return deck

def initialize_cards():
  global deck
  deck = Deck()

  suspect_card_names = ["scarlett", "green", "plum", "mustard", "white", "peacock"]
  weapon_card_names = ["candlesticks", "knife", "revolver","leadpipe", "wrench", "rope"]
  room_card_names = ["library", "foyer", "ballroom", "conservatory", "study", "kitchen", "hall"]

  descripS = {}
  descripS["scarlett"] = "Hello, there, darling, I'm Scarlett. I am much more than your usual Femme Fatal!"
  descripS["green"] = "Ah, Hello! Nice to meet you. I'm Mr. Green, your local, trustworthy business man who loves him his green!"
  descripS["plum"] = "Professor Plum, here. Many say I'm just an absented minded professor  but, in reality,... what was I saying, again?"
  descripS["mustard"]= "Attention! I am your commanding officer, Colonel Mustard."
  descripS["white"]= "I'm Mrs. White, the one responsble for actually keeping this estate from burning to the ground. And if it weren't for you meddling kids... "
  descripS["peacock"] = "Hi, I'm Mrs. Peacock. It's a pleasure to make your acquaintance. You must know my husband..."

  descripR ={}
  descripR["ballroom"] = "You are in a spacious ballroom. On every wall there are rich, maroon curtains, and the floor is made out of granite. Above you, there is a enormous sparking chandelier. You think you can hear music tinkling softly in the distance..."
  descripR["library"]="Books, lots and lots of books, surround you on every wall. There are long mahagony tables with those green shaded lamps you always see in fancy, old libraries. There's a wheeled ladder in one corner, leading to a loft of ... even more books"
  descripR["foyer"]="You are in the foyer of the mansion, where all noble guests are first received and welcomed. There is a large, curving, granite staircase in the center and you see large, airy rooms off to either side."
  descripR["conservatory"] = "It's humid. There's condensation on the walls, and greenery all around you. You're particularly intrigued by a bright, blood-red flower that seems to continuously open and close, slowly, and slightly rotate as if there is some unfeelable breeze..."
  descripR["study"] = "It's rather more cramped in here than you expected, but more home-y then the other rooms you have visited as of yet. There are ink smudges on the desk, and a blanket on the couch, and the light has a soft yellow tint to it. You feel like you could see yourself working here comfortably."
  descripR["kitchen"] = "It's an industrial sized kitchen with pots hanging from the ceiling and large, metal sinks along the wall. Clearly, this estate is accustomed to hosting numerous guests for large receptions. There's a smell of lentil soup that you can't quite shake..."
  descripR["hall"] = "There's a grand piano in one corner. The carpet feels soft and comfortable under your feet. There's remarkably little furniture, but the tall window frames leave this room filled with light."

  descripW = {}
  descripW["candlesticks"]= "It is better to light a candle than curse the darkness. - Eleanor Roosevelt"

  descripW["knife"]="Et tu, Brute?"
  descripW["revolver"]="Our whole universe was in a hot, dense state until... and it all started with the big bang - BANG"
  descripW["leadpipe"]="Kind of like those cylinders from 8.02, but not."
  descripW["wrench"]="A determined soul will do more with a rusty monkey wrench than a loafer will accomplish with all the tools in a machine shop."
  descripW["rope"]= "Are you, are you? Coming to the tree? Strange things did happen there no stranger would it be. If we met. At midnight. Near the hanging tree..."

  for s in suspect_card_names:
      deck.suspects[s] = Card(s, "Suspect", descripS[s])
  for w in weapon_card_names:
      deck.weapons[w] = Card(w, "Weapon", descripW[w])
  for r in room_card_names:
      deck.rooms[r] = Card(r, "Room", descripR[r])

class Deck():

    def __init__(self):
        self.suspects = {}
        self.weapons = {}
        self.rooms = {}

class Card():

  def __init__(self, name, category, description):
    self.category = category
    self.name = name
    self.description = description


  def __str__(self):
      return "Type: "+ self.category+ "\n Name: "+ self.name + "\n Description: " +self.description
      #return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description)


  def __eq__(self, other_card):
      return (self.category == other_card.category and self.name == other_card.name)

def get_sheet(world):
    deck = get_cards()
    player = world.get_current_player_name()
    #print world.get_cards(player)
    #player_cards = code.get_cards(player)
    #seen_cards = code.get_seen_cards(player)


    top_row1= """\
    --------------------------------
    |Suspects  |"""
    l = max(0, 10- len(player))/2
    top_row1 = top_row1 +" "*l +player[:10] + " "*l
    rest ="""| Jarvis  |
    --------------------------------
    """
    top_row1 = top_row1 + rest

    top_row2 = """\
    --------------------------------
    |Weapons   |"""
    l = max(0, 10- len(player))/2
    top_row2 = top_row2 +" "*l +player[:10] + " "*l

    top_row2 = top_row2 + rest
    #l = max(0, 12- len(player.character_name))/2
    top_row3 = """\
    --------------------------------
    |Rooms     |"""
    top_row3 = top_row3 +" "*l +player[:10] + " "*l

    top_row3 = top_row3 + rest

    sus = top_row1 + "\n"
    sus_cards = deck.suspects
    count = 0
    for i in sus_cards:#.keys():
        space = max(0, 8-len(i[:7]))
        sus = sus +"     |"+ str(count) + "."+ i[:7] + " "*space +"|"
        has_card = i in world.get_cards(player)["suspects"]
        ad_in_seen_cards = i in list(world.get_seen_cards(player))
        if has_card:
            sus = sus + "    X   |"#+ "         |\n"
        else:
            sus = sus + "        |"#         |\n"
        if ad_in_seen_cards:
            sus = sus + "    X    |\n"
        else:
            sus = sus+ "         |\n"
        count+=1
    weap = "\n"+ top_row2 + "\n"
    weap_cards = deck.weapons
    count = 0
    for i in weap_cards:#.keys():
        space = max(0, 8-len(i[:7]))
        weap = weap +"     |"+ str(count) + "."+ i[:7] + " "*space +"|"
        has_card = i in world.get_cards(player)["weapons"]
        ad_in_seen_cards = i in list(world.get_seen_cards(player))
        if has_card:
            weap = weap + "    X   |"#         |"+ "\n"
        else:
            weap = weap + "        |"#         |\n"
        if ad_in_seen_cards:
            weap = weap + "    X    |\n"
        else:
            weap = weap + "         |\n"
        count+=1

    room = "\n"+ top_row3 + "\n"
    room_cards = deck.rooms
    count = 0
    for i in room_cards:#.keys():
        space = max(0, 8-len(i[:7]))
        room = room +"     |"+ str(count) + "."+ i[:7] + " "*space +"|"
        has_card = i in world.get_cards(player)["rooms"]
        ad_in_seen_cards = i in list(world.get_seen_cards(player))
        if has_card:
            room = room + "    X   |"#         |"+ "\n"
        else:
            room = room + "        |"#         |\n"
        if ad_in_seen_cards:
            room = room + "    X    |\n"
        else:
            room = room + "         |\n"
        count+=1

    final = sus+ weap + room + "     --------------------------------\n" + "Locations:\n"
    f = final

    q = "\n"
    for p in world.get_players():

      add = (p + " is in the " + world.get_location(p)+ "\n")
      q = q + add
    print f + "\n"+ q
    return f + "\n"+ q

#Lab9: A Cluefull (less) Adventure

"""
Welcome to Boddy Estate! 
"""
#We suggest making a Player class, too.
class Player:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards
        self.location = 'foyer'



class World: 
    
    # state = {"envelope":[suspect, weapon, room (no order enforced)], 
    #          "players":[players in order of turn], 
    #          "playersCards":{"playerName":{"weapons":[weapons list], 
    #                                        "rooms":[rooms list], 
    #                                        "suspects":[suspects list]},
    #                          "playerName2":{"weapons":[weapons list], 
    #                                        "rooms":[rooms list], 
    #                                        "suspects":[suspects list]}}}
    def __init__(self, state):
        self.state = state
        # Make Player Objects Accessible
        players = []
        for playerName in state['players']:
            players.append(Player(playerName, state['playersCards'][playerName]))
        self.players = players
        self.currentPlayer = players[0]

        
    #Define any helper methods you'd like, as usual
        
    # These methods allow the UI and test infrastructure
    # to peek into your game state. You MUST implement each
    # of these methods, and they must return the proper type
    # according to the readme.

    def get_current_player_name(self):
       #Returns the name (string) of the current player
        return self.currentPlayer.name

    def get_players(self):
        #Returns a list of players' names as described in the ReadMe
        return self.state['players']

    def get_location(self, player_string):
        #Returns the location of the specified player
        return self.state['']

    def get_cards(self, player_string):
        # Return a dictionary of cards held by a player
        # with the keys described in the README
        return NotImplementedError()


    def get_revealed_cards(self):
        #Return a list of revealed cards (order matters!)
        return NotImplementedError

    def get_seen_cards(self, player_string):
        #Return the list of cards seen by this player
        return NotImplementedError


    #This method controls game play

    def take_turn(self, action, args):
    # action is one of {"travel", "guess", "accuse"}
    # arguments are action-dependent. Consult the readme for details
        if action == "travel":
            # fill in code here, args is a destination like "ballroom"
            return "travel"
        elif action == "guess":
            # fill in code here, args is {"suspect":guess, "room":guess, "weapon":guess}, guess of next player in array
            # if player not in room in guess, return "invalid room"
        elif action == "accuse":
        else:
            return None
               
   

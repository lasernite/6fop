#Lab9: A Cluefull (less) Adventure

"""
Welcome to Boddy Estate! 
"""
#We suggest making a Player class, too.

class World: 
    
    def __init__(self, state):
        return NotImplementedError()
        
    #Define any helper methods you'd like, as usual
        
    # These methods allow the UI and test infrastructure
    # to peek into your game state. You MUST implement each
    # of these methods, and they must return the proper type
    # according to the readme.
    
    def get_current_player_name(self):
       #Returns the name (string) of the current player
        return NotImplementedError()
    
    def get_players(self):
        #Returns a list of players' names as described in the ReadMe
        return NotImplementedError()

    def get_location(self, player_string):
        #Returns the location of the specified player
        return NotImplementedError()

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
        return NotImplementedError
        
        
   

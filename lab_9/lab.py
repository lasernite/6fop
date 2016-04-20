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
        self.seenCards = []



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
        players = {}
        for playerName in state['players']:
            players[playerName] = Player(playerName, state['playersCards'][playerName])
        self.players = players
        # first player starts
        self.currentPlayer = players[state['players'][0]]
        # revealed cards
        self.revealedCards = []

        
    #Define any helper methods you'd like, as usual
    def get_next_player_name(self, currentPlayerName, playersOrderedNames):
        currentPlayerIndex = playersOrderedNames.index(currentPlayerName)
        nextPlayerIndex = currentPlayerIndex + 1
        if nextPlayerIndex >= len(playersOrderedNames):
            nextPlayerIndex = 0
        nextPlayerName = playersOrderedNames[nextPlayerIndex]
        return nextPlayerName
        
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
        return self.players[player_string].location

    def get_cards(self, player_string):
        # Return a dictionary of cards held by a player
        # with the keys described in the README
        return self.players[player_string].cards


    def get_revealed_cards(self):
        #Return a list of revealed cards (order matters!)
        return self.revealedCards

    def get_seen_cards(self, player_string):
        #Return the list of cards seen by this player
        return self.players[player_string].seenCards


    #This method controls game play

    def take_turn(self, action, args):
    # action is one of {"travel", "guess", "accuse"}
    # arguments are action-dependent. Consult the readme for details
        if action == "travel":
            # fill in code here, args is a destination like "ballroom"
            # change current player location
            self.currentPlayer.location = args
            # change current player and end turn
            nextPlayerName = get_next_player_name(self, self.currentPlayer.name, self.state['players'])
            self.currentPlayer = self.players[nextPlayerName]
            return "travel"
        elif action == "guess":
            nextPlayerName = get_next_player_name(self, self.currentPlayer.name, self.state['players'])
            # next player is adversary
            nextPlayer = self.players[nextPlayerName]
            # fill in code here, args is {"suspect":guess, "weapon":guess, "room":guess}, guess of next player in array
            # if player not in room in guess, return "invalid room"
            if args['room'] != self.currentPlayer.location:
                self.currentPlayer = nextPlayer
                return "invalid room"

            # get list of matches, in order of potential reveal
            matches = []
            if args['suspect'] in self.cards['suspects']:
                matches.append(args['suspect'])
            if args['weapon'] in self.cards['weapons']:
                matches.append(args['weapons'])
            if args['room'] in self.cards['rooms']:
                matches.append(args['room'])

            # if no matches spit back failure
            if len(matches) == 0:
                self.currentPlayer = nextPlayer
                return "none"

            # check if any have already been shown, if so return it
            for card in matches:
                if card in self.revealedCards:
                    self.currentPlayer = nextPlayer
                    return card

            # otherwise add as revealed and seen cards and return lowest importance card
            self.revealedCards.append(matches[0])
            self.currentPlayer.seenCards.append(matches[0])
            self.currentPlayer = nextPlayer
            return matches[0]
        elif action == "accuse":
            e = self.state['envelope']
            if args['suspect'] in e and args['weapon'] in e and args['room'] in e:
                return self.currentPlayer
            else:
                nextPlayerName = get_next_player_name(self, self.currentPlayer.name, self.state['players'])
                # next player is adversary
                return self.players[nextPlayerName]
        else:
            return None
               
   

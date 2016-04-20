from lab import *
#import clue_universe_gutted.py as world


def parse_input(input_for_turn, cards):
    #player = get_current_player_name()

    if input_for_turn == "":
        return "That was an illegal input"       
    
    input_split = input_for_turn.split()
    input_lower = [x.lower() for x in input_split]
    if input_lower[0] == "quit":
        return "game over"
    if input_lower[0] == "quit" and input_lower[1] == "game":
        return "game over"

    turn_type = input_lower[0]
    
    if turn_type == "guess" or turn_type == "accuse":
        start = 1
        suspect, weapon, room = None, None, None
        #must be person in the x with the y
        for i in xrange(1, len(input_lower)):
            if input_lower[i] == "in":
                suspect = " ".join(input_lower[start: i])
                start = i+2
            if input_lower[i] == "with":
                if i+2 >= len(input_lower):
                    return "That was an invalid guess or accusation"
                room = " ".join(input_lower[start : i])
                weapon = input_lower[i + 2]
        #print [suspect, weapon, room]
        if None in [suspect, weapon, room]:
            return "That was an invalid guess or accusation!"
 
        if suspect not in cards.suspects:
            suspect_arg = None
        else:
            suspect_arg = suspect
        if weapon not in cards.weapons:
            weapon_arg = None
        else:
            weapon_arg = weapon
        if room not in cards.rooms:
            room_arg = None
        else:
            room_arg = room
##        suspect_arg = cards["suspects"].get(suspect)
##        room_arg = cards["rooms"].get(room)
##        weapon_arg = cards["weapons"].get(weapon)
     
        if None != suspect_arg and None != room_arg and None != weapon_arg:
        
            if turn_type == "guess":
                guess = {}
                guess["type"] = "guess"
                guess["args"] = {}
                guess["args"]["suspect"] = suspect
                guess["args"]["weapon"] = weapon
                guess["args"]["room"] = room
                #print "guess", guess, "suspect", suspect_arg, "w", weapon_arg, "r", room_arg
                return guess 
 
            else:
                accuse = {}
                accuse["type"] = "accuse"
                accuse["args"] = {}
                accuse["args"]["suspect"] = suspect
                accuse["args"]["weapon"] = weapon
                accuse["args"]["room"] = room
                return accuse
        else:
            return "That was an invalid guess or accusation!"
        
    elif turn_type == "travel":
        room = None
        for i in xrange(1, len(input_lower)-1):
            if input_lower[i] == "the":
                room = " ".join(input_lower[i+1:])
                continue
                
        if room != None:
            #print room, "ROOM"
            #print cards["rooms"], "ROOM CARDS"
            if room in cards.rooms:#.keys():
                travel = {}
                travel["type"] = "travel"
                travel["args"] = room
                return travel
            else:
                return "That was an invalid travel request!"
                
        else:
            return "That was an invalid travel request!"
        
    elif turn_type == "show":
        if len(input_lower) < 2:
            return "That was an invalid show request"
            
        article = input_lower[1]
        if article in cards.rooms:#.keys():
            return cards.rooms[article].description
            
        elif article in cards.suspects:#.keys():
            return cards.suspects[article].description
            
        elif article in cards.weapons:#.keys():
            return cards.weapons[article].description
        else:
            return "That was an invalid show request"
    
    else:
        return "That was an invalid input!"

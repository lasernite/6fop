import traceback

def verify(result, input_data, gold):
    ok = True
    message = "looks good, yay!"
    try:
        if input_data["test"] == "i":
          # Testing initializing
          correct = gold["correct"]
          for c in xrange(len(correct)):
              if correct[c] != result[c]:
                  print "You are not initializing correctly"
                  ok = False
        else:
            #Testing game play
            if result["playerResult"] != gold["playerResult"]:
                print "Your player results are wrong"
                ok = False
            if result["locationResult"] != gold["locationResult"]:
                print "your location results are wrong"
                ok = False
            if result["revealedResult"] != gold["revealedResult"]:
                print "your revealed results are wrong"
                ok = False
            if result["seenResult"] != gold["seenResult"]:
                print "your seen results are wrong"
                ok = False
            if result["returnResult"] != gold["returnResult"]:
                print "Your return values are wrong"
                ok = False
            if not ok: 
                message = "Something's not right..."
    except:
        traceback.print_exc();
        ok = False
        message = "CRASHED! :(. See above for details"
    
    return (ok, message)

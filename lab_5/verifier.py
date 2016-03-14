import traceback

def verify(result, input_data, gold):
    ok = True
    try:
        if type(result) != dict:
            message = "didn't work :( " + str(result)
            ok = False
        elif ("width" not in result) or ("height" not in result) or ("maze" not in result):
            message = "didn't work :( Your code outputs something a dictionary with incorrect keys!"
            ok = False
        else:
            # TODO: check to make sure result is a dictionary and has the right keys.
            ok = ok and (result["height"] == gold["height"])
            ok = ok and (result["width"] == gold["width"])
            ok = ok and (len(result["maze"]) == len(gold["maze"]))
            if not ok:
                message = "isn't right :(. The dimensions of your output are not correct!"
            else:
                errors = 0
                for i in xrange(len(gold["maze"])):
                    if result["maze"][i] != gold["maze"][i]:
                        errors += 1
                        ok = False
                message = "isn't right :(. There are " + str(errors) + " incorrect squares in your result!"

            if ok:
                message = "is correct. Hooray!"
    except:
        traceback.print_exc();
        ok = False
        message = "crashed :(. Stack trace is printed above so you can debug."

    return ok, message

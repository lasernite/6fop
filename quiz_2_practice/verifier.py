import traceback

def verify_get_all_elements(result, gold):
    if sorted(result) == sorted(gold):
        return True, "Looks good!"
    else:
        return False, "Your code produces an incorrect result : " + str(result)

def verify_magic_square(result, grid, magic_sum, choices):
    try:
        # Check that output is proper size
        length = len(grid)
        if len(result) != length:
            return False, "Square has incorrect type or dimensions"
        for row in result:
            if isinstance(row, (int, long, float)) or len(row) != length:
                return False, "Square has incorrect type or dimensions"
        # Check that only valid choices were placed in empty squares
        missingSquares = []
        for r in range(length):
            for c in range(length):
                if grid[r][c] == -1:
                    missingSquares.append((r, c))
        for (r,c) in missingSquares:
            if result[r][c] not in choices:
                return False, "Square has invalid values"
        # Check that the given grid elements are the same
        for r in range(length):
            for c in range(length):
                if (r,c) in missingSquares:
                    continue
                if result[r][c] != grid[r][c]:
                    return False, "You modified some grid values :("

        # Check that rows/columns/diagonals sum to magic_sum
        for row in result:
            if sum(row) != magic_sum:
                return False, "At least one row, column, or diagonal does not add up to the magic_sum"
        for c in range(length):
            s = 0
            for r in range(length):
                s += result[r][c]
            if s != magic_sum:
                return False, "At least one row, column, or diagonal does not add up to the magic_sum"
        main_diag_sum = 0
        for i in range(length):
            main_diag_sum += result[i][i]
        if main_diag_sum != magic_sum:
            return False, "At least one row, column, or diagonal does not add up to the magic_sum"
        off_diag_sum = 0
        for i in range(length):
            off_diag_sum += result[i][length-i-1]
        if off_diag_sum != magic_sum:
            return False, "At least one row, column, or diagonal does not add up to the magic_sum"
        return True, "Looks good!"
    except:
        return False, "Something is very wrong with your solution :("

def verify( result, input_data, gold ):
  try:
    message = "isn't right :(, your code produces %s" % str(result)
    if (input_data["function"] == "solve_magicsquare_recursive"):
        ok, message = verify_magic_square(result, input_data["inputs"]["grid"], input_data["inputs"]["magic_sum"], input_data["inputs"]["choices"])
    elif (input_data["function"] == "get_all_elements"):
        ok, message = verify_get_all_elements(result, gold)
    else:
        ok =  (result == gold)
    if ok:
      message = "looks good, yay!"
  except:
    print traceback.format_exc()
    ok = False
    message = "CRASHED! :(. See above for details."
  return ok, message

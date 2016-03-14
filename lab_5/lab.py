def solve_maze(m, start_x, start_y, goal_x, goal_y):
  # instantiate solution maze
  sol = [['X' for x in range(m['width'])] for row in range(m['height'])]
  # pass maze, solution, and arguments into solve_maze_utility
  solve_maze_utility(m, start_x, start_y, goal_x, goal_y, sol, 0)
  # return solution
  m['maze'] = sol
  return m

def solve_maze_utility(m, x, y, goal_x, goal_y, sol, coins):
  # if (x, y) is goal:
  if (x, y) == (goal_x, goal_y):
    # set current coins value: grab square in m, add 1 if coin, set to 0 if bomb
    square = m['maze'][y][x]
    if square == 'c':
      coins += 1
    elif square == 'b':
      coins = 0
    # mark square in sol with new coin value
    sol[y][x] = coins
    # return True, coins
    return True, coins


  if is_safe(m, x, y):
    # set current coins value: grab square in m, add 1 if coin, set to 0 if bomb
    square = m['maze'][y][x]
    if square == 'c':
      coins += 1
    elif square == 'b':
      coins = 0
    # mark (x,y) as part of solution path in sol
    sol[y][x] = coins
    # recurse right
    solve_maze_utility(m, x+1, y, goal_x, goal_y, sol, coins)
    right = solve_maze_utility(m, x+1, y, goal_x, goal_y, sol, coins)
    # recurse down
    solve_maze_utility(m, x, y+1, goal_x, goal_y, sol, coins)
    left = solve_maze_utility(m, x, y+1, goal_x, goal_y, sol, coins)

    # if both x and y recursion return True, return max coin value between the calls
    print left
    print right
    if left[0] and right[0]:
      return max(left[1],right[1])
    # if one recursion returns True, return its coin value
    elif left[0]:
      return left[1]
    elif right[0]:
      return right[1]
    # if none of these movements work, then backtrack & return False, coins
    else:
      return False, coins

  # otherwise:
    # return False, coins
  else:
    return False, coins


def is_safe(m, x, y):
  # print 'y and x'
  # print y
  # print x
  # print 'height and width'
  # print m['height']
  # print m['width']
  # x & y are not in dimensions of maze
  if (x > (m['width'] - 1) or y > (m['height'] - 1)) or (x < 0 or y < 0):
    return False
  # this square in m is a wall
  elif m['maze'][y][x] == 1:
    return False
  else:
    return True
















def solve_maze(m, start_x, start_y, goal_x, goal_y):
  # instantiate solution maze
  sol = [['X' for x in range(m['width'])] for row in range(m['height'])]
  # pass maze, solution, and arguments into solve_maze_utility
  solve_maze_utility(m, start_x, start_y, goal_x, goal_y, sol, 0)
  # turn impossibilities/edge cases based on goal and start into X's
  for row_i in range(len(sol)):
    for column_i in range(len(sol[row_i])):
      # before start space
      if (row_i < start_y) or (column_i < start_x):
        sol[row_i][column_i] = 'X'
      # beyond goal space
      elif (row_i > goal_y) or (column_i > goal_x):
        sol[row_i][column_i] = 'X'

      # else:
      # 	print path_to_goal_exists(m, column_i, row_i, goal_x, goal_y, [])
      #   if not path_to_goal_exists(m, column_i, row_i, goal_x, goal_y, []):
      #     sol[row_i][column_i] = 'X'
  # goal_paths = []
  # paths_to_goal(m, start_x, start_y, goal_x, goal_y, goal_paths)
  # print goal_paths
  #new_goals = [x for y in goal_paths for y in x]
  #set(new_goals)
  # return solution
  # print 'original maze'
  # print m
  m['maze'] = sol
  # print 'solution'
  # print m
  return m

# def path_to_goal_exists(m, x, y, goal_x, goal_y, goal_path):
#   if (x, y) == (goal_x, goal_y):
#   	goal_path.append
#     return True
#   elif count == 10:
#   	return False
#   else:
#     if is_safe(m, x, y):
#       path_to_goal_exists(m, x+1, y, goal_x, goal_y, count + 1)
#       path_to_goal_exists(m, x, y+1, goal_x, goal_y, count + 1)
#     else:
#     	path_to_goal_exists(m, x, y, goal_x, goal_y, count + 1)

# def paths_to_goal(m, x, y, goal_x, goal_y, goal_paths):
# 	#depth = 0
# 	queue = [[[x, y]]]
# 	max_depth = max(m['height'],m['width'])

# 	while queue:
# 		path = queue.pop(0)
# 		# print len(queue)
# 		# print queue
# 		# print path
# 		#print path
# 		current_x = path[-1][0]
# 		current_y = path[-1][1]
# 		#print current_x
# 		#print current_y
# 		if (current_x, current_y) == (goal_x, goal_y):
# 			goal_paths.append(path)
# 			#print path
# 			#return path
# 		elif is_safe(m, current_x, current_y):
# 			right = path[:]
# 			if not [current_x+1, current_y] in right:
# 			  right.append([current_x+1, current_y])
# 			if not right in queue:
# 			  queue.append(right)

# 			down = path[:]
# 			if not [current_x, current_y+1] in down:
# 			  down.append([current_x, current_y+1])
# 			if not down in queue:
# 			  queue.append(down)


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
    if not sol[y][x] == 'X':
    	sol[y][x] = max(sol[y][x], coins)
    else:
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
    if not sol[y][x] == 'X':
    	sol[y][x] = max(sol[y][x], coins)
    else:
    	sol[y][x] = coins
    # recurse right
    #solve_maze_utility(m, x+1, y, goal_x, goal_y, sol, coins)
    right = solve_maze_utility(m, x+1, y, goal_x, goal_y, sol, coins)
    # recurse down
    #solve_maze_utility(m, x, y+1, goal_x, goal_y, sol, coins)
    down = solve_maze_utility(m, x, y+1, goal_x, goal_y, sol, coins)

    # if both x and y recursion return True, return max coin value between the calls
    # print 'down'
    # print down[0]
    # print 'right'
    # print right[0]
    # print x, y
    if down[0] and right[0]:
      return True, max(down[1],right[1])
    # if one recursion returns True, return its coin value
    elif down[0]:
      return True, down[1]
    elif right[0]:
      return True, right[1]
    # if none of these movements work, then backtrack & return False, coins
    else:
      # if is_safe(m, x-1, y):
      # 	sol[y][x-1] = 0
      #   solve_maze_utility(m, x-1, y, goal_x, goal_y, sol, 0)
      # if is_safe(m, x, y-1):
      # 	sol[y-1][x] = 0
      #   solve_maze_utility(m, x, y-1, goal_x, goal_y, sol, 0)
      sol[y][x] = 'X'
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
  # # if both down and right are not safe from there, neither is the space
  # elif (not is_also_safe(m, x+1, y)) and (not is_also_safe(m, x, y+1)):
  #   return False
  else:
    return True

# def is_also_safe(m, x, y):
#   if (x > (m['width'] - 1) or y > (m['height'] - 1)) or (x < 0 or y < 0):
#     return False
#   # this square in m is a wall
#   elif m['maze'][y][x] == 1:
#     return False
#   else:
#     return True
















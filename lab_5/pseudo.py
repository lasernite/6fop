def solve_maze(m, start_x, start_y, goal_x, goal_y):
    # instantiate solution maze
    # pass maze, solution, and arguments into solve_maze_utility
    # return solution

    pass

def solve_maze_utility(m, x, y, goal_x, goal_y, sol, coins):
    # if (x, y) is goal:
        # set current coins value: grab square in m, add 1 if coin, set to 0 if bomb
        # mark square in sol with new coin value
        # return True, coins

    # if is_safe(m, x, y):
        # set current coins value: grab square in m, add 1 if coin, set to 0 if bomb
        # mark (x,y) as part of solution path in sol

        # recurse right
        # recurse down

        # if both x and y recursion return True, return max coin value between the calls
        # if one recursion returns True, return its coin value
        # if none of these movements work, then backtrack & return False, coins

    # otherwise:
        # return False, coins

    pass


def is_safe(m, x, y):
    # x & y are in dimensions of maze
    # this square in m is not a wall
    pass
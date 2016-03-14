def solve_maze(m, start_x, start_y, goal_x, goal_y):

    ### Edge cases
    # if goal before start, no path
    if start_x > goal_x and start_y > goal_y:
        # make all 'x' maze
        xm = [['X' for x in range(m['width'])] for row in range(m['height'])]
        return {"height": m['height'], "width": m['width'], "maze": xm}


    ### Pre-processing
    newmaze = []
    # All spaces before (above, to left) start are X, and all states after (below, to right) end are X
    # turn walls in 'w' and open space into 'o'
    for (row_i, row) in enumerate(m['maze']):
        newrow = []
        for (column_i, element) in enumerate(row):
            # start space
            if (row_i < start_y) or (column_i < start_x):
                newrow.append('X')
            # goal space
            elif (row_i > goal_y) or (column_i > goal_x):
                newrow.append('X') 
            else:
                if element == 0:
                    newrow.append('o')
                elif element == 1:
                    newrow.append('w')
                else:
                    newrow.append(element)
        newmaze.append(newrow)
    
    def get_best_result(m, start_x, start_y, goal_x, goal_y):
        current = m[start_y][start_x]
        newm = m[:]

        ### Calculate Score
        ## One space down
        # Empty space
        if m[start_y+1][start_x] == 0:
            newm[start_y+1][start_x] = current
        # Bomb
        if m[start_y+1][start_x] == 'b':
            newm[start_y+1][start_x] = 0
        # Coin
        if m[start_y+1][start_x] == 'c':
            newm[start_y+1][start_x] = current + 1
        # Wall
        if m[start_y+1][start_x] == 1:
            newm[start_y+1][start_x] = 'X'
        ## One space right
        # Empty space
        if m[start_y][start_x+1] == 0:
            newm[start_y][start_x+1] = current
        # Bomb
        if m[start_y][start_x+1] == 'b':
            newm[start_y][start_x+1] = 0
        # Coin
        if m[start_y][start_x+1] == 'c':
            newm[start_y][start_x+1] = current + 1
        # Wall
        if m[start_y][start_x+1] == 1:
            newm[start_y][start_x+1] = 'X'




    # Get best result for every element and save to maze
    finalmaze = newmaze[:]
    for (row_i, row) in enumerate(finalmaze):
        for (column_i, element) in enumerate(row):
            finalmaze[row_i][column_i] = get_best_result(newmaze, column_i, row_i)

    return finalmaze
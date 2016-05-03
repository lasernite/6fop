boardWidth = 0
boardHeight = 0
ballPosition = 0
ballVelocity = 0

def init(width, height, ball_position, ball_velocity, bricks):
	global boardHeight
	global boardWidth
	global ballPosition
	global ballVelocity

	boardHeight = height
	boardWidth = width

	ballPosition = ball_position
	ballVelocity = ball_velocity

	return None

def step(time, paddle_1_xpos, paddle_2_xpos, paddle_offset, paddle_radius):
	global ballPosition
	global ballVelocity
	global boardHeight
	global boardWidth
	
	
	left_intersect = line_intersection([0,boardHeight],[0,0], ballPosition, ballVelocity, time)
	right_intersect = line_intersection([boardWidth,0],[boardWidth,boardHeight], ballPosition, ballVelocity, time)
	top_intersect = line_intersection([0,0], [boardWidth, 0], ballPosition, ballVelocity, time)
	bottom_intersect = line_intersection([0, boardHeight], [boardWidth, boardHeight], ballPosition, ballVelocity, time)
	# Collides left wall
	if left_intersect[0]:
		# point of collision left_intersect[1]
		newX = -ballVelocity[0]
		newY = ballVelocity[1]
		ballVelocity = [newX,newY]
		ballPosition = [left_intersect[1][0] + ballVelocity[0]*0.001, left_intersect[1][1] + ballVelocity[1]*0.001]
		#ballPosition = [ballPosition[0] + ballVelocity[0]*0.001, ballPosition[1] + ballVelocity[1]*0.001]
		return 0
	# Collides with right wall
	elif right_intersect[0]:
		newX = -ballVelocity[0]
		newY = ballVelocity[1]
		ballVelocity = [newX,newY]
		#ballPosition = [ballPosition[0] + ballVelocity[0]*0.001, ballPosition[1] + ballVelocity[1]*0.001]
		ballPosition = [right_intersect[1][0] + ballVelocity[0]*0.001, right_intersect[1][1] + ballVelocity[1]*0.001]
		return 0
	# Collides with Top, player 1 scores
	elif top_intersect[0]:
		newX = ballVelocity[0]
		newY = -ballVelocity[1]
		ballVelocity = [newX,newY]
		#ballPosition = [ballPosition[0] + ballVelocity[0]*0.001, ballPosition[1] + ballVelocity[1]*0.001]
		ballPosition = [top_intersect[1][0] + ballVelocity[0]*0.001, top_intersect[1][1] + ballVelocity[1]*0.001]
		return 1
	# Collides with Bottom, player 2 scores
	elif bottom_intersect[0]:
		newX = ballVelocity[0]
		newY = -ballVelocity[1]
		ballVelocity = [newX,newY]
		# ballPosition = [ballPosition[0] + ballVelocity[0]*0.001, ballPosition[1] + ballVelocity[1]*0.001]
		ballPosition = [bottom_intersect[1][0] + ballVelocity[0]*0.001, bottom_intersect[1][1] + ballVelocity[1]*0.001]
		return -1

	# paddle intersections
	bottom_paddle = circle_intersection([paddle_1_xpos, boardHeight + paddle_offset], paddle_radius, ballPosition, ballVelocity, time)
	top_paddle = circle_intersection([paddle_2_xpos, -paddle_offset], paddle_radius, ballPosition, ballVelocity, time)
	if bottom_paddle[0]:
		# normal is simply the vector from the center of the circle to the point of intersection
		n = normal([paddle_1_xpos, boardHeight + paddle_offset], bottom_paddle[1])
		newVelocity = vector_subtract(ballVelocity, [2*proj(ballVelocity, n)[0], 2*proj(ballVelocity, n)[1]])
		ballVelocity = newVelocity
		ballPosition = [bottom_paddle[1][0] + ballVelocity[0]*0.001, bottom_paddle[1][1] + ballVelocity[1]*0.001]
		return 0
	elif top_paddle[0]:
		n = normal([paddle_2_xpos, -paddle_offset], top_paddle[1])
		newVelocity = vector_subtract(ballVelocity, [2*proj(ballVelocity, n)[0], 2*proj(ballVelocity, n)[1]])
		ballVelocity = newVelocity
		ballPosition = [top_paddle[1][0] + ballVelocity[0]*0.001, top_paddle[1][1] + ballVelocity[1]*0.001]
		return 0

	# no collision
	# New ball position at end of time
	ballPosition = [ballPosition[0] + ballVelocity[0] * time, ballPosition[1] + ballVelocity[1] * time]
	
	return 0

# lineStart, lineEnd, ball point, ball velocity, time
def line_intersection(p3, p4, p1, v1, checkTime):
	v2 = vector_subtract(p4, p3)

	# no collision
	if (cross_z( v2, v1 ) == 0) or (cross_z( v1, v2 ) == 0):
		return False, [0,0]

	t = cross_z( v2, vector_subtract(p3, p1)) / cross_z( v2, v1 )
	u = cross_z( v1,vector_subtract(p1, p3) ) / cross_z( v1, v2 )

	if (0 < u < 1) and (0 < t):
		if t <= checkTime:
			# collide at time t true, and point of intersection
			return True, [p1[0] + t*v1[0], p1[1] + t*v1[1]]
		else:
			return False, [0,0]
	else:
		return False, [0,0]

def circle_intersection(c, r, p1, v1, checkTime):

	# if inside paddle, no collision
	distance = vector_subtract(p1, c)
	ldistance = (distance[0]**2 + distance[1]**2)**0.5
	if ldistance < r:
		return False, [0,0]

	a = dot(v1, v1)
	b = 2*dot(v1, vector_subtract(p1, c))
	d = dot(vector_subtract(p1, c), vector_subtract(p1, c)) - r*r
	argSqr = b**2 - 4*a*d
	if argSqr < 0:
		return False, [0,0]

	t1 = (-b + (argSqr)**0.5 ) / (2*a)
	t2 = (-b - (argSqr)**0.5 ) / (2*a)

	times = []
	if t1 > 0:
		times.append(t1)
	if t2 > 0:
		times.append(t2)

	if len(times) == 0:
		return False, [0,0]
	else:
		t = min(times)
		if t <= checkTime:
			return True, [p1[0] + t * v1[0], p1[1] + t * v1[1]]
		else:
			return False, [0,0]


# You may assume the canvas is blank
def draw(canvas, paddle_1_xpos, paddle_2_xpos, paddle_offset, paddle_radius):
	# canvas.draw_circle(center_x, center_y, radius, color)
	# canvas.draw_rectangle(upper_left_x, upper_left_y, lower_right_x, lower_right_y, color)

	# Draw player 1 (on bottom)
	canvas.draw_circle(paddle_1_xpos, boardHeight + paddle_offset, paddle_radius, "#FFFFFF")

	# Draw player 2 (on top)
	canvas.draw_circle(paddle_2_xpos, -paddle_offset, paddle_radius, "#FFFFFF")

	# Draw ball
	canvas.draw_circle(ballPosition[0], ballPosition[1], 5, "#FFFFFF")

	return None


# Helpers

def dot(a,b):
	return a[0]*b[0] + a[1]*b[1]

def cross_z(a,b):
	return (float(a[0])*b[1]) - (float(a[1])*b[0])

def normal(center, point):
	return (point[0] - center[0], point[1] - center[1])

def proj(v,n):
	return [dot(v,n) / dot(n,n) * n[0], dot(v,n) / dot(n,n) * n[1]]

def bounced_velocity(v, n):
	return [v[0] - (2 * proj(v,n)), v[1] - (2 * proj(v,n))]

def vector_add(v1, v2):
	return [v1[0] + v2[0], v1[1] + v2[1]]

def vector_subtract(v1, v2):
	return [v1[0] - v2[0], v1[1] - v2[1]]











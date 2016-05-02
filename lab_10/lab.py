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
	
	print 'the position'
	print ballPosition
	# Collides left wall
	left_intersect = line_intersection([0,0], [0,boardHeight], ballPosition, ballVelocity)
	right_intersect = line_intersection([boardWidth,0],[boardWidth,boardHeight], ballPosition, ballVelocity)
	top_intersect = line_intersection([0,0], [boardWidth, 0], ballPosition, ballVelocity)
	bottom_intersect = line_intersection([0, boardHeight], [boardWidth, boardHeight], ballPosition, ballVelocity)
	if left_intersect[0]:
		print 'left has happened'
		# point of collision left_intersect[1]
		newX = -ballVelocity[0]
		newY = ballVelocity[1]
		ballVelocity = [newX,newY]
		#ballPosition = [left_intersect[1][0] + ballVelocity[0]*0.001, left_intersect[1][1] + ballVelocity[1]*0.001]
		ballPosition = [ballPosition[0] + ballVelocity[0]*0.001, ballPosition[1] + ballPosition[1]*0.001]
		return 0
	# Collides with right wall
	elif right_intersect[0]:
		print 'right now'
		newX = -ballVelocity[0]
		newY = ballVelocity[1]
		ballVelocity = [newX,newY]
		ballPosition = [ballPosition[0] + ballVelocity[0]*0.001, ballPosition[1] + ballVelocity[1]*0.001]
		return 0
	# Collides with Top
	elif top_intersect[0]:
		return 1
	# Collides with Bottom
	elif bottom_intersect[0]:
		return -1
	# no collision


	# New ball position at end of time
	ballPosition = [ballPosition[0] + ballVelocity[0] * time, ballPosition[1] + ballVelocity[1] * time]
	
	return 0

# lineStart, lineEnd, ball point, ball velocity, time
def line_intersection(p3, p4, p1, v1):
	v2 = vector_subtract(p4, p3)

	# no collision
	if cross_z( v2, v1 ) == 0 or cross_z( v1, v2 ) == 0:
		return False, [0,0]

	t = cross_z( v2, vector_subtract(p3, p1)) / cross_z( v2, v1 )
	u = cross_z( v1,vector_subtract(p1, p3) ) / cross_z( v1, v2 )

	# if collision
	if (p1[0] + t*v1[0], p1[1] + t*v1[1]) == (p3[0] + u*v2[0], p3[1] + u*v2[1]):
		# and at time T
		if 0 < u < 1 or 0 < t:
			# collide at time t true, and point of intersection
			print 'intersection point'
			print (p1[0] + t*v1[0], p1[1] + t*v1[1])
			return True, (p1[0] + t*v1[0], p1[1] + t*v1[1])
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
	return a[0]*b[1] - a[1]*b[0]

def normal(center, point):
	return (point[0] - center[0], point[1] - center[1])

def proj(v,n):
	return dot(v,n) / dot(n,n) * n

def bounced_velocity(v, n):
	return [v[0] - (2 * proj(v,n)), v[1] - (2 * proj(v,n))]

def vector_add(v1, v2):
	return [v1[0] + v2[0], v1[1] + v2[1]]

def vector_subtract(v1, v2):
	return [v1[0] - v2[0], v1[1] - v2[1]]











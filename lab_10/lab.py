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

	# New ball position at end of time
	ballPosition = [ballPosition[0] + ballVelocity[0] * time, ballPosition[1] + ballVelocity[0] * time]
	print ballPosition
	
	return 0


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
	return v - 2 * proj(v,n)
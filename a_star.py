import math
import copy 
import maze_runner
from Queue import PriorityQueue
import pdb
from fire import start_fire
from fire import spread_fire

# Given a co-ordinate (x,y), calculates the manhattan distance from the destination (dim-1, dim-1)
def manhattan_heuristic(x, y, dim):
	return (abs(x - dim)+abs(y - dim))

# Given a co-ordinate (x,y), calculates the euclidian distance from the destination (dim-1, dim-1)
def euclidian_heuristic(x, y, dim):
	return math.sqrt((x - dim)**2+(y - dim)**2)

# Given a co-ordinate (x,y), calculates the length of path traversed to reach (x,y) from source (0, 0)
def source_dist(x, y, maze):
	path = maze_runner.get_path(x, y, maze)
	return len(path)

"""
checks for valid neighbours which are not yet explored by any other cell 
i.e. it is neither in the fringe nor in the closed set
and adds them to the fringe based on a priority. 
Priority for each cell is calculated using two functions:
1. f(x): distance traversed from source to point (x,y) 
2. h(x): heuristic function that estimates the distance from (x,y) to destination
Fringe is implemented using a Priority Queue. 
The order of exploration of cells does not matter as the fringe
is sorted based on the priority assigned the cell.
"""
def get_neighbors(maze, x, y, dim, heuristic, fringe):
	source_distance = source_dist(x, y, maze) 
	if(x-1>=0 and maze[x-1][y].value!=1 and not maze[x-1][y].visited):
			maze[x-1][y].visited = True
			maze[x-1][y].parent = (x,y)
			if heuristic == "manhattan":
				priority_value = (source_distance + 1) + manhattan_heuristic(x-1, y, dim)
			elif heuristic == "euclidian":
				priority_value = (source_distance + 1) + euclidian_heuristic(x-1, y, dim)
			fringe.put((priority_value, (x-1, y)))
			
	# bottom neighbor
	if(x+1<=dim-1 and maze[x+1][y].value!=1 and not maze[x+1][y].visited):
			maze[x+1][y].visited = True
			maze[x+1][y].parent = (x,y)
			if heuristic == "manhattan":
				priority_value = (source_distance + 1) + manhattan_heuristic(x+1, y, dim)
			elif heuristic == "euclidian":
				priority_value = (source_distance + 1) + euclidian_heuristic(x+1, y, dim)
			fringe.put((priority_value, (x+1, y)))
	
	# left neighbor
	if(y-1>=0 and maze[x][y-1].value!=1 and not maze[x][y-1].visited):
			maze[x][y-1].visited = True
			maze[x][y-1].parent = (x,y)
			if heuristic == "manhattan":
				priority_value = (source_distance + 1) + manhattan_heuristic(x, y-1, dim)
			elif heuristic == "euclidian":
				priority_value = (source_distance + 1) + euclidian_heuristic(x, y-1, dim)
			fringe.put((priority_value, (x, y-1)))
	
	# right neighbor
	if(y+1<=dim-1 and maze[x][y+1].value!=1 and not maze[x][y+1].visited):
			maze[x][y+1].visited = True
			maze[x][y+1].parent = (x,y)
			if heuristic == "manhattan":
				priority_value = (source_distance + 1) + manhattan_heuristic(x, y+1, dim)
			elif heuristic == "euclidian":
				priority_value = (source_distance + 1) + euclidian_heuristic(x, y+1, dim)
			fringe.put((priority_value, (x, y+1)))
	
	return fringe

# traverses the graph using A* algorithm given a heuristic
"""
parameters: maze, heuristic
return values: boolean representing solvability of maze, 
			   max fringe size, average fringe size,
			   closed set
"""
def a_star_traversal(maze, heuristic):
	closed_set = set()
	fringe = PriorityQueue()
	fringe.put((0, (0, 0)))
	maze[0][0].visited = True
	dim = len(maze)
	max_fringe = None

	exploration_steps = 0	
	max_fringe_length = 0
	avg_fringe_length = 0

	while(not(fringe.empty())):
		(priority, (x, y)) = fringe.get()
		exploration_steps+=1

		if((x,y)==(dim-1, dim-1)):
			# Solution found
			closed_set.add((dim-1, dim-1))
			result_dict = {
				"is_solvable": True, 
				"total_steps": exploration_steps, 
				"max_fringe_length": max_fringe_length, 
				"avg_fringe_length": avg_fringe_length, 
				"closed_set": closed_set}
			return result_dict

		fringe = get_neighbors(maze, x, y, dim, heuristic, fringe)
		fringe_len = fringe.qsize()
		if fringe_len>max_fringe_length:
			max_fringe_length = fringe_len
			max_fringe = PriorityQueue()
			max_fringe.queue = copy.deepcopy(fringe.queue)
		avg_fringe_length = avg_fringe_length + (fringe_len - avg_fringe_length)/exploration_steps
		closed_set.add((x,y))

	# print max_fringe
	# max_fringe_list = []
	# for i in range(max_fringe.qsize()):
	# 	max_fringe_list.append(max_fringe.queue[i][1])
	# maze_runner.visualize_explored_cells(maze, max_fringe_list)
	# print "No Solution"
	result_dict = {
		"is_solvable": False, 
		"total_steps": exploration_steps, 
		"max_fringe_length": max_fringe_length, 
		"avg_fringe_length": avg_fringe_length, 
		"closed_set": closed_set}
	return result_dict


def a_star_traversal_with_fire(maze, heuristic, q):
	closed_set = set()
	fringe = PriorityQueue()
	fringe.put((0, (0, 0)))
	dim = len(maze)

	exploration_steps = 0	
	max_fringe_length = 0
	avg_fringe_length = 0
	# Puts the top right cell on fire
	maze = start_fire(maze, dim)
	# Keeps record of the cells which are on fire and are on the boudry of the fire cluster. Since this
	# is baseline algorithm, we would not be maintaining boundary_cells.
	boundary_cells = set()
	while(not(fringe.empty())):
		(priority, (x, y)) = fringe.get()
		exploration_steps+=1
		if((x,y)==(dim-1, dim-1)):
			# Solution found
			closed_set.add((dim-1, dim-1))
			return 1, exploration_steps, max_fringe_length, avg_fringe_length, closed_set, -1, -1
		if(maze[x][y].value == 2):
			# We got burnt. Coordinates at which we got burnt are recorded and returned for visualization
			return -1, exploration_steps, max_fringe_length, avg_fringe_length, closed_set, x, y
		fringe = get_neighbors(maze, x, y, dim, heuristic, fringe)
		fringe_len = fringe.qsize()
		if fringe_len>max_fringe_length:
			max_fringe_length = fringe_len
		avg_fringe_length = avg_fringe_length + (fringe_len - avg_fringe_length)/exploration_steps
		closed_set.add((x,y))
		# Spreads fire to the neighboring cell as mentioned in the question
		maze, boundary_cells = spread_fire(maze, dim, q, boundary_cells)
	# No Solution
	return 0, exploration_steps, max_fringe_length, avg_fringe_length, closed_set, -1, -1


def test_a_star(dim, p):
	test_maze = maze_runner.get_maze(dim, p)
	
	# a-star with manhattan heuristic
	maze = copy.deepcopy(test_maze)
	manhattan_result_dict = a_star_traversal(maze, "manhattan")
	if manhattan_result_dict["is_solvable"]:
	 	path = maze_runner.get_path(dim-1, dim-1, maze)
	 	print "Path", path
	 	print "Length of path: ", len(path)
	 	maze_runner.trace_path(maze, path)
	else:
	 	maze_runner.visualize_maze(maze)

	# a-star with euclidian heuristic
 	maze = copy.deepcopy(test_maze)
	euclidian_result_dict = a_star_traversal(maze, "euclidian")
	if euclidian_result_dict["is_solvable"]:
		path = maze_runner.get_path(dim-1, dim-1, maze)
		print "Path", path
	 	print "Length of path: ", len(path)
		maze_runner.trace_path(maze, path)
	else:
		maze_runner.visualize_maze(maze)

#Fire code
'''
dim = 50
p = 0.306
q = 0.1
maze = maze_runner.get_maze(dim, p)
maze_runner.visualize_maze(maze)
manhattan_result, manhattan_steps, manhattan_max_fringe_length, manhattan_avg_fringe_length, manhattan_closed_set, x_cord, y_cord = a_star_traversal_with_fire(maze, "manhattan", q)
maze_runner.visualize_maze(maze)
if manhattan_result == 1:
	print "Solution found"
	path = maze_runner.get_path(dim-1, dim-1, maze)
	maze_runner.trace_path(maze, path)
elif manhattan_result == 0:
	print "Solution not found"
	maze_runner.visualize_maze(maze)
else:
	print "Burnt at " + str(x_cord) + ", " + str(y_cord)
	maze[x_cord][y_cord].value = 1.5
	path = maze_runner.get_path(x_cord, y_cord, maze)
	maze_runner.trace_path(maze, path)
'''
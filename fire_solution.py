import math
import copy 
import maze_runner as mr
from Queue import PriorityQueue
import pdb
from bfs_2 import bfs_traversal_fire_distance 
from fire import start_fire
from fire import spread_fire
import copy 
from maze_runner import get_path_from_a_b

'''
This method calculates the distance from the nearest fire by taking the min of all the distances 
from that cell to all the cells present in the boundary_cells. boundary_cells is the set of all the cells 
which are on fire and are present at the edge of the fire cluster.
'''
def update_fringe_using_boundary_cells(fringe, maze, boundary_cells):
	dim_2 = len(maze)
	new_fringe = PriorityQueue()
	for i in xrange(fringe.qsize()):
		(priority, (x, y)) = fringe.get()
		priority =  manhattan_heuristic(x, y, dim_2) - get_closest_fire_cell_using_boundary_cells(maze, x, y, boundary_cells)
		new_fringe.put((priority, (x, y)))
	return new_fringe

'''
This method calculates the distance from the nearest fire by using BFS where goal
node is the first cell on fire encountered.
'''
def update_fringe(fringe, maze):
	new_fringe = PriorityQueue()
	for i in xrange(fringe.qsize()):
		(priority, (x, y)) = fringe.get()
		priority =  manhattan_heuristic(x, y, dim) - get_closest_fire_cell(maze, x, y)
		new_fringe.put((priority, (x, y)))
	return new_fringe

# Finds the closest cell on fire using BFS where goal node is the first cell on fire encountered
def get_closest_fire_cell(maze, x, y):
	temp_maze = copy.deepcopy(maze)
	dim_2 = len(maze)
	dist = bfs_traversal_fire_distance(temp_maze, dim_2, x, y)
	temp_maze = []
	return dist

# Finds the closest cell on fire using the set boundary_cells which is the set of all the cells 
# on fire and are present at the edge of the fire cluster.
def get_closest_fire_cell_using_boundary_cells(maze, x, y, boundary_cells):
	dim_2 = len(maze)
	min_dist = 2*dim_2
	for [a, b] in boundary_cells:
		dist = (abs(a-x)+abs(y-b))
		if min_dist > dist:
			min_dist = dist
	return min_dist

# Given a co-ordinate (x,y), calculates the manhattan distance from the destination (dim-1, dim-1)
def manhattan_heuristic(x, y, dim):
	return abs(x - dim)+abs(y - dim)

"""
checks for valid neighbours which are not yet explored by any other cell 
i.e. it is neither in the fringe nor in the closed set
and adds them to the fringe based on a priority 0. Since we are updating priorities
of all the cells in the cell after everytime step, we can have the priority of the
new cells to be zero for the time being
Fringe is implemented using a Priority Queue. 
The order of exploration of cells does not matter as the fringe
is sorted based on the priority assigned the cell.
"""
def get_neighbors(maze, x, y, dim, fringe):
	# pdb.set_trace()
	# top neighbor
	# print x,y
	if(x-1>=0 and maze[x-1][y].value!=1 and not maze[x-1][y].visited):
		maze[x-1][y].visited = True
		maze[x-1][y].parent = (x,y)
		priority_value = 0
		fringe.put((priority_value, (x-1, y)))
			
	# bottom neighbor
	if(x+1<=dim-1 and maze[x+1][y].value!=1 and not maze[x+1][y].visited):
		maze[x+1][y].visited = True
		maze[x+1][y].parent = (x,y)
		priority_value = 0
		fringe.put((priority_value, (x+1, y)))
	
	# left neighbor
	if(y-1>=0 and maze[x][y-1].value!=1 and not maze[x][y-1].visited):
		maze[x][y-1].visited = True
		maze[x][y-1].parent = (x,y)
		priority_value = 0
		fringe.put((priority_value, (x, y-1)))
	
	# right neighbor
	if(y+1<=dim-1 and maze[x][y+1].value!=1 and not maze[x][y+1].visited):
		maze[x][y+1].visited = True
		maze[x][y+1].parent = (x,y)
		priority_value = 0
		fringe.put((priority_value, (x, y+1)))
	
	return fringe

'''
For fire traversal, we are using the heuristic = (manhattan distance from the goal + mahattan distance
from the nearest cell on fire). Since fire spreads after every time step, the priority values of cells
in the fringe also need to be updated after every time step.
'''
def fire_traversal(maze, q):
	closed_set = set()
	fringe = PriorityQueue()
	fringe.put((0, (0, 0)))
	dim = len(maze)

	exploration_steps = 0	
	max_fringe_length = 0
	avg_fringe_length = 0
	# Puts the top right cell on fire
	maze = start_fire(maze, dim)
	# Keeps record of the cells which are on fire and are on the boudry of the fire cluster.
	boundary_cells = set()
	boundary_cells.add((0, dim -1))
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
		fringe = get_neighbors(maze, x, y, dim, fringe)
		fringe_len = fringe.qsize()
		if fringe_len>max_fringe_length:
			max_fringe_length = fringe_len
		avg_fringe_length = avg_fringe_length + (fringe_len - avg_fringe_length)/exploration_steps
		closed_set.add((x,y))
		# Spreads fire to the neighboring cell as mentioned in the question. Since we might have
		# more cells on fire, the boundary_cells also get updated
		maze, boundary_cells = spread_fire(maze, dim, q, boundary_cells)
		fringe = update_fringe_using_boundary_cells(fringe, maze, boundary_cells)
	# No Solution
	return 0, exploration_steps, max_fringe_length, avg_fringe_length, closed_set, -1, -1

# Main code
dim = 30
p = 0.22
q = 0.2
maze = mr.get_maze(dim, p)
mr.visualize_maze(maze)
manhattan_result, manhattan_steps, manhattan_max_fringe_length, manhattan_avg_fringe_length, manhattan_closed_set, x_cord, y_cord = fire_traversal(maze, q)
mr.visualize_maze(maze)
if manhattan_result == 1:
	print "Solution found"
	path = mr.get_path(dim-1, dim-1, maze)
	mr.trace_path(maze, path)
elif manhattan_result == 0:
	print "Solution not found"
	mr.visualize_maze(maze)
else:
	print "Burnt at " + str(x_cord) + ", " + str(y_cord)
	maze[x_cord][y_cord].value = 1.5
	path = mr.get_path(x_cord, y_cord, maze)
	mr.trace_path(maze, path)
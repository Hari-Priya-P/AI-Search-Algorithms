from maze_runner import get_maze
from maze_runner import get_path
from maze_runner import get_path_from_a_b
from maze_runner import trace_path
import copy 

"""
checks for valid neighbours which are not present and in
the closed set and adds them to the fringe.
"""
def get_neighbors(maze, x, y, dim, closed_set, fringe):
	if(x-1>=0):
		if(maze[x-1][y].value!=1 and (x-1,y) not in closed_set):
			maze[x-1][y].parent = (x,y)
			fringe.append((x-1, y))
	if(y-1>=0):
		if(maze[x][y-1].value!=1 and (x,y-1) not in closed_set):
			maze[x][y-1].parent = (x,y)
			fringe.append((x, y-1))
	if(x+1<=dim-1):
		if(maze[x+1][y].value!=1 and (x+1,y) not in closed_set):
			maze[x+1][y].parent = (x,y)
			fringe.append((x+1, y))		
	if(y+1<=dim-1):
		if(maze[x][y+1].value!=1 and (x,y+1) not in closed_set):
			maze[x][y+1].parent = (x,y)
			fringe.append((x, y+1))	
	return fringe

# traverses the graph using BFS algorithm
def bfs_traversal(maze, dim):
	closed_set = set()
	fringe = [(0,0)]
	while(len(fringe) > 0):
		((x,y)) = fringe.pop(0)
		if((x,y) in closed_set):
			continue
		if((x,y)==(dim-1, dim-1)):
			print "Solution found"
			return True
		fringe = get_neighbors(maze, x, y, dim, closed_set, fringe)
		closed_set.add((x,y))
	print "No Solution"
	return False

# Finds the length of the shortest path from a cell (a, b) to the nearest cell on fire
def bfs_traversal_fire_distance(maze, dim, a, b):
	closed_set = set()
	fringe = [(a,b)]
	while(len(fringe) > 0):
		((x,y)) = fringe.pop(0)
		if((x,y) in closed_set):
			continue
		if(maze[x][y].value == 2):
			# Cell is on fire
			return abs(x-a) + abs(y-b)
		fringe = get_neighbors(maze, x, y, dim, closed_set, fringe)
		closed_set.add((x,y))
	return 2*dim